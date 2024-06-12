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



def home(request):
    data = {}
    data['empresas'] = empresa.objects.all()
    return render(request, 'reviews/home.html', data)


@login_required
def detalhes(request, pk):
    data = {}
    empresa_obj = empresa.objects.get(pk=pk)
    data['empresa'] = empresa_obj
    reviews = empresa_obj.reviews.all().order_by('-data')
    data['reviews'] = reviews
    
    # Add a 'is_new' attribute to each review
    now = timezone.now()
    for review in reviews:
        review.recente = (now - review.data) < timedelta(minutes=5)
    
    return render(request, 'reviews/detalhes.html', data)




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
            # Redirecionar de volta para a página de detalhes após adicionar a avaliação
            return redirect('url_detalhes', pk=pk)

    return redirect('url_detalhes', pk=pk)


def deletarReview(request, pk):
    reviewAtual = review.objects.get(pk=pk)
    reviewAtual.delete()
    return redirect('url_detalhes', pk=reviewAtual.empresa.pk)
