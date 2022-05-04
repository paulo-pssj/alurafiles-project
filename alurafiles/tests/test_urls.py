from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            id=0,
            username='Teste',
            email='teste@email.com',
        )
        self.user.set_password('123999')
        self.user.save()

    def test_index_status_code_200(self):
        """Teste resposta status code 200 da página index"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_analise_status_code_200(self):
        """Teste resposta status code 200 da página analise"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('analise'))
        self.assertEqual(response.status_code, 200)

    def test_analise_suspeitos_status_code_302(self):
        """Teste resposta status code 200 da página analise suspeitos"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('analise_suspeitos'))
        self.assertEqual(response.status_code, 302)
