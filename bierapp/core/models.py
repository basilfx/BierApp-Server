from django.db import models
from django.core.urlresolvers import reverse

from bierapp.accounts.models import User, Site

from django_extensions.db.models import TimeStampedModel


class ProductGroup(models.Model):
    site = models.ForeignKey(Site, related_name="product_groups")
    title = models.CharField(max_length=255)

    is_hidden = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse(
            "bierapp.core.views.product_group", kwargs={"id": self.pk})


class TransactionTemplateCategory(models.Model):
    site = models.ForeignKey(Site, related_name="+")
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.title)


class TransactionTemplate(models.Model):
    category = models.ForeignKey(TransactionTemplateCategory, related_name="+")
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.title)

    def to_transaction(self, accounted_user, executing_user=None):
        """
        Commit this instance as a transaction.
        """

        if executing_user is None:
            executing_user = accounted_user

        transaction = Transaction(
            description="Committing %s" % self.title,
            site=self.category.site
        )

        transaction.save()

        for item in self.items.all():
            transaction.transaction_items.create(
                product=item.product,
                count=item.count,
                accounted_user=accounted_user,
                executing_user=executing_user
            )

        return transaction


class TransactionTemplateItem(models.Model):
    transaction_template = models.ForeignKey(
        "TransactionTemplate", related_name="items")

    product = models.ForeignKey("Product")
    count = models.IntegerField(null=False, default=0)


class Product(TimeStampedModel, models.Model):
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    is_hidden = models.BooleanField(default=True)
    product_group = models.ForeignKey(ProductGroup, related_name="products")

    logo = models.ImageField(
        width_field="logo_width", height_field="logo_height",
        upload_to="apps/bierapp/logos/", null=True)
    logo_height = models.PositiveIntegerField(null=True)
    logo_width = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse(
            "bierapp.core.views.product_group_product",
            kwargs={"group_id": self.product_group.pk, "id": self.pk})


class Transaction(TimeStampedModel, models.Model):
    site = models.ForeignKey(Site, related_name="transactions")
    description = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        ordering = ("-created", )


class TransactionItem(models.Model):
    """

    Although `product_group` can be derrived from `product`, it is added
    because a product can move to a different product group. Furthermore, it
    simplifies lookups.
    """

    transaction = models.ForeignKey(
        "Transaction", related_name="transaction_items")

    product = models.ForeignKey(Product)
    count = models.IntegerField(null=False, default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    accounted_user = models.ForeignKey(User, related_name="+")
    executing_user = models.ForeignKey(User, related_name="+")

    def save(self, *args, **kwargs):
        if self.value is None:
            self.value = self.product.value * self.count

        super(TransactionItem, self).save(*args, **kwargs)


class XPTransaction(TimeStampedModel, models.Model):
    site = models.ForeignKey("accounts.Site", related_name="xp_transactions")
    user = models.ForeignKey("accounts.User")

    parent = models.ForeignKey("XPTransaction", null=True)

    value = models.IntegerField()
    description = models.TextField()

    class Meta:
        ordering = ("-created", )
