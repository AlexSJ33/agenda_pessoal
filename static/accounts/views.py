# from cgitb import reset
# from os import execv
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha   = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request,user)
        messages.success(request, 'Você está logado.')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome         = request.POST.get('nome')
    sobrenome    = request.POST.get('sobrenome')
    email        = request.POST.get('email')
    usuario      = request.POST.get('usuario')
    senha        = request.POST.get('senha')
    repete_senha = request.POST.get('repete_senha')

    if not nome or not sobrenome or not email or not usuario or not senha or not repete_senha:
        messages.error(request, 'Favor, preencher todos os campos.')
        return render(request, 'accounts/cadastro.html')
    
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter 6 ou mais caracteres.')
        return render(request, 'accounts/cadastro.html')


    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter 6 ou mais caracteres.')
        return render(request, 'accounts/cadastro.html')

    if repete_senha != senha:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/cadastro.html')        


    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já cadastrado com outro usuario.')
        return render(request, 'accounts/cadastro.html')        


    messages.success(request,'Usuário registrado com sucesso')
    user = User.objects.create_user(username=usuario, email=email,password=senha,first_name=nome,last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name= 'login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Não foi possivel enviar o Formulário')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')
    if len(descricao) < 8:
        messages.error(request, 'O campo descricao precisar ter mais de 8 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} {request.POST.get("sobrenome")} salvo com sucesso!')
    return redirect('dashboard')