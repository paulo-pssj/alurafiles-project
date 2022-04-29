from random import randint

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User, UserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from alurafiles.views import index


def register(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome = request.POST['nome']
            number = randint(0, 10000)
            username = nome.split()[0] + str(number)
            first_name = nome.split(' ', 1)[0]
            last_name = nome.split(' ', 1)[1]
            email = request.POST['email']

            if campo_vazio(nome):
                messages.error(
                    request, 'O campo nome não pode ficar em branco'
                )
                return redirect('register')
            if campo_vazio(email):
                messages.error(
                    request, 'O campo nome não pode ficar em branco'
                )
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Usuário já cadastrado')
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário já cadastrado')
                return redirect('register')

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            password = UserManager.make_random_password(
                user, length=6, allowed_chars='0123456789'
            )
            user.set_password(password)
            user.save()
            send_mail(
                'Senha Alura Files',
                f'Senha: {password}',
                settings.EMAIL_HOST_USER,
                [email],
            )
            messages.success(request, 'Registro realizado com sucesso.')
            return redirect('login')

        return render(request, 'usuarios/register.html')
    else:
        return redirect(index)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(
                request, 'Os campos email e senha não podem ficar em branco'
            )
            return redirect('login')
        if User.objects.filter(email=email).exists():
            email = (
                User.objects.filter(email=email)
                .values_list('username', flat=True)
                .get()
            )
            user = auth.authenticate(username=email, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect(index)
    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def usuarios_cadastrados(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_active=True).all()
        context = {'users': users}
        return render(request, 'usuarios/cadastrados.html', context=context)
    else:
        return render(request, 'usuarios/login.html')


def editar_usuarios(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        context = {'user': user}
        return render(request, 'usuarios/editar.html', context)
    else:
        return redirect(index)


def deletar(request, user_id):
    if request.user.is_authenticated:
        user_delete = get_object_or_404(User, pk=user_id)
        if request.user.username not in user_delete.username:
            user_delete.is_active = False
            user_delete.save()
            messages.success(request, 'Usuário deletado com sucesso.')
            return redirect('cadastrados')

        messages.error(request, 'Seu usuário não pode ser deletado.')
        return redirect('cadastrados')
    else:
        return redirect(index)


def campo_vazio(campo):
    return not campo.strip()


def atualiza_usuarios(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        u = User.objects.get(pk=user_id)
        u.first_name = request.POST['nome'].split(' ', 1)[0]
        u.last_name = request.POST['nome'].split(' ', 1)[1]
        u.email = request.POST['email']
        u.save()
        return redirect('cadastrados')
