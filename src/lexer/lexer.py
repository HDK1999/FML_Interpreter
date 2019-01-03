from .dfa import DFA, DFA_DATA, Token, SpecificCharSet


# 词法分析器
class Lexer(object):
    def __init__(self):
        # 初始化 DFA 集合
        self.dfa_set = set()
        for i in DFA_DATA:
            self.dfa_set.add(DFA(i))

        # 输入队列 源码字符串队列
        self.input_queue = []
        # 处理过的源码字符串
        self.source_code = []
        # 处理结果 记号流
        self.token_stream = []

        # 错误记号记录
        self.err_token = []

        # 输出队列 记号队列
        self.output_queue = []

    # 往输入队列追加输入
    def append(self, input_queue, eof_flag=False):
        if type(input_queue) == str:
            self.input_queue.append(input_queue)
        elif type(input_queue) in (list, tuple):
            self.input_queue.extend(input_queue)

        # 追加输入后进行词法分析
        self.analyse(eof_flag)

    # 进行词法分析
    # eof_flag 是文件结束标记，若文件结束，则为 True，否则为 False 或者省略
    def analyse(self, eof_flag=False):

        input_char_buffer = []
        token_char_buffer = []
        alive_dfa = self.dfa_set.copy()
        access_token = None

        # 清空 DFA 状态
        for dfa in self.dfa_set:
            dfa.clear()

        while self.input_queue:
            # 预处理 全部转为小写
            input_char_buffer.extend([ch for ch in self.input_queue.pop(0).lower()])

            while input_char_buffer:
                token_char_buffer.append(input_char_buffer.pop(0))

                for dfa in alive_dfa.copy():
                    if dfa.move(token_char_buffer[len(token_char_buffer) - 1]):
                        if dfa.is_access():  # 可接受
                            if dfa.token_type != Token.ERR_TOKEN:
                                access_token = (dfa.token_type, ''.join(token_char_buffer))
                            elif access_token is None or access_token[0] == Token.ERR_TOKEN:
                                access_token = (dfa.token_type, ''.join(token_char_buffer))
                            else:
                                alive_dfa.remove(dfa)
                    else:
                        alive_dfa.remove(dfa)

                if len(alive_dfa) == 0:  # 大家都尽力了
                    if access_token is not None:
                        # 记录识别成功的记号
                        if access_token[0] not in (Token.ERR_TOKEN, Token.COMMENT):
                            self.output_queue.append(access_token)
                        self.token_stream.append(access_token)
                        if access_token[0] == Token.ERR_TOKEN:
                            row_num = 1
                            col_num = 0
                            for i in ''.join(self.source_code):
                                col_num += 1
                                if i == '\n':
                                    row_num += 1
                                    col_num = 0
                            self.err_token.append((access_token, (row_num, col_num + 1)))

                        # 退回一个字符到输入缓冲区
                        input_char_buffer.insert(0, token_char_buffer.pop())

                        # 记录识别的源代码
                        self.source_code.append(''.join(token_char_buffer))
                    elif len(token_char_buffer) == 1 and \
                            token_char_buffer[0] in SpecificCharSet.CHARSET_MAP.get(SpecificCharSet.BLANK):
                        self.source_code.append(token_char_buffer[0])
                    else:  # 出错
                        print('lexer error')

                    # 复位
                    token_char_buffer = []
                    access_token = None
                    for dfa in self.dfa_set:
                        dfa.clear()
                    alive_dfa = self.dfa_set.copy()

        if eof_flag:
            if len(input_char_buffer) > 0:
                self.token_stream.append((Token.ERR_TOKEN, ''.join(input_char_buffer)))
            self.output_queue.append((Token.NON_TOKEN, ''))
            self.token_stream.append((Token.NON_TOKEN, ''))
        elif len(token_char_buffer) > 0:
            # print(''.join(token_char_buffer))
            self.input_queue.append(''.join(token_char_buffer))

    # 取出下一个（或若干个）已分析的记号
    def next_token(self, num=1, debug=False):
        if num == 0:
            num = len(self.output_queue)
        if num < 1:
            num = 1
        res = self.output_queue[:num]
        self.output_queue = self.output_queue[num:]
        return res

    # 获取所有已分析记号
    def get_token(self, debug=False):
        if debug:
            return self.token_stream.copy()

        output_queue_copy = []
        for token in self.token_stream:
            if token[0] not in (Token.COMMENT, Token.ERR_TOKEN):
                output_queue_copy.append(token)

        return output_queue_copy

    def get_source_code(self):
        return self.source_code.copy()

    def get_err_token(self):
        return self.err_token.copy()

    # 重置为初始状态
    def clear(self):
        for dfa in self.dfa_set:
            dfa.clear()
        self.source_code = ''
