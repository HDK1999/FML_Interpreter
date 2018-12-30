from lexer import Lexer

main_lexer = Lexer()

with open('../test_data/test1.fml', 'r', encoding='utf-8') as file:
    text = 'what'
    while len(text) > 0:
        text = file.read(32)
        main_lexer.append(text)
    main_lexer.append('\n', True)

for i in main_lexer.get_token():
    print(i)
