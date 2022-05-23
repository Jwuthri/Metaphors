from enum import Enum


SIMPLE_SPLITTER = "([\t \n-.!?;:(){}'])"


class OutputFormat(Enum):
    HTML = "html"
    PYTHON = "python"
    TEXT = "text"


class StopWordsBehavior(Enum):
    KEEP = "keep"
    REMOVE = "remove"
    IGNORE = "ignore"
