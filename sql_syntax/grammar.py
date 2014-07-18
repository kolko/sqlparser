from . import lexis

tokens = lexis.tokens

precedence = (
#     ('right', '='),
#     ('right', 'QUANTIFIER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', '*', 'DIVIDE'),
)

def p_log(p):
    '''log : select_query END_QUERY
           | select_query END_QUERY log'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_empty(p):
    'empty : '
    pass

def p_select_query1(p):
    '''select_query : SELECT fields_part FROM from_part WHERE where_list'''
    p[0] = {
        'type': 'SELECT',
        'fields': p[2],
        'from': p[4],
        'where': p[6],
    }

def p_select_query2(p):
    '''select_query : SELECT fields_part FROM from_part'''
    p[0] = {
        'type': 'SELECT',
        'fields': p[2],
        'from': p[4],
    }

def p_select_query3(p):
    '''select_query : SELECT FIRST NUMBER fields_part FROM from_part WHERE where_list
                    | SELECT LAST NUMBER fields_part FROM from_part WHERE where_list'''
    p[0] = {
        'type': 'SELECT',
        'limit_type': p[2].lower(),
        'limit': p[3],
        'fields': p[4],
        'from': p[6],
        'where': p[8],
    }

def p_select_query4(p):
    '''select_query : SELECT FIRST NUMBER fields_part FROM from_part
                    | SELECT LAST NUMBER fields_part FROM from_part'''
    p[0] = {
        'type': 'SELECT',
        'limit_type': p[2].lower(),
        'limit': p[3],
        'fields': p[4],
        'from': p[6],
    }

def p_fields_part(p):
    '''fields_part : field_record
                   | field_record COMMA fields_part'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_field_record(p):
    '''field_record : where_and_field_item
                    | where_and_field_item AS NAME
                    | "*"
                    | NAME "." "*"
    '''
    res = {
        'type': 'FIELD',
    }
    if len(p) == 4 and p[2] == 'as':
        res = p[1]
        res['type'] = 'FIELD'
        assert 'as' not in res
        res['as'] = p[3]
        p[0] = res
        return
    if len(p) == 2 and 'type' in p[1] and p[1]['type'] == 'WHERE_AND_FIELD_ITEM':
        res = p[1]
        res['type'] = 'FIELD'
        p[0] = res
        return
    if len(p) == 2:
        res['value'] = p[1]
        p[0] = res
        return
    if len(p) == 4 and p[2] == ".":
        res['from_alias'] = p[1]
        res['value'] = p[3]
        p[0] = res
        return

def p_from_part(p):
    '''from_part : NAME
                 | NAME NAME
                 | NAME AS NAME'''
    res = {
        'type': 'FROM_PART',
    }
    if len(p) == 2:
        res['value'] = p[1]
        p[0] = res
        return
    if len(p) == 3:
        res['value'] = p[1]
        res['alias'] = p[2]
        p[0] = res
        return
    if len(p) == 4 and p[2].lower() == 'as':
        res['value'] = p[1]
        res['alias'] = p[3]
        p[0] = res
        return

#на порядок and/or правил - забиваем (временно?)
def p_where_list(p):
    '''where_list : where_object
                  | "(" where_list ")"
                  | where_object AND where_list
                  | where_object OR where_list
                  | "(" where_list ")" AND where_list
                  | "(" where_list ")" OR where_list
                  '''
    if len(p) == 2:
        p[0] = p[1]
        return
    if len(p) == 4 and p[1] == "(":
        #скобки без выражений - просто возвращаем содержимое
        p[0] = p[2]
        return
    res = {
    }
    if len(p) == 4 and (p[2].lower() == 'and' or p[2].lower() == 'or'):
        res = {
            'type': 'WHERE_EXPRESSION',
            'exp_type': p[2],
            'values': [p[1], p[3]]
        }
        if 'type' in p[3] and p[3]['type'] == 'WHERE_EXPRESSION':
            #пытаемся объеденить последовательность and .. and ... and
            if p[3]['exp_type'].lower() == p[2].lower():
                res = {
                    'type': 'WHERE_EXPRESSION',
                    'exp_type': p[2],
                    'values': [p[1]] + p[3]['values'],
                }
        p[0] = res
        return
    if len(p) == 6 and p[1] == '(' and (p[4] == 'and' or p[4] == 'or'):
        res = {
            'type': 'WHERE_EXPRESSION',
            'exp_type': p[4],
            'values': [p[2], p[5]]
        }
        p[0] = res
        return


def p_where_object(p):
    '''where_object : where_compare_item COMPARE_TYPE where_compare_item
                    | where_compare_item IS where_compare_item
                    | where_compare_item IN where_compare_item'''
    res = {
        'compare_list' : [p[1], p[3]],
        'compare_type': p[2],
    }
    p[0] = res

def p_where_compare_item(p):
    '''where_compare_item : where_and_field_item
    '''
    res = p[1]
    res['type'] = 'WHERE_COMPARE_ITEM'
    p[0] = res

def p_where_and_field_item(p):
    '''where_and_field_item : NUMBER
                            | NAME
                            | NAME "." NAME
                            | "(" select_query ")"
                            | STRING
                            | DQ_STRING'''
    res = {
        'type': 'WHERE_AND_FIELD_ITEM',
    }
    if len(p) == 2:
        res['value'] = p[1]
        p[0] = res
        return
    if len(p) == 4 and 'type' in p[2] and p[2]['type'] == 'SELECT':
        res['value'] = p[2]
        p[0] = res
        return
    if len(p) == 4 and p[2] == '.':
        res['value'] = p[3]
        res['from_alias'] = p[1]
        p[0] = res
        return

def p_where_and_field_item2_functions(p):
    '''where_and_field_item : NAME "(" where_and_field_item_list ")"
                            | NAME "(" "*" ")"
                            | NAME "(" ")"'''
    p[0] = {
        'type': 'function',
        'function': p[1],
    }
    if len(p) > 4:
        p[0]['args'] = p[3]

def p_arithmetic_expression(p): # трабла с порядком вычислений - забиваем
    '''
    where_and_field_item : where_and_field_item PLUS where_and_field_item
                         | where_and_field_item MINUS where_and_field_item
                         | where_and_field_item "*" where_and_field_item
                         | where_and_field_item DIVIDE where_and_field_item
    '''
    p[0] = {
        'type': 'arichmetic',
        'args': [p[1], p[3]],
        'sign': p[2],
    }


def p_where_and_field_item4(p):
    '''where_and_field_item : "(" where_and_field_item_list ")" '''
    if len(p[2]) == 1:
        p[0] = p[2][0]
    else:
        p[0] = {
            'type': 'item_list',
            'value': p[2],
        }

def p_where_and_field_item_list(p):
    '''where_and_field_item_list : where_and_field_item COMMA where_and_field_item_list
                                 | where_and_field_item'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]