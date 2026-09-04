"""Text cleaning utilities for document ingestion."""

import re


def clean_text(text: str) -> str:
    """Clean extracted PDF text.

    - Fix hyphenated line breaks
    - Normalize whitespace
    - Remove excessive newlines
    """
    if not text:
        return ""

                                             
    text = re.sub(r"-\n", "", text)

                                  
    text = re.sub(r"\n+", " ", text)

                               
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()
