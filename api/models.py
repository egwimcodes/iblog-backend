from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from accounts.models import IBlogUser

        
class BlogPost(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name='Blog Title')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(verbose_name='Content')
    author = models.ForeignKey(IBlogUser, related_name='blogs', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True, )
    featured_img = models.ImageField(blank=True, upload_to="featured_images")

    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        
    def str(self):
        return self.title
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        num = 1
        while BlogPost.objects.filter(slug__iexact=slug).exists():
            slug = f'{self.title}-{num}'
            num += 1
        self.slug = slug
        super().save(*args, **kwargs)
            

class Category(models.Model):
    category = models.CharField(max_length=50, blank=True, default="Uncategorized")
    blog_post = models.ForeignKey(BlogPost, on_delete=models.DO_NOTHING)
    
    def str(self):
        return self.category
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        