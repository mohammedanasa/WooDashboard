import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.models import User



class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    aid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstaddress = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.street

    
class Modifier(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    

class ModifierGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mgid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    modifiers = models.ManyToManyField(Modifier, related_name='groups',blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, null=True)
    modifier_groups = models.ManyToManyField(ModifierGroup, related_name='products',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='product/photos/', null=True, blank=True)
    
    

    def __str__(self):
        return self.name

#Category Model
class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    cid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)  
    description = models.TextField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product, blank=True, null=True, related_name="catprods")
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='category/photos/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Menu(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    menuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250,null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
  
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Restaurant(models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    lid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    menu = models.ManyToManyField(Menu, blank=True, null=True)
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True) 
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

