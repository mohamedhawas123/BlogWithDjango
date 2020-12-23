from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .form import SearchFomr
#from django.contrib.postgres.search import TrigramSimilarity


#Searching with trigram similarity
#psql blog
#CREATE EXTENSION pg_trgm;
#results = Post.published.annotate(
   # similarity=TrigramSimilarity('title', query),
#).filter(similarity__gt=0.1).order_by('-similarity')


#search_vector = SearchVector('title', weight='A') + \
 #SearchVector('body', weight='B')
#search_query = SearchQuery(query)
#results = Post.published.annotate(
#rank=SearchRank(search_vector, search_query)
#).filter(rank__gte=0.3).order_by('-rank')


def post_search(request):
    form = SearchFomr()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchFomr(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector, rank=search_query).filter(search=search_query).order_by('-rank')
          
    return render(request,
                  'blogg/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paignoter = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paignoter.page(page)
    except PageNotAnInteger:
        posts = paignoter.page(1)
    except EmptyPage:
        posts = paignoter.page(paignoter.num_pages)
        
    return render(request, 'blogg/post/list.html', {'posts': posts, 'page': page, 'tag': tag})



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

    posts_tags_ids = posts.tags.values_list('id', flat=True)
    similir_posts = Post.published.filter(tags__in=posts_tags_ids).exclude(id=posts.id)
    similir_posts = similir_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blogg/post/detail.html', {'post': posts,
    'comments': comments,
    'new_comment': new_comment,
    'comment_form': comment_form,
    'similir_posts' : similir_posts
    })


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
           