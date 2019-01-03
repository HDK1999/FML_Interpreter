from enum import unique, Enum


class DFA:
    def __init__(self, source_data):

        if type(source_data) != dict:
            raise TypeError('第 1 个参数期望 {arg_type_expect} 类型，却接收到类型 {arg_type} '.format(
                arg_type_expect='dict', arg_type=str(type(source_data))
            ))

        if type(source_data.get('type')) != Token:
            raise TypeError('第 1 个参数的 "type" 字段期望 {arg_type_expect} 类型，却接收到类型 {arg_type} '.format(
                arg_type_expect='Token', arg_type=str(type(source_data.get('type')))
            ))
        self.token_type = source_data.get('type')

        if type(source_data.get('as_set')) != set:
            raise TypeError('第 1 个参数的 "as_set" 字段期望 {arg_type_expect} 类型，却接收到类型 {arg_type} '.format(
                arg_type_expect='set', arg_type=str(type(source_data.get('as_set')))
            ))
        self.as_set = source_data.get('as_set')

        if type(source_data.get('stm')) != dict:
            raise TypeError('第 1 个参数的 "stm" 字段期望 {arg_type_expect} 类型，却接收到类型 {arg_type} '.format(
                arg_type_expect='dict', arg_type=str(type(source_data.get('stm')))
            ))
        self.stm = source_data.get('stm')

        self.state = 0

    # 清除状态（回到初态）
    def clear(self):
        self.state = 0

    # 状态转移函数
    # 返回 bool 类型，转移成功返回 True，否则返回 False
    def move(self, ch):

        # 条件跳转
        if self.stm.get(ch) is not None:
            if self.stm.get(ch)[self.state] is not None:
                self.state = self.stm.get(ch)[self.state]
            else:
                return False

        # 特殊字符集跳转
        elif self.stm.get(SpecificCharSet.BLANK) is not None \
                and ch in SpecificCharSet.CHARSET_MAP.get(SpecificCharSet.BLANK):
            if self.stm.get(SpecificCharSet.BLANK)[self.state] is not None:
                self.state = self.stm.get(SpecificCharSet.BLANK)[self.state]
            else:
                return False
        elif self.stm.get(SpecificCharSet.NONZERO_DIGIT) is not None \
                and ch in SpecificCharSet.CHARSET_MAP.get(SpecificCharSet.NONZERO_DIGIT):
            if self.stm.get(SpecificCharSet.NONZERO_DIGIT)[self.state] is not None:
                self.state = self.stm.get(SpecificCharSet.NONZERO_DIGIT)[self.state]
            else:
                return False
        elif self.stm.get(SpecificCharSet.DIGIT) is not None \
                and ch in SpecificCharSet.CHARSET_MAP.get(SpecificCharSet.DIGIT):
            if self.stm.get(SpecificCharSet.DIGIT)[self.state] is not None:
                self.state = self.stm.get(SpecificCharSet.DIGIT)[self.state]
            else:
                return False

        # 任意跳转
        elif self.stm.get(SpecificCharSet.ANY) is not None:
            if self.stm.get(SpecificCharSet.ANY)[self.state] is not None:
                self.state = self.stm.get(SpecificCharSet.ANY)[self.state]
            else:
                return False

        # 非接受字符集
        else:
            return False

        return True

    # 判断是否处于接受状态
    def is_access(self):
        return self.state in self.as_set


@unique
class Token(Enum):
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
    COLOR = 10
    BACKGROUND = 11

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

    COMMENT = 61    # 注释
    NON_TOKEN = 62  # 空记号（源程序结束）
    ERR_TOKEN = 63  # 错误记号


class SpecificCharSet(object):
    NONZERO_DIGIT = 'NONZERO_DIGIT'
    DIGIT = 'DIGIT'
    BLANK = 'BLANK'
    ANY = 'ANY'

    CHARSET_MAP = {
        'NONZERO_DIGIT': {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
        'DIGIT': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
        'BLANK': {'\n', ' '}
    }


# 识别各种记号的 DFA
# type 是 DFA 识别的记号的类型
# as_set 是 DFA 的接受状态集，access state set
# stm 是 DFA 状态转移矩阵，state transition matrix，状态 0 为起始状态
DFA_DATA = (
    # 保留字
    {
        'type': Token.ORIGIN,
        'as_set': {7, },
        'stm': {
            'o':                   (1,    None, None, None, None, None, None, None),
            'r':                   (None, 2,    None, None, None, None, None, None),
            'i':                   (None, None, 3,    None, 5,    None, None, None),
            'g':                   (None, None, None, 4,    None, None, None, None),
            'n':                   (None, None, None, None, None, 6,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, None, None, 7,    None)
        }
    }, {
        'type': Token.SCALE,
        'as_set': {6, },
        'stm': {
            's':                   (1,    None, None, None, None, None, None),
            'c':                   (None, 2,    None, None, None, None, None),
            'a':                   (None, None, 3,    None, None, None, None),
            'l':                   (None, None, None, 4,    None, None, None),
            'e':                   (None, None, None, None, 5,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, None, 6,    None)
        }
    }, {
        'type': Token.ROT,
        'as_set': {4, },
        'stm': {
            'r':                   (1,    None, None, None, None),
            'o':                   (None, 2,    None, None, None),
            't':                   (None, None, 3,    None, None),
            SpecificCharSet.BLANK: (None, None, None, 4,    None)
        }
    }, {
        'type': Token.IS,
        'as_set': {3, },
        'stm': {
            'i':                   (1,    None, None, None),
            's':                   (None, 2,    None, None),
            SpecificCharSet.BLANK: (None, None, 3,    None)
        }
    }, {
        'type': Token.TO,
        'as_set': {3, },
        'stm': {
            't':                   (1,    None, None, None),
            'o':                   (None, 2,    None, None),
            SpecificCharSet.BLANK: (None, None, 3,    None)
        }
    }, {
        'type': Token.STEP,
        'as_set': {5, },
        'stm': {
            's':                   (1,    None, None, None, None, None),
            't':                   (None, 2,    None, None, None, None),
            'e':                   (None, None, 3,    None, None, None),
            'p':                   (None, None, None, 4,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, 5,    None),
        }
    }, {
        'type': Token.DRAW,
        'as_set': {5, },
        'stm': {
            'd':                   (1,    None, None, None, None, None),
            'r':                   (None, 2,    None, None, None, None),
            'a':                   (None, None, 3,    None, None, None),
            'w':                   (None, None, None, 4,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, 5,    None),
        }
    }, {
        'type': Token.FOR,
        'as_set': {4, },
        'stm': {
            'f':                   (1,    None, None, None, None),
            'o':                   (None, 2,    None, None, None),
            'r':                   (None, None, 3,    None, None),
            SpecificCharSet.BLANK: (None, None, None, 4,    None)
        }
    }, {
        'type': Token.FROM,
        'as_set': {5, },
        'stm': {
            'f':                   (1,    None, None, None, None, None),
            'r':                   (None, 2,    None, None, None, None),
            'o':                   (None, None, 3,    None, None, None),
            'm':                   (None, None, None, 4,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, 5,    None)
        }
    }, {
        'type': Token.COLOR,
        'as_set': {6, },
        'stm': {
            'c':                   (1,    None, None, None, None, None, None),
            'o':                   (None, 2,    None, 4,    None, None, None),
            'l':                   (None, None, 3,    None, None, None, None),
            'r':                   (None, None, None, None, 5,    None, None),
            SpecificCharSet.BLANK: (None, None, None, None, None, 6,    None)
        }
    }, {
        'type': Token.BACKGROUND,
        'as_set': {11, },
        'stm': {
            'b':                   (1,    None, None, None, None, None, None, None, None, None, None, None),
            'a':                   (None, 2,    None, None, None, None, None, None, None, None, None, None),
            'c':                   (None, None, 3,    None, None, None, None, None, None, None, None, None),
            'k':                   (None, None, None, 4,    None, None, None, None, None, None, None, None),
            'g':                   (None, None, None, None, 5,    None, None, None, None, None, None, None),
            'r':                   (None, None, None, None, None, 6,    None, None, None, None, None, None),
            'o':                   (None, None, None, None, None, None, 7,    None, None, None, None, None),
            'u':                   (None, None, None, None, None, None, None, 8,    None, None, None, None),
            'n':                   (None, None, None, None, None, None, None, None, 9,    None, None, None),
            'd':                   (None, None, None, None, None, None, None, None, None, 10,   None, None),
            SpecificCharSet.BLANK: (None, None, None, None, None, None, None, None, None, None, 11,   None)
        }
    },

    # 分隔符
    {
        'type': Token.SEMICOLON,
        'as_set': {1, },
        'stm': {
            ';': (1, None)
        }
    }, {
        'type': Token.L_BRACKET,
        'as_set': {1, },
        'stm': {
            '(': (1, None)
        }
    }, {
        'type': Token.R_BRACKET,
        'as_set': {1, },
        'stm': {
            ')': (1, None)
        }
    }, {
        'type': Token.COMMA,
        'as_set': {1, },
        'stm': {
            ',': (1, None)
        }
    },

    # 运算符
    {
        'type': Token.PLUS,
        'as_set': {1, },
        'stm': {
            '+': (1, None)
        }
    }, {
        'type': Token.MINUS,
        'as_set': {1, },
        'stm': {
            '-': (1, None)
        }
    }, {
        'type': Token.MUL,
        'as_set': {1, },
        'stm': {
            '*': (1, None)
        }
    }, {
        'type': Token.DIV,
        'as_set': {1, },
        'stm': {
            '/': (1, None)
        }
    }, {
        'type': Token.POWER,
        'as_set': {1, },
        'stm': {
            '^': (1, None)
        }
    },

    # 其他
    {
        'type': Token.FUNC,
        'as_set': {10, },
        'stm': {
            'a': (None, 6,    None, None, None, None, None, None, None, None, None),
            'c': (3,    None, None, None, None, None, None, None, None, None, None),
            'e': (4,    None, None, None, None, None, None, None, None, None, None),
            'i': (None, None, 6,    None, None, None, None, None, None, None, None),
            'l': (6,    None, None, None, None, None, None, None, None, None, None),
            'n': (None, None, None, None, None, None, 10,   None, None, None, None),
            'o': (None, None, None, 8,    None, None, None, None, None, None, None),
            'p': (None, None, None, None, None, None, None, None, None,   10, None),
            'q': (None, None, 5,    None, None, None, None, None, None, None, None),
            'r': (None, None, None, None, None, 7,    None, None, None, None, None),
            's': (2,    None, None, None, None, None, None, None, 10,   None, None),
            't': (1,    None, None, None, None, None, None, 10,   None, None, None),
            'x': (None, None, None, None, 9,    None, None, None, None, None, None)
        }
    }, {
        'type': Token.NUM,
        'as_set': {2, 3, 4},
        'stm': {
            SpecificCharSet.NONZERO_DIGIT: (3,    4,    None, 3,    4),
            '0':                           (2,    4,    None, 3,    4),
            '.':                           (1,    None, 4,    4,    None)
        }
    }, {
        'type': Token.CONST_ID,
        'as_set': {2, },
        'stm': {
            'e': (2,    None, None),
            'p': (1,    None, None),
            'i': (None, 2,    None),
        }
    }, {
        'type': Token.T,
        'as_set': {1, },
        'stm': {
            't': (1, None)
        }
    }, {
        'type': Token.COMMENT,
        'as_set': {3, },
        'stm': {
            SpecificCharSet.ANY: (None, None, 2,    None),
            '/':                 (1,    2,    2,    None),
            '\n':                (None, None, 3,    None),
        }
    }, {
        'type': Token.ERR_TOKEN,
        'as_set': {0, 1},
        'stm': {
            SpecificCharSet.ANY:   (1,    1),
            SpecificCharSet.BLANK: (None, None)
        }
    }
)
