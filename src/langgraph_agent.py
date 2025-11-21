#!/usr/bin/env python3
"""
AI Agent for Code Documentation Generation (LangGraph Implementation)

This script defines an AI agent that autonomously generates, critiques, and refines
documentation for code projects using a stateful graph managed by LangGraph.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional, TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from .doc_generator import save_documentation
from .agent_core import AIAgent
from .base_agent import AgentConfig
from .utils.semantic_code_analyzer import SemanticCodeAnalyzer

load_dotenv()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('langgraph_agent.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


# --- State Definition for the Graph ---
class AgentState(TypedDict):
    """
    Represents the state of our documentation generation agent.
    """
    directory: Path
    max_files: int
    model: str
    project_type: Optional[str]
    output_format: str
    output_file: Optional[str]
    file_contents: List[Dict[str, str]]
    documentation: Optional[str]
    critique: Optional[str]
    iteration: int
    max_iterations: int
    config: AgentConfig
    agent: Optional[AIAgent]
    semantic_analyzer: Optional[SemanticCodeAnalyzer]
    semantic_analysis: Optional[Dict[str, any]]


# --- Node Implementations ---
def analyze_codebase(state: AgentState) -> AgentState:
    """
    Analyzes the codebase to find and read relevant files.
    This node populates the 'file_contents' in the state and initializes the agent.
    """
    logger.info(f"Analyzing directory: {state['directory']}")

    # Create agent and let it handle the analysis
    agent = AIAgent(
        directory=str(state['directory']),
        max_files=state['max_files'],
        model=state['model'],
        project_type=state.get('project_type'),
        output_format=state['output_format'],
        output_file=state['output_file'],
        config=state['config']
    )

    # Analyze the codebase using the agent's method
    agent.analyze_codebase()

    return {
        **state,
        "file_contents": agent.file_contents,
        "project_type": agent.project_type,
        "agent": agent,
    }

def perform_semantic_analysis(state: AgentState) -> AgentState:
    """
    Performs semantic code analysis to understand relationships and architecture.
    """
    logger.info("Performing semantic code analysis...")

    # Initialize semantic analyzer with file contents
    semantic_analyzer = SemanticCodeAnalyzer(state['file_contents'])

    # Perform comprehensive analysis
    coupling_analysis = semantic_analyzer.get_coupling_analysis()
    central_elements = semantic_analyzer.get_central_elements(top_n=10)
    architecture_patterns = semantic_analyzer.detect_architecture_patterns()

    # Store analysis results
    semantic_analysis = {
        "coupling_analysis": coupling_analysis,
        "central_elements": central_elements,
        "architecture_patterns": architecture_patterns,
        "code_elements_count": len(semantic_analyzer.code_elements),
        "dependencies_count": len(semantic_analyzer.dependencies),
    }

    logger.info(f"Semantic analysis complete: {len(semantic_analyzer.code_elements)} elements, "
               f"{len(semantic_analyzer.dependencies)} dependencies, "
               f"{len(architecture_patterns)} patterns detected")

    return {
        **state,
        "semantic_analyzer": semantic_analyzer,
        "semantic_analysis": semantic_analysis,
    }

def generate_draft(state: AgentState) -> AgentState:
    """
    Generates the initial documentation draft enhanced with semantic analysis.
    """
    logger.info("Generating initial documentation draft...")

    agent = state['agent']

    # Enhance agent with semantic analysis if available
    if state.get('semantic_analysis'):
        # Add semantic analysis to the agent's file contents for better context
        semantic_info = state['semantic_analysis']

        # Create enhanced file contents with semantic insights
        enhanced_contents = state['file_contents'].copy()

        # Add a semantic analysis summary file
        semantic_summary = f"""# Semantic Code Analysis Summary

## Architecture Overview
- **Code Elements**: {semantic_info['code_elements_count']}
- **Dependencies**: {semantic_info['dependencies_count']}
- **Architecture Patterns**: {len(semantic_info['architecture_patterns'])}

## Key Architectural Patterns
"""
        for pattern in semantic_info['architecture_patterns'][:5]:  # Top 5 patterns
            semantic_summary += f"- **{pattern.pattern_type}**: {pattern.description} (confidence: {pattern.confidence:.2f})\n"

        semantic_summary += "\n## Central Code Elements\n"
        for element, score in semantic_info['central_elements'][:10]:
            semantic_summary += f"- {element}: {score:.2f}\n"

        # Add semantic summary as a virtual file
        enhanced_contents.append({
            'path': 'semantic_analysis_summary.md',
            'content': semantic_summary
        })

        # Create a temporary agent with enhanced contents for better documentation
        # We'll modify the agent's file_contents temporarily
        original_contents = agent.file_contents
        agent.file_contents = enhanced_contents

        documentation = agent.generate_documentation_draft()

        # Restore original contents
        agent.file_contents = original_contents
    else:
        documentation = agent.generate_documentation_draft()

    return {**state, "documentation": documentation}

def critique_document(state: AgentState) -> AgentState:
    """
    Critiques the current documentation draft.
    """
    logger.info("Critiquing documentation...")

    agent = state['agent']
    critique = agent.critique_documentation(state['documentation'])

    return {**state, "critique": critique}

def refine_document(state: AgentState) -> AgentState:
    """
    Refines the documentation based on the critique.
    """
    logger.info("Refining documentation...")

    agent = state['agent']
    refined_documentation = agent.refine_documentation(state['documentation'], state['critique'])

    return {**state, "documentation": refined_documentation, "iteration": state["iteration"] + 1}


# --- Conditional Edge Logic ---
def should_continue(state: AgentState) -> str:
    """
    Determines whether to continue refining or to finish.
    """
    logger.info(f"Iteration {state['iteration']} / {state['max_iterations']}")

    if state['iteration'] >= state['max_iterations']:
        logger.info("Max iterations reached. Finishing.")
        return "finish"

    agent = state['agent']

    if agent.is_critique_positive(state['critique']):
        logger.info("Critique is positive. Finishing.")
        return "finish"
    else:
        return "refine"


# --- Graph Definition ---
def build_graph() -> StateGraph:
    """
    Builds the LangGraph agent.
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("analyze_codebase", analyze_codebase)
    workflow.add_node("semantic_analysis", perform_semantic_analysis)
    workflow.add_node("generate_draft", generate_draft)
    workflow.add_node("critique_document", critique_document)
    workflow.add_node("refine_document", refine_document)

    # Set entry point
    workflow.set_entry_point("analyze_codebase")

    # Add edges
    workflow.add_edge("analyze_codebase", "semantic_analysis")
    workflow.add_edge("semantic_analysis", "generate_draft")
    workflow.add_edge("generate_draft", "critique_document")
    
    workflow.add_conditional_edges(
        "critique_document",
        should_continue,
        {
            "refine": "refine_document",
            "finish": END,
        },
    )
    
    workflow.add_edge("refine_document", "critique_document")

    return workflow.compile()


def main():
    parser = argparse.ArgumentParser(
        description="AI agent to generate and refine documentation for code projects using LangGraph.",
    )
    
    parser.add_argument("--directory", help="Directory to analyze (default: current directory)")
    parser.add_argument("--max-files", type=int, default=30, help="Maximum files to analyze")
    parser.add_argument("--model", default="gpt-oss:120b-cloud", help="Ollama model")
    parser.add_argument("--format", default="markdown", choices=["markdown", "html", "pdf"], help="Output format")
    parser.add_argument("--output", help="Output filename (without extension)")
    parser.add_argument("--project-type", choices=["frontend", "backend", "mixed"], help="Project type (default: auto-detect)")
    parser.add_argument("--iterations", type=int, default=3, help="Max refinement iterations")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    directory = args.directory or str(Path.cwd())
    
    # Initialize the agent state
    initial_state = AgentState(
        directory=Path(directory).resolve(),
        max_files=args.max_files,
        model=args.model,
        project_type=args.project_type,
        output_format=args.format,
        output_file=args.output,
        file_contents=[],
        documentation=None,
        critique=None,
        iteration=0,
        max_iterations=args.iterations,
        config=AgentConfig(),
        agent=None,
        semantic_analyzer=None,
        semantic_analysis=None
    )
    
    # Build and run the graph
    app = build_graph()
    final_state = app.invoke(initial_state)
    
    # Save the final documentation
    if final_state.get("documentation") and final_state.get("agent"):
        agent = final_state["agent"]
        agent.documentation = final_state["documentation"]
        output_path = agent.save_documentation()
        logger.info(f"Documentation saved to: {output_path}")
    else:
        logger.error("Failed to generate documentation.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
