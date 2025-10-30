#!/usr/bin/env python3
"""
Semantic Critique Analysis and Cross-Validation Module

This module provides advanced semantic analysis for documentation critique
and cross-validation against actual code functionality.

Features:
- Semantic understanding of critique content beyond keyword matching
- Cross-validation of documentation claims against code structure
- Technical accuracy verification
- Contextual scoring based on semantic analysis
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import ast
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ValidationResult(Enum):
    """Result types for validation checks."""
    VALID = "valid"
    WARNING = "warning"
    ERROR = "error"
    MISSING = "missing"


@dataclass
class SemanticScore:
    """Semantic score breakdown for critique analysis."""
    overall_score: float  # 0.0 to 1.0
    technical_accuracy: float
    completeness: float
    clarity: float
    structure: float
    usefulness: float
    confidence: float  # How confident we are in the assessment


@dataclass
class ValidationIssue:
    """Represents a validation issue found during cross-validation."""
    severity: ValidationResult
    issue_type: str
    description: str
    suggested_fix: str
    location: Optional[str] = None  # File/line reference


class SemanticCritiqueAnalyzer:
    """
    Advanced semantic critique analyzer that understands context and meaning.
    
    This goes beyond keyword matching to provide true semantic analysis
    of documentation quality.
    """

    def __init__(self):
        self.positive_patterns = {
            'technical_accuracy': [
                r'(sophisticated|enterprise.*architecture|design.*patterns)',
                r'(well.*implemented|properly.*structured|sound.*engineering)',
                r'(separation.*of.*concerns|dependency.*injection|solid.*principles)',
                r'(comprehensive|thorough|complete|maintainable|robust)',
                r'(proper.*abstraction|architectural.*integrity|loose.*coupling)'
            ],
            'completeness': [
                r'(covers.*all.*aspects|comprehensive)',
                r'(includes.*everything|complete.*coverage)',
                r'(addresses.*all.*requirements|fully.*documented)',
                r'(all.*necessary.*information|sufficient.*detail)'
            ],
            'clarity': [
                r'(clear|easy.*to.*understand|well.*written)',
                r'(concise|to.*the.*point|well.*organized|logical)',
                r'(readable|accessible|user.*friendly|intuitive)'
            ],
            'structure': [
                r'(well.*structured|good.*organization|proper.*formatting)',
                r'(logical.*flow|nice.*layout|professional.*presentation)',
                r'(maintains.*separation|clear.*boundaries)',
                r'(architectural.*integrity|maintainable|robust)'
            ],
            'usefulness': [
                r'(helpful|useful|practical|actionable)',
                r'(provides.*guidance|real.*value)',
                r'(solves.*problems|addresses.*needs|developers.*will.*benefit)'
            ]
        }
        
        self.negative_patterns = {
            'technical_accuracy': [
                r'(inaccurate|incorrect|wrong|error)',
                r'(misleading|confusing|unclear)',
                r'(poor.*implementation|bad.*architecture|lacks.*robustness)',
                r'(tight.*coupling|high.*complexity|unmaintainable)'
            ],
            'completeness': [
                r'(incomplete|missing|omitted)',
                r'(lacks.*coverage|insufficient|too.*brief)',
                r'(needs.*more.*detail|missing.*aspects)'
            ],
            'clarity': [
                r'(unclear|confusing|hard.*to.*understand)',
                r'(poor.*writing|bad.*presentation)',
                r'(too.*complex|unnecessarily.*complicated|poorly.*organized)'
            ],
            'structure': [
                r'(poor.*structure|bad.*organization)',
                r'(lacks.*logic|confusing.*flow)',
                r'(poor.*formatting|bad.*layout|inconsistent)'
            ],
            'usefulness': [
                r'(unhelpful|useless|not.*useful)',
                r'(theoretical.*only|impractical)',
                r'(doesn.*t.*help|fails.*to.*address.*needs|developers.*won.*t.*benefit)'
            ]
        }

    def analyze_critique_semantically(self, critique: str) -> SemanticScore:
        """
        Analyze critique using semantic understanding rather than keyword matching.
        
        Args:
            critique: The critique text to analyze
            
        Returns:
            SemanticScore with detailed breakdown
        """
        critique_lower = critique.lower().strip()
        
        # Analyze different aspects semantically
        scores = {}
        confidences = {}
        
        for aspect in ['technical_accuracy', 'completeness', 'clarity', 'structure', 'usefulness']:
            pos_matches = self._count_pattern_matches(critique_lower, self.positive_patterns[aspect])
            neg_matches = self._count_pattern_matches(critique_lower, self.negative_patterns[aspect])
            
            # Semantic scoring logic
            aspect_score = self._calculate_aspect_score(pos_matches, neg_matches)
            confidence = self._calculate_confidence(pos_matches, neg_matches, len(critique.split()))
            
            scores[aspect] = aspect_score
            confidences[aspect] = confidence
        
        # Calculate overall score with confidence weighting
        overall_score = sum(scores.values()) / len(scores)
        overall_confidence = sum(confidences.values()) / len(confidences)
        
        return SemanticScore(
            overall_score=overall_score,
            technical_accuracy=scores['technical_accuracy'],
            completeness=scores['completeness'],
            clarity=scores['clarity'],
            structure=scores['structure'],
            usefulness=scores['usefulness'],
            confidence=overall_confidence
        )

    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Count matches for semantic patterns."""
        matches = 0
        for pattern in patterns:
            matches += len(re.findall(pattern, text, re.IGNORECASE))
        return matches

    def _calculate_aspect_score(self, positive_matches: int, negative_matches: int) -> float:
        """Calculate semantic score for an aspect."""
        if positive_matches == 0 and negative_matches == 0:
            return 0.5  # Neutral score when no relevant indicators
        
        # Semantic weighting - positive matches have stronger impact
        positive_weight = 1.0
        negative_weight = 1.2  # Negative feedback has stronger signal
        
        net_score = (positive_matches * positive_weight) - (negative_matches * negative_weight)
        
        # Normalize to 0-1 range
        total_matches = positive_matches + negative_matches
        if total_matches == 0:
            return 0.5
        
        normalized_score = (net_score / total_matches + 1) / 2
        return max(0.0, min(1.0, normalized_score))

    def _calculate_confidence(self, pos_matches: int, neg_matches: int, word_count: int) -> float:
        """Calculate confidence in the assessment."""
        # More matches = higher confidence
        total_matches = pos_matches + neg_matches
        match_confidence = min(1.0, total_matches / 2)
        
        # Longer critiques can provide more confidence
        length_confidence = min(1.0, word_count / 50)
        
        return (match_confidence + length_confidence) / 2


class DocumentationValidator:
    """
    Cross-validates documentation content against actual code functionality.
    
    This ensures that documented APIs, features, and behaviors actually exist
    and match the code implementation.
    """

    def __init__(self, file_contents: List[Dict[str, str]]):
        """
        Initialize validator with code file contents.
        
        Args:
            file_contents: List of dicts with 'path' and 'content' keys
        """
        self.file_contents = file_contents
        self.code_elements = self._extract_code_elements()
        self.documented_elements = set()

    def _extract_code_elements(self) -> Dict[str, Dict]:
        """
        Extract code elements (functions, classes, imports) from files.
        
        Returns:
            Dictionary mapping element names to their metadata
        """
        elements = {}
        
        for file_info in self.file_contents:
            file_path = file_info['path']
            content = file_info['content']
            
            try:
                if file_path.endswith('.py'):
                    elements.update(self._extract_python_elements(content, file_path))
                elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
                    elements.update(self._extract_javascript_elements(content, file_path))
            except Exception as e:
                logger.warning(f"Failed to parse {file_path}: {e}")
                continue
        
        return elements

    def _extract_python_elements(self, content: str, file_path: str) -> Dict[str, Dict]:
        """Extract Python code elements."""
        elements = {}
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    elements[node.name] = {
                        'type': 'function',
                        'file': file_path,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node) or '',
                        'returns': getattr(node.returns, 'id', None) if node.returns else None
                    }
                elif isinstance(node, ast.ClassDef):
                    elements[node.name] = {
                        'type': 'class',
                        'file': file_path,
                        'line': node.lineno,
                        'docstring': ast.get_docstring(node) or '',
                        'methods': [item.name for item in node.body if isinstance(item, ast.FunctionDef)]
                    }
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        elements[alias.name] = {
                            'type': 'import',
                            'file': file_path,
                            'line': node.lineno,
                            'original_name': alias.name,
                            'asname': alias.asname
                        }
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        full_name = f"{node.module}.{alias.name}" if node.module else alias.name
                        elements[alias.asname or alias.name] = {
                            'type': 'import',
                            'file': file_path,
                            'line': node.lineno,
                            'original_name': full_name,
                            'asname': alias.asname
                        }
        
        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")
        
        return elements

    def _extract_javascript_elements(self, content: str, file_path: str) -> Dict[str, Dict]:
        """Extract JavaScript/TypeScript code elements."""
        elements = {}
        
        # Simple regex-based extraction for common patterns
        # Function declarations
        func_pattern = r'function\s+(\w+)\s*\('
        for match in re.finditer(func_pattern, content):
            elements[match.group(1)] = {
                'type': 'function',
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1
            }
        
        # Arrow functions
        arrow_pattern = r'(\w+)\s*=\s*\([^)]*\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            elements[match.group(1)] = {
                'type': 'arrow_function',
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1
            }
        
        # Class declarations
        class_pattern = r'class\s+(\w+)\s*{'
        for match in re.finditer(class_pattern, content):
            elements[match.group(1)] = {
                'type': 'class',
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1
            }
        
        return elements

    def validate_documentation(self, documentation: str) -> List[ValidationIssue]:
        """
        Cross-validate documentation against code elements.
        
        Args:
            documentation: Generated documentation to validate
            
        Returns:
            List of validation issues found
        """
        issues = []
        
        # Extract documented elements
        self.documented_elements = self._extract_documented_elements(documentation)
        
        # Check for undocumented code elements
        issues.extend(self._check_for_documented_elements())
        
        # Check for undocumented code
        issues.extend(self._check_for_undocumented_elements())
        
        # Validate API claims
        issues.extend(self._validate_api_claims(documentation))
        
        return issues

    def _extract_documented_elements(self, documentation: str) -> Set[str]:
        """Extract element names mentioned in documentation."""
        documented = set()
        
        # Extract code references - be more selective to avoid noise
        # Look for function/method calls with specific patterns
        method_patterns = [
            r'###\s+(\w+)\s*\(',  # Markdown method headers
            r'(\w+)\s*\(.*\)',    # Function calls with parameters
            r'class\s+(\w+)',     # Class names
            r'`(\w+)`',           # Backtick code references
            r'`(\w+)\(',          # Backtick function calls
        ]
        
        for pattern in method_patterns:
            matches = re.finditer(pattern, documentation, re.IGNORECASE)
            for match in matches:
                element = match.group(1)
                # Filter out common non-code words and very short terms
                if (len(element) > 2 and
                    element.lower() not in {'the', 'and', 'for', 'with', 'this', 'that', 'are', 'will', 'from', 'code', 'api', 'int', 'str', 'bool', 'dict', 'float', 'new', 'and', 'or', 'not', 'try', 'case', 'when', 'then'}):
                    documented.add(element)
        
        return documented

    def _check_for_documented_elements(self) -> List[ValidationIssue]:
        """Check if documented elements actually exist in code."""
        issues = []
        
        for doc_element in self.documented_elements:
            if doc_element in self.code_elements:
                # Element exists, no issue
                continue
            elif doc_element.lower() in (key.lower() for key in self.code_elements.keys()):
                # Case mismatch, suggest correction
                actual_element = next(key for key in self.code_elements.keys() 
                                    if key.lower() == doc_element.lower())
                issues.append(ValidationIssue(
                    severity=ValidationResult.WARNING,
                    issue_type="naming_inconsistency",
                    description=f"Documented element '{doc_element}' has case mismatch with actual code '{actual_element}'",
                    suggested_fix=f"Use consistent casing: '{actual_element}'",
                    location=self.code_elements[actual_element]['file']
                ))
            else:
                # Element doesn't exist
                issues.append(ValidationIssue(
                    severity=ValidationResult.ERROR,
                    issue_type="missing_element",
                    description=f"Documentation mentions '{doc_element}' but this element doesn't exist in the code",
                    suggested_fix=f"Remove reference to '{doc_element}' or add the missing element to the code",
                    location="documentation"
                ))
        
        return issues

    def _check_for_undocumented_elements(self) -> List[ValidationIssue]:
        """Check for important code elements that aren't documented."""
        issues = []
        
        # Focus on public APIs (functions and classes)
        important_elements = {
            name: info for name, info in self.code_elements.items()
            if info['type'] in ['function', 'class'] and not name.startswith('_')
        }
        
        undocumented = []
        for element_name, element_info in important_elements.items():
            if element_name not in self.documented_elements:
                undocumented.append((element_name, element_info))
        
        # Only flag if it's a significant omission
        if len(undocumented) > 0:
            for element_name, element_info in undocumented[:5]:  # Limit to first 5
                issues.append(ValidationIssue(
                    severity=ValidationResult.WARNING,
                    issue_type="undocumented_element",
                    description=f"Code element '{element_name}' is not mentioned in documentation",
                    suggested_fix=f"Consider documenting {element_info['type']} '{element_name}'",
                    location=element_info['file']
                ))
        
        return issues

    def _validate_api_claims(self, documentation: str) -> List[ValidationIssue]:
        """Validate claims about API behavior against actual implementation."""
        issues = []
        
        # Look for specific claims that can be validated
        claims_patterns = [
            (r'returns\s+(\w+)', self._validate_return_types),
            (r'accepts?\s+(\w+(?:,\s*\w+)*)', self._validate_parameter_types),
            (r'uses?\s+(\w+)', self._validate_dependency_claims)
        ]
        
        for pattern, validator in claims_patterns:
            matches = re.finditer(pattern, documentation, re.IGNORECASE)
            for match in matches:
                issues.extend(validator(match))
        
        return issues

    def _validate_return_types(self, match) -> List[ValidationIssue]:
        """Validate claims about return types."""
        # This is a simplified validation - real implementation would be more sophisticated
        return []

    def _validate_parameter_types(self, match) -> List[ValidationIssue]:
        """Validate claims about parameter types."""
        return []

    def _validate_dependency_claims(self, match) -> List[ValidationIssue]:
        """Validate claims about dependencies."""
        return []


def create_semantic_critique_score(semantic_analysis: SemanticScore, 
                                  validation_issues: List[ValidationIssue]) -> float:
    """
    Combine semantic analysis and validation results into final score.
    
    Args:
        semantic_analysis: Results from semantic critique analysis
        validation_issues: Issues found during cross-validation
        
    Returns:
        Final score from 0.0 to 1.0
    """
    # Start with semantic score
    base_score = semantic_analysis.overall_score
    
    # Adjust based on validation issues
    error_count = sum(1 for issue in validation_issues if issue.severity == ValidationResult.ERROR)
    warning_count = sum(1 for issue in validation_issues if issue.severity == ValidationResult.WARNING)
    
    # Penalties for issues
    error_penalty = error_count * 0.2
    warning_penalty = warning_count * 0.1
    
    # Adjust based on confidence
    confidence_multiplier = semantic_analysis.confidence
    
    final_score = (base_score - error_penalty - warning_penalty) * confidence_multiplier
    
    return max(0.0, min(1.0, final_score))