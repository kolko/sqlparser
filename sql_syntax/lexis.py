reserved = {
    'from': 'FROM',
    'select': 'SELECT',
    'insert': 'INSERT',
    'update': 'UPDATE',
    'as': 'AS',
    'where': 'WHERE',
    'and': 'AND',
    'or': 'OR',
    'is': 'IS'
}

t_COMPARE_TYPE = r'\!=|==|>|<|>=|<=|='

def t_NAME(t):
    r'[_a-zA-Z][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = reserved.get(t.value.lower(), 'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_END_QUERY = r';'
t_COMMA = r','

t_ignore_COMMENT = r'--.*'


tokens = (
    'COMPARE_TYPE',
    'NAME', 'NUMBER',
    'END_QUERY', 'COMMA', 'ANY',
) + tuple(set(reserved.values()))

literals = '(){}@%.,*'

t_ignore = ' \t\n'