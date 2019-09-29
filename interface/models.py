from django.core import validators
from django.db import models


from interface.fields import EANField


class Brand(models.Model):
    """
    A specific brand, like "Douwe Egberts" or "Albert Heijn"
    """
    name = models.CharField(
        max_length=255,
        help_text="Brand name, for example 'Douwe Egberts'.",
    )


class Product(models.Model):
    """
    Defines specific instances of a certain thing.

    For example,
    * "Douwe Egberts Aroma Rood koffie, 500g."
    * "Albert Heijn Mineraalwater koolzuurhoudend, 1.5L"

    These products might come in different packages,
    and those packages might contain more of same product.
    """

    #: Name of a product
    name = models.CharField(max_length=255, help_text="Product name")

    #: Description. Should be optional
    description = models.TextField(null=True, blank=True)

    #: Brand name
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)


class Packaging(models.Model):
    """
    The physical wrappers around specific :class:`Product`s.

    A specific :class:`Product` may be packaged in many different ways.
    For example, it may be available on its own, or in multi-packs.
    Also, EAN numbers might change over time.

    This class represents all packagings for a specific product,
    with an optional amount.
    """

    #: the label on the product
    label = EANField()

    #: count: Number of items in a package
    count = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            validators.MinValueValidator(1),
        ],
    )

    #: description
    description = models.CharField(
        max_length=255,
        help_text="Short description.",
        blank=True,
        null=True,
    )
