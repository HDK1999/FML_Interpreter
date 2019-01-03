# Grammar
# =======
#
# Program -> { Statement SEMICOLON }
#
# Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement | ColorStatement | BgStatement
#
# OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
# ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
# RotStatement -> ROT IS Expression
# ColorStatement -> COLOR IS L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
# BgStatement -> BACKGROUND IS L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
# ForStatement -> FOR T
#                 FROM Expression
#                 TO Expression
#                 STEP Expression
#                 DRAW L_BRACKET Expression COMMA Expression R_BRACKET
#
# Expression -> Term { ( PLUS | MINUS ) Term }
# Term -> Factor { ( MUL | DIV ) Factor }
# Factor -> ( PLUS | MINUS ) Factor | Component
# Component -> Atom [ POWER Component ]
# Atom -> CONST_ID | T | NUM |
#         FUNC L_BRACKET Expression R_BRACKET |
#         L_BRACKET Expression R_BRACKET

from enum import Enum, unique
from lexer import Token


@unique
class NonTerminals(Enum):
    PROGRAM = 0

    STATEMENT = 1
    ORIGIN_STATEMENT = 11
    SCALE_STATEMENT = 12
    ROT_STATEMENT = 13
    FOR_STATEMENT = 14
    COLOR_STATEMENT = 15
    BG_STATEMENT = 16

    EXPRESSION = 2
    TERM = 21
    FACTOR = 22
    COMPONENT = 23
    ATOM = 24


@unique
class Terminals(Enum):
    ORIGIN = Token.ORIGIN
    SCALE = Token.SCALE
    ROT = Token.ROT
    COLOR = Token.COLOR
    BACKGROUND = Token.BACKGROUND

    IS = Token.IS
    FOR = Token.FOR
    FROM = Token.FROM
    TO = Token.TO
    STEP = Token.STEP
    DRAW = Token.DRAW

    SEMICOLON = Token.SEMICOLON
    COMMA = Token.COMMA
    L_BRACKET = Token.L_BRACKET
    R_BRACKET = Token.R_BRACKET

    PLUS = Token.PLUS
    MINUS = Token.MINUS
    MUL = Token.MUL
    DIV = Token.DIV
    POWER = Token.POWER

    CONST_ID = Token.CONST_ID
    T = Token.T
    NUM = Token.NUM
    FUNC = Token.FUNC

    NONE = 0
