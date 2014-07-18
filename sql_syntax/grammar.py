from . import lexis

# select z.a from b as z where b=z.c
#
# exp : select fields from name alias where
# select : SELECT
# fields : field | fields comma field
# field : name | name DOT name
# comma : ,
# DOT : .
# from : FROM
# name : ID
# alias : as name | empty
# as : AS
# where : WHERE clouse | empty

tokens = lexis.tokens

# precedence = (
#     ('right', '='),
#     ('right', 'QUANTIFIER'),
# )

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
    '''select_query : SELECT fields_part FROM from_part where_part'''
    res = {
        'type': 'SELECT',
        'fields': p[2],
        'from': p[4],
        }
    if len(p) == 6:
        res['where'] = p[5]
    p[0] = res

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
                 | NAME NAME'''
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


def p_where_part(p):
    '''where_part : WHERE where_list
                  | empty'''
    if len(p) == 3:
        res = {
            'type': 'WHERE',
            'value': p[2],
        }
        p[0] = res


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
    if len(p) == 4 and (p[2] == 'and' or p[2] == 'or'):
        res = {
            'type': 'WHERE_EXPRESSION',
            'exp_type': p[2],
            'values': [p[1], p[3]]
        }
        if 'type' in p[3] and p[3]['type'] == 'WHERE_EXPRESSION':
            #пытаемся объеденить последовательность and .. and ... and
            if p[3]['exp_type'] == p[2]:
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
                    | where_compare_item IS where_compare_item'''
    res = {
        'compare_list' : [p[1], p[3]],
        'compare_type': p[2],
    }
    p[0] = res

def p_where_compare_item(p):
    '''where_compare_item : where_and_field_item
    '''
    res = {
        'type': 'WHERE_COMPARE_ITEM',
    }
    if len(p) == 2 and 'type' in p[1] and p[1]['type'] == 'WHERE_AND_FIELD_ITEM':
        res = p[1]
        res['type'] = 'WHERE_COMPARE_ITEM'
        p[0] = res
        return

def p_where_and_field_item(p):
    '''where_and_field_item : NUMBER
                            | NAME
                            | NAME "." NAME
                            | "(" select_query ")" '''
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