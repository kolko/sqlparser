from sql_syntax.parser import Parser
import json
import time

parser = Parser()#, debug=True)

with open('test.sql', 'r') as f:
    data = f.read()

res = parser.parse(data)#, debug=True)
if res:
    for query in res:
        print(json.dumps(query))
# exit(0)
with open('cb5_test_select.sql', 'r') as f:
    data = f.readlines()

start_time = time.time()
ok = false = 0
for line in data:
    if ';;' in line:
        line = line[:-2]
    res = parser.parse(line)
    if res:
        ok += 1
    else:
        print(line)
        false += 1
end_time = time.time()
print('OK: %s FAILED: %s TIME: %s' % (ok, false, end_time-start_time))
#MacBook-Pro:sqlparser kolko$ cat cb5_test_select.sql | wc -l
#  153151
#OK: 82786 FAILED: 70365 TIME: 296.2884738445282
#OK: 115009 FAILED: 38141 TIME: 394.52152013778687
#OK: 115009 FAILED: 38141 TIME: 361.0259680747986
#OK: 120747 FAILED: 32403 TIME: 3449.98547911644
#OK: 129252 FAILED: 23898 TIME: 406.76648592948914
#egrep ' - [ ]*SELECT' cb5_test.sql
#cat cb5_test_tmp | while read t t t t t sql; do [ '${sql%%*;}' == '' ] && echo $sql || echo "$sql;"; done > cb5_test_select.sql

# from sql_syntax import lexis
#
# from ply.lex import lex
# lexer = lex(module=lexis, debug=1)
# lexer.input(data)
# for tok in lexer:
#     print(tok)