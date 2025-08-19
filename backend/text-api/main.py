import logging
import uuid
from abc import ABC

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from operations.text_operations import TextOperationsFactory, TextOperation


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

@app.get("/")
async def read_root():
    return {"Hello": "World"}


from fastapi import APIRouter

text_operations_router = APIRouter(
    prefix="/text-operations",
    tags=["text_operations"]
)

def resolve_text_operation(operation_name: str) -> TextOperation:
    """
    This function resolves the text operation based on the operation name.
    In a real application, you would implement logic to return the appropriate handler.
    """
    return TextOperationsFactory().get_processor(operation_name)

@text_operations_router.get("")
async def list_operations():
    """
    List all available text operations.
    """
    return {"available_operations": TextOperationsFactory.list_available_operations()}

@text_operations_router.post("/{operation_name}")
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


app.include_router(text_operations_router)

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8001)