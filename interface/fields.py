import stdnum.ean
from django import forms
from django.db.models import fields

from interface.validators import ean_validator


class EANFormField(forms.Field):
    """Form field for EAN codes"""
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = (
            kwargs.get('validators', []) + [ean_validator])
        super().__init__(*args, **kwargs)

    def clean(self, value):
        return super().clean(value)


class EANField(fields.CharField):
    """Model field for EAN codes"""

    description = "EAN-13 field"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        kwargs['validators'] = (
            kwargs.get('validators', []) + [ean_validator])

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['max_length'] = 13
        kwargs['min_length'] = 8

        return super().formfield(**kwargs)

    def to_python(self, value):
        return stdnum.ean.compact(value)

    def __str__(self):
        return stdnum.ean.format(self.value)

    def deconstruct(self):
        """
        Deconstruct this custom form field

        See `https://docs.djangoproject.com/en/2.2/howto/custom-model-fields/#field-deconstruction`
        """  # noqa
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        if 'validators' in kwargs:
            kwargs['validators'].remove(ean_validator)

        return name, path, args, kwargs
