import re
import string
from typing import List, Tuple


class BionicReading:
    """Read faster with your brain, not your eyes."""

    def __init__(self, fixation: float = .6, saccades: float = .75, opacity: float = .75):
        """
        Inits BionicReading

        :param fixation: Fixation you define the expression of the letter combinations
        :type fixation: float
        :param saccades: Saccades you define the visual jumps from fixation to fixation
        :type saccades: float
        :param opacity: Opacity you define the visibility of your fixation
        :type opacity: float
        """
        self.fixation = fixation
        self.saccades = saccades
        self.opacity = opacity
        self.non_tokens = string.punctuation + " \n\t"
        self.bold = '\033[1m'
        self.end = '\033[0m'
        self.bold_weight = opacity * 1000

    @staticmethod
    def split_text_to_words(text: str) -> List[str]:
        """
        It splits a string into a list of words

        :param text: The text to split into words
        :type text: str
        :return: A list of strings
        """
        tokens = re.split("([\t \n-])", text)

        return [token for token in tokens if len(token) > 0]

    def opacity_highlight(self, token: str, output_format: str) -> str:
        """
        If the output format is HTML, return the token surrounded by `<b>` tags. Otherwise, return the token surrounded
        by the `bold` and `end` attributes of the `self` object.

        :param token: The token to be highlighted
        :type token: str
        :param output_format: The output format of the code. This can be "html" or "terminal"
        :type output_format: str
        :return: The token is being returned with the bold formatting.
        """
        if output_format == "html":
            return f"<b>{token}</b>"
        else:
            return f"{self.bold}{token}{self.end}"

    def fixation_highlight(self, token: str) -> Tuple[str, str]:
        """
        It takes a string and returns a tuple of two strings. The first string is the part of the string that should be
        highlighted, and the second string is the part of the string that should not be highlighted

        :param token: the string to be highlighted
        :type token: str
        :return: The first return value is the part of the token that has been read, and the second return value is the
        part of the token that has not been read.
        """
        if len(token) <= 2:
            return token[0], token[1:]
        last_char_index = round(self.fixation * len(token))

        return token[:last_char_index], token[last_char_index:]

    def saccades_highlight(self, tokens: List[str], output_format: str) -> List[str]:
        """
        If the saccades value is less than 1/3, then every third token is highlighted. If the saccades value is less
        than 2/3, then every second token is highlighted. Otherwise, every token is highlighted

        :param tokens: a list of tokens to highlight
        :type tokens: List[str]
        :param output_format: The format of the output. This is used to determine the color of the highlighted text
        :type output_format: str
        :return: A list of tokens with the saccades highlighted.
        """
        token_to_skip = 3 if self.saccades < 1/3 else 2 if self.saccades < 2/3 else 1
        index = 0
        highlighted_tokens = []
        for token in tokens:
            if token not in self.non_tokens:
                index += 1
                if index % token_to_skip == 0 or index == 1:
                    token_to_highlight, token_not_to_highlight = self.fixation_highlight(token)
                    token = self.opacity_highlight(token_to_highlight, output_format) + token_not_to_highlight
            highlighted_tokens.append(token)

        return highlighted_tokens

    @staticmethod
    def tokens_to_text(tokens: List[str]) -> str:
        """
        It takes a list of tokens and returns a string

        :param tokens: A list of tokens
        :type tokens: List[str]
        :return: A string of the tokens joined together.
        """
        return "".join(tokens)

    def to_output_format(self, text: str, output_format: str) -> str:
        """
        If the output format is HTML, then add the HTML tags to the highlighted text

        :param text: The text to be highlighted
        :type text: str
        :param output_format: The format of the output. Can be "html" or "text"
        :type output_format: str
        :return: The highlighted text.
        """
        output = text
        if output_format == "html":
            style = "b {font-weight: %d}" % self.bold_weight
            output = f"<!DOCTYPE html><html><head><style>{style}</style></head><body><p>{text}</p></body></html>"

        return output

    def read_faster(self, text: str, output_format: str = "html"):
        """
        The function takes a string of text, splits it into a list of words, highlights the words, and then returns the
        highlighted text

        :param text: the text you want to read faster
        :type text: str
        :param output_format: The format of the output. Can be "html" or "text", defaults to html
        :type output_format: str (optional)
        :return: The highlighted text
        """
        tokens = self.split_text_to_words(text)
        highlighted_tokens = self.saccades_highlight(tokens, output_format)
        highlighted_text = self.tokens_to_text(highlighted_tokens)

        return self.to_output_format(highlighted_text, output_format)
