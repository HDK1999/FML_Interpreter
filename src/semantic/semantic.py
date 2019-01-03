from enum import Enum, unique
from fml_parser import Terminals, NonTerminals
from math import sin, cos, tan, sqrt, exp, log, pi, e


class Semantic(object):
    def __init__(self, grammar_tree):
        self.grammar_tree = grammar_tree
        self.operation_queue = []
        self.analyse(self.grammar_tree)

    def get_operation_queue(self):
        return self.operation_queue.copy()

    def analyse(self, grammar_tree):
        if grammar_tree is None:
            self.operation_queue.append((Operation.EMPTY, ))
            return

        if grammar_tree[0] in (NonTerminals.PROGRAM, NonTerminals.STATEMENT):
            for i in grammar_tree[1]:
                self.analyse(i)
            return

        if grammar_tree[0] == NonTerminals.ORIGIN_STATEMENT:
            if len(grammar_tree[1]) != 7:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            expression_x = self.analyse(grammar_tree[1][3])
            expression_y = self.analyse(grammar_tree[1][5])
            if type(expression_x) not in (int, float) or type(expression_y) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return
            self.operation_queue.append((Operation.SET_ORIGIN, expression_x, expression_y))
            return

        elif grammar_tree[0] == NonTerminals.SCALE_STATEMENT:
            if len(grammar_tree[1]) != 7:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            expression_x = self.analyse(grammar_tree[1][3])
            expression_y = self.analyse(grammar_tree[1][5])
            if type(expression_x) not in (int, float) or type(expression_y) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return
            self.operation_queue.append((Operation.SET_SCALE, expression_x, expression_y))
            return

        elif grammar_tree[0] == NonTerminals.ROT_STATEMENT:
            if len(grammar_tree[1]) != 3:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            expression_rot = self.analyse(grammar_tree[1][2])
            if type(expression_rot) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return
            self.operation_queue.append((Operation.SET_ROT, expression_rot))
            return

        elif grammar_tree[0] == NonTerminals.FOR_STATEMENT:
            if len(grammar_tree[1]) != 14:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            start = Semantic.expression_calc(grammar_tree[1][3])
            end = Semantic.expression_calc(grammar_tree[1][5])
            step = Semantic.expression_calc(grammar_tree[1][7])
            if type(start) not in (int, float) or type(end) not in (int, float) or type(step) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return

            if step > 0 and end < start:
                pass
            elif step < 0 and end > start:
                pass
            elif step == 0 and end != start:
                pass
            elif step == 0:
                step = 10

            i = start
            while ((step > 0) and (i <= end)) or ((step < 0) and (i >= end)):
                x = Semantic.expression_calc(grammar_tree[1][10], i)
                y = Semantic.expression_calc(grammar_tree[1][12], i)
                if type(x) not in (int, float) or type(y) not in (int, float):
                    self.operation_queue.append((Operation.EMPTY,))
                    return
                self.operation_queue.append((Operation.DRAW, x, y))
                i += step

        elif grammar_tree[0] == NonTerminals.COLOR_STATEMENT:
            if len(grammar_tree[1]) != 9:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            r = self.analyse(grammar_tree[1][3])
            g = self.analyse(grammar_tree[1][5])
            b = self.analyse(grammar_tree[1][7])
            if type(r) not in (int, float) or type(g) not in (int, float) or type(b) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return
            self.operation_queue.append((Operation.SET_COLOR, r, g, b))
            return

        elif grammar_tree[0] == NonTerminals.BG_STATEMENT:
            if len(grammar_tree[1]) != 9:
                self.operation_queue.append((Operation.EMPTY, ))
                return
            r = self.analyse(grammar_tree[1][3])
            g = self.analyse(grammar_tree[1][5])
            b = self.analyse(grammar_tree[1][7])
            if type(r) not in (int, float) or type(g) not in (int, float) or type(b) not in (int, float):
                self.operation_queue.append((Operation.EMPTY, ))
                return
            self.operation_queue.append((Operation.SET_BG, r, g, b))
            return

        elif grammar_tree[0] == NonTerminals.EXPRESSION:
            return Semantic.expression_calc(grammar_tree)
        elif grammar_tree[0] == Terminals.SEMICOLON:
            return
        else:
            self.operation_queue.append((Operation.EMPTY,))
            return

    @staticmethod
    def expression_calc(grammar_tree, t=None):
        if grammar_tree[0] == NonTerminals.EXPRESSION:
            try:
                res = 0
                sign = 1
                for i in grammar_tree[1]:
                    if i[0] == Terminals.MINUS:
                        sign = -1
                    elif i[0] == Terminals.PLUS:
                        sign = 1
                    else:
                        res += Semantic.expression_calc(i, t) * sign
                return res
            except TypeError:
                return None

        elif grammar_tree[0] == NonTerminals.TERM:
            res = 1
            sign = True  # 乘
            for i in grammar_tree[1]:
                if i[0] == Terminals.MUL:
                    sign = True
                elif i[0] == Terminals.DIV:
                    sign = False
                else:
                    if sign:
                        res *= Semantic.expression_calc(i, t)
                    else:
                        res /= Semantic.expression_calc(i, t)
            return res
        elif grammar_tree[0] == NonTerminals.FACTOR:
            if len(grammar_tree[1]) == 1:
                return Semantic.expression_calc(grammar_tree[1][0], t)
            else:
                return Semantic.expression_calc(grammar_tree[1][1], t) *\
                       (1 if grammar_tree[1][0][0] == Terminals.PLUS else -1)
        elif grammar_tree[0] == NonTerminals.COMPONENT:
            if len(grammar_tree[1]) == 1:
                return Semantic.expression_calc(grammar_tree[1][0], t)
            else:
                return Semantic.expression_calc(grammar_tree[1][0], t) **\
                       Semantic.expression_calc(grammar_tree[1][2], t)
        elif grammar_tree[0] == NonTerminals.ATOM:
            if len(grammar_tree[1]) == 1:
                atom = grammar_tree[1][0]
                if atom[0] == Terminals.CONST_ID:
                    return pi if atom[1][1] == 'pi' else e
                elif atom[0] == Terminals.T:
                    return t
                elif atom[0] == Terminals.NUM:
                    num = atom[1][1]
                    return int(num) if num.find('.') == -1 else float(num)
            elif len(grammar_tree[1]) == 3:
                return Semantic.expression_calc(grammar_tree[1][1], t)
            elif len(grammar_tree[1]) == 4:
                func = grammar_tree[1][0]
                expression = grammar_tree[1][2]
                if func[1][1] == 'sin':
                    return sin(Semantic.expression_calc(expression, t))
                elif func[1][1] == 'cos':
                    return cos(Semantic.expression_calc(expression, t))
                elif func[1][1] == 'tan':
                    return tan(Semantic.expression_calc(expression, t))
                elif func[1][1] == 'sqrt':
                    return sqrt(Semantic.expression_calc(expression, t))
                elif func[1][1] == 'exp':
                    return exp(Semantic.expression_calc(expression, t))
                elif func[1][1] == 'ln':
                    return log(Semantic.expression_calc(expression, t), e)
            else:
                return None


@unique
class Operation(Enum):
    SET_ORIGIN = 1
    SET_SCALE = 2
    SET_ROT = 3
    SET_COLOR = 4
    SET_BG = 5
    DRAW = 6
    EMPTY = 7  # 空操作，表示无法识别的语义
