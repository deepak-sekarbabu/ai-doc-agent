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

# Assuming the original doc_generator functions are compatible or will be adapted
from .doc_generator import (
    find_code_files,
    read_file_safe,
    save_documentation,
    detect_project_type,
    DocGeneratorError,
)
from .ai_agent import (
    AIAgent,
    AgentConfig
)

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


# --- Node Implementations ---
def analyze_codebase(state: AgentState) -> AgentState:
    """
    Analyzes the codebase to find and read relevant files.
    This node populates the 'file_contents' in the state.
    """
    logger.info(f"Analyzing directory: {state['directory']}")
    
    project_type = state.get('project_type')
    if project_type is None:
        project_type = detect_project_type(str(state['directory']))
        logger.info(f"Auto-detected project type: {project_type}")
    
    code_files = find_code_files(
        str(state['directory']),
        state['max_files'],
        project_type
    )
    
    if not code_files:
        raise DocGeneratorError("No supported code files found.")

    logger.info(f"Found {len(code_files)} files to analyze")
    
    file_contents = []
    for file_path in code_files:
        rel_path = os.path.relpath(file_path, state['directory'])
        logger.debug(f"Reading: {rel_path}")
        content = read_file_safe(file_path)
        
        if content:
            file_contents.append({
                "path": rel_path,
                "content": content
            })

    if not file_contents:
        raise DocGeneratorError("No files could be read successfully.")
    
    logger.info(f"Successfully read {len(file_contents)} files")
    
    return {
        **state,
        "file_contents": file_contents,
        "project_type": project_type,
    }

def generate_draft(state: AgentState) -> AgentState:
    """
    Generates the initial documentation draft.
    """
    logger.info("Generating initial documentation draft...")
    
    agent = AIAgent(
        directory=state['directory'],
        max_files=state['max_files'],
        model=state['model'],
        project_type=state['project_type'],
        output_format=state['output_format'],
        output_file=state['output_file'],
        config=state['config']
    )
    agent.file_contents = state['file_contents']
    
    documentation = agent.generate_documentation_draft()
    
    return {**state, "documentation": documentation}

def critique_document(state: AgentState) -> AgentState:
    """
    Critiques the current documentation draft.
    """
    logger.info("Critiquing documentation...")
    
    agent = AIAgent(
        directory=state['directory'],
        max_files=state['max_files'],
        model=state['model'],
        project_type=state['project_type'],
        output_format=state['output_format'],
        output_file=state['output_file'],
        config=state['config']
    )
    
    critique = agent.critique_documentation(state['documentation'])
    
    return {**state, "critique": critique}

def refine_document(state: AgentState) -> AgentState:
    """
    Refines the documentation based on the critique.
    """
    logger.info("Refining documentation...")
    
    agent = AIAgent(
        directory=state['directory'],
        max_files=state['max_files'],
        model=state['model'],
        project_type=state['project_type'],
        output_format=state['output_format'],
        output_file=state['output_file'],
        config=state['config']
    )
    agent.file_contents = state['file_contents']

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
    
    agent = AIAgent(
        directory=state['directory'],
        max_files=state['max_files'],
        model=state['model'],
        project_type=state['project_type'],
        output_format=state['output_format'],
        output_file=state['output_file'],
        config=state['config']
    )
    
    if agent._is_critique_positive(state['critique']):
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
    workflow.add_node("generate_draft", generate_draft)
    workflow.add_node("critique_document", critique_document)
    workflow.add_node("refine_document", refine_document)

    # Set entry point
    workflow.set_entry_point("analyze_codebase")

    # Add edges
    workflow.add_edge("analyze_codebase", "generate_draft")
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
        config=AgentConfig()
    )
    
    # Build and run the graph
    app = build_graph()
    final_state = app.invoke(initial_state)
    
    # Save the final documentation
    if final_state.get("documentation"):
        output_path = save_documentation(
            final_state["documentation"],
            final_state["output_format"],
            final_state["output_file"],
            output_dir=final_state["directory"] / "output"
        )
        logger.info(f"Documentation saved to: {output_path}")
    else:
        logger.error("Failed to generate documentation.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
