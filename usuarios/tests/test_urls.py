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

    def test_login_status_code_200(self):
        """Teste resposta status code 200 da página login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_status_code_302(self):
        """Teste resposta status code da página register"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_cadastrados_status_code_302(self):
        """teste resposta status code da página cadastrados"""
        response = self.client.get(reverse('cadastrados'))
        self.assertEqual(response.status_code, 302)

    def test_editar_status_code_302(self):
        """teste resposta status code da página editar"""
        response = self.client.get(reverse('editar_usuarios', args=[0]))
        self.assertEqual(response.status_code, 302)

    def test_deletar_status_code_302(self):
        """teste resposta status code da página deletar"""
        response = self.client.get(reverse('deletar', args=[0]))
        self.assertEqual(response.status_code, 302)

    def test_login_status_code_302(self):
        """Teste se redireciona para index"""
        response = self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['location'], '/')

    def test_editar_usuario_status_code_200(self):
        """teste retorno status code 200"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('editar_usuarios', args=[0]))
        self.assertEqual(response.status_code, 200)

    def test_cadastrados_status_code_200(self):
        """teste retorno status code 200"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('cadastrados'))
        self.assertEqual(response.status_code, 200)
