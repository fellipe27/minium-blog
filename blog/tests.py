from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Post, Comment

class HomePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')

    @staticmethod
    def get_url():
        return reverse('blog:home')

    def test_authentication_required(self):
        self.client.logout()

        response = self.client.get(self.get_url())
        self.assertRedirects(response, reverse('accounts:login'))

    def test_home_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_home_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, 'For you')
        self.assertContains(response, 'Following')

class NewStoryPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')

    @staticmethod
    def get_url():
        return reverse('blog:new_story')

    def test_authentication_required(self):
        self.client.logout()

        response = self.client.get(self.get_url())
        self.assertRedirects(response, reverse('accounts:login'))

    def test_create_new_post(self):
        data = {
            'title': 'title',
            'story': 'story'
        }

        response = self.client.post(self.get_url(), data)
        post = Post.objects.get(author=self.user)

        self.assertTrue(Post.objects.filter(author=self.user).exists())
        self.assertRedirects(response, reverse('blog:view_post', kwargs={
            'username': self.user.username,
            'post_id': post.id
        }))

    def test_new_story_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/new_story.html')

    def test_new_story_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, 'Publish')

class ProfilePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')

    def get_url(self):
        return reverse('blog:profile', kwargs={ 'username': self.user.username })

    def test_profile_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/profile.html')

    def test_profile_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, f'{self.user.username}\'s posts')
        self.assertContains(response, self.user.username)
        self.assertContains(response, 'No bio yet.')
        self.assertContains(response, 'Edit profile')
        self.assertContains(response, 'Sign out')

class ViewPostPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.user
        )

    def get_url(self):
        return reverse('blog:view_post', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })

    def test_view_post_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/view_post.html')

    def test_view_post_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.story)
        self.assertContains(response, 'Edit post')
        self.assertContains(response, 'Delete post')
        self.assertContains(response, 'Responses: (0)')

class UpdatePostPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.user
        )

    def get_url(self):
        return reverse('blog:update_post', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })

    def test_update_post(self):
        data = {
            'title': 'new title',
            'story': 'new story'
        }

        response = self.client.post(self.get_url(), data)
        updated_post = Post.objects.get(id=self.post.id)

        self.assertEqual(updated_post.title, data.get('title'))
        self.assertRedirects(response, reverse('blog:view_post', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        }))

    def test_update_post_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/new_story.html')

    def test_update_post_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.story)
        self.assertContains(response, 'Update')

class UpdateProfilePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')

    def get_url(self):
        return reverse('blog:update_profile', kwargs={
            'username': self.user.username
        })

    def test_update_profile(self):
        response = self.client.post(self.get_url(), {
            'bio': 'new bio'
        })
        updated_user = User.objects.get(id=self.user.id)

        self.assertRedirects(response, reverse('blog:profile', kwargs={
            'username': self.user.username
        }))
        self.assertEqual(updated_user.bio, 'new bio')

    def test_update_profile_page_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, 'blog/update_profile.html')

    def test_update_profile_page_content(self):
        response = self.client.get(self.get_url())

        self.assertContains(response, 'Minium')
        self.assertContains(response, 'Profile information')
        self.assertContains(response, 'Short bio')
        self.assertContains(response, 'Cancel')
        self.assertContains(response, 'Save changes')

class SearchPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.second_user = User.objects.create_user(
            email='second@email.com',
            username='username for python and django',
            password='password'
        )

        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='python',
            story='story',
            author=self.user
        )

    @staticmethod
    def get_url(category):
        return reverse('blog:search', kwargs={
            'category': category
        })

    def test_search_posts(self):
        response = self.client.get(self.get_url('posts'), {
            'q': 'python and django'
        })

        self.assertContains(response, 'python and django')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.story)

    def test_search_users(self):
        response = self.client.get(self.get_url('users'), {
            'q': 'python and django'
        })

        self.assertContains(response, 'python and django')
        self.assertContains(response, self.second_user.username)
        self.assertContains(response, 'Follow')

    def test_search_page_template(self):
        response = self.client.get(self.get_url('posts'), {
            'q': 'python and django'
        })
        self.assertTemplateUsed(response, 'blog/search.html')

    def test_search_page_content(self):
        response = self.client.get(self.get_url('posts'), {
            'q': 'python and django'
        })

        self.assertContains(response, 'Minium')
        self.assertContains(response, 'Results for')
        self.assertContains(response, 'python and django')
        self.assertContains(response, 'Stories')
        self.assertContains(response, 'People')
        self.assertContains(response, 'Make sure all words are spelled correctly.')
        self.assertContains(response, 'Try different keywords.')
        self.assertContains(response, 'Try more general keywords.')

class DeletePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.user
        )

    def test_delete_post(self):
        response = self.client.post(reverse('blog:delete_post', kwargs={
            'post_id': self.post.id
        }))

        self.assertRedirects(response, reverse('blog:profile', kwargs={
            'username': self.user.username
        }))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

class CommentPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.second_user = User.objects.create_user(
            email='second@email.com',
            username='second username',
            password='password'
        )

        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.second_user
        )

    def test_comment_post(self):
        response = self.client.post(reverse('blog:comment_post', kwargs={
            'username': self.second_user.username,
            'post_id': self.post.id
        }), {
            'comment': 'python is amazing'
        })

        self.assertRedirects(response, reverse('blog:view_post', kwargs={
            'username': self.second_user.username,
            'post_id': self.post.id
        }))
        self.assertTrue(Comment.objects.filter(post=self.post).exists())

        response = self.client.get(reverse('blog:view_post', kwargs={
            'username': self.second_user.username,
            'post_id': self.post.id
        }))

        self.assertContains(response, self.user.username)
        self.assertContains(response, 'python is amazing')

class ToggleLikePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.second_user = User.objects.create_user(
            email='second@email.com',
            username='second username',
            password='password'
        )

        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.second_user
        )

    def get_url(self, url):
        return reverse(url, kwargs={
            'username': self.second_user.username,
            'post_id': self.post.id
        })

    def test_toggle_like_post(self):
        self.assertEqual(self.post.likes.all().count(), 0)

        response = self.client.post(self.get_url('blog:like_post'))

        self.assertRedirects(response, self.get_url('blog:view_post'))
        self.assertEqual(self.post.likes.all().count(), 1)

        response = self.client.post(self.get_url('blog:like_post'))
        self.assertRedirects(response, self.get_url('blog:view_post'))
        self.assertEqual(self.post.likes.all().count(), 0)

class ToggleFollowUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email.com',
            username='username',
            password='password'
        )
        self.second_user = User.objects.create_user(
            email='second@email.com',
            username='second username',
            password='password'
        )

        self.client.login(email=self.user.email, password='password')
        self.post = Post.objects.create(
            title='title',
            story='story',
            author=self.second_user
        )

    def get_follow_url(self, category, q=None):
        return reverse('blog:follow_user', kwargs={
            'username': self.second_user.username,
            'category': category,
            'q': q
        })

    def get_profile_url(self):
        return reverse('blog:profile', kwargs={
            'username': self.second_user.username
        })

    def test_toggle_follow_user_by_profile_page(self):
        self.assertFalse(self.user.is_following(self.second_user))

        response = self.client.post(self.get_follow_url('profile'))

        self.assertTrue(self.user.is_following(self.second_user))
        self.assertRedirects(response, self.get_profile_url())

        response = self.client.post(self.get_follow_url('profile'))

        self.assertFalse(self.user.is_following(self.second_user))
        self.assertRedirects(response, self.get_profile_url())

    def test_toggle_follow_user_by_search_page(self):
        self.assertFalse(self.user.is_following(self.second_user))

        self.client.post(self.get_follow_url('users', 'second username'))
        self.assertTrue(self.user.is_following(self.second_user))

        self.client.post(self.get_follow_url('users', 'second username'))
        self.assertFalse(self.user.is_following(self.second_user))
