from lexer import Lexer
from parser import Parser, Terminals


def print_grammmar_tree(tree, level=0):
    if tree is None:
        print('  ' * level + str(tree))
        return
    if type(tree[0]) == Terminals:
        print('  ' * level + str(tree[0]) + ' -- ' + str(tree[1]))
    else:
        print('  ' * level + str(tree[0]))
        for j in tree[1]:
            print_grammmar_tree(j, level + 1)


main_lexer = Lexer()
main_parser = Parser()

with open('../test_data/test1.fml', 'r', encoding='utf-8') as file:
    text = 'what'
    while len(text) > 0:
        text = file.read(1)
        main_lexer.append(text)
    main_lexer.append('\n', True)

for i in main_lexer.get_token(True):
    print(i)
print(''.join(main_lexer.get_source_code()))
for i in main_lexer.get_err_token():
    print(i)

# grammar_tree = Parser.program(main_lexer.get_token(False))
# print_grammmar_tree(grammar_tree)
