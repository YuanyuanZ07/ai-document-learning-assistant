def extract_text_from_file(file_path):
    """Read a file and return its text content."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text
