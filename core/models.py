from django.db import models
from django.utils import timezone

class Quadra(models.Model):
    numero = models.IntegerField()
    def __str__(self):
        return f"Quadra {self.numero}"

class Lote(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    numero = models.IntegerField()
    def __str__(self):
        return f"Lote {self.numero} - Quadra {self.quadra.numero}"

class Gaveta(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    numero = models.IntegerField()
    def __str__(self):
        return f"Gaveta {self.numero} - {self.lote}"

class Falecido(models.Model):
    SITUACAO_CHOICES = [
        ('sepultado', 'Sepultado'),
        ('exumado', 'Exumado (Histórico)'),
    ]

    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField(null=True, blank=True)
    data_falecimento = models.DateField()
    gaveta = models.ForeignKey(Gaveta, on_delete=models.CASCADE, related_name='falecidos')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='sepultado')
    data_exumacao = models.DateField(null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
