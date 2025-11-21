"""Setup configuration for AI Documentation Agent."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
req_file = this_directory / "config" / "requirements.txt"
if req_file.exists():
    requirements = [line.strip() for line in req_file.read_text().split('\n') 
                   if line.strip() and not line.startswith('#')]

setup(
    name="ai-doc-agent",
    version="2.0.0",
    author="Deepak",
    author_email="deepakinmail@gmail.com",
    description="AI-powered documentation generator with iterative self-improvement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepak-sekarbabu/ai-doc-agent",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [

            "ai-doc-agent=langgraph_agent:main",
            "doc-generator=doc_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md"],
    },
    keywords="documentation ai llm ollama code-analysis agent automation",
)
