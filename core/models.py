from django.db import models
from datetime import date, timedelta

class Quadra(models.Model):
    numero = models.IntegerField(unique=True)
    
    class Meta:
        ordering = ['numero'] # Garante ordem das quadras
        
    def __str__(self): return f"Quadra {self.numero}"

class Lote(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='lotes')
    numero = models.IntegerField()
    proprietario = models.CharField(max_length=200, blank=True, null=True, verbose_name="Comprador")

    class Meta: 
        unique_together = ('quadra', 'numero')
        ordering = ['numero'] # <--- ISSO CONSERTA A ORDEM DOS LOTES (1, 2, 3...)
    
    def __str__(self): return f"Q{self.quadra.numero}-L{self.numero}"

    @property
    def esta_cheio(self):
        """Verifica se todas as gavetas estão ocupadas"""
        total = self.gavetas.count()
        ocupadas = self.gavetas.filter(status='Ocupado').count()
        # Só está cheio se tiver gavetas e todas estiverem ocupadas
        return total > 0 and total == ocupadas

class Gaveta(models.Model):
    STATUS = [('Livre','Livre'), ('Ocupado','Ocupado')]
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='gavetas')
    numero = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='Livre')
    nome = models.CharField(max_length=200, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    
    class Meta: 
        unique_together = ('lote', 'numero')
        ordering = ['numero'] # Garante ordem das gavetas

    @property
    def situacao_exumacao(self):
        if not self.data: return True, "Vazio"
        hoje = date.today()
        # Bloqueio de 3 anos (1095 dias)
        libera = self.data + timedelta(days=1095)
        if hoje >= libera: return True, "✅ Exumação Autorizada"
        return False, f"⛔ Bloqueado até {libera.strftime('%d/%m/%Y')}"
