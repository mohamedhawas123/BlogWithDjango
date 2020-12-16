from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_post():
    return Post.published.count()

@register.inclusion_tag('blogg/post/lastest_post.html')
def show_latest_posts(count=5):
    lastest = Post.published.order_by('-publish')[:count]
    return {'latest': lastest}

