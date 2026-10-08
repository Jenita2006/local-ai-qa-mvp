from pathlib import Path
import pandas as pd
from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}


def load_pdf(file_path):
    documents = []

    reader = PdfReader(file_path)

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append({
                "text": text.strip(),
                "source": Path(file_path).name,
                "page": page_number,
                "file_type": "PDF"
            })

    return documents


def load_txt(file_path):
    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if not text.strip():
        return []

    return [{
        "text": text.strip(),
        "source": Path(file_path).name,
        "page": None,
        "file_type": "TXT"
    }]


def load_docx(file_path):
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    text = "\n".join(paragraphs)

    if not text.strip():
        return []

    return [{
        "text": text,
        "source": Path(file_path).name,
        "page": None,
        "file_type": "DOCX"
    }]


def load_csv(file_path):
    dataframe = pd.read_csv(file_path)

    text = dataframe.to_string(
        index=False
    )

    if not text.strip():
        return []

    return [{
        "text": text,
        "source": Path(file_path).name,
        "page": None,
        "file_type": "CSV"
    }]


def load_document(file_path):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".txt":
        return load_txt(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    if extension == ".csv":
        return load_csv(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def load_documents(folder="data/documents"):
    folder_path = Path(folder)
    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    all_documents = []

    for file_path in folder_path.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        documents = load_document(file_path)

        all_documents.extend(documents)

    return all_documents