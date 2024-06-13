from django.shortcuts import render,redirect
from .models import empresa,review
from .forms import ReviewForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy


#Função que redireciona para pagina principal e carrega seus dados
@login_required
def home(request):
    data = {}
    data['empresas'] = empresa.objects.all()
    return render(request, 'reviews/home.html', data)


#Função que redireciona para pagina de detalhes e carrega seus dados
@login_required
def detalhes(request, pk):
    data = {}
    empresa_obj = empresa.objects.get(pk=pk)
    data['empresa'] = empresa_obj
    reviews = empresa_obj.reviews.all().order_by('-data')
    data['reviews'] = reviews
    data['estrelas'] = range(5)
    
    #Função para colocar tag "Novo comentario" para novas reviews
    now = timezone.now()
    for review in reviews:
        review.recente = (now - review.data) < timedelta(minutes=5)
    
    return render(request, 'reviews/detalhes.html', data)



#Função para adicionar uma review a uma empresa
@csrf_protect
@login_required
def adicionar_review(request, pk):
    if request.method == 'POST':
        try:
            empresa_obj = empresa.objects.get(pk=pk)
        except empresa.DoesNotExist:
            return redirect('url_detalhes', pk=pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            novo_review = form.save(commit=False)
            novo_review.empresa = empresa_obj
            novo_review.usuario = request.user
            novo_review.save()
            return redirect('url_detalhes', pk=pk)

    return redirect('url_detalhes', pk=pk)


#Função que permite que reviews sejam deletadas
def deletarReview(request, pk):
    reviewAtual = review.objects.get(pk=pk)
    reviewAtual.delete()
    return redirect('url_detalhes', pk=reviewAtual.empresa.pk)
