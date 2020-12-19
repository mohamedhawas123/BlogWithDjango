from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    tilte = 'My Blog'
    link = reverse_lazy('blogg:post_list')
    description = 'New posts of my Blog'

    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title 
    def item_description(self, item):
        return truncatewords(item.body, 30)
        