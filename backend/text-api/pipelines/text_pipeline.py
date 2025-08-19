from abc import ABC, abstractmethod

class TextPipeline(ABC):
    @abstractmethod
    def run(self, text: str) -> str:
        """
        Run the text pipeline on the provided text.

        :param text: The input text to be processed.
        :return: A dictionary containing the results of the processing.
        """
        pass

class CompositeTextPipeline(TextPipeline):
    def __init__(self, operations: list[TextPipeline]):
        """
        Initialize the composite text pipeline with a list of operations.

        :param operations: A list of TextPipeline instances to be executed in sequence.
        """
        super().__init__()
        self.operations = operations

    def run(self, text: str) -> str:
        """
        Run the composite text pipeline on the provided text.

        :param text: The input text to be processed.
        :return: A dictionary containing the results of the processing.
        """
        result = text
        for operation in self.operations:
            result = operation.run(text)
        return result

class LowercaseTextOperation(TextPipeline):
    def run(self, text: str) -> str:
        return text.lower()

class RemovePunctuationOperation(TextPipeline):
    def run(self, text: str) -> str:
        import re
        return re.sub(r'[^\w\s]', '', text)

class TextPipelineFactory:
    @staticmethod
    def list_available_pipelines() -> list:
        """
        List all available text pipelines.

        :return: A list of pipeline names.
        """
        return ["lowercase-text", "clean-text"]

    @staticmethod
    def create_pipeline(pipeline_name: str) -> TextPipeline:
        """
        Create an instance of a text pipeline based on the provided name.

        :param pipeline_name: The name of the text pipeline to create.
        :return: An instance of the specified text pipeline.
        """
        if pipeline_name == "lowercase-text":
            return LowercaseTextOperation()
        elif pipeline_name == "clean-text":
            return CompositeTextPipeline(operations=[
                LowercaseTextOperation(),
                RemovePunctuationOperation()
            ])
        else:
            raise ValueError(f"Unknown pipeline name: {pipeline_name}")
