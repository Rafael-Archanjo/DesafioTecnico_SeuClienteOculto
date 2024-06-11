from django.contrib import admin
from .models import empresa, review


@admin.register(empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'descricao', 'media_avaliacoes')  # Mostrar a média das avaliações no admin

@admin.register(review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'usuario', 'avaliacao', 'data')