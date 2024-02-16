from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  
    path('blogs/<int:author_id>/', views.blogs_of_specific_author, name='blogs_of_specific_author'),
    path('top-commented-blogs/<int:user_id>/', views.top_commented_blogs, name='top_commented_blogs'),
    path('top-liked-disliked-blogs/', views.top_liked_disliked_blogs, name='top_liked_disliked_blogs'),
    path('my-recent-liked-blogs/<int:user_id>/', views.my_recent_liked_blogs, name='my_recent_liked_blogs'),
    path('my-comment-history-for-specific-blog/<int:user_id>/<int:blog_id>/', views.my_comment_history_for_specific_blog, name='my_comment_history_for_specific_blog'),
    path('my-comment-history-for-author/<int:user_id>/<int:author_id>/', views.my_comment_history_for_author, name='my_comment_history_for_author'),
]
