import os
from abc import ABC, abstractmethod

class FileIngestionStep(ABC):
    def run(self, file_path: str, encoding: str = "utf-8"):
        if not file_path:
            raise ValueError("File path cannot be empty.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        return self.read_file(file_path, encoding)

    @abstractmethod
    def read_file(self, file_path: str, encoding: str = "utf-8"):
        raise NotImplementedError("This method should be overridden in subclasses.")

class DocumentIngestionStep(FileIngestionStep):
    def read_file(self, file_path: str, encoding: str = "utf-8"):
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        result = converter.convert(file_path)
        if not result or result.errors:
            raise ValueError(f"Failed to convert document {file_path}. Errors: {result.errors}")

        results = []
        for t in result.document.texts:
            results.append({
                "label": t.label.value,
                "text": t.text,
            })
        return results

class CsvFileIngestionStep(FileIngestionStep):
    def read_file(self, file_path: str, encoding: str = "utf-8"):
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")

class FileIngestionFactory:
    @staticmethod
    def create_ingestion_step(file_extension: str) -> FileIngestionStep:
        if file_extension.endswith(("pdf", "docx", "doc", "xls", "xlsx", "ppt", "pptx")):
            return DocumentIngestionStep()
        elif file_extension.endswith("csv"):
            return CsvFileIngestionStep()
        else:
            raise ValueError(f"Unsupported file type for {file_extension}.")