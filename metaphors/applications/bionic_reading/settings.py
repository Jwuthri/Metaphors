from enum import Enum


SIMPLE_SPLITTER = "([\t\] \n-.!?;:(){}'/[])"


class OutputFormat(Enum):
    PYTHON = "python"
    TEXT = "text"
    HTML = "html"


class StopWordsBehavior(Enum):
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"
    REMOVE = "remove"
    IGNORE = "ignore"
    BOLD = "bold"


class RareBehavior(Enum):
    HIGHLIGHT = "highlight"
    UNDERLINE = "underline"
    BOLD = "bold"


class Format(Enum):
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"
    UNDERLINE = "underline"
    BOLD = "bold"
