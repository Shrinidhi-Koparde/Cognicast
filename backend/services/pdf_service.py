"""
PDF processing service — extracts text and images using PyMuPDF.
"""

import fitz  # PyMuPDF
import base64
import os
from typing import List


def extract_content(pdf_path: str) -> dict:
    """
    Extract text and images from a PDF file.

    Returns:
        {
            "text": str (full text),
            "chunks": [str] (~1000 words each),
            "images": [str] (base64-encoded images),
            "page_count": int
        }
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    images = []
    page_count = len(doc)

    for page_num in range(page_count):
        page = doc[page_num]

        # Extract text
        page_text = page.get_text("text")
        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"

        # Extract images
        try:
            image_list = page.get_images(full=True)
            for img_index, img_info in enumerate(image_list):
                try:
                    xref = img_info[0]
                    pix = fitz.Pixmap(doc, xref)

                    # Convert CMYK to RGB if needed
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    img_bytes = pix.tobytes("png")
                    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                    images.append(img_b64)
                    pix = None  # free memory
                except Exception:
                    continue  # Skip problematic images
        except Exception:
            pass  # Skip if image extraction fails for this page

    doc.close()

    # Split text into ~1000-word chunks
    chunks = _split_into_chunks(full_text, max_words=1000)

    return {
        "text": full_text,
        "chunks": chunks,
        "images": images,
        "page_count": page_count,
    }


def _split_into_chunks(text: str, max_words: int = 1000) -> List[str]:
    """Split text into chunks of approximately max_words words."""
    words = text.split()
    chunks = []
    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1

        if word_count >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks if chunks else [text]
