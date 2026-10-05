# Document MCP Server

An MCP (Model Context Protocol) server that provides document reading, searching, and listing capabilities for AI assistants.

## Features

- **List files** - Discover all supported documents in the workspace
- **Read files** - Read text/markdown files directly
- **Search files** - Full-text search across all supported formats
- **Get document** - Extract text and metadata from PDF, DOCX, TXT, and Markdown

## Supported Formats

| Format | Extension | Text Extraction |
|--------|-----------|-----------------|
| Text | `.txt` | ✅ |
| Markdown | `.md` | ✅ |
| PDF | `.pdf` | ✅ (via pypdf) |
| Word | `.docx` | ✅ (via python-docx) |

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone and navigate to project
cd document-mcp-server

# Install dependencies
uv sync
# or: pip install -e .
```

### Project Structure

```
document-mcp-server/
├── server.py              # Main MCP server entry point
├── pyproject.toml         # Project configuration
├── uv.lock                # Locked dependencies
├── documents/             # Place your documents here (auto-created)
└── .venv/                 # Virtual environment (ignored)
```

### Running the Server

```bash
# Development mode (with hot reload)
uv run mcp dev server.py

# Production mode
uv run mcp run server.py

# Or run directly
uv run python server.py
```

## MCP Tools

### `list_files()` → `list[dict]`
Returns all supported documents in the documents directory.

```json
[
  {"name": "report.pdf", "path": "report.pdf", "type": ".pdf", "size_bytes": 245123},
  {"name": "notes.txt", "path": "notes.txt", "type": ".txt", "size_bytes": 1834}
]
```

### `read_file(filename: str)` → `str`
Reads a text or Markdown file by name.

```python
read_file("notes.txt")  # Returns file contents
```

### `search_files(query: str)` → `list[dict]`
Searches for text across all supported documents.

```python
search_files("machine learning")
# Returns: [{"file": "report.pdf", "match": "...machine learning snippet..."}]
```

### `get_document(filename: str, max_characters: int = 10000)` → `dict`
Extracts full text and metadata from any supported document.

```python
get_document("report.pdf")
# Returns: {"name": "report.pdf", "type": ".pdf", "size_bytes": 245123, "characters": 8234, "truncated": false, "content": "..."}
```

## Configuration

The server uses a `documents/` folder in the project root. All documents must be placed there for security (path traversal protection).

```python
DOCUMENTS_DIR = Path("./documents").resolve()
```

## Security

- **Path traversal protection** - `safe_path()` ensures files can't escape the documents directory
- **File type validation** - Only supported extensions are processed
- **Input sanitization** - Search queries and filenames are validated

## Development

### Adding New Document Types

1. Add extension to `SUPPORTED_EXTENSIONS`
2. Add extraction logic in `extract_text()`
3. Update `read_file()` restrictions if needed

### Testing

```bash
# Run the server in dev mode
uv run mcp dev server.py

# Test with MCP client (e.g., Claude Desktop)
```

## Roadmap

- [ ] Vector embeddings for semantic search
- [ ] Document chunking for large files
- [ ] Metadata extraction (author, dates, etc.)
- [ ] OCR support for scanned PDFs
- [ ] Caching layer for repeated searches

## License

MIT