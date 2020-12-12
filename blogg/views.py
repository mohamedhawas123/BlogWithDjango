from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blogg/post/list.html', {'posts': posts})



def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, slug=post,
     status="draft",
     publish__year = year,
     publish__month = month,
     publish_day = day
    )
    return render(request, 'blogg/post/detail.html', {'posts': posts})