FROM python:3.12-slim

# Install OS-level deps (wkhtmltopdf)
RUN apt-get update && apt-get install -y wkhtmltopdf && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY . /app

# Install the package (editable not needed)
RUN python -m venv .venv \
    && . .venv/bin/activate \
    && pip install -e .[dev]

USER app

ENTRYPOINT ["ai-doc-agent"]
CMD ["--help"]
