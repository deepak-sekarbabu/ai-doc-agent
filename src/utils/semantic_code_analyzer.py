#!/usr/bin/env python3
"""
Semantic Code Relationship Analyzer

This module provides advanced analysis of code relationships, dependencies,
and architectural patterns across files and modules.

Features:
- Cross-file dependency analysis
- Semantic understanding of code relationships
- Architectural pattern recognition
- Import hierarchy analysis
- Code coupling assessment
"""

import ast
import re
import logging
import sys
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from .semantic_critique import ValidationIssue, ValidationResult

logger = logging.getLogger(__name__)


class CodeElementType:
    """Types of code elements."""
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    IMPORT = "import"
    VARIABLE = "variable"
    CONSTANT = "constant"


@dataclass
class CodeElement:
    """Represents a code element with its relationships."""
    name: str
    element_type: str
    file_path: str
    line_number: int
    docstring: str = ""
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)
    annotations: List[str] = field(default_factory=list)


@dataclass
class Dependency:
    """Represents a dependency relationship between code elements."""
    source: str
    target: str
    dependency_type: str  # import, call, inheritance, etc.
    file_path: str
    line_number: int


@dataclass
class ArchitecturePattern:
    """Represents an architectural pattern detected in the codebase."""
    pattern_type: str
    description: str
    files: List[str]
    confidence: float
    elements: List[CodeElement]


class SemanticCodeAnalyzer:
    """
    Advanced analyzer for understanding code relationships and dependencies.
    
    This goes beyond simple parsing to understand semantic relationships
    and architectural patterns in the codebase.
    """

    def __init__(self, file_contents: List[Dict[str, str]]):
        """
        Initialize analyzer with file contents.
        
        Args:
            file_contents: List of dicts with 'path' and 'content' keys
        """
        self.file_contents = file_contents
        self.code_elements: Dict[str, CodeElement] = {}
        self.dependencies: List[Dependency] = []
        self.file_relationships: Dict[str, Set[str]] = defaultdict(set)
        self.architecture_patterns: List[ArchitecturePattern] = []
        
        self._analyze_all_files()

    def _analyze_all_files(self):
        """Analyze all files to extract elements and relationships."""
        for file_info in self.file_contents:
            file_path = file_info['path']
            content = file_info['content']
            
            try:
                if file_path.endswith('.py'):
                    self._analyze_python_file(content, file_path)
                elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
                    self._analyze_javascript_file(content, file_path)
            except Exception as e:
                logger.warning(f"Failed to analyze {file_path}: {e}")
                continue

        # After individual file analysis, find cross-file relationships
        self._analyze_cross_file_relationships()

    def _analyze_python_file(self, content: str, file_path: str):
        """Analyze Python file for code elements and relationships."""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._process_python_function(node, file_path)
                elif isinstance(node, ast.ClassDef):
                    self._process_python_class(node, file_path)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._process_python_import(node, file_path)
                    
        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")

    def _analyze_javascript_file(self, content: str, file_path: str):
        """Analyze JavaScript/TypeScript file for code elements and relationships."""
        # Extract functions using regex patterns
        self._extract_js_functions(content, file_path)
        self._extract_js_classes(content, file_path)
        self._extract_js_imports(content, file_path)

    def _process_python_function(self, node: ast.FunctionDef, file_path: str):
        """Process a Python function definition."""
        element_name = f"{file_path}:{node.name}"
        
        # Extract parameters
        parameters = [arg.arg for arg in node.args.args]
        
        # Extract return type if available
        return_type = None
        if node.returns:
            return_type = getattr(node.returns, 'id', None)
        
        element = CodeElement(
            name=element_name,
            element_type=CodeElementType.FUNCTION,
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node) or "",
            parameters=parameters,
            return_type=return_type
        )
        
        self.code_elements[element_name] = element

    def _process_python_class(self, node: ast.ClassDef, file_path: str):
        """Process a Python class definition."""
        element_name = f"{file_path}:{node.name}"
        
        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        # Check for inheritance
        inheritance = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                inheritance.append(base.id)
        
        element = CodeElement(
            name=element_name,
            element_type=CodeElementType.CLASS,
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node) or "",
            annotations=inheritance
        )
        
        self.code_elements[element_name] = element

    def _process_python_import(self, node, file_path: str):
        """Process Python import statements."""
        imports = []
        
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
        
        for import_name in imports:
            element_name = f"{file_path}:import_{hash(import_name) % 10000}"
            
            element = CodeElement(
                name=element_name,
                element_type=CodeElementType.IMPORT,
                file_path=file_path,
                line_number=node.lineno,
                annotations=[import_name]
            )
            
            self.code_elements[element_name] = element
            
            # Create dependency relationship
            dependency = Dependency(
                source=element_name,
                target=import_name,
                dependency_type="import",
                file_path=file_path,
                line_number=node.lineno
            )
            self.dependencies.append(dependency)

    def _extract_js_functions(self, content: str, file_path: str):
        """Extract JavaScript function definitions."""
        # Function declarations
        func_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            element_name = f"{file_path}:{func_name}"
            element = CodeElement(
                name=element_name,
                element_type=CodeElementType.FUNCTION,
                file_path=file_path,
                line_number=line_number
            )
            self.code_elements[element_name] = element
        
        # Arrow functions
        arrow_pattern = r'(\w+)\s*=\s*\([^)]*\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            func_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            element_name = f"{file_path}:{func_name}"
            element = CodeElement(
                name=element_name,
                element_type=CodeElementType.FUNCTION,
                file_path=file_path,
                line_number=line_number
            )
            self.code_elements[element_name] = element

    def _extract_js_classes(self, content: str, file_path: str):
        """Extract JavaScript class definitions."""
        class_pattern = r'class\s+(\w+)\s*{'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            element_name = f"{file_path}:{class_name}"
            element = CodeElement(
                name=element_name,
                element_type=CodeElementType.CLASS,
                file_path=file_path,
                line_number=line_number
            )
            self.code_elements[element_name] = element

    def _extract_js_imports(self, content: str, file_path: str):
        """Extract JavaScript import statements."""
        import_patterns = [
            r'import\s+(.+?)\s+from\s+[\'"](.+?)[\'"]',
            r'require\([\'"](.+?)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                line_number = content[:match.start()].count('\n') + 1
                module_path = match.group(2) if pattern.startswith('import') else match.group(1)
                
                element_name = f"{file_path}:import_{hash(module_path) % 10000}"
                element = CodeElement(
                    name=element_name,
                    element_type=CodeElementType.IMPORT,
                    file_path=file_path,
                    line_number=line_number,
                    annotations=[module_path]
                )
                self.code_elements[element_name] = element

    def _analyze_cross_file_relationships(self):
        """Analyze relationships between different files."""
        # Group elements by file
        elements_by_file = defaultdict(list)
        for element in self.code_elements.values():
            elements_by_file[element.file_path].append(element)
        
        # Analyze file relationships
        for file_path, elements in elements_by_file.items():
            for element in elements:
                # Find dependencies to other files
                for dep in self.dependencies:
                    if dep.source == element.name:
                        self._resolve_dependency(dep, elements_by_file)

    def _resolve_dependency(self, dependency: Dependency, elements_by_file: Dict[str, List[CodeElement]]):
        """Resolve a dependency to find actual target elements."""
        # Simple heuristic: look for matching element names or imported modules
        for file_path, elements in elements_by_file.items():
            for element in elements:
                # Check if dependency target matches element name
                if dependency.target in element.name or dependency.target in element.annotations:
                    dependency.target = element.name
                    
                    # Update file relationships
                    source_file = dependency.file_path
                    target_file = element.file_path
                    if source_file != target_file:
                        self.file_relationships[source_file].add(target_file)

    def get_code_relationship_score(self, element1: str, element2: str) -> float:
        """
        Calculate semantic relationship score between two code elements.
        
        Args:
            element1: First element name
            element2: Second element name
            
        Returns:
            Relationship score from 0.0 to 1.0
        """
        if element1 not in self.code_elements or element2 not in self.code_elements:
            return 0.0
        
        score = 0.0
        
        # Direct dependency
        for dep in self.dependencies:
            if (dep.source == element1 and dep.target == element2) or \
               (dep.source == element2 and dep.target == element1):
                score += 0.8
        
        # Same file
        elem1 = self.code_elements[element1]
        elem2 = self.code_elements[element2]
        if elem1.file_path == elem2.file_path:
            score += 0.3
        
        # Type compatibility
        if elem1.element_type == elem2.element_type:
            score += 0.1
        
        # Parameter/return type matching
        if elem1.return_type and elem1.return_type in elem2.parameters:
            score += 0.2
        
        if elem2.return_type and elem2.return_type in elem1.parameters:
            score += 0.2
        
        return min(1.0, score)

    def detect_architecture_patterns(self) -> List[ArchitecturePattern]:
        """
        Detect architectural patterns in the codebase.
        
        Returns:
            List of detected architecture patterns
        """
        patterns = []
        
        # Detect MVC pattern
        mvc_pattern = self._detect_mvc_pattern()
        if mvc_pattern:
            patterns.append(mvc_pattern)
        
        # Detect service layer pattern
        service_pattern = self._detect_service_layer_pattern()
        if service_pattern:
            patterns.append(service_pattern)
        
        # Detect repository pattern
        repository_pattern = self._detect_repository_pattern()
        if repository_pattern:
            patterns.append(repository_pattern)
        
        return patterns

    def _detect_mvc_pattern(self) -> Optional[ArchitecturePattern]:
        """Detect Model-View-Controller pattern."""
        controllers = []
        models = []
        views = []
        
        for element in self.code_elements.values():
            name_lower = element.name.lower()
            
            if 'controller' in name_lower:
                controllers.append(element)
            elif 'model' in name_lower or element.element_type == CodeElementType.CLASS:
                models.append(element)
            elif 'view' in name_lower or 'component' in name_lower:
                views.append(element)
        
        if controllers and models and views:
            files = list(set(element.file_path for element in controllers + models + views))
            return ArchitecturePattern(
                pattern_type="Model-View-Controller",
                description="Detected MVC architecture with separate controller, model, and view components",
                files=files,
                confidence=0.7,
                elements=controllers + models + views
            )
        
        return None

    def _detect_service_layer_pattern(self) -> Optional[ArchitecturePattern]:
        """Detect service layer pattern."""
        services = []
        
        for element in self.code_elements.values():
            name_lower = element.name.lower()
            if 'service' in name_lower:
                services.append(element)
        
        if len(services) >= 2:  # At least 2 services
            files = list(set(element.file_path for element in services))
            return ArchitecturePattern(
                pattern_type="Service Layer",
                description="Detected service layer architecture with multiple service components",
                files=files,
                confidence=0.8,
                elements=services
            )
        
        return None

    def _detect_repository_pattern(self) -> Optional[ArchitecturePattern]:
        """Detect repository pattern."""
        repositories = []
        
        for element in self.code_elements.values():
            name_lower = element.name.lower()
            if 'repository' in name_lower or 'repo' in name_lower:
                repositories.append(element)
        
        if repositories:
            files = list(set(element.file_path for element in repositories))
            return ArchitecturePattern(
                pattern_type="Repository",
                description="Detected repository pattern with data access abstraction",
                files=files,
                confidence=0.9,
                elements=repositories
            )
        
        return None

    def get_coupling_analysis(self) -> Dict[str, float]:
        """
        Analyze coupling between different parts of the codebase.
        
        Returns:
            Dictionary mapping file pairs to coupling scores
        """
        coupling_scores: Dict[str, float] = {}
        
        files = list(self.file_relationships.keys())
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                # Calculate coupling based on dependencies and shared elements
                shared_elements = 0
                total_elements = len(self.code_elements)
                
                for element in self.code_elements.values():
                    if element.file_path in [file1, file2]:
                        shared_elements += 1
                
                if shared_elements > 0:
                    coupling = shared_elements / total_elements
                    coupling_scores[f"{file1} <-> {file2}"] = coupling
        
        return coupling_scores

    def get_central_elements(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Identify the most central/important elements in the codebase.
        
        Args:
            top_n: Number of top elements to return
            
        Returns:
            List of (element_name, centrality_score) tuples
        """
        centrality_scores = {}
        
        for element_name in self.code_elements.keys():
            score = 0.0
            
            # Count direct dependencies
            for dep in self.dependencies:
                if dep.source == element_name:
                    score += 1.0
                if dep.target == element_name:
                    score += 1.0
            
            # Count cross-file relationships
            element = self.code_elements[element_name]
            for related_file in self.file_relationships.get(element.file_path, set()):
                score += 0.5
            
            centrality_scores[element_name] = score
        
        # Sort by centrality and return top N
        sorted_elements = sorted(centrality_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_elements[:top_n]


class SemanticCodeValidator:
    """
    Enhanced validator that uses semantic code analysis for validation.
    
    This validator goes beyond simple element matching to understand
    semantic relationships and architectural consistency.
    """

    def __init__(self, file_contents: List[Dict[str, str]]):
        """
        Initialize validator with file contents and semantic analyzer.
        
        Args:
            file_contents: List of dicts with 'path' and 'content' keys
        """
        self.semantic_analyzer = SemanticCodeAnalyzer(file_contents)
        self.file_contents = file_contents

    def validate_documentation_semantically(self, documentation: str) -> List[ValidationIssue]:
        """
        Validate documentation using semantic understanding of code relationships.
        
        Args:
            documentation: Generated documentation to validate
            
        Returns:
            List of validation issues found
        """
        issues = []
        
        # Extract documented elements
        documented_elements = self._extract_documented_elements(documentation)
        
        # Validate element existence and relationships
        issues.extend(self._validate_element_relationships(documented_elements))
        
        # Validate architectural consistency
        issues.extend(self._validate_architectural_consistency(documentation))
        
        # Validate cross-file references
        issues.extend(self._validate_cross_file_references(documentation))
        
        return issues

    def _extract_documented_elements(self, documentation: str) -> Set[str]:
        """Extract element names mentioned in documentation."""
        documented = set()
        
        # Enhanced patterns for extracting code references
        patterns = [
            r'###\s+(\w+)\s*\(',  # Method headers
            r'(\w+)\s*\([^)]*\)',  # Function calls
            r'class\s+(\w+)',      # Class names
            r'`(\w+)(?:\([^)]*\))?`',  # Backtick references
            r'(\w+)\.(\w+)',       # Method calls on objects
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, documentation, re.IGNORECASE)
            for match in matches:
                element = match.group(1)
                if len(element) > 2 and element.lower() not in self._get_common_words():
                    documented.add(element)
        
        return documented

    def _get_common_words(self) -> Set[str]:
        """Get common words that should be filtered out."""
        return {
            'the', 'and', 'for', 'with', 'this', 'that', 'are', 'will', 'from',
            'code', 'api', 'int', 'str', 'bool', 'dict', 'float', 'new', 'and',
            'or', 'not', 'try', 'case', 'when', 'then', 'use', 'using', 'based',
            'function', 'class', 'method', 'object', 'string', 'number', 'boolean'
        }

    def _validate_element_relationships(self, documented_elements: Set[str]) -> List[ValidationIssue]:
        """Validate that documented elements have proper relationships."""
        issues = []
        
        for doc_element in documented_elements:
            # Find matching elements in the codebase
            matching_elements = []
            for element_name, element in self.semantic_analyzer.code_elements.items():
                if doc_element.lower() in element.name.lower() or \
                   doc_element.lower() in [ann.lower() for ann in element.annotations]:
                    matching_elements.append(element_name)
            
            if not matching_elements:
                issues.append(ValidationIssue(
                    severity=ValidationResult.ERROR,
                    issue_type="missing_element",
                    description=f"Documentation mentions '{doc_element}' but this element doesn't exist in the code",
                    suggested_fix=f"Remove reference to '{doc_element}' or add the missing element to the code"
                ))
            elif len(matching_elements) > 1:
                # Multiple potential matches - suggest clarification
                issues.append(ValidationIssue(
                    severity=ValidationResult.WARNING,
                    issue_type="ambiguous_reference",
                    description=f"Documentation reference '{doc_element}' could refer to multiple elements",
                    suggested_fix=f"Be more specific about which {matching_elements[0].split(':')[1]} you mean"
                ))
        
        return issues

    def _validate_architectural_consistency(self, documentation: str) -> List[ValidationIssue]:
        """Validate that documentation is consistent with detected architecture patterns."""
        issues = []
        
        # Detect architecture patterns
        patterns = self.semantic_analyzer.detect_architecture_patterns()
        
        for pattern in patterns:
            # Check if documentation mentions the pattern appropriately
            pattern_mentioned = any(
                pattern.pattern_type.lower() in line.lower()
                for line in documentation.split('\n')
            )
            
            if pattern.confidence > 0.7 and not pattern_mentioned:
                issues.append(ValidationIssue(
                    severity=ValidationResult.WARNING,
                    issue_type="architecture_awareness",
                    description=f"Codebase uses {pattern.pattern_type} pattern but documentation doesn't mention it",
                    suggested_fix=f"Consider documenting the {pattern.pattern_type} architecture used in this project"
                ))
        
        return issues

    def _validate_cross_file_references(self, documentation: str) -> List[ValidationIssue]:
        """Validate cross-file references in documentation."""
        issues = []
        
        # Check for mentions of file relationships
        file_relationships = self.semantic_analyzer.file_relationships
        
        # Extract potential cross-file references from documentation
        ref_pattern = r'(\w+)\s+(?:imports|uses|calls|extends|implements)\s+(\w+)'
        matches = re.finditer(ref_pattern, documentation, re.IGNORECASE)
        
        for match in matches:
            source_element = match.group(1)
            target_element = match.group(2)
            
            # Check if this relationship exists
            relationship_exists = False
            for source, targets in file_relationships.items():
                if any(target_element.lower() in target.lower() for target in targets):
                    relationship_exists = True
                    break
            
            if not relationship_exists:
                issues.append(ValidationIssue(
                    severity=ValidationResult.WARNING,
                    issue_type="cross_file_reference",
                    description=f"Documentation mentions relationship between '{source_element}' and '{target_element}' but analysis shows no such dependency",
                    suggested_fix="Verify the cross-file relationship or update documentation to reflect actual code structure"
                ))
        
        return issues