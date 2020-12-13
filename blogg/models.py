from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='draft')

class Post(models.Model):
    title = models.CharField(max_length=55)
    slug = models.SlugField(max_length=55, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts' ,on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    class Meta:
        ordering = ('-publish', )

    def get_absolute_url(self):
        return reverse('blogg:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


    def __str__(self):
        return self.title

    published = PublishManager()


