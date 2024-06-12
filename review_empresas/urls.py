
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from reviews.views import home, detalhes, adicionar_review, deletarReview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='url_home'),
    path('detalhes/<int:pk>',detalhes,name='url_detalhes'), 
    path('adicionar_review/<int:pk>/', adicionar_review, name='adicionar_review'),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('deletar/<int:pk>/',deletarReview, name= 'url_deletar'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)