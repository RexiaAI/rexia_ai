# document_handler.py
from docx import Document

class DocumentHandler:
    """Handler for Word documents."""

    def create_word_document(self, text: str, file_path: str) -> None:
        """
        Create a Word document with the given text and save it to the specified file path.

        Parameters:
        text (str): The text to add to the document.
        file_path (str): The path where the document should be saved.
        """
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)# document_handler.py
from docx import Document