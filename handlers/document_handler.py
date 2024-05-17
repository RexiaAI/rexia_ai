# document_handler.py
from docx import Document

class DocumentHandler:
    def create_word_document(self, text, file_path):
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)