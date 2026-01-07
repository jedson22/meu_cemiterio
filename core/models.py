from django.db import models
from datetime import datetime, timedelta

class Quadra(models.Model):
    numero = models.IntegerField(unique=True)
    def __str__(self): return f"Quadra {self.numero}"

class Lote(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='lotes')
    numero = models.IntegerField()
    # NOVO CAMPO: Aqui salvamos quem comprou o lote inteiro
    proprietario = models.CharField(max_length=200, blank=True, null=True, verbose_name="Comprador")

    class Meta: 
        unique_together = ('quadra', 'numero')
    
    def __str__(self): 
        return f"Q{self.quadra.numero}-L{self.numero}"

class Gaveta(models.Model):
    STATUS = [('Livre','Livre'), ('Ocupado','Ocupado'), ('Vendido','Vendido')]
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='gavetas')
    numero = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='Livre')
    nome = models.CharField(max_length=200, blank=True, null=True) # Nome do falecido
    data = models.DateField(blank=True, null=True)
    
    class Meta: 
        unique_together = ('lote', 'numero')
        
    def situacao(self):
        if self.status == 'Livre': return "LIVRE", "success", ""
        if self.status == 'Vendido': return "VENDIDO", "info", "Proprietário"
        if self.data:
            libera_em = self.data + timedelta(days=730)
            if datetime.now().date() >= libera_em: return "PODE EXUMAR", "danger", "Prazo Vencido!"
            return "OCUPADO", "warning", f"Libera em {libera_em.strftime('%d/%m/%Y')}"
        return "OCUPADO", "warning", "Sem Data"
