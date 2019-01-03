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


from .grammar import NonTerminals, Terminals


# 语法分析器
class Parser(object):

    def __init__(self, token_stream):
        self.token_stream = token_stream
        self.grammar_tree = Parser.program(token_stream)

    def get_grammar_tree(self):
        return self.grammar_tree

    @staticmethod
    def print_grammmar_tree(tree, level=0):
        if tree is None:
            print('  ' * level + str(tree))
            return
        if type(tree[0]) == Terminals:
            print('  ' * level + str(tree[0]) + ' -- ' + str(tree[1]))
        else:
            print('  ' * level + str(tree[0]))
            for i in tree[1]:
                Parser.print_grammmar_tree(i, level + 1)

    @staticmethod
    def map_non_terminals_to_func(non_terminals):
        if non_terminals == NonTerminals.PROGRAM:
            return Parser.program
        elif non_terminals == NonTerminals.STATEMENT:
            return Parser.statement
        elif non_terminals == NonTerminals.ORIGIN_STATEMENT:
            return Parser.origin_statement
        elif non_terminals == NonTerminals.SCALE_STATEMENT:
            return Parser.scale_statement
        elif non_terminals == NonTerminals.ROT_STATEMENT:
            return Parser.rot_statement
        elif non_terminals == NonTerminals.FOR_STATEMENT:
            return Parser.for_statement
        elif non_terminals == NonTerminals.EXPRESSION:
            return Parser.expression
        elif non_terminals == NonTerminals.TERM:
            return Parser.term
        elif non_terminals == NonTerminals.FACTOR:
            return Parser.factor
        elif non_terminals == NonTerminals.COMPONENT:
            return Parser.component
        elif non_terminals == NonTerminals.ATOM:
            return Parser.atom
        else:
            return None

    # Program -> { Statement SEMICOLON }
    @staticmethod
    def program(token_stream):
        sub_tree = []
        token_buffer = []
        for token in token_stream:
            if token[0] == Terminals.SEMICOLON.value:
                tree = Parser.statement(token_buffer)
                if tree is None:
                    return None
                sub_tree.append(tree)
                sub_tree.append((Terminals.SEMICOLON, token))
                token_buffer = []
            else:
                token_buffer.append(token)
        return NonTerminals.PROGRAM, tuple(sub_tree)

    # Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement | ColorStatement | BgStatement
    @staticmethod
    def statement(token_stream):
        cases = (
            Parser.origin_statement,
            Parser.scale_statement,
            Parser.rot_statement,
            Parser.for_statement,
            Parser.color_statement,
            Parser.bg_statement
        )
        for case in cases:
            tree = case(token_stream)
            if tree is not None:
                return NonTerminals.STATEMENT, (tree,)
        else:
            return None

    # OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
    @staticmethod
    def origin_statement(token_stream):
        expect_sentence = (
            Terminals.ORIGIN, Terminals.IS, Terminals.L_BRACKET, NonTerminals.EXPRESSION,
            Terminals.COMMA, NonTerminals.EXPRESSION, Terminals.R_BRACKET
        )

        return Parser.seq_statement_template(NonTerminals.ORIGIN_STATEMENT, expect_sentence, token_stream)

    # ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
    @staticmethod
    def scale_statement(token_stream):
        expect_sentence = (
            Terminals.SCALE, Terminals.IS, Terminals.L_BRACKET, NonTerminals.EXPRESSION,
            Terminals.COMMA, NonTerminals.EXPRESSION, Terminals.R_BRACKET
        )

        return Parser.seq_statement_template(NonTerminals.SCALE_STATEMENT, expect_sentence, token_stream)

    # RotStatement -> ROT IS Expression
    @staticmethod
    def rot_statement(token_stream):
        expect_sentence = (
            Terminals.ROT, Terminals.IS, NonTerminals.EXPRESSION
        )

        return Parser.seq_statement_template(NonTerminals.ROT_STATEMENT, expect_sentence, token_stream)

    # ColorStatement -> COLOR IS L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
    @staticmethod
    def color_statement(token_stream):
        expect_sentence = (
            Terminals.COLOR, Terminals.IS, Terminals.L_BRACKET,
            NonTerminals.EXPRESSION, Terminals.COMMA,
            NonTerminals.EXPRESSION, Terminals.COMMA,
            NonTerminals.EXPRESSION, Terminals.R_BRACKET
        )

        return Parser.seq_statement_template(NonTerminals.COLOR_STATEMENT, expect_sentence, token_stream)

    # BgStatement -> BACKGROUND IS L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
    @staticmethod
    def bg_statement(token_stream):
        expect_sentence = (
            Terminals.BACKGROUND, Terminals.IS, Terminals.L_BRACKET,
            NonTerminals.EXPRESSION, Terminals.COMMA,
            NonTerminals.EXPRESSION, Terminals.COMMA,
            NonTerminals.EXPRESSION, Terminals.R_BRACKET
        )

        return Parser.seq_statement_template(NonTerminals.BG_STATEMENT, expect_sentence, token_stream)

    # ForStatement -> FOR T
    #                 FROM Expression
    #                 TO Expression
    #                 STEP Expression
    #                 DRAW L_BRACKET Expression COMMA Expression R_BRACKET
    @staticmethod
    def for_statement(token_stream):
        expect_sentence = (
            Terminals.FOR, Terminals.T, Terminals.FROM, NonTerminals.EXPRESSION, Terminals.TO, NonTerminals.EXPRESSION,
            Terminals.STEP, NonTerminals.EXPRESSION, Terminals.DRAW, Terminals.L_BRACKET, NonTerminals.EXPRESSION,
            Terminals.COMMA, NonTerminals.EXPRESSION, Terminals.R_BRACKET
        )

        return Parser.seq_statement_template(NonTerminals.FOR_STATEMENT, expect_sentence, token_stream)

    # Expression -> Term { ( PLUS | MINUS ) Term }
    @staticmethod
    def expression(token_stream):
        token_buffer = []
        sub_tree = []
        for token in token_stream:
            if token[0] in (Terminals.PLUS.value, Terminals.MINUS.value):
                tree = Parser.term(token_buffer)
                if tree is not None:
                    sub_tree.append(tree)
                    sub_tree.append((Terminals.PLUS if token[0] == Terminals.PLUS.value else Terminals.MINUS, token))
                    token_buffer = []
                else:
                    token_buffer.append(token)
            else:
                token_buffer.append(token)

        tree = Parser.term(token_buffer)
        if tree is not None:
            sub_tree.append(tree)
            return NonTerminals.EXPRESSION, tuple(sub_tree)

        return None

    # Term -> Factor { ( MUL | DIV ) Factor }
    @staticmethod
    def term(token_stream):
        token_buffer = []
        sub_tree = []
        for token in token_stream:
            if token[0] in (Terminals.MUL.value, Terminals.DIV.value):
                tree = Parser.factor(token_buffer)
                if tree is not None:
                    sub_tree.append(tree)
                    sub_tree.append((Terminals.MUL if token[0] == Terminals.MUL.value else Terminals.DIV, token))
                    token_buffer = []
                else:
                    token_buffer.append(token)
            else:
                token_buffer.append(token)

        tree = Parser.factor(token_buffer)
        if tree is not None:
            sub_tree.append(tree)
            return NonTerminals.TERM, tuple(sub_tree)

        return None

    # Factor -> ( PLUS | MINUS ) Factor | Component
    @staticmethod
    def factor(token_stream):
        if len(token_stream) > 1:
            if token_stream[0][0] in (Terminals.PLUS.value, Terminals.MINUS.value):
                tree = Parser.factor(token_stream[1:])
                if tree is not None:
                    return NonTerminals.FACTOR, ((
                                                     Terminals.PLUS
                                                     if token_stream[0][0] == Terminals.PLUS.value
                                                     else Terminals.MINUS, token_stream[0]
                                                 ), tree)

        tree = Parser.component(token_stream)
        if tree is not None:
            return NonTerminals.FACTOR, (tree, )

        return None

    # Component -> Atom [ POWER Component ]
    @staticmethod
    def component(token_stream):
        tree = Parser.atom(token_stream)
        if tree is not None:
            return NonTerminals.COMPONENT, (tree, )

        expect_sentence = (NonTerminals.ATOM, Terminals.POWER, NonTerminals.COMPONENT)
        tree = Parser.seq_statement_template(NonTerminals.COMPONENT, expect_sentence, token_stream)
        if tree is not None:
            return tree

        return None

    # Atom -> CONST_ID | T | NUM |
    #         FUNC L_BRACKET Expression R_BRACKET |
    #         L_BRACKET Expression R_BRACKET
    @staticmethod
    def atom(token_stream):
        if len(token_stream) == 1:
            if token_stream[0][0] == Terminals.CONST_ID.value:
                return NonTerminals.ATOM, ((Terminals.CONST_ID, token_stream[0]), )
            elif token_stream[0][0] == Terminals.T.value:
                return NonTerminals.ATOM, ((Terminals.T, token_stream[0]), )
            elif token_stream[0][0] == Terminals.NUM.value:
                return NonTerminals.ATOM, ((Terminals.NUM, token_stream[0]), )
            else:
                return None

        expect_sentence = (Terminals.L_BRACKET, NonTerminals.EXPRESSION, Terminals.R_BRACKET)
        tree = Parser.seq_statement_template(NonTerminals.ATOM, expect_sentence, token_stream)
        if tree is not None:
            return tree

        expect_sentence = (Terminals.FUNC, Terminals.L_BRACKET, NonTerminals.EXPRESSION, Terminals.R_BRACKET)
        tree = Parser.seq_statement_template(NonTerminals.ATOM, expect_sentence, token_stream)
        if tree is not None:
            return tree

        return None

    @staticmethod
    def seq_statement_template(node_type, expect_sentence, token_stream):
        sub_tree = []
        token_stream = token_stream.copy()

        non_terminals_buffer = (None, [])
        symbol = 0
        while symbol < len(expect_sentence) and len(expect_sentence) > 0:

            if type(expect_sentence[symbol]) == Terminals:  # 接下来期望一个终结符
                if len(token_stream) > 0 and token_stream[0][0] == expect_sentence[symbol].value:  # 可接受该终结符
                    if non_terminals_buffer[0] is None:  # 前面没有挂起的非终结符，直接接受
                        sub_tree.append((expect_sentence[symbol], token_stream[0]))
                        token_stream.pop(0)
                        symbol += 1
                        continue
                    else:  # 前面挂起一个非终结符，先尝试匹配该非终结符
                        tree = Parser.map_non_terminals_to_func(non_terminals_buffer[0])(non_terminals_buffer[1])
                        if tree is not None:  # 挂起的非终结符接受
                            sub_tree.append(tree)
                            sub_tree.append((expect_sentence[symbol], token_stream[0]))
                            token_stream.pop(0)
                            non_terminals_buffer = (None, [])
                            symbol += 1
                            continue
                        else:  # 挂起的非终结符不接受
                            non_terminals_buffer[1].append(token_stream.pop(0))
                            continue
                elif len(token_stream) > 0:  # 不可接受该终结符，但是记号流不为空
                    if non_terminals_buffer[0] is None:
                        return None
                    else:
                        non_terminals_buffer[1].append(token_stream.pop(0))
                        continue
                else:  # 记号流为空
                    return None
            else:  # 接下来期望一个非终结符
                if non_terminals_buffer[0] is None:  # 挂起该非终结符
                    non_terminals_buffer = (expect_sentence[symbol], [])
                    symbol += 1
                    continue
                else:  # 前面已有一个非终结符被挂起
                    tree = Parser.map_non_terminals_to_func(non_terminals_buffer[0])(non_terminals_buffer[1])
                    if tree is not None:  # 挂起的非终结符接受
                        sub_tree.append(tree)
                        token_stream.pop(0)
                        non_terminals_buffer = (expect_sentence[symbol], [])
                        symbol += 1
                        continue
                    else:  # 挂起的非终结符不接受
                        non_terminals_buffer[1].append(token_stream.pop(0))
                        continue
        else:
            if non_terminals_buffer[0] is not None:
                tree = Parser.map_non_terminals_to_func(non_terminals_buffer[0])(token_stream)
                if tree is not None:  # 挂起的非终结符接受
                    sub_tree.append(tree)
                else:  # 挂起的非终结符不接受
                    return None

        return node_type, tuple(sub_tree)

