from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='default_avatar.png')
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="market_author_groups",
        related_query_name="market_author",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="market_author_permissions",
        related_query_name="market_author",
    )

    class Meta:
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.username

    @property
    def likes(self):
        return self.like_set.count()


class Product(AbstractBaseModel):
    PRODUCT_TYPE_CHOICES = (
        ('digital', 'Digital'),
        ('physical', 'Physical'),
        ('service', 'Service'),
        ('music', 'Music'),
        ('video', 'Video'),
        ('blockchain', 'Blockchain'),
        ('ai', 'Artificial Intelligence'),
        ('iot', 'Internet of Things'),
        ('other', 'Other'),
    )

    name = models.ForeignKey(Author, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='products/', null=True, blank=True, default='default_product.png')
    ends_in = models.DateTimeField()  # renamed from 'ends_in'
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='other')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Products'
        db_table = 'products'