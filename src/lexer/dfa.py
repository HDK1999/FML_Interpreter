from enum import unique, Enum


@unique
class Token(Enum):
    # 注释
    COMMENT = 0

    # 保留字
    ORIGIN = 1
    SCALE = 2
    ROT = 3
    IS = 4
    TO = 5
    STEP = 6
    DRAW = 7
    FOR = 8
    FROM = 9

    # 分隔符
    SEMICOLON = 21  # 分号
    L_BRACKET = 22  # 左括号
    R_BRACKET = 23  # 右括号
    COMMA = 24      # 逗号

    # 运算符
    PLUS = 35   # 加号
    MINUS = 36  # 减号
    MUL = 37    # 乘号
    DIV = 38    # 除号
    POWER = 39  # 乘方号

    # 其他
    FUNC = 51      # 函数
    NUM = 52       # 数值字面量
    CONST_ID = 53  # 常量
    T = 54         # 参数

    NON_TOKEN = 61  # 空记号（源程序结束）
    ERR_TOKEN = 62  # 错误记号


# 识别各种记号的 DFA
# type 是 DFA 识别的记号的类型
# stm 是 DFA 状态转移矩阵，state transition matrix
DFA = (
    {
        'type': Token.COMMA,
        'stm':
    }
)