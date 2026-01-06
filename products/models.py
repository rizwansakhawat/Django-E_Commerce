from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product:products_by_category', kwargs={'category_slug': self.slug})


#  Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product:products_by_brand', kwargs={'brand_slug': self.slug})


#  Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='products', blank=True, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)  # ProductSKU (Stock Keeping Unit)  #89270182
    short_description = models.CharField(max_length=255, blank=True, null=True)  # Short tagline
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)  ##"Trending Items"
    is_promotion = models.BooleanField(default=False)  # For promotional banners
    promotion_theme = models.CharField(max_length=50, blank=True, null=True)  # 'bg-black-darker', 'bg-blue', 'bg-silver'
    promotion_size = models.CharField(max_length=20, default='regular', choices=[('large', 'Large'), ('regular', 'Regular')])
    main_image = models.ImageField(upload_to='products/')
    warranty_years = models.PositiveIntegerField(default=0)  # 1, 2, 3 years
    warranty_info = models.CharField(max_length=200, blank=True, null=True)  # "Local Manufacturer Warranty"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_discount_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0


# ProductImage Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.product.name}"


# ProductReview Model
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1, help_text='Rating from 1.0 to 5.0')
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"


#makemigrations ProductSpecification Model 
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    specification = models.CharField(max_length=255)  #  "5.5" Retina HD Display with 3D Touch"

    def __str__(self):
        return self.specification


#  ProductDescription Model 
class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descriptions')
    title = models.CharField(max_length=200)  #  "3D Touch", "12MP Camera"
    content = models.TextField()  # Description text
    image = models.ImageField(upload_to='product_descriptions/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.title}"


#  ProductAdditionalInfo Model 
class ProductAdditionalInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_info')
    attribute_name = models.CharField(max_length=100)  ## "Capacity", "Display", "Camera"
    attribute_value = models.TextField()  # Long text for detailed specs
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Product Additional Info"

    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}"










