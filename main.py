from sql_syntax.parser import Parser
import json

parser = Parser()#, debug=True)

with open('test.sql', 'r') as f:
    data = f.read()

res = parser.parse(data)#, debug=True)
if res:
    for query in res:
        print(json.dumps(query))

# from sql_syntax import lexis
#
# from ply.lex import lex
# lexer = lex(module=lexis, debug=1)
# lexer.input(data)
# for tok in lexer:
#     print(tok)