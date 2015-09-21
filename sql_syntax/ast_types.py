class _ContainerWithSetter(type):
    def __new__(cls, name, bases, attrs):
        fields = attrs.get('FIELDS', [])
        for field_name, field_type in fields:
            fun = __class__._create_setter(field_name, field_type)
            attrs['set_{}'.format(field_name)] = fun
            attrs[field_name] = None
        attrs['__str__'] = __class__._create_str()
        return super(__class__, cls).__new__(cls, name, bases, attrs)

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

    @staticmethod
    def _create_str():
        def fun(self):
            res = '{}:\n'.format(self.__class__.__name__)

            for field_name, field_type in self.FIELDS:
                val = getattr(self, field_name, None)
                if not val:
                    continue

                res += '    {}:\n'.format(field_name.capitalize())
                if isinstance(val, list):
                    res += ''.join(inc_tab(field, 2) for field in val)
                elif isinstance(val, SqlObject):
                    res += inc_tab(val, 2)
                else:
                    res += (inc_tab(val, 2) + '\n')
            return res
        return fun

def inc_tab(s, count=1):
    tabs = '    '*count
    res = ''.join('{}{}'.format(tabs, line) for line in str(s).splitlines(True))
    return res


class SqlObject(metaclass=_ContainerWithSetter):
    pass


class Limit(SqlObject):
    FIELDS = [
        ('val', None),
        ('type', None),
        ('offset', None),
    ]

    def __init__(self, val, type='first'):
        self.val = val
        self.type = type.lower()


class Field(SqlObject):
# expression
    FIELDS = [
        ('value', None),
        ('table_name', None),
        ('alias', None),
    ]


class Table(SqlObject):
    FIELDS = [
        ('name', None),
        ('alias', None),
    ]

    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name


class VirtualTable(SqlObject):
    FIELDS = [
        ('select', None),
        ('alias', None),
    ]

    def __init__(self, select):
        assert isinstance(select, Select)
        self.select = select


class Select(SqlObject):
    FIELDS = [
        ('field_part', [Field]),
        ('from_part', None),
        ('where_part', None),
        ('distinct', str),
        ('limit', Limit),
    ]