from lexer import Lexer
from parser import Parser, Terminals
from semantic import Semantic
from actuator import Actuator


# 词法分析
main_lexer = Lexer()

with open('../test_data/test1.fml', 'r', encoding='utf-8') as file:
    text = 'what'
    while len(text) > 0:
        text = file.read(1)
        main_lexer.append(text)
    main_lexer.append('\n', True)

print('记号流：')
for i in main_lexer.get_token(True):
    print(i)

if len(main_lexer.get_err_token()) != 0:
    print("错误流：")
    for i in main_lexer.get_err_token():
        print(i)
    exit()


# 语法分析
main_parser = Parser(main_lexer.get_token())
grammar_tree = main_parser.get_grammar_tree()
print('语法树：')
Parser.print_grammmar_tree(grammar_tree)
if grammar_tree is None:
    exit()


# 语义分析
main_semantic = Semantic(grammar_tree)
operation_queue = main_semantic.get_operation_queue()
print('中间代码：')
for i in operation_queue:
    print(i)


# 执行
main_actuator = Actuator()
main_actuator.append(operation_queue)
main_actuator.execute()
main_actuator.create_image()
