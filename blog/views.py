from django.shortcuts import render, redirect
from .models import Post, Comment
from accounts.models import User
from django.db.models import Q
from .utils import parse_user, extract_keywords

def home_page(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    feed = request.GET.get('feed')
    results = []

    if feed:
        following_users = request.user.following.exclude(pk=request.user.id)
        results = Post.objects.filter(author__in=following_users).order_by('-created_at')
    else:
        interests = request.session.get('interests', [])

        if interests:
            query = Q()

            for kw in interests:
                query |= Q(story__icontains=kw) | Q(title__icontains=kw)

            results = Post.objects.filter(query).exclude(author=request.user).order_by('-created_at').distinct()

    return render(request, 'blog/home.html', {
        'feed': feed,
        'results': results
    })

def new_story_page(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        title = request.POST.get('title')
        story = request.POST.get('story')
        file = request.FILES.get('image')

        post = Post.objects.create(title=title, story=story, author=request.user)

        if file:
            post.picture = file.read()

        post.save()

        return redirect('blog:view_post', username=request.user.username, post_id=post.id)

    return render(request, 'blog/new_story.html', {
        'new_post': True
    })

def profile_page(request, username):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile = User.objects.get(username=username)
    posts = Post.objects.filter(author=profile)

    return render(request, 'blog/profile.html', {
        'profile': parse_user(request.user, profile),
        'posts': posts
    })

def view_post_page(request, username, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    _author = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post_id=post_id)

    title_keywords = extract_keywords(post.title)
    story_keywords = extract_keywords(post.story)
    interests = request.session.get('interests', [])

    [interests.append(kw) for kw in title_keywords if kw not in interests]
    [interests.append(kw) for kw in story_keywords if kw not in interests]

    request.session['interests'] = interests
    user_liked_post = post.user_liked_post(request.user)

    return render(request, 'blog/view_post.html', {
        'post': post,
        'comments': comments,
        'user_liked': user_liked_post
    })

def update_post_page(request, username, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        story = request.POST.get('story')
        file = request.FILES.get('image')

        post.title = title
        post.story = story

        if file:
            post.picture = file.read()

        post.save()

        return redirect('blog:view_post', username=username, post_id=post.id)

    return render(request, 'blog/new_story.html', {
        'post': post,
        'new_post': False
    })

def update_profile_page(request, username):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = User.objects.get(username=username)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        file = request.FILES.get('image')

        user.bio = bio

        if file:
            user.picture = file.read()

        user.save()

        return redirect('blog:profile', username=user.username)

    return render(request, 'blog/update_profile.html', {
        'user': user
    })

def search_page(request, category):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    q = request.GET.get('q')
    results = []

    if q and category == 'posts':
        results = Post.objects.filter(Q(title__icontains=q) | Q(story__icontains=q)).exclude(author=request.user)
    elif q and category == 'users':
        results = [
            parse_user(request.user, user)
            for user in User.objects.filter(username__icontains=q)
        ]

    return render(request, 'blog/search.html', {
        'q': q,
        'category': category,
        'results': results
    })

def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    post = Post.objects.get(id=post_id)
    post.delete()

    return redirect('blog:profile', username=request.user.username)

def comment_post(request, username, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    content = request.POST.get('comment')
    comment = Comment.objects.create(content=content, author=request.user, post_id=post_id)
    comment.save()

    return redirect('blog:view_post', username=username, post_id=post_id)

def toggle_like_post(request, username, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if username == request.user.username:
        return redirect('blog:view_post', username=username, post_id=post_id)

    post = Post.objects.get(id=post_id)

    if post.user_liked_post(request.user):
        post.unlike_post(request.user)
    else:
        post.like_post(request.user)

    post.save()

    return redirect('blog:view_post', username=username, post_id=post_id)

def toggle_follow_user(request, username, category, q=None):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = User.objects.get(id=request.user.id)
    user_to_follow = User.objects.get(username=username)

    if user.is_following(user_to_follow):
        user.unfollow(user_to_follow)
    else:
        user.follow(user_to_follow)

    user.save()

    if category == 'profile':
        return redirect('blog:profile', username=user_to_follow.username)

    return redirect(f'/search/{category}/?q={q}')
