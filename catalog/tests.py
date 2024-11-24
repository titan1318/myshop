from django.urls import reverse
from .models import Product, Category, BlogPost, Version
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from catalog.services import get_categories
from django.core.cache import cache

User = get_user_model()


class ProductPermissionsTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Создаем владельца
        self.owner = User.objects.create_user(
            email='owner@test.com',
            password='password123',
            username='owner_user'
        )

        # Создаем другого пользователя
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='password123',
            username='other_user'
        )

        # Создаем категорию и продукт
        self.category = Category.objects.create(name='Категория', description='Описание')
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=1000,
            category=self.category,
            owner=self.owner,
            is_published=True
        )

        # Создаем модераторскую группу и пользователя-модератора
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='password123',
            username='moderator_user'
        )

        self.moderator_group = Group.objects.create(name='Модераторы')
        permissions = Permission.objects.filter(codename__in=[
            'can_change_any_description',
            'can_change_any_category'
        ])
        self.moderator_group.permissions.set(permissions)
        self.moderator.groups.add(self.moderator_group)

    def test_owner_can_edit_product(self):
        self.client.login(email='owner@test.com', password='password123')
        response = self.client.get(reverse('catalog:update_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit_product(self):
        self.client.login(email='other@test.com', password='password123')
        response = self.client.get(reverse('catalog:update_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 403)

    def test_moderator_can_edit_any_product(self):
        self.client.login(email='moderator@test.com', password='password123')
        response = self.client.get(reverse('catalog:update_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_delete_product(self):
        self.client.login(email='owner@test.com', password='password123')
        response = self.client.post(reverse('catalog:delete_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)


class CategoryServiceTests(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        Category.objects.create(name='Категория 1', description='Описание 1')
        Category.objects.create(name='Категория 2', description='Описание 2')

    def test_get_categories_caching(self):
        cache.clear()
        categories = get_categories()
        self.assertEqual(len(categories), 2)
        Category.objects.all().delete()
        cached_categories = get_categories()
        self.assertEqual(len(cached_categories), 2)

    def test_product_detail_view(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_category_list_view(self):
        response = self.client.get(reverse('catalog:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_category_list_caching(self):
        # Ensure cache is clear
        cache.clear()

        # Access category list view and cache data
        response = self.client.get(reverse('catalog:category_list'))
        self.assertEqual(response.status_code, 200)

        # Add a new category after the cache is populated
        Category.objects.create(name='New Category', description='New Description')

        # Fetch from the view again; data should come from cache
        cached_response = self.client.get(reverse('catalog:category_list'))
        self.assertNotContains(cached_response, 'New Category')

        # Clear the cache and fetch again; new category should appear
        cache.clear()
        updated_response = self.client.get(reverse('catalog:category_list'))
        self.assertContains(updated_response, 'New Category')


class BlogPostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='Test Blog Content',
            is_published=True
        )

    def test_blog_post_detail_view(self):
        response = self.client.get(reverse('catalog:blogpost_detail', args=[self.blog_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog_post.title)

    def test_blog_post_list_view(self):
        response = self.client.get(reverse('catalog:blogpost_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog_post.title)


class VersionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Product with Version',
            description='Product Description',
            price=200.00,
            category=Category.objects.create(name='Category for Versions'),
            owner=User.objects.create_user(
                username='owner_with_version',
                email='owner_with_version@test.com',
                password='password123'
            )
        )
        self.version = Version.objects.create(
            product=self.product,
            version_number='1.0',
            version_name='Initial Version',
            is_current=True
        )

    def test_version_creation(self):
        self.assertEqual(self.version.version_number, '1.0')
        self.assertTrue(self.version.is_current)

    def test_version_list_in_product_detail(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.version.version_name)
