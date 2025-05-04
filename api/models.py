from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class IBlogUser(AbstractUser):
    class Meta:
        verbose_name = "IBlog User"
        verbose_name_plural = "IBlog Users"
        
class BlogPost(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name='Blog Title')
    description = models.CharField(max_length=500, verbose_name='Description')
    content = models.TextField(verbose_name='Content')
    published_date = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return self.title
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

class PostCategory(models.Model):
    category = models.CharField(max_length=50, blank=True, default="Uncategorized")
    ibloguser = models.ForeignKey(IBlogUser, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.DO_NOTHING)
    
    def str(self):
        return self.category
    
    class Meta:
        verbose_name = "Blog Categories"
        verbose_name_plural = "Blog Categoriess"
        