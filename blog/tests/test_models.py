from django.test import TestCase
from django.utils import timezone
from blog.models import Post, Comment

class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Model Teszt',
            body='Model teszt body.',
            published_at=timezone.now()
        )

    def test_str_method(self):
        """__str__ visszaadja a címet"""
        self.assertEqual(str(self.post), 'Model Teszt')

    def test_create_and_count(self):
        """Objektum létrejön, count() növekszik"""
        self.assertEqual(Post.objects.count(), 1)

    def test_update(self):
        """Frissítés után az új cím mentődik"""
        self.post.title = 'Új cím'
        self.post.save()
        self.assertEqual(Post.objects.get(pk=self.post.pk).title, 'Új cím')

    def test_delete(self):
        """Törlés után a rekord nem létezik"""
        pk = self.post.pk
        self.post.delete()
        self.assertFalse(Post.objects.filter(pk=pk).exists())


class CommentModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Cikk',
            body='Valami szöveg.',
            published_at=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author='Alice',
            text='Szuper cikk!'
        )

    def test_str_method(self):
        """__str__ visszaadja 'Comment by {author}' formátumot"""
        self.assertEqual(str(self.comment), 'Comment by Alice')

    def test_comment_creation(self):
        """Egy új komment jön létre"""
        self.assertEqual(Comment.objects.count(), 1)

    def test_invalid_comment(self):
        """Hiányzó mező esetén kivétel dobódik"""
        with self.assertRaises(Exception):
            Comment.objects.create(post=None, author='', text='')
