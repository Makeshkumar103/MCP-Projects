from pathlib import Path
from typing import Optional

from mcp.server.mcpserver import MCPServer

# Optional document libraries
from pypdf import PdfReader
from docx import Document


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Document Assistant")


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# All documents must be inside this folder.
DOCUMENTS_DIR = Path("./documents").resolve()

# Create the folder if it doesn't exist.
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
}


# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------

def safe_path(filename: str) -> Path:
    """
    Convert a user-provided filename into a safe path.

    Prevents paths such as:
        ../../secret.txt
        /etc/passwd
    """

    requested_path = (DOCUMENTS_DIR / filename).resolve()

    try:
        requested_path.relative_to(DOCUMENTS_DIR)
    except ValueError:
        raise ValueError("Access denied: file is outside the documents directory.")

    return requested_path


# ---------------------------------------------------------
# DOCUMENT TEXT EXTRACTION
# ---------------------------------------------------------

def extract_text(path: Path) -> str:
    """
    Extract text from TXT, Markdown, PDF, or DOCX.
    """

    extension = path.suffix.lower()

    if extension in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    elif extension == ".pdf":
        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    elif extension == ".docx":
        document = Document(str(path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )


# ---------------------------------------------------------
# TOOL 1: LIST FILES
# ---------------------------------------------------------

@mcp.tool()
def list_files() -> list[dict]:
    """
    List all supported documents inside the documents directory.
    """

    files = []

    for path in DOCUMENTS_DIR.rglob("*"):

        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:

            relative_path = path.relative_to(DOCUMENTS_DIR)

            files.append({
                "name": path.name,
                "path": str(relative_path),
                "type": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
            })

    return files


# ---------------------------------------------------------
# TOOL 2: READ FILE
# ---------------------------------------------------------

@mcp.tool()
def read_file(filename: str) -> str:
    """
    Read a text or Markdown file.

    Example:
        read_file("notes.txt")
    """

    path = safe_path(filename)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    if not path.is_file():
        raise ValueError(
            f"Not a file: {filename}"
        )

    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError(
            "read_file() supports only TXT and Markdown files. "
            "Use get_document() for PDF/DOCX."
        )

    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------
# TOOL 3: SEARCH FILES
# ---------------------------------------------------------

@mcp.tool()
def search_files(query: str) -> list[dict]:
    """
    Search for text inside supported documents.

    Returns matching files and snippets.
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    query_lower = query.lower()

    results = []

    for path in DOCUMENTS_DIR.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            text = extract_text(path)
        except Exception:
            continue

        text_lower = text.lower()

        if query_lower not in text_lower:
            continue

        # Find first occurrence
        index = text_lower.find(query_lower)

        start = max(0, index - 100)
        end = min(len(text), index + len(query) + 200)

        snippet = text[start:end].replace("\n", " ")

        results.append({
            "file": str(path.relative_to(DOCUMENTS_DIR)),
            "match": snippet,
        })

    return results


# ---------------------------------------------------------
# TOOL 4: GET DOCUMENT
# ---------------------------------------------------------

@mcp.tool()
def get_document(
    filename: str,
    max_characters: Optional[int] = 10000
) -> dict:
    """
    Extract text and metadata from a document.

    Supports:
        TXT
        Markdown
        PDF
        DOCX
    """

    path = safe_path(filename)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {filename}"
        )

    if not path.is_file():
        raise ValueError(
            f"Not a file: {filename}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )

    text = extract_text(path)

    truncated = False

    if max_characters and len(text) > max_characters:
        text = text[:max_characters]
        truncated = True

    return {
        "name": path.name,
        "path": str(path.relative_to(DOCUMENTS_DIR)),
        "type": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "characters": len(text),
        "truncated": truncated,
        "content": text,
    }


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
