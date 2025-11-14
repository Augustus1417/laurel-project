from dataclasses import dataclass
from typing import Optional, Any

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_EQ = 'EQ'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_DOT = 'DOT'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_ARROW = 'ARROW'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'

KEYWORDS = [
  'and', 'or', 'not',
  'if', 'elif', 'else', 'then', 'end',
  'for', 'to', 'step', 'while', 'fun', 'return', 'continue', 'break',
  'repeat', 'times', 'is'
]

@dataclass
class Token:
    type: str
    value: Optional[Any] = None
    pos_start: Any = None
    pos_end: Any = None

    def matches(self, type_: str, value: Any) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
