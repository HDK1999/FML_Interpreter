# 文法定义

初始

```text
Program -> ε | Program Statement SEMICOLON

Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement

OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
RotStatement -> ROT IS Expression
ForStatement -> FOR T FROM Expression TO Expression STEP Expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET

Expression -> Expression PLUS Expression |
              Expression MINUS Expression |
              Expression MUL Expression |
              Expression DIV Expression |
              PLUS Expression |
              MINUS Expression |
              Expression POWER Expression |
              CONST_ID |
              NUM |
              T |
              FUNC L_BRACKET Expression R_BRACKET |
              L_BRACKET Expression R_BRACKET |

```

消除左递归 消除二义性 提取左因子

```text
Program -> Statement SEMICOLON Program | ε

Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement

OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
RotStatement -> ROT IS Expression
ForStatement -> FOR T FROM Expression TO Expression STEP Expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET

Expression -> Term Expression'
Expression' -> PLUS Term Expression' |
               MINUS Term Expression' |
               ε
Term -> Factor Term'
Term' -> MUL Factor Term' | DIV Factor Term' | ε
Factor -> PLUS Factor | MINUS Factor | Component
Component -> Atom POWER Component | Atom
Atom -> CONST_ID | T | NUM |
        FUNC L_BRACKET Expression R_BRACKET |
        L_BRACKET Expression R_BRACKET

```

将文法改写成 EBNF

```text
Program -> { Statement SEMICOLON }

Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement

OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
RotStatement -> ROT IS Expression
ForStatement -> FOR T FROM Expression TO Expression STEP Expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET

Expression -> Term { ( PLUS | MINUS ) Term }
Term -> Factor { ( MUL | DIV ) Factor }
Factor -> ( PLUS | MINUS ) Factor | Component
Component -> Atom [ POWER Component ]
Atom -> CONST_ID | T | NUM |
        FUNC L_BRACKET Expression R_BRACKET |
        L_BRACKET Expression R_BRACKET

```
