from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('new_story/', views.new_story_page, name='new_story'),
    path('@<str:username>/', views.profile_page, name='profile'),
    path('@<str:username>/<uuid:post_id>/', views.view_post_page, name='view_post'),
    path('@<str:username>/<uuid:post_id>/update/', views.update_post_page, name='update_post'),
    path('@<str:username>/update/', views.update_profile_page, name='update_profile'),
    path('search/<str:category>/', views.search_page, name='search'),
    path('<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<str:username>/<uuid:post_id>/comment/', views.comment_post, name='comment_post'),
    path('<str:username>/<uuid:post_id>/like/', views.toggle_like_post, name='like_post'),
    path('follow/<str:username>/<str:category>/<str:q>/', views.toggle_follow_user, name='follow_user')
]
