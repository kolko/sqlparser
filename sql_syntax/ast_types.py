class _ContainerWithSetter(type):
    def __new__(cls, name, bases, attrs):
        fields = attrs.get('FIELDS', [])
        for field_name, field_type in fields:
            fun = _ContainerWithSetter._create_setter(field_name, field_type)
            attrs['set_{}'.format(field_name)] = fun
            attrs[field_name] = None
        return super(_ContainerWithSetter, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def _create_setter(field_name, field_type):
        def fun(self, _field):
            assert not getattr(self, field_name, None), u'Already set {}'.format(field_name)
            if _field is not None and field_type:
                if isinstance(field_type, list):
                    for item in _field:
                        assert isinstance(item, field_type[0]), u'Wrong type! Must be {}, but got {}'\
                            .format(field_type[0], type(item))
                else:
                    assert isinstance(_field, field_type), u'Wrong type! Must be {}, but got {}'\
                        .format(field_type, type(_field))
            setattr(self, field_name, _field)
        return fun

def inc_tab(s, count=1):
    tabs = '    '*count
    return '\n'.join('{}{}'.format(tabs, line) for line in str(s).splitlines())

class Limit(metaclass=_ContainerWithSetter):
    FIELDS = [
        ('offset', None),
    ]

    def __init__(self, val, type='first'):
        self.val = val
        self.type = type.lower()

    def __str__(self):
        return u'''Limit:
    val:
        {0.val}
    type:
        {0.type}
    offset:
        {0.offset}
        '''.format(self)


class Field(metaclass=_ContainerWithSetter):
# expression
    FIELDS = [
        ('value', None),
        ('table_name', None),
        ('alias', None),
    ]

    def __str__(self):
        value = '    Value:\n{}'.format(inc_tab(self.value, 2))
        return u'''Field:
{1}
    table_name:
        {0.table_name}
    alias:
        {0.alias}
        '''.format(self, value)


class Table(metaclass=_ContainerWithSetter):
    FIELDS = [
        ('alias', None),
    ]

    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name

class VirtualTable(metaclass=_ContainerWithSetter):
    FIELDS = [
        ('alias', None),
    ]

    def __init__(self, select):
        assert isinstance(select, Select)
        self.select = select

class Select(metaclass=_ContainerWithSetter):
    FIELDS = [
        ('field_part', [Field]),
        ('from_part', None),
        ('where_part', None),
        ('distinct', str),
        ('limit', Limit),
    ]

    def __str__(self):
        res = 'SELECT:\n'

        res += '    Field part:\n'
        res += ''.join('{}\n'.format(inc_tab(field, 2)) for field in self.field_part)

        res += '    From part:\n'
        res += inc_tab(self.from_part, 2)

        if self.where_part:
            res += '    Where part:\n'
            res += inc_tab(self.where_part, 2)

        if self.distinct:
            res += '     distinct:\n'
            res += inc_tab(self.distinct, 2)

        if self.limit:
            res += '     limit:\n'
            res += inc_tab(self.limit, 2)

        return res