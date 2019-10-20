from django.core import validators
from django.core.exceptions import ValidationError
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

    @staticmethod
    def get_brand_identifier(ean):
        return ean[:7]

    @classmethod
    def by_ean(cls, ean):
        if not isinstance(ean, str):
            ean = str(ean)

        pk = (cls.objects.all().filter(
                  product__packaging__label__startswith=(
                    cls.get_brand_identifier(ean)))
              .values_list('pk').distinct()).get()
        return cls.objects.get(pk=pk)

    def __str__(self):
        return self.name


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
        null=True,
        blank=True,
    )

    #: count
    count = models.PositiveIntegerField(default=0)

    @classmethod
    def by_ean(cls, ean):
        return cls.objects.get(packaging__label=ean)

    def __str__(self):
        return f"{self.brand} {self.name}"

    def clean(self):
        for item in self.packaging_set.all():
            try:
                brand = Brand.by_ean(item.label)
            except Brand.MultipleObjectsReturned as e:
                raise ValidationError({
                    'brand':
                    "More than one brand associated with this EAN?",
                }) from e
            if self.brand != brand:
                raise ValidationError({
                    'brand':
                    f"{brand} is already associated with this EAN",
                })
        return super().clean()


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
        help_text="Number of product per package (e.g. sixpack).",
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

    def clean(self):
        try:
            brand = Brand.by_ean(self.label)
        except Brand.DoesNotExist:
            brand = self.product.brand
        except Brand.MultipleObjectsReturned as e:
            raise ValidationError({
                'label':
                'This EAN is associated with more than 1 product!',
            }) from e

        if self.product.brand != brand:
            msg = (f"This EAN is associated with brand '{brand}', not with "
                   f"product's brand '{self.product.brand}'")
            raise ValidationError({
                'product': msg,
                'label': msg,
            })

        return super().clean()


class GenericProduct(models.Model):
    """Generic version of a product, e.g. "coffee beans"."""

    #: name of the generic variants
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
