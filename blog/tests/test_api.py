from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post

class PostAPITest(APITestCase):
    def setUp(self):
        self.list_url = reverse('post-list')
        self.sample_data = {
            'title': 'Teszt cím',
            'body': 'Ez egy teszt body.',
        }

    def test_create_post(self):
        """POST /api/posts/ → 201 + adatbázisban új rekord"""
        resp = self.client.post(self.list_url, self.sample_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, self.sample_data['title'])

    def test_list_posts(self):
        """GET /api/posts/ → 200 + listában visszakapjuk a posztot"""
        Post.objects.create(**self.sample_data)
        resp = self.client.get(self.list_url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], self.sample_data['title'])

    def test_update_post(self):
        """PUT /api/posts/{id}/ → 200 + rekord frissül"""
        post = Post.objects.create(**self.sample_data)
        detail_url = reverse('post-detail', args=[post.pk])
        new_data = {'title': 'Frissített cím', 'body': 'Új body szöveg.'}
        resp = self.client.put(detail_url, new_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, new_data['title'])

    def test_delete_post(self):
        """DELETE /api/posts/{id}/ → 204 + rekord törlődik"""
        post = Post.objects.create(**self.sample_data)
        detail_url = reverse('post-detail', args=[post.pk])
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
