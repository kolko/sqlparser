from . import lexis
from .ast_types import *

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

def p_select_query(p):
    '''select_query : SELECT distinct fields_part from where'''
    select = Select()
    select.set_distinct(p[2])
    select.set_fields_part(p[3])
    select.set_from_part(p[4])
    select.set_where_part(p[5])
    p[0] = select

def p_select_query2(p): #TODO: distinct
    '''select_query : SELECT FIRST NUMBER fields_part from where
                    | SELECT LAST NUMBER fields_part from where'''
    select = Select()
    select.set_fields_part(p[4])
    select.set_from_part(p[5])
    select.set_where_part(p[6])

    limit = Limit(p[3], type=p[2])
    select.set_limit(limit)
    p[0] = select

def p_select_query3(p):
    '''select_query : SELECT distinct fields_part from where LIMIT NUMBER
                    | SELECT distinct fields_part from where LIMIT NUMBER OFFSET NUMBER'''
    select = Select()
    select.set_distinct(p[2])
    select.set_fields_part(p[3])
    select.set_from_part(p[4])
    select.set_where_part(p[5])

    limit = Limit(p[7])
    if len(p) == 10:
        limit.set_offset(p[9])
    select.set_limit(limit)

    p[0] = select

def p_distinct(p):
    '''distinct : DISTINCT
                | ALL
                | empty'''
    if p[1]:
        p[0] = p[1]
    else:
        p[0] = None

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
                    | where_object
    '''
    # where_object тут до первого рефакторинга
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

def p_from(p):
    '''from : FROM from_list'''
    p[0] = p[2]

def p_from2(p):
    '''from : empty'''
    p[0] = None

def p_from_list(p):
    '''from_list : from_object'''
    p[0] = [p[1]]

def p_from_list2(p):
    '''from_list : from_object join_part'''
    join_part = p[2]
    if join_part['more_join']:
        more_join = join_part['more_join']
        join_part['more_join'] = None
        join_part = [join_part] + more_join
    else:
        join_part = [join_part]
    p[0] = [{
        'value': p[1],
        'joins': join_part,
        'type': 'from_object',
    }]

def p_from_list3(p):
    '''from_list : from_list COMMA from_list'''
    p[0] = p[1] + p[3]



def p_join_part(p):
    '''join_part : join from_object
                 | join from_object join_part'''
    p[0] = {
        'type': 'join',
        'join_type': p[1],
        'value': p[2],
        'more_join': None,
    }
    if len(p) == 4:
        if p[3]['more_join']:
            more_join = p[3]['more_join']
            p[3]['more_join'] = None
            p[0]['more_join'] = [p[3]] + more_join
        else:
            p[0]['more_join'] = [p[3]]

def p_join_part_on(p):
    '''join_part : join from_object ON where_list
                 | join from_object ON where_list join_part'''
    p[0] = {
        'type': 'join',
        'join_type': p[1],
        'value': p[2],
        'on': p[4],
        'more_join': None,
    }
    if len(p) == 6:
        if p[5]['more_join']:
            more_join = p[5]['more_join']
            p[5]['more_join'] = None
            p[0]['more_join'] = [p[5]] + more_join
        else:
            p[0]['more_join'] = [p[5]]



def p_join(p):
    '''join : JOIN
            | RIGHT JOIN
            | LEFT JOIN
            | FULL JOIN
            | LEFT OUTER JOIN
            | RIGHT OUTER JOIN'''
    p[0] = p[1]
    if len(p) == 3:
        p[0] = '%s %s' % (p[1], p[2])
    if len(p) == 4:
        p[0] = '%s %s %s' % (p[1], p[2], p[3])

def p_from_object(p):
    '''from_object : NAME'''
    p[0] = {
        'type': 'from_object',
        'value': p[1],
    }

def p_from_object2(p):
    '''from_object : NAME NAME
                   | NAME AS NAME'''
    res = {
        'type': 'from_object',
    }
    if len(p) == 3:
        res['value'] = p[1]
        res['alias'] = p[2]
        p[0] = res
    else:
        res['value'] = p[1]
        res['alias'] = p[3]
        p[0] = res

def p_where(p):
    '''where : WHERE where_list
             | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

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
    if len(p) == 4 and (p[2].lower() == 'and' or p[2].lower() == 'or'):
        res = {
            'type': 'WHERE_EXPRESSION',
            'exp_type': p[2].lower(),
            'values': [p[1], p[3]]
        }
        if 'type' in p[3] and p[3]['type'] == 'WHERE_EXPRESSION':
            #пытаемся объеденить последовательность and .. and ... and
            if p[3]['exp_type'].lower() == p[2].lower():
                res = {
                    'type': 'WHERE_EXPRESSION',
                    'exp_type': p[2].lower(),
                    'values': [p[1]] + p[3]['values'],
                }
        p[0] = res
        return
    if len(p) == 6 and p[1] == '(' and (p[4].lower() == 'and' or p[4].lower() == 'or'):
        res = {
            'type': 'WHERE_EXPRESSION',
            'exp_type': p[4].lower(),
            'values': [p[2], p[5]]
        }
        p[0] = res
        return
    raise Exception('FAIL')


def p_where_object(p):
    '''where_object : where_compare_item COMPARE_TYPE where_compare_item
                    | where_compare_item IS where_compare_item
                    | where_compare_item IN where_compare_item
                    | where_compare_item BETWEEN between_compare_item'''
    res = {
        'type': 'compare',
        'compare_list': [p[1], p[3]],
        'compare_type': p[2],
    }
    p[0] = res

def p_where_compare_item(p):
    '''where_compare_item : where_and_field_item
    '''
    res = p[1]
    # res['type'] = 'WHERE_COMPARE_ITEM'
    p[0] = res

def p_where_and_field_item_number(p):
    '''where_and_field_item : NUMBER'''
    p[0] = {
        'type': 'number',
        'value': p[1],
    }

def p_where_and_field_item_string(p):
    '''where_and_field_item : STRING'''
    p[0] = {
        'type': 'string',
        'value': p[1],
    }

def p_where_and_field_item(p):
    '''where_and_field_item : NAME
                            | NAME "." NAME
                            | "(" select_query ")"
                            | DQ_STRING
                            | LIMIT
                            | NAME "." LIMIT
                            | LIMIT "." NAME
                            | LIMIT "." LIMIT'''
    # dirty bugfix of LIMIT field - TODO: delete limit from lexer?
    res = {
        'type': 'WHERE_AND_FIELD_ITEM',
    }
    if len(p) == 2:
        res['value'] = p[1]
        p[0] = res
        return
    if len(p) == 4 and isinstance(p[2], Select):
        res['value'] = p[2]
        p[0] = res
        return
    if len(p) == 4 and p[2] == '.':
        res['value'] = p[3]
        res['from_alias'] = p[1]
        p[0] = res
        return
    raise Exception('FAIL')

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

def p_where_and_field_item5_null(p):
    '''where_and_field_item : NULL'''
    p[0] = {
        'type': 'null'
    }

def p_where_and_field_item6_not(p):
    '''where_and_field_item : NOT where_and_field_item'''
    p[0] = {
        'type': 'not',
        'value': p[2],
    }

def p_between_compare_item(p):
    '''between_compare_item : where_and_field_item AND where_and_field_item '''
    p[0] = {
        'type': 'between',
        'value': [p[1], p[3]],
    }

def p_where_and_field_item_list(p):
    '''where_and_field_item_list : where_and_field_item COMMA where_and_field_item_list
                                 | where_and_field_item'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]