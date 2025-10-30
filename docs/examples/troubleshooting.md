# Troubleshooting

Common issues and their solutions when using the AI Documentation Agent.

## Quick Diagnosis

### Symptom Checklist

Check this first:

- [ ] Ollama is running: `ollama list`
- [ ] Model is installed: `ollama list | grep your-model`
- [ ] Python version: `python --version` (need 3.8+)
- [ ] Dependencies installed: `pip list | grep requests`
- [ ] `.env` file exists and configured
- [ ] Directory path is correct

## Common Issues

### Installation Issues

#### Issue: Python Not Found

**Symptom:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
```bash
# Reinstall Python with "Add to PATH" checked
# Or add Python to PATH manually
setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"
```

**Linux/macOS:**
```bash
# Use python3
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
ai-doc-agent --help

# Or create alias
echo "alias ai-doc='ai-doc-agent'" >> ~/.bashrc
source ~/.bashrc
```

---

#### Issue: Module Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**

```bash
# Install dependencies
pip install -r config/requirements.txt

# Or specific package
pip install requests dotenv markdown pdfkit

# Verify installation
pip list | grep requests
```

**Still not working?**
```bash
# Use pip3
pip3 install -r config/requirements.txt

# Or use python -m pip
python -m pip install -r config/requirements.txt

# Check if using virtual environment
which python  # Should point to venv if activated
```

---

### Ollama Connection Issues

#### Issue: Cannot Connect to Ollama

**Symptom:**
```
ERROR - Cannot connect to Ollama API
ConnectionError: [Errno 111] Connection refused
```

**Solutions:**

**1. Check if Ollama is running:**
```bash
# Test Ollama
ollama list

# If not running, start it
ollama serve

# On Windows (if installed as service)
# Check Services app for "Ollama" service
```

**2. Verify API URL:**
```bash
# Check .env file
cat .env | grep OLLAMA_API_URL

# Should be:
OLLAMA_API_URL=http://localhost:11434/api/generate

# Test manually
curl http://localhost:11434/api/tags
```

**3. Check firewall:**
```bash
# Ensure port 11434 is not blocked
netstat -an | grep 11434

# Or use telnet
telnet localhost 11434
```

---

#### Issue: Model Not Found

**Symptom:**
```
ERROR - Model 'llama2:7b' not found
```

**Solutions:**

```bash
# List available models
ollama list

# Pull the model
ollama pull llama2:7b

# Verify installation
ollama list | grep llama2

# Update .env
MODEL_NAME=llama2:7b
```

**Common models:**
```bash
ollama pull llama2:7b      # Fast, general
ollama pull mistral        # Balanced
ollama pull codellama      # Code-focused
ollama pull llama2:13b     # High quality
```

---

### API Timeout Issues

#### Issue: Request Timeout

**Symptom:**
```
ERROR - API request timeout after 300 seconds
ReadTimeout: HTTPSConnectionPool
```

**Solutions:**

**1. Increase timeout:**
```bash
# Edit .env
API_TIMEOUT=600  # 10 minutes

# Or even longer
API_TIMEOUT=900  # 15 minutes
```

**2. Reduce file count:**
```bash
ai-doc-agent --max-files 20
```

**3. Use faster model:**
```bash
# In .env
MODEL_NAME=llama2:7b  # Faster than llama2:13b

# Or command line
ai-doc-agent --model llama2:7b
```

**4. Reduce iterations:**
```bash
ai-doc-agent --max-iterations 2
```

---

### File Discovery Issues

#### Issue: No Files Found

**Symptom:**
```
WARNING - No files found in directory
INFO - Found 0 files to analyze
```

**Solutions:**

**1. Check directory path:**
```bash
# Use absolute path
ai-doc-agent --directory /absolute/path/to/project

# Or relative from project root
ai-doc-agent --directory ./my-project

# Verify directory exists
ls /path/to/project
```

**2. Check file types:**
```bash
# List files in directory
ls -la my-project/

# Check if any supported files
find my-project -name "*.py" -o -name "*.js"

# Supported extensions:
# .py, .js, .ts, .tsx, .jsx, .java, .cs, .go, .php, .rb, .rs
# .c, .cpp, .h, .hpp, .html, .css, .scss, .sql, .sh
# .kt, .swift, .vue, .svelte, .xml, .gradle
```

**3. Check ignored directories:**
```python
# Edit src/doc_generator.py if needed
IGNORED_DIRECTORIES = frozenset([
    "node_modules", ".git", ".vscode", "__pycache__",
    "dist", "build", "target"
    # Add or remove as needed
])
```

**4. Use verbose mode:**
```bash
ai-doc-agent --directory ./project --verbose
# Will show file discovery process
```

---

### Permission Issues

#### Issue: Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Solutions:**

**Linux/macOS:**
```bash
# Check permissions
ls -la /path/to/project

# Fix permissions
chmod -R 755 /path/to/project

# Or run with sudo (not recommended)
sudo ai-doc-agent --directory /path/to/project
```

**Windows:**
```bash
# Run as Administrator
# Right-click Command Prompt → "Run as administrator"

# Or check folder permissions
# Right-click folder → Properties → Security
```

---

### Output Issues

#### Issue: Output File Not Created

**Symptom:**
```
INFO - Documentation generated
# But file doesn't exist
```

**Solutions:**

**1. Check output directory:**
```bash
# Default location
ls output/

# Create if missing
mkdir output

# Check permissions
ls -la output/
```

**2. Specify output name:**
```bash
ai-doc-agent --output my_docs
# Creates: output/my_docs.md
```

**3. Check for errors:**
```bash
# Run with verbose
ai-doc-agent --verbose

# Check logs
cat ai_agent.log
```

---

#### Issue: PDF Generation Fails

**Symptom:**
```
ERROR - PDF generation failed
OSError: No wkhtmltopdf executable found
```

**Solutions:**

**1. Install wkhtmltopdf:**

**Windows:**
```bash
# Using Chocolatey
choco install wkhtmltopdf

# Or download from
# https://wkhtmltopdf.org/downloads.html
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

**2. Verify installation:**
```bash
wkhtmltopdf --version
```

**3. Use alternative format:**
```bash
# Use HTML instead
ai-doc-agent --format html

# Convert HTML to PDF manually later
wkhtmltopdf output/docs.html output/docs.pdf
```

---

### Quality Issues

#### Issue: Poor Documentation Quality

**Symptom:**
- Documentation lacks detail
- Missing sections
- Unclear explanations
- No examples

**Solutions:**

**1. Increase iterations:**
```bash
ai-doc-agent --max-iterations 5  # Default is 3
```

**2. Use better model:**
```bash
ai-doc-agent --model codellama  # Better for code

# Or in .env
MODEL_NAME=codellama
```

**3. Analyze more files:**
```bash
ai-doc-agent --max-files 100  # Default is 30
```

**4. Specify project type:**
```bash
ai-doc-agent --project-type backend
# More accurate than auto-detection
```

**5. Lower quality threshold (faster but lower quality):**
```bash
# In .env
CRITIQUE_THRESHOLD=0.7  # Default is 0.8
```

---

#### Issue: Documentation is Incomplete

**Symptom:**
- Missing deployment section
- No examples
- Incomplete API documentation

**Solutions:**

**1. More iterations:**
```bash
ai-doc-agent --max-iterations 7
```

**2. Increase timeout:**
```bash
# In .env
API_TIMEOUT=900
```

**3. Check critique logs:**
```bash
# Run with verbose
ai-doc-agent --verbose

# Look for critique feedback
grep "Critique:" ai_agent.log
```

**4. Ensure important files are analyzed:**
```bash
# Check if README is included
ai-doc-agent --verbose | grep README

# Increase file limit if needed
ai-doc-agent --max-files 75
```

---

### Performance Issues

#### Issue: Generation is Very Slow

**Symptom:**
- Takes > 15 minutes
- Each iteration takes very long

**Solutions:**

**1. Use faster model:**
```bash
MODEL_NAME=llama2:7b  # Faster than llama2:13b
```

**2. Reduce file count:**
```bash
ai-doc-agent --max-files 20
```

**3. Reduce iterations:**
```bash
ai-doc-agent --max-iterations 2
```

**4. Check system resources:**
```bash
# CPU usage
top  # Linux/macOS
taskmgr  # Windows

# Ollama status
ollama ps
```

**5. Close other applications:**
- LLMs need significant RAM and CPU
- Close browsers, IDEs, etc.

---

### Configuration Issues

#### Issue: Environment Variables Not Loading

**Symptom:**
- Settings in .env are ignored
- Using default values

**Solutions:**

**1. Check .env location:**
```bash
# Must be in project root
ls -la .env

# Not in config/
# Not in src/
```

**2. Check .env syntax:**
```bash
# Correct format (no spaces around =)
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b

# Wrong format
OLLAMA_API_URL = http://localhost:11434/api/generate  # No spaces!
```

**3. Check for quotes:**
```bash
# Don't use quotes unless needed
API_TIMEOUT=300  # Correct
API_TIMEOUT="300"  # Wrong (will be string)
```

**4. Verify loading:**
```python
# Test in Python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('MODEL_NAME'))
# Should print your model name
```

---

### Docker Issues

#### Issue: Docker Container Can't Connect to Ollama

**Symptom:**
```
ERROR - Connection refused to Ollama
```

**Solutions:**

**Windows/macOS:**
```bash
# Use host.docker.internal
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  ai-doc-agent --directory /workspace
```

**Linux:**
```bash
# Use host network
docker run --rm --network host \
  -v "$(pwd):/workspace" \
  ai-doc-agent --directory /workspace
```

---

#### Issue: Volume Mount Issues

**Symptom:**
- Files not accessible in container
- Permission denied

**Solutions:**

```bash
# Windows (use forward slashes)
docker run -v "//c/Projects/myapp:/workspace" ...

# Linux/macOS (use absolute paths)
docker run -v "/home/user/project:/workspace" ...

# Check current directory mount
docker run -v "$(pwd):/workspace" ...
```

---

## Error Messages Reference

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `Connection refused` | Ollama not running | `ollama serve` |
| `Model not found` | Model not installed | `ollama pull model-name` |
| `Permission denied` | File access issue | Check permissions |
| `Timeout` | Request too slow | Increase timeout |
| `No files found` | Directory issue | Check path |
| `Module not found` | Missing dependency | `pip install -r requirements.txt` |

---

## Debug Mode

### Enable Verbose Logging

```bash
# Command line
ai-doc-agent --verbose

# Check logs
tail -f ai_agent.log

# Search for errors
grep ERROR ai_agent.log

# Search for warnings
grep WARNING ai_agent.log
```

### Log File Analysis

```bash
# View full log
cat ai_agent.log

# Last 50 lines
tail -50 ai_agent.log

# Follow in real-time
tail -f ai_agent.log

# Search for specific issue
grep "timeout" ai_agent.log
grep "connection" ai_agent.log
```

---

## Getting Help

### Information to Provide

When asking for help, include:

1. **Error message** (full traceback)
2. **Command used** (exact command)
3. **Environment**:
   - OS and version
   - Python version: `python --version`
   - Ollama version: `ollama --version`
   - Model: `MODEL_NAME` from `.env`
4. **Log file** (relevant sections)
5. **Configuration** (`.env` without secrets)

### Example Bug Report

```markdown
**Issue:** Cannot generate documentation

**Error:**
```
ERROR - Connection refused to Ollama API
ConnectionError: [Errno 111]
```

**Command:**
```bash
ai-doc-agent --directory ./my-project --verbose
```

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.11.2
- Ollama: 0.1.14
- Model: llama2:7b

**Configuration:**
```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
```

**Logs:**
[Attach ai_agent.log]
```

---

## Advanced Troubleshooting

### Network Issues

```bash
# Test Ollama connectivity
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama2:7b","prompt":"test"}'

# Check port
netstat -an | grep 11434

# Test DNS
ping localhost
```

### Memory Issues

```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Ollama memory usage
ollama ps

# Close large models
ollama stop model-name
```

### File System Issues

```bash
# Check disk space
df -h

# Check output directory
ls -la output/

# Test file creation
touch output/test.txt
rm output/test.txt
```

---

## Prevention Tips

### 1. Regular Maintenance

```bash
# Update dependencies
pip install --upgrade -r config/requirements.txt

# Update Ollama
# Download latest from ollama.ai

# Update models
ollama pull llama2:7b
```

### 2. Test Before Important Runs

```bash
# Test with small project first
ai-doc-agent --directory ./examples --max-files 5

# Then run on actual project
ai-doc-agent --directory ./my-project
```

### 3. Use Version Control

```bash
# Save working configuration
cp .env .env.backup

# Track changes
git add .env.backup
git commit -m "Working configuration"
```

---

## Next Steps

- [Sample Projects](samples.md) - Working examples
- [Configuration](../getting-started/configuration.md) - Setup guide
- [Quick Start](../getting-started/quickstart.md) - Getting started
- [Command Reference](../guide/commands.md) - All commands
