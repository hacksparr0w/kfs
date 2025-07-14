from pathlib import Path

import pypdf


def extract_text(file: Path) -> str:
    reader = pypdf.PdfReader(file)
    content = []

    for page in reader.pages:
        content.append(page.extract_text(0))

    return "".join(content)
