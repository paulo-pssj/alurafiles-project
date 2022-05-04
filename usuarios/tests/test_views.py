from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TemplatesUsuariosTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            id=0,
            username='Teste',
            email='teste@email.com',
        )
        self.user.set_password('123999')
        self.user.save()

    def test_login_template_logado(self):
        """Teste se exibe template login para usuarios logados"""
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'usuarios/login.html')

    def test_cadastrados_template_logado(self):
        """Teste se exibe template cadastrados para usuarios logados"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('cadastrados'))
        self.assertTemplateUsed(response, 'usuarios/cadastrados.html')

    def test_editar_template_logado(self):
        """Teste se exibe template editar para usuarios logados"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('editar_usuarios', args=[0]))
        self.assertTemplateUsed(response, 'usuarios/editar.html')

    def test_register_template_logado(self):
        """Teste se exibe template register para usuarios logados"""
        self.client.post(
            reverse('login'),
            {'email': 'teste@email.com', 'senha': '123999'},
            format='text/html',
        )
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'usuarios/register.html')
