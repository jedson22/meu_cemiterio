from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Quadra(models.Model):
    numero = models.IntegerField(unique=True)
    class Meta: ordering = ['numero']
    def __str__(self): return f"Quadra {self.numero}"

class Lote(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='lotes')
    numero = models.IntegerField()
    proprietario = models.CharField(max_length=200, blank=True, null=True, verbose_name="Comprador")

    class Meta: 
        unique_together = ('quadra', 'numero')
        ordering = ['numero']
    
    def __str__(self): return f"Q{self.quadra.numero}-L{self.numero}"

    @property
    def esta_cheio(self):
        # OTIMIZAÇÃO: Usa a lista já carregada na memória (prefetch)
        # em vez de fazer .count() no banco de dados
        gavetas_lista = list(self.gavetas.all())
        total = len(gavetas_lista)
        
        if total == 0:
            return False
            
        ocupadas = sum(1 for g in gavetas_lista if g.status == 'Ocupado')
        return total == ocupadas

class Gaveta(models.Model):
    STATUS = [('Livre','Livre'), ('Ocupado','Ocupado')]
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='gavetas')
    numero = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='Livre')
    nome = models.CharField(max_length=200, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    
    class Meta: 
        unique_together = ('lote', 'numero')
        ordering = ['numero']

    @property
    def situacao_exumacao(self):
        if not self.data: return True, "Vazio"
        hoje = date.today()
        libera = self.data + timedelta(days=730) 
        if hoje >= libera: return True, "✅ Exumação Autorizada"
        return False, f"⛔ Bloqueado até {libera.strftime('%d/%m/%Y')}"
