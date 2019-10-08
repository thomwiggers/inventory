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
        unique=True,
    )

    @classmethod
    def by_ean(cls, ean):
        return cls.objects.get(brandean__label=ean[:7])

    def __str__(self):
        return self.name


class BrandEAN(models.Model):
    """
    EAN brand associations

    EAN numbers have an indication for the brand name.
    We record this for easier classification.
    """

    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE,
    )

    label = models.CharField(
        max_length=7,
        help_text="First 7 numbers of the EAN, which indicate the brand",
        unique=True,
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

    #: Brand name
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    #: Name of a product
    name = models.CharField(max_length=255, help_text="Product name")

    #: Description. Should be optional
    description = models.TextField(null=True, blank=True)

    #: Generic variant, e.g. "coffee beans"
    generic_product = models.ForeignKey(
        'GenericProduct',
        on_delete=models.PROTECT,
    )

    @classmethod
    def by_ean(cls, ean):
        return cls.objects.get(packaging__label=ean)

    def __str__(self):
        return f"{self.brand}: {self.name}"


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
    label = EANField('EAN code', unique=True)

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

    #: Associated product
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        label = f"Packaging for {self.count}x {self.product}"
        if self.description:
            label += f" ({self.description})"
        return label


class GenericProduct(models.Model):
    """Generic version of a product, e.g. "coffee beans"."""

    #: name of the generic variants
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
