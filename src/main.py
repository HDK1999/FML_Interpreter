from lexer import Lexer
from fml_parser import Parser
from semantic import Semantic
from actuator import Actuator
import sys

for argc in sys.argv[1:]:
    if argc in ('-h', '-H', '--help'):
        print('FML v0.0.1')
        print('Usage: ./fml [option] [input_file] [output_file] ...')
        print('Options:')
        print('-h, -H, --help     Print this message and exit.')
        print('-v, -V, --version  Print the version number of fml and exit.')
        print()
        print('Report bugs to <keyboard-l@outlook.com>')
        sys.exit()
    elif argc in ('-v', '-V', '--version'):
        print('FML v0.0.1')
        sys.exit()


input_file = ''
output_file = ''
if len(sys.argv) <= 1:
    input_file = input('Input File: ')
    output_file = input('Output File (Press ENTER to skip, and `whatever.png` as default): ')
    if len(output_file) == 0:
        output_file = 'whatever.png'
elif len(sys.argv) >= 2:
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        if input_file[-4:].lower() == '.fml':
            output_file = input_file[:-4] + '.png'
        else:
            output_file = input_file + '.png'

if output_file[-4:].lower() != '.png':
        output_file += '.png'


# 词法分析
main_lexer = Lexer()

with open(input_file, 'r', encoding='utf-8') as file:
    text = 'what'
    while len(text) > 0:
        text = file.read(32)
        main_lexer.append(text)
    main_lexer.append('\n', True)

print('记号流：')
for i in main_lexer.get_token(True):
    print(i)

if len(main_lexer.get_err_token()) != 0:
    print("错误流：")
    for i in main_lexer.get_err_token():
        print(i)
    sys.exit()


# 语法分析
main_parser = Parser(main_lexer.get_token())
grammar_tree = main_parser.get_grammar_tree()
print('语法树：')
Parser.print_grammmar_tree(grammar_tree)
if grammar_tree is None:
    sys.exit()


# 语义分析
main_semantic = Semantic(grammar_tree)
operation_queue = main_semantic.get_operation_queue()
print('中间代码：')
for i in operation_queue:
    print(i)


# 执行
main_actuator = Actuator(output_file)
main_actuator.append(operation_queue)
main_actuator.execute()
main_actuator.create_image()
