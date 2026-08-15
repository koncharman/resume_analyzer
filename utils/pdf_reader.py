
from io import BytesIO

from pypdf import PdfReader


def extract_pdf_text(uploaded_file) -> str:
    """
    Extract text from a Streamlit UploadedFile PDF.

    Returns:
        Extracted text from all readable PDF pages.

    Raises:
        ValueError: If no readable text is found.
    """

    pdf_bytes = uploaded_file.getvalue()
    reader = PdfReader(BytesIO(pdf_bytes))

    page_texts: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            raise ValueError(
                f"Could not read page {page_number}: {exc}"
            ) from exc

        cleaned_text = text.strip()

        if cleaned_text:
            page_texts.append(cleaned_text)

    full_text = "\n\n".join(page_texts).strip()

    if not full_text:
        raise ValueError(
            "No readable text was found. "
            "The PDF may be scanned or image-based."
        )

    return full_text


