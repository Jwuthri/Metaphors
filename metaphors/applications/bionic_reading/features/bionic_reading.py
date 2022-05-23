import re
import string
import pandas as pd

from typing import List, Tuple
from sklearn.feature_extraction.text import CountVectorizer

from metaphors.data import stopwords
from metaphors.utils.string_utils import string_contains_digit, strike_string
from metaphors.applications.bionic_reading.settings import RareBehavior, Format
from metaphors.applications.bionic_reading.settings import SIMPLE_SPLITTER, OutputFormat, StopWordsBehavior


class BionicReading:
    """Read faster with your brain, not your eyes."""

    def __init__(
        self,
        fixation: float = 0.6,
        saccades: float = 0.75,
        opacity: float = 0.75,
        stopwords: float = 0.25,
        stopwords_behavior: str = StopWordsBehavior.STRIKETHROUGH.value,
        output_format: str = OutputFormat.HTML.value,
        rare_words_behavior: str = RareBehavior.UNDERLINE.value,
        rare_words_max_freq: int = 5,
    ):
        """
        Inits BionicReading

        :param fixation: Fixation you define the expression of the letter combinations
        :type fixation: float
        :param saccades: Saccades you define the visual jumps from fixation to fixation
        :type saccades: float
        :param opacity: Opacity you define the visibility of your fixation
        :type opacity: float
        :param stopwords: Determine whether the list of stopwords is long or not
        :type stopwords: float
        :param stopwords_behavior: Change the way the stopwords are handled (remove, ignore, keep)
        :type stopwords_behavior: str
        :param output_format: The format of the output. Can be "html" or "python", defaults to html
        :type output_format: str
        :param rare_words_behavior: Change the way the rare words are handled (highlight, underline)
        :type rare_words_behavior: str
        :param rare_words_max_freq: Max frequency word to be considered as uncommon
        :type rare_words_max_freq: int
        """
        self.fixation = fixation
        self.saccades = saccades
        self.opacity = opacity
        self.stopwords = stopwords
        self.output_format = output_format
        self.stopwords_behavior = stopwords_behavior
        self.rare_words_behavior = rare_words_behavior
        self.rare_words_max_freq = rare_words_max_freq
        self.non_tokens = string.punctuation + " \n\t"
        self.highlight = "\033[93m"
        self.underline = "\033[4m"
        self.bold = "\033[1m"
        self.end = "\033[0m"

    @property
    def fixation(self):
        """
        It returns the fixation of the object.
        :return: The fixation is being returned.
        """
        return self._fixation

    @fixation.setter
    def fixation(self, value: float):
        """
        This function takes a float value and checks that it is between 0 and 1. If it is, it sets the value of the fixation
        attribute to the value passed in

        :param value: the value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a fixation float type"
        assert 0 <= value <= 1, "please enter a fixation value between 0 and 1"
        self._fixation = value

    @fixation.deleter
    def fixation(self):
        """
        It deletes the fixation attribute of the object.
        """
        del self._fixation

    @property
    def saccades(self):
        """
        This function returns the saccades of the current trial
        :return: The saccades are being returned.
        """
        return self._saccades

    @saccades.setter
    def saccades(self, value: float):
        """
        This function takes a float value between 0 and 1 and assigns it to the saccades attribute

        :param value: the value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a saccades float type"
        assert 0 <= value <= 1, "please enter a saccades value between 0 and 1"
        self._saccades = value

    @saccades.deleter
    def saccades(self):
        """
        It deletes the attribute `_saccades` from the object `self`
        """
        del self._saccades

    @property
    def opacity(self):
        """
        It returns the opacity of the object.
        :return: The opacity of the object.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        """
        This function takes in a float value and checks if it is between 0 and 1. If it is, it sets the opacity to that
        value

        :param value: The value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a opacity float type"
        assert 0 <= value <= 1, "please enter an opacity value between 0 and 1"
        self._opacity = value

    @opacity.deleter
    def opacity(self):
        """
        It deletes the opacity attribute of the object.
        """
        del self._opacity

    @property
    def stopwords_behavior(self):
        """
        This function returns the stopwords behavior of the tokenizer
        :return: The stopwords_behavior is being returned.
        """
        return self._stopwords_behavior

    @stopwords_behavior.setter
    def stopwords_behavior(self, value: str):
        """
        The function takes in a string value and checks to see if it's a valid stopwords_behavior. If it is, it sets the
        stopwords_behavior to that value

        :param value: the value to be checked
        :type value: str
        """
        possible_values = [behavior.value.lower() for behavior in StopWordsBehavior]
        assert isinstance(value, str), "please use a stopwords_behavior str type"
        assert value in possible_values, f"please enter a stopwords_behavior within {possible_values}"
        self._stopwords_behavior = value

    @stopwords_behavior.deleter
    def stopwords_behavior(self):
        """
        It deletes the stopwords_behavior attribute from the object
        """
        del self._stopwords_behavior

    @property
    def stopwords(self):
        """
        The function stopwords() returns the stopwords of the object
        :return: The stopwords are being returned.
        """
        return self._stopwords

    @stopwords.setter
    def stopwords(self, value: float):
        """
        If the value is less than or equal to 1/4, then the stopwords set is very light. If the value is less than or equal
        to 1/2, then the stopwords set is light. If the value is less than or equal to 3/4, then the stopwords set is
        normal. Otherwise, the stopwords set is strong

        :param value: the value of the stopwords parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a stopwords float type"
        assert 0 <= value <= 1, "please enter a stopwords value between 0 and 1"
        self._stopwords = (
            stopwords.VERY_LIGHT_STOPWORDS_SET
            if value <= 1 / 4
            else stopwords.LIGHT_STOPWORDS_SET
            if value <= 1 / 2
            else stopwords.NORMAL_STOPWORDS_SET
            if value <= 3 / 4
            else stopwords.STRONG_STOPWORDS_SET
        )

    @stopwords.deleter
    def stopwords(self):
        """
        It deletes the stopwords attribute of the object
        """
        del self._stopwords

    def get_rare_words(self, text: str) -> List[str]:
        """
        Takes a string of text, and returns a list of words that appear more than a certain number of times in the text

        :param text: The text to be analyzed
        :type text: str
        :return: A list of uncommon words
        """
        vectorizer = CountVectorizer()
        transformed = vectorizer.fit_transform([text])
        data = pd.DataFrame(transformed.toarray(), columns=vectorizer.get_feature_names_out()).T
        data.columns = ["freq"]
        uncommon_words = data[data["freq"] > self.rare_words_max_freq].index.tolist()
        uncommon_words = [word for word in uncommon_words if not string_contains_digit(word)]

        return uncommon_words

    @staticmethod
    def split_text_to_words(text: str) -> List[str]:
        """
        It splits a string into a list of words

        :param text: The text to split into words
        :type text: str
        :return: A list of strings
        """
        tokens = re.split(SIMPLE_SPLITTER, text)

        return [token for token in tokens if len(token) > 0]

    def opacity_highlight(self, token: str, highlight_format: str = Format.BOLD.value) -> str:
        """
        If the output format is HTML, then return the HTML tag for the given format. Otherwise, return the ANSI escape code
        for the given format

        :param token: The token to be highlighted
        :type token: str
        :param highlight_format: This is the format that you want to highlight the token with
        :type highlight_format: str
        :return: A string with the token in the specified format.
        """
        if self.output_format == OutputFormat.HTML.value:
            if highlight_format == Format.HIGHLIGHT.value:
                return f"<mark>{token}</mark>"
            elif highlight_format == Format.UNDERLINE.value:
                return f"<u>{token}</u>"
            elif highlight_format == Format.STRIKETHROUGH.value:
                return f"<s>{token}</s>"
            else:
                return f"<b>{token}</b>"
        else:
            if highlight_format == Format.HIGHLIGHT.value:
                return f"{self.highlight}{token}{self.end}"
            elif highlight_format == Format.UNDERLINE.value:
                return f"{self.underline}{token}{self.end}"
            elif highlight_format == Format.STRIKETHROUGH.value:
                return strike_string(token)
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

    def saccades_highlight(self) -> int:
        """
        If the saccades are less than 1/3, return 3, else if the saccades are less than 2/3, return 2, else return 1
        :return: an integer value.
        """
        return 3 if self.saccades < 1 / 3 else 2 if self.saccades < 2 / 3 else 1

    def stopwords_highlight(self, token: str) -> str:
        """
        If the stopwords behavior is set to remove, return an empty string, otherwise return the token

        :param token: The token to highlight
        :type token: str
        """
        if self.stopwords_behavior == StopWordsBehavior.REMOVE.value:
            return ""
        elif self.stopwords_behavior == StopWordsBehavior.STRIKETHROUGH.value:
            return self.opacity_highlight(token, self.stopwords_behavior)
        else:
            return token

    def rare_words_highlight(self, token: str) -> str:
        """
        If the token is a rare word, then return the token with the opacity set to the value of the rare_words_behavior
        attribute

        :param token: the token to highlight
        :type token: str
        :return: The opacity_highlight function is being returned.
        """
        return self.opacity_highlight(token, self.rare_words_behavior)

    def highlight_tokens(self, tokens: List[str], uncommon_words: List[str]) -> List[str]:
        """
        The function takes a list of tokens and an output format, and returns a list of tokens with the tokens that are
        highlighted

        :param tokens: a list of tokens to highlight
        :type tokens: List[str]
        :param uncommon_words: List of all uncommon words
        :type uncommon_words: List[str]
        :return: A list of tokens with the tokens that are highlighted.
        """
        index = 0
        highlighted_tokens = []
        for token in tokens:
            if token not in self.non_tokens:
                index += 1
                if token.lower() in uncommon_words:
                    token = self.rare_words_highlight(token)
                elif token in self.stopwords and self.stopwords_behavior not in (
                    StopWordsBehavior.HIGHLIGHT.value,
                    StopWordsBehavior.BOLD.value,
                ):
                    token = self.stopwords_highlight(token)
                    index -= 1
                elif index % self.saccades_highlight() == 0 or index == 1:
                    (
                        token_to_highlight,
                        token_not_to_highlight,
                    ) = self.fixation_highlight(token)
                    if token in self.stopwords:
                        token_to_highlight = self.opacity_highlight(token_to_highlight, self.stopwords_behavior)
                    else:
                        token_to_highlight = self.opacity_highlight(token_to_highlight)
                    token = token_to_highlight + token_not_to_highlight
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

    def to_output_format(self, text: str) -> str:
        """
        If the output format is HTML, then add the HTML tags to the highlighted text

        :param text: The text to be highlighted
        :type text: str
        :return: The highlighted text.
        """
        output = text
        if self.output_format == OutputFormat.HTML.value:
            style = "b {font-weight: %d}" % (self.opacity * 1000)
            output = f"<!DOCTYPE html><html><head><style>{style}</style></head><body><p>{text}</p></body></html>"

        return output

    def read_faster(
        self,
        text: str,
    ) -> str:
        """
        The function takes a string of text, splits it into a list of words, highlights the words, and then returns the
        highlighted text

        :param text: the text you want to read faster
        :type text: str
        :return: The highlighted text
        """
        tokens = self.split_text_to_words(text)
        uncommon_words = self.get_rare_words(text)
        highlighted_tokens = self.highlight_tokens(tokens, uncommon_words)
        highlighted_text = self.tokens_to_text(highlighted_tokens)

        return self.to_output_format(highlighted_text)


if __name__ == "__main__":
    _ = BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html").read_faster(
        text="We are happy if as many people as possible can use the advantage of Bionic Reading."
    )
    print(_)
