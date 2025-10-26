FROM python:3.11-slim

# Install wkhtmltopdf for PDF support
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ai_agent.py .
COPY src/doc_generator.py .

# Copy .env if it exists, otherwise use .env.example
COPY config/.env* ./
RUN if [ -f .env ]; then \
        echo "Using existing .env file"; \
    elif [ -f .env.example ]; then \
        cp .env.example .env && echo "Created .env from .env.example"; \
    else \
        echo "Warning: No .env file found"; \
    fi

# Create directory for output
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create entrypoint script
RUN echo '#!/bin/bash\ncd /workspace && python /app/ai_agent.py "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["--help"]
