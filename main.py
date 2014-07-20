from sql_syntax.parser import Parser
import json
import time
from copy import deepcopy

parser = Parser()#, debug=True)

with open('test.sql', 'r') as f:
    data = f.read()

res = parser.parse(data)#, debug=True)
if res:
    for query in res:
        print(json.dumps(query))
# exit(0)
def cb5_brenchmark():
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
# cb5_brenchmark()


# from sql_syntax import lexis
#
# from ply.lex import lex
# lexer = lex(module=lexis, debug=1)
# lexer.input(data)
# for tok in lexer:
#     print(tok)

def recursive_del_variables(d):
    if d['type'] == 'string' or d['type'] == 'number':
        d['value'] = '<VARIABLE>'
        return
    for _, item in d.items():
        if isinstance(item, dict):
            recursive_del_variables(item)
        elif isinstance(item, list):
            for _item in item:
                if isinstance(_item, dict):
                    recursive_del_variables(_item)


def sql_equal(sql1, sql2):
    '''Return true if two sql are equals, without variable strings and numbers'''
    sql1 = deepcopy(sql1[0])
    sql2 = deepcopy(sql2[0])
    recursive_del_variables(sql1)
    recursive_del_variables(sql2)
    return sql1 == sql2

def sql_wc(filename):
    counts = []
    with open(filename, 'r') as f:
        for sql_str in f.readlines():
            if ';;' in sql_str:
                sql_str = sql_str[:-2]
            sql_ast = parser.parse(sql_str)
            if not sql_ast:
                #cant parse
                continue
            done = False
            for count_item in counts:
                _sql = count_item['ast'][0]
                if sql_equal(_sql, sql_ast):
                    done = True
                    count_item['count'] += 1
                    if not sql_ast in count_item['ast']:
                        count_item['ast'].append(sql_ast)
                    break
            if not done:
                counts.append({
                    'ast': [sql_ast],
                    'count': 1,
                    'sql_string': sql_str,
                })
            if len(counts) > 100:
                break
    for count_item in sorted(counts, key=lambda x: x['count'], reverse=True):
        print(count_item['count'], ' [', len(count_item['ast']), ']: ', count_item['sql_string'])

# sql_wc('sql_wc_test.sql')

start_time = time.time()
sql_wc('cb5_test_select.sql')
end_time = time.time()
print('TIME: %s' % (end_time-start_time))
#TIME: 9561.41975903511  !!!!!