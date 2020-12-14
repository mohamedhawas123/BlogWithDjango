from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import EmailPostForm, CommentForm
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

    comments = posts.comments.filter(active = True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post=posts
            new_comment.save()

    else:
        comment_form = CommentForm()


    return render(request, 'blogg/post/detail.html', {'post': posts, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def post_share(request, post_id):
    sent = False
    post = get_object_or_404(Post, id=post_id, status='draft')
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommend you read" f"{post.title}"
            message = f" Read {post.title} at {post_url}\n\n"
            send_mail(subject, message, 'mohamedhawas123@gmail.com', [cd['to']])
            sent= True

            

    else:
        form = EmailPostForm()
    
    return render(request, 'blogg/post/share.html', {'post': post, 'form': form, 'sent': sent})
           