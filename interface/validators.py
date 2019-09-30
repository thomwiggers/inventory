from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
import stdnum.ean
import stdnum.exceptions


@deconstructible
def ean_validator(value):
    """
    Validate EAN identifiers

    Examples::

        >>> ean_valitator('1')
        ValidationError(..)
        >>> ean_validator('8718265638716')
    """
    try:
        stdnum.ean.validate(value)
    except stdnum.exceptions.ValidationError as e:
        raise ValidationError(e.message) from e
