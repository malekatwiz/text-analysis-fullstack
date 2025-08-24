import logging
import os
import uuid
from abc import ABC
from functools import lru_cache

from fastapi import FastAPI, Depends, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

import config
from llm.prompts import PromptsFactory
from operations.text_operations import TextOperationsFactory, TextOperation
from pipelines.ingestion import FileIngestionStep, FileIngestionFactory
from services.similarity import TextSimilarityService
from services.text_generator import TextGeneratorService


class OperationRequest(BaseModel, ABC):
    """
    Base class for all operation requests.
    This class is abstract and should not be instantiated directly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    request_id: str = Field(
        default=str(uuid.uuid4()),
        title="Request ID",
        description="Unique identifier for the request, automatically generated."
    )

class TextOperationRequest(OperationRequest):
    text_content: str = Field(
        default="",
        title="Text Content",
        description="The text content to be processed by the operation."
    )

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@lru_cache
def get_settings():
    return config.Configuration()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Text Operations API"}


from fastapi import APIRouter

text_router = APIRouter(
    prefix="/text",
    tags=["text"]
)

def resolve_text_operation(operation_name: str) -> TextOperation:
    """
    This function resolves the text operation based on the operation name.
    In a real application, you would implement logic to return the appropriate handler.
    """
    return TextOperationsFactory().get_processor(operation_name)

def file_ingestion(file_name: str) -> FileIngestionStep:
    file_extension = file_name.split('.')[-1].lower()
    return FileIngestionFactory.create_ingestion_step(file_extension)

@text_router.get("")
async def list_operations():
    """
    List all available text operations.
    """
    return {"available_operations": TextOperationsFactory.list_available_operations()}

@text_router.post("/{operation_name}")
async def process_text(request: TextOperationRequest, processor: TextOperation = Depends(resolve_text_operation)):
    try:
        operation_result = processor.run(request.text_content)
        return {
            "request_id": request.request_id,
            "result": operation_result
        }
    except Exception as e:
        logging.error(f"Error processing text: {e}")
        return {"error": str(e)}

class TextSimilarityRequest(BaseModel):
    text: list[str] = Field(
        default=[],
        title="Text List",
        description="A list of text contents for similarity calculation."
    )

class TextExtractionRequest(BaseModel):
    text: str = Field(
        default="",
        title="Text Content",
        description="The text content to extract information from."
    )

    prompt_id: str = Field(
        default="",
        title="Prompt ID",
        description="Identifier for the extraction prompt to be used."
    )

@text_router.post("similarity-score")
async def calculate_similarity_score(request: TextSimilarityRequest):
    try:
        processor = TextSimilarityService()
        operation_result = await processor.compute_similarity(request.text)

        return {
            "similarity_score": operation_result
        }
    except Exception as e:
        logging.error(f"Error processing text: {e}")
        return {"error": str(e)}

@text_router.post("extract")
async def generate_extraction(request: TextExtractionRequest):
    try:
        text_generator = TextGeneratorService()

        generated_response = await text_generator.generate_text(request.prompt_id, request.text)
        return {
            "extracted_information": generated_response
        }
    except Exception as e:
        logging.error(f"Error processing text extraction: {e}")
        return {"error": str(e)}

files_router = APIRouter(
    prefix="/files",
    tags=["files"]
)

@files_router.post("/upload")
async def upload_file(file: UploadFile, settings: config.Configuration = Depends(get_settings)):
    """
    Upload a file and process it using the appropriate ingestion step.
    """
    allowed_extensions = ["txt", "pdf", "docx", "csv", "json"]
    if not file.filename.split('.')[-1].lower() in allowed_extensions:
        return HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types are: {', '.join(allowed_extensions)}"
        )

    if file.size > settings.max_file_size:  # Limit file size to 10MB
        return HTTPException(
            status_code=400,
            detail="File size exceeds the limit of 10MB."
        )

    try:
        destination_dir = os.path.join(settings.file_upload_dir, str(uuid.uuid4()))
        os.makedirs(destination_dir, exist_ok=True)
        file_path = os.path.join(destination_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logging.info(f"File uploaded successfully: {file_path}")

        # Process the file using the ingestion step
        file_content = file_ingestion(file.filename).run(file_path)
        return {
            "request_id": str(uuid.uuid4()),
            "file_path": file_path,
            "file_content": file_content
        }

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return {"error": str(e)}

app.include_router(text_router)
app.include_router(files_router)

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=get_settings().logging_level)
    uvicorn.run(app, host="0.0.0.0", port=8001)