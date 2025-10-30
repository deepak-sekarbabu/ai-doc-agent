# Sample Projects

Examples demonstrating how to use the AI Documentation Agent with different project types.

## Overview

This guide provides practical examples for generating documentation across various project types, languages, and frameworks.

## Quick Start Example

### Basic Python Project

Generate documentation for a simple Python project:

```bash
# Navigate to your project
cd my-python-project

# Generate documentation
ai-doc-agent
```

**Output:** `output/my-python-project_documentation.md`

## Project Type Examples

### Example 1: Flask API Backend

**Project Structure:**
```
flask-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── config.py
└── run.py
```

**Generate Documentation:**

```bash
ai-doc-agent \
--directory ./flask-api \
--project-type backend \
--model codellama \
  --format html \
  --output flask_api_docs
```

**Expected Output:**
- API endpoints documented
- Database models explained
- Configuration options listed
- Setup instructions included

**Result:** `output/flask_api_docs.html`

---

### Example 2: React Frontend

**Project Structure:**
```
react-app/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Dashboard.tsx
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

**Generate Documentation:**

```bash
ai-doc-agent \
--directory ./react-app \
--project-type frontend \
--format markdown \
--max-iterations 4 \
--output react_component_docs
```

**Expected Output:**
- Component hierarchy explained
- Props and state documented
- Routing structure outlined
- Build configuration detailed

**Result:** `output/react_component_docs.md`

---

### Example 3: Full-Stack Application

**Project Structure:**
```
fullstack-app/
├── frontend/
│   ├── src/
│   └── package.json
├── backend/
│   ├── api/
│   └── requirements.txt
└── README.md
```

**Generate Documentation:**

```bash
# Document entire project
ai-doc-agent \
--directory ./fullstack-app \
--project-type mixed \
--max-files 100 \
--max-iterations 5 \
--format pdf \
--output comprehensive_docs

# Or document separately
ai-doc-agent --directory ./fullstack-app/frontend --project-type frontend
ai-doc-agent --directory ./fullstack-app/backend --project-type backend
```

**Expected Output:**
- System architecture overview
- Frontend and backend integration
- API contracts documented
- Deployment instructions

**Result:** `output/comprehensive_docs.pdf`

---

### Example 4: Microservices Architecture

**Project Structure:**
```
microservices/
├── user-service/
│   └── src/
├── auth-service/
│   └── src/
├── payment-service/
│   └── src/
└── docker-compose.yml
```

**Generate Documentation:**

```bash
# Document each service
for service in user-service auth-service payment-service; do
ai-doc-agent \
--directory ./microservices/$service \
--project-type backend \
--output ${service}_docs \
--format html
done

# Combine later or document entire system
ai-doc-agent \
--directory ./microservices \
--max-files 150 \
--output microservices_architecture \
--max-iterations 5
```

---

### Example 5: Mobile App (React Native)

**Project Structure:**
```
mobile-app/
├── src/
│   ├── screens/
│   ├── components/
│   ├── navigation/
│   └── services/
├── package.json
├── app.json
└── babel.config.js
```

**Generate Documentation:**

```bash
ai-doc-agent \
--directory ./mobile-app \
--project-type frontend \
--max-files 75 \
--format html \
--output mobile_app_docs
```

---

### Example 6: Java Spring Boot

**Project Structure:**
```
spring-api/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── controllers/
│   │   │       ├── services/
│   │   │       └── repositories/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
└── pom.xml
```

**Generate Documentation:**

```bash
ai-doc-agent \
  --directory ./spring-api \
  --project-type backend \
  --model codellama \
  --max-files 80 \
  --max-iterations 4 \
  --output spring_api_reference
```

---

### Example 7: Go Microservice

**Project Structure:**
```
go-service/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handlers/
│   ├── models/
│   └── services/
├── go.mod
└── go.sum
```

**Generate Documentation:**

```bash
ai-doc-agent \
  --directory ./go-service \
  --project-type backend \
  --model codellama \
  --output go_service_docs
```

---

### Example 8: Vue.js SPA

**Project Structure:**
```
vue-app/
├── src/
│   ├── views/
│   ├── components/
│   ├── store/
│   └── router/
├── package.json
└── vite.config.js
```

**Generate Documentation:**

```bash
ai-doc-agent \
  --directory ./vue-app \
  --project-type frontend \
  --format html \
  --output vue_documentation
```

## Advanced Examples

### Example 9: Multi-Format Documentation

Generate all three formats for distribution:

```bash
#!/bin/bash
PROJECT_DIR="./my-project"
OUTPUT_NAME="project_docs"

# Markdown for GitHub
ai-doc-agent \
  --directory $PROJECT_DIR \
  --format markdown \
  --output $OUTPUT_NAME

# HTML for web viewing
ai-doc-agent \
  --directory $PROJECT_DIR \
  --format html \
  --output $OUTPUT_NAME

# PDF for printing
ai-doc-agent \
  --directory $PROJECT_DIR \
  --format pdf \
  --output $OUTPUT_NAME

echo "Generated all formats in output/ directory"
```

---

### Example 10: CI/CD Integration

Automated documentation in GitHub Actions:

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [main]

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r config/requirements.txt
      
      - name: Generate documentation
        run: |
          ai-doc-agent \
            --directory . \
            --format markdown \
            --output docs/API_REFERENCE \
            --max-iterations 3
      
      - name: Commit documentation
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add docs/API_REFERENCE.md
          git commit -m "Auto-generate API documentation" || exit 0
          git push
```

---

### Example 11: Batch Processing

Document multiple projects:

```bash
#!/bin/bash
# batch_document.sh

PROJECTS=(
  "/path/to/project1"
  "/path/to/project2"
  "/path/to/project3"
)

for project in "${PROJECTS[@]}"; do
  project_name=$(basename $project)
  
  echo "Generating docs for $project_name..."
  
  ai-doc-agent \
    --directory $project \
    --output ${project_name}_docs \
    --format html \
    --max-iterations 3 \
    --verbose
  
  echo "✓ Completed $project_name"
done

echo "All projects documented!"
```

---

### Example 12: Custom Quality Settings

High-quality documentation with strict criteria:

```bash
# Create custom .env
cat > .env.custom << EOF
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=codellama
API_TIMEOUT=900
MAX_RETRIES=5
RETRY_DELAY=3
CRITIQUE_THRESHOLD=0.95
EOF

# Use custom configuration
cp .env.custom .env

# Generate with high quality
ai-doc-agent \
  --directory ./important-project \
  --max-iterations 10 \
  --max-files 200 \
  --format pdf \
  --output premium_documentation \
  --verbose
```

## Language-Specific Examples

### Python Projects

```bash
# Django project
ai-doc-agent \
  --directory ./django-app \
  --project-type backend \
  --max-files 80

# FastAPI
ai-doc-agent \
  --directory ./fastapi-service \
  --project-type backend \
  --model codellama

# Data Science project
ai-doc-agent \
  --directory ./ml-project \
  --max-files 50 \
  --format html
```

### JavaScript/TypeScript Projects

```bash
# Express API
ai-doc-agent \
  --directory ./express-api \
  --project-type backend

# Next.js app
ai-doc-agent \
  --directory ./nextjs-app \
  --project-type frontend \
  --max-files 100

# Angular app
ai-doc-agent \
  --directory ./angular-app \
  --project-type frontend
```

### Java Projects

```bash
# Spring Boot
ai-doc-agent \
  --directory ./spring-boot-app \
  --project-type backend \
  --model codellama

# Maven project
ai-doc-agent \
  --directory ./maven-project \
  --max-files 100
```

### Go Projects

```bash
# Go service
ai-doc-agent \
  --directory ./go-service \
  --project-type backend \
  --model codellama
```

## Testing the Agent

### Sample Test Project

Use the included example:

```bash
# Test with sample project
ai-doc-agent \
  --directory ./examples \
  --max-files 5 \
  --verbose

# Verify output
cat output/examples_documentation.md
```

### Create Test Project

```bash
# Create minimal test project
mkdir test-project
cd test-project

# Create files
cat > app.py << EOF
"""Sample Flask application."""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    """Home endpoint."""
    return {"message": "Hello World"}
EOF

cat > requirements.txt << EOF
Flask==2.0.0
EOF

# Generate docs
python ../run.py --directory . --verbose
```

## Output Examples

### Markdown Output Sample

```markdown
# Project Documentation

## Overview
A Flask-based REST API providing...

## Architecture
### System Components
- **Flask Application**: Main web server
- **SQLite Database**: Data persistence
- **Redis Cache**: Session management

## API Endpoints
### GET /api/users
Retrieve all users from database.

**Response:**
```json
{
  "users": [...]
}
```
...
```

### HTML Output Features

- Professional styling
- Syntax-highlighted code blocks
- Responsive design
- Table of contents
- Print-friendly layout

### PDF Output Features

- Professional formatting
- Proper pagination
- Headers and footers
- Table of contents
- Print-ready quality

## Troubleshooting Examples

### Issue: Large Project Timeout

```bash
# Problem: Project with 500+ files times out

# Solution 1: Limit files
ai-doc-agent --directory ./large-project --max-files 100

# Solution 2: Increase timeout
# In .env: API_TIMEOUT=900
ai-doc-agent --directory ./large-project

# Solution 3: Document in parts
ai-doc-agent --directory ./large-project/backend --output backend_docs
ai-doc-agent --directory ./large-project/frontend --output frontend_docs
```

### Issue: Poor Quality Output

```bash
# Problem: Documentation lacks detail

# Solution 1: More iterations
ai-doc-agent --directory ./project --max-iterations 7

# Solution 2: Better model
ai-doc-agent --directory ./project --model codellama

# Solution 3: More files
ai-doc-agent --directory ./project --max-files 100

# Solution 4: Specify project type
ai-doc-agent --directory ./project --project-type backend
```

## Best Practices

### 1. Start Small

```bash
# Test with limited files first
ai-doc-agent --directory ./project --max-files 20 --max-iterations 2

# Then scale up
ai-doc-agent --directory ./project --max-files 100 --max-iterations 5
```

### 2. Use Appropriate Models

```bash
# Quick testing
ai-doc-agent --model llama2:7b

# Production docs
ai-doc-agent --model codellama
```

### 3. Specify Project Type

```bash
# More accurate results
ai-doc-agent --project-type backend
```

### 4. Use Verbose Mode

```bash
# See what's happening
ai-doc-agent --verbose
```

## Next Steps

- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Quick Start](../getting-started/quickstart.md) - Get started guide
- [Command Reference](../guide/commands.md) - All commands
- [Configuration](../getting-started/configuration.md) - Setup options
