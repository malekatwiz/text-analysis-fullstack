import abc


class TextOperation(abc.ABC):
    """
    Abstract base class for text operations.
    All text operations should inherit from this class and implement the `run` method.
    """

    @abc.abstractmethod
    def run(self, text: str) -> dict:
        """
        Run the text operation on the provided text.

        :param text: The input text to be processed.
        :return: A dictionary containing the results of the processing.
        """
        pass

class BadOfWordsOperation(TextOperation):
    def run(self, text: str) -> dict:
        """
        Run the Bag of Words operation on the provided text.

        :param text: The input text to be processed.
        :return: A dictionary containing the bag of words representation.
        """
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer()

        x = vectorizer.fit_transform([text])
        bag_of_words = x.toarray()

        vocabulary = vectorizer.get_feature_names_out()
        return {
            "bag_of_words": bag_of_words.tolist(),
            "vocabulary": vocabulary.tolist()
        }

class TextOperationsFactory:
    """
    Factory class to create instances of text operations.
    This class can be extended to add more text operations.
    """

    @staticmethod
    def list_available_operations() -> list:
        """
        List all available text operations.

        :return: A list of operation names.
        """
        return ["bag-of-words"]

    @staticmethod
    def get_processor(operation_name: str) -> TextOperation:
        """
        Get an instance of the specified text operation.

        :param operation_name: The name of the text operation to create.
        :return: An instance of the specified text operation.
        """
        if operation_name == "bag-of-words":
            return BadOfWordsOperation()
        else:
            raise ValueError(f"Unknown operation: {operation_name}")