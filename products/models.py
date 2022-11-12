from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
# Category Model




class Category(models.Model):
    name = models.CharField(max_length=300)
  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

#Product Model
class  Product(models.Model):
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='images', blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.FloatField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('products:product')

    def get_absolute_url(self):
        return reverse("products:product", kwargs={
            'slug': self.slug
        })

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)
        

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    pub_date = models.DateTimeField('date published', editable=True)
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200, editable=True)
    rating = models.IntegerField(choices=RATING_CHOICES, editable=True)



        

