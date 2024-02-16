from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse

from BlogPortal import settings
from .models import Blog, Comment, Response
from django.db.models import Count
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse

'''
home(request): Renders the home page template.

blogs_of_specific_author(request, author_id): 
    Retrieves blogs of a specific author along with their likes, dislikes, and comments count. The function takes an author ID as input and returns JSON data containing information about the author's blogs.

top_commented_blogs(request, user_id): 
    Retrieves the top 5 commented blogs of a specific user. The function takes a user ID as input and returns JSON data containing information about the user's top commented blogs.

top_liked_disliked_blogs(request): 
    Retrieves the top 5 liked and disliked blogs in the last 3 days. The function returns JSON data containing information about the top liked and disliked blogs within the specified time frame.
'''

def home(request):
    base_url = settings.BASE_URL
    return render(request, 'app/home.html',{'base_url': base_url})

def blogs_of_specific_author(request, author_id):
    # Retrieve blogs of a specific author along with likes, dislikes, and comments count
    author = get_object_or_404(User, id=author_id)
    blogs = Blog.objects.filter(author=author).annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('response', filter=Q(response__like_or_not=True)),
        dislikes_count=Count('response', filter=Q(response__like_or_not=False))
    )

    # Handling the case where author_id doesn't exist so as to fetch blogs
    if(not blogs) : 
        return HttpResponseBadRequest("Bad request message")
    
    # Prepare data to be sent as JSON response
    data = {
        'author': author.username,
        'blogs': list(blogs.values('name', 'content', 'created_date', 'modified_date', 'comments_count', 'likes_count', 'dislikes_count'))
    }
    return JsonResponse(data)

def top_commented_blogs(request, user_id):
    # Retrieve top 5 commented blogs of a user
    user = get_object_or_404(User, id=user_id)
    top_commented_blogs = Blog.objects.filter(author=user).annotate(
        comments_count=Count('comment')
    ).order_by('-comments_count')[:5]

    # Prepare data to be sent as JSON response
    data = {
        'user': user.username,
        'top_commented_blogs': list(top_commented_blogs.values('name', 'content', 'created_date', 'modified_date', 'comments_count'))
    }
    return JsonResponse(data)

def top_liked_disliked_blogs(request):
    # Retrieve top 5 liked and disliked blogs in the last 3 days
    three_days_ago = datetime.now() - timedelta(days=3)
    top_liked_blogs = Blog.objects.filter(response__like_or_not=True, response__response_date__gte=three_days_ago).annotate(
        likes_count=Count('response')
    ).order_by('-likes_count')[:5]
    top_disliked_blogs = Blog.objects.filter(response__like_or_not=False, response__response_date__gte=three_days_ago).annotate(
        dislikes_count=Count('response')
    ).order_by('-dislikes_count')[:5]

    # Prepare data to be sent as JSON response
    data = {
        'top_liked_blogs': list(top_liked_blogs.values('name', 'content', 'created_date', 'modified_date', 'likes_count')),
        'top_disliked_blogs': list(top_disliked_blogs.values('name', 'content', 'created_date', 'modified_date', 'dislikes_count'))
    }
    return JsonResponse(data)

def my_recent_liked_blogs(request, user_id):
    # Retrieve recent 5 liked blogs of a specific user
    user = get_object_or_404(User, id=user_id)
    recent_liked_blogs = Response.objects.filter(user=user, like_or_not=True).order_by('-response_date')[:5]
    data = {
        'user': user.username,
        'recent_liked_blogs': list(recent_liked_blogs.values('blog__name', 'blog__content', 'blog__created_date', 'blog__modified_date'))
    }
    return JsonResponse(data)

def my_comment_history_for_specific_blog(request, user_id, blog_id):
    # Retrieve comment history for a specific blog by a user
    user = get_object_or_404(User, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)
    comment_history = Comment.objects.filter(user=user, blog=blog).order_by('-created_date')
    data = {
        'user': user.username,
        'blog': blog.name,
        'comment_history': list(comment_history.values('comment_text', 'created_date', 'modified_date'))
    }
    return JsonResponse(data)

def my_comment_history_for_author(request, user_id, author_id):
    # Retrieve comment history for a particular author by a user
    user = get_object_or_404(User, id=user_id)
    author = get_object_or_404(User, id=author_id)
    comment_history = Comment.objects.filter(user=user, blog__author=author).order_by('-created_date')
    data = {
        'user': user.username,
        'author': author.username,
        'comment_history': list(comment_history.values('blog__name', 'comment_text', 'created_date', 'modified_date'))
    }
    return JsonResponse(data)