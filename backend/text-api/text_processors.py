import time
from abc import ABC, abstractmethod

from token_count import TokenCount


class TextOperationResult:
    def __init__(self, processed_text: str, results: dict, execution_time: float = 0.0):
        """
        Initialize the result of a text operation.

        :param processed_text: The text after processing.
        """
        self.processed_text = processed_text
        self.results = results
        self.execution_time = execution_time

    def __repr__(self):
        return f"TextOperationResult(processed_text={self.processed_text}, execution_time={self.execution_time})"

class TextOperation(ABC):
    def __init__(self, operation_name: str):
        """
        Initialize the text operation with a name.

        :param operation_name: The name of the text operation.
        """
        self.operation_name = operation_name

    @abstractmethod
    def run_operation(self, text: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method.")

    def execute(self, text: str) -> TextOperationResult:
        start_time = time.perf_counter()
        result = self.run_operation(text)
        duration_ms = (time.perf_counter() - start_time) * 1000 # Convert to milliseconds
        duration_ms = round(duration_ms, 2)  # Round to 2 decimal places

        return TextOperationResult(processed_text=text, results=result, execution_time=duration_ms)

class TokensCountOperation(TextOperation):
    def __init__(self):
        """
        Initialize the TokensCountOperation with a specific operation name.
        """
        super().__init__(operation_name="tokens-count")

    def run_operation(self, text: str) -> dict:
        token_counter = TokenCount()
        tokens_count = token_counter.num_tokens_from_string(text)
        return {"tokens_count": tokens_count}

class BagOfWordsOperation(TextOperation):
    def __init__(self):
        """
        Initialize the BagOfWordsOperation with a specific operation name.
        """
        super().__init__(operation_name="bag-of-words")

    def run_operation(self, text: str) -> dict:
        # Here you would implement the logic for the bag-of-words operation
        # For demonstration, we will just return the original text
        return {"bag_of_words": text.split()}

class TextOperationsFactory:
    def __init__(self):
        self.available_operations = {
            "tokens-count": TokensCountOperation,
            "bag-of-words": BagOfWordsOperation
        }

    def get_processor(self, operation_type: str) -> TextOperation:
        """
        Factory method to get the appropriate text processor based on the type.

        :param operation_type: The type of text processor to create.
        :return: An instance of a TextProcessor.
        """
        if operation_type in self.available_operations:
            return self.available_operations[operation_type]()
        raise ValueError(f"Processor type '{operation_type}' is not supported.")

    def get_available_operations(self) -> list:
        """
        Get a list of available text operations.

        :return: A list of operation names.
        """
        return list(self.available_operations.keys())