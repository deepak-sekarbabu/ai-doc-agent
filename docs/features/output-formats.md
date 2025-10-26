# Multi-Format Output

Generate documentation in multiple professional formats: Markdown, HTML, and PDF.

## Overview

The AI Documentation Agent can output documentation in three formats, each optimized for different use cases. All formats contain the same comprehensive content, just styled differently.

## Supported Formats

### Markdown

GitHub/GitLab-ready documentation format.

**File Extension:** `.md`

**Use Cases:**
- ✅ GitHub/GitLab repositories
- ✅ Version control friendly
- ✅ Documentation sites (MkDocs, Docusaurus)
- ✅ Easy to edit and maintain
- ✅ Maximum portability

**Generate:**
```bash
# Default format
python run.py

# Explicit markdown
python run.py --format markdown
```

**Example Output:**
```markdown
# Project Documentation

## Overview
A modern web application built with React and TypeScript...

## Architecture
### Frontend
- React 18 with TypeScript
- Vite for bundling
- Tailwind CSS for styling

## Key Components
### App.tsx
Main application component that handles routing...
```

**Advantages:**
- ✅ Plain text - works everywhere
- ✅ Git-friendly - clear diffs
- ✅ Easy to edit with any text editor
- ✅ Supported by all documentation platforms
- ✅ No dependencies required

**Best For:**
- Open-source projects
- GitHub/GitLab documentation
- Team wikis
- Developer handbooks
- README files

---

### HTML

Styled, browser-ready documentation.

**File Extension:** `.html`

**Use Cases:**
- ✅ Internal documentation portals
- ✅ Team knowledge bases
- ✅ Offline documentation
- ✅ Professional presentations
- ✅ Shareable documentation

**Generate:**
```bash
python run.py --format html
```

**Features:**
- Professional styling
- Syntax highlighting
- Table of contents navigation
- Print-friendly layout
- Self-contained (CSS embedded)

**Example Output:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Project Documentation</title>
    <style>
        body { font-family: -apple-system, sans-serif; }
        code { background: #f4f4f4; padding: 2px 6px; }
        pre { background: #2d2d2d; color: #f8f8f2; }
        /* Professional styling... */
    </style>
</head>
<body>
    <h1>Project Documentation</h1>
    <nav><!-- Table of contents --></nav>
    <section>
        <h2>Overview</h2>
        <p>A modern web application...</p>
    </section>
    <!-- Styled content -->
</body>
</html>
```

**Advantages:**
- ✅ Professional appearance
- ✅ Works in any browser
- ✅ Syntax highlighting included
- ✅ No external dependencies
- ✅ Easy to share (single file)

**Best For:**
- Internal team documentation
- Client deliverables
- Documentation portals
- Offline documentation
- Quick sharing via email

---

### PDF

Print-ready, professional documentation.

**File Extension:** `.pdf`

**Use Cases:**
- ✅ Client deliverables
- ✅ Technical specifications
- ✅ Printed documentation
- ✅ Formal documentation
- ✅ Archive purposes

**Requirements:**
```bash
# Install wkhtmltopdf first

# Windows
choco install wkhtmltopdf

# macOS
brew install wkhtmltopdf

# Linux
sudo apt-get install wkhtmltopdf
```

**Generate:**
```bash
python run.py --format pdf
```

**Features:**
- Professional PDF layout
- Pagination
- Page numbers
- Table of contents
- Print-optimized styling
- Proper page breaks

**Advantages:**
- ✅ Professional appearance
- ✅ Fixed layout (looks same everywhere)
- ✅ Easy to print
- ✅ Universal compatibility
- ✅ Good for archives

**Disadvantages:**
- ⚠️ Requires wkhtmltopdf installation
- ⚠️ Larger file size
- ⚠️ Not easily editable
- ⚠️ Slower generation

**Best For:**
- Client presentations
- Formal specifications
- Printed manuals
- Technical reports
- Compliance documentation

## Format Comparison

| Feature | Markdown | HTML | PDF |
|---------|----------|------|-----|
| **File Size** | Small (~50KB) | Medium (~200KB) | Large (~500KB) |
| **Dependencies** | None | None | wkhtmltopdf |
| **Editable** | ✅ Very easy | ⚠️ Possible | ❌ Difficult |
| **Portable** | ✅ Excellent | ✅ Good | ✅ Excellent |
| **Styling** | ⚠️ Basic | ✅ Professional | ✅ Professional |
| **Print Quality** | ⚠️ Varies | ✅ Good | ✅ Excellent |
| **Git-Friendly** | ✅ Yes | ⚠️ Large diffs | ❌ Binary |
| **Generation Speed** | ⚡⚡⚡ Fast | ⚡⚡ Medium | ⚡ Slow |
| **Best For** | Repos | Web | Print |

## Usage Examples

### Example 1: GitHub Project Documentation

```bash
# Generate Markdown for README
python run.py \
  --directory ~/my-project \
  --format markdown \
  --output README
```

**Result:** `output/README.md` ready for GitHub

---

### Example 2: Internal Team Docs

```bash
# Generate HTML for team wiki
python run.py \
  --directory ~/api-server \
  --format html \
  --output team_api_docs
```

**Result:** `output/team_api_docs.html` - share via web or email

---

### Example 3: Client Deliverable

```bash
# Generate professional PDF
python run.py \
  --directory ~/client-project \
  --format pdf \
  --output client_documentation \
  --iterations 5
```

**Result:** `output/client_documentation.pdf` - professional PDF for client

---

### Example 4: Multi-Format Documentation

```bash
# Generate all three formats
python run.py --format markdown --output docs
python run.py --format html --output docs
python run.py --format pdf --output docs
```

**Result:**
- `output/docs.md` - For version control
- `output/docs.html` - For web viewing
- `output/docs.pdf` - For printing

## HTML Styling

The HTML output includes professional styling:

### Features

**Typography:**
- System font stack for native look
- Proper heading hierarchy
- Readable line spacing
- Optimized font sizes

**Code Blocks:**
```html
<pre><code class="language-python">
def hello():
    print("Syntax highlighted")
</code></pre>
```

**Colors:**
- Syntax highlighting
- Semantic colors for warnings/notes
- Professional color scheme
- Dark mode friendly code blocks

**Layout:**
- Responsive design
- Maximum width for readability
- Proper spacing and margins
- Print-friendly layout

### Customization

Edit styling in `src/doc_generator.py`:

```python
HTML_STYLE = """
<style>
    /* Customize your styles here */
    body {
        font-family: 'Your Preferred Font', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
    }
    /* More custom styles... */
</style>
"""
```

## PDF Generation

### Installation

#### Windows

```bash
# Using Chocolatey
choco install wkhtmltopdf

# Or download installer
# https://wkhtmltopdf.org/downloads.html
```

#### macOS

```bash
# Using Homebrew
brew install wkhtmltopdf
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install wkhtmltopdf

# Fedora
sudo dnf install wkhtmltopdf

# Arch
sudo pacman -S wkhtmltopdf
```

### Verification

```bash
# Check if installed
wkhtmltopdf --version

# Should output version number
wkhtmltopdf 0.12.6 (with patched qt)
```

### PDF Options

The agent uses optimized PDF settings:

```python
# In src/doc_generator.py
pdfkit.from_string(
    html_content,
    output_path,
    options={
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None
    }
)
```

### Troubleshooting PDF

#### wkhtmltopdf not found

```bash
# Add to PATH (Windows)
setx PATH "%PATH%;C:\Program Files\wkhtmltopdf\bin"

# Add to PATH (Linux/Mac)
export PATH=$PATH:/usr/local/bin
```

#### PDF generation fails

```bash
# Use HTML instead
python run.py --format html

# Convert HTML to PDF manually
wkhtmltopdf output/docs.html output/docs.pdf
```

#### Poor PDF quality

```bash
# Increase DPI in options
# Edit src/doc_generator.py:
options = {
    'dpi': 300,  # Higher quality
    'image-quality': 100
}
```

## Output Location

All formats are saved to `output/` directory:

```
output/
├── my_project_docs.md       # Markdown
├── my_project_docs.html     # HTML
└── my_project_docs.pdf      # PDF
```

**Directory Creation:**
- `output/` created automatically if missing
- Existing files are overwritten
- Subdirectories supported

**Custom Location:**
```bash
# Output directory is always 'output/'
# But you can move files after generation
python run.py --output my_docs --format html
mv output/my_docs.html /path/to/destination/
```

## Best Practices

### 1. Choose Format by Use Case

```bash
# For GitHub/GitLab
python run.py --format markdown

# For internal docs
python run.py --format html

# For clients
python run.py --format pdf
```

### 2. Generate Multiple Formats

```bash
# Create a script to generate all formats
#!/bin/bash
python run.py --format markdown --output docs
python run.py --format html --output docs
python run.py --format pdf --output docs
```

### 3. Version Control Consideration

```bash
# Add to .gitignore
echo "output/*.html" >> .gitignore
echo "output/*.pdf" >> .gitignore

# Keep markdown in version control
git add output/*.md
```

### 4. File Naming

```bash
# Descriptive names
python run.py --output api_documentation_v1.0
python run.py --output user_guide_2024

# Include date for versioning
python run.py --output docs_$(date +%Y%m%d)
```

## Format-Specific Tips

### Markdown Tips

**Optimize for GitHub:**
```bash
# Generate and place in root
python run.py --output README --format markdown
cp output/README.md ./README.md
```

**For MkDocs:**
```bash
# Generate for docs site
python run.py --output docs/api --format markdown
```

**For Wiki:**
```bash
# Generate and upload to wiki
python run.py --output wiki/Home --format markdown
```

### HTML Tips

**Hosting:**
```bash
# Generate HTML
python run.py --format html --output docs

# Serve locally
cd output
python -m http.server 8000
# Visit: http://localhost:8000/docs.html
```

**Embedding:**
```html
<!-- Embed in existing site -->
<iframe src="docs.html" width="100%" height="800px"></iframe>
```

### PDF Tips

**Professional Output:**
```bash
# Maximum quality
python run.py \
  --format pdf \
  --iterations 5 \
  --model codellama \
  --output professional_docs
```

**Batch Generation:**
```bash
# Generate PDFs for multiple projects
for dir in projects/*/; do
    python run.py --directory "$dir" --format pdf
done
```

## Performance Comparison

| Format | Generation Time | File Size | Quality |
|--------|----------------|-----------|---------|
| **Markdown** | 5 min | 50 KB | Text-based |
| **HTML** | 5.5 min | 200 KB | Styled |
| **PDF** | 6-8 min | 500 KB | Print-quality |

*Times for 30 files, 3 iterations*

**Optimization:**
```bash
# Fastest
python run.py --format markdown

# Balance speed/appearance
python run.py --format html

# Best appearance (slower)
python run.py --format pdf
```

## Conversion Between Formats

### Markdown → HTML

```bash
# Using pandoc
pandoc output/docs.md -o output/docs.html --standalone

# Or regenerate
python run.py --format html
```

### Markdown → PDF

```bash
# Using pandoc
pandoc output/docs.md -o output/docs.pdf

# Or regenerate with wkhtmltopdf
python run.py --format pdf
```

### HTML → PDF

```bash
# Using wkhtmltopdf directly
wkhtmltopdf output/docs.html output/docs.pdf
```

## Next Steps

- [Iterative Refinement](iterative-refinement.md) - Quality improvement
- [Project Detection](project-detection.md) - Smart file analysis
- [Quick Start](../getting-started/quickstart.md) - Get started
- [Configuration](../getting-started/configuration.md) - Customize output
