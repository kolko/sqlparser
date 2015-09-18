class _ContainerWithSetter(type):
    def __new__(cls, name, bases, attrs):
        fields = attrs.get('FIELDS', [])
        for field_name, field_type in fields:
            fun = _ContainerWithSetter._create_setter(field_name, field_type)
            attrs['set_{}'.format(field_name)] = fun
        return super(_ContainerWithSetter, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def _create_setter(field_name, field_type):
        def fun(self, _field):
            assert not getattr(self, field_name, None), u'Already set {}'.format(field_name)
            if _field is not None and field_type:
                assert isinstance(_field, field_type), u'Wrong type! Must be {}, but got {}'\
                    .format(field_type, type(_field))
            setattr(self, field_name, _field)
        return fun


class Limit(metaclass=_ContainerWithSetter):
    __metaclass__ = _ContainerWithSetter
    FIELDS = [
        ('offset', None),
    ]

    def __init__(self, val, type='first'):
        self.val = val
        self.type = type.lower()


class Select(metaclass=_ContainerWithSetter):
    __metaclass__ = _ContainerWithSetter
    FIELDS = [
        ('fields_part', None),
        ('from_part', None),
        ('where_part', None),
        ('distinct', str),
        ('limit', Limit),
        ('limit_type', None),
        ('limit_offset', None),
    ]


