from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    object_list = Post.published.all()
    paignoter = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paignoter.page(page)
    except PageNotAnInteger:
        posts = paignoter.page(1)
    except EmptyPage:
        posts = paignoter.page(paignoter.num_pages)
        
    return render(request, 'blogg/post/list.html', {'posts': posts, 'page': page})



def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, slug=post,
     status="draft",
     publish__year = year,
     publish__month = month,
     publish__day = day
    )
    return render(request, 'blogg/post/detail.html', {'post': posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='draft')
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_aboslute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommend you read" f"{cd['post.ttile']}"

            

    else:
        form = EmailPostForm()
    
    return render(request, 'blogg/post/share.html', {'post': post, 'form': form})
           