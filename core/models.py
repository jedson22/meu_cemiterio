from django.db import models
from datetime import date, timedelta

class Quadra(models.Model):
    numero = models.IntegerField(unique=True)
    def __str__(self): return f"Quadra {self.numero}"

class Lote(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='lotes')
    numero = models.IntegerField()
    proprietario = models.CharField(max_length=200, blank=True, null=True, verbose_name="Comprador")

    class Meta: 
        unique_together = ('quadra', 'numero')
        ordering = ['numero']
    
    def __str__(self): return f"Q{self.quadra.numero}-L{self.numero}"

class Gaveta(models.Model):
    STATUS = [('Livre','Livre'), ('Ocupado','Ocupado')]
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='gavetas')
    numero = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='Livre')
    nome = models.CharField(max_length=200, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    
    class Meta: unique_together = ('lote', 'numero')

    @property
    def situacao_exumacao(self):
        """Retorna (Pode Exumar?, Texto Explicativo)"""
        if not self.data:
            return True, "Vazio"
        
        # Regra: 3 anos (1095 dias) para exumação
        hoje = date.today()
        data_liberacao = self.data + timedelta(days=1095) # 3 anos
        
        if hoje >= data_liberacao:
            return True, "✅ Exumação Autorizada"
        else:
            return False, f"⛔ Bloqueado até {data_liberacao.strftime('%d/%m/%Y')}"
