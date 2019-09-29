from django.db.models import fields
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

import stdnum.ean
import stdnum.exceptions


@deconstructible
def ean_validator(value):
    """Validate EAN numbers"""
    try:
        stdnum.ean.validate(value)
    except stdnum.exceptions.ValidationError as e:
        raise ValidationError from e


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

        return super().formfield(kwargs)

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
