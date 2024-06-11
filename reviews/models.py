from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class empresa(models.Model):
    empresa = models.CharField(max_length=40)
    descricao = models.TextField()
    foto_empresa = models.ImageField(upload_to='fotos/')
    
    def __str__(self):
       return self.empresa

    @property    
    def media_avaliacoes(self):
        reviews = self.reviews.all()
        if reviews.exists():
            media = reviews.aggregate(models.Avg('avaliacao'))['avaliacao__avg']
            return round(media, 2)
        return 0.0

   
class review(models.Model):
    empresa = models.ForeignKey(empresa, related_name='reviews', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    avaliacao = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

        
    def __str__(self):
        return f'Review de {self.usuario.username} para {self.empresa.empresa}'
    