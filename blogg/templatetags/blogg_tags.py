from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_post():
    return Post.published.count()

@register.inclusion_tag('blogg/post/lastest_post.html')
def show_latest_posts(count=5):
    lastest = Post.published.order_by('-publish')[:count]
    return {'latest': lastest}


@register.inclusion_tag('blogg/post/latest_comments.html')
def get_most_comments_post(count=5):
    comment =  Post.published.annotate(
        total_comments =Count('comments')).order_by('-total_comments')[:count]
    
    return {'comment': comment}


@register.filter(name='markdown')
def makedown_format(text):
    return mark_safe(markdown.markdown(text))
