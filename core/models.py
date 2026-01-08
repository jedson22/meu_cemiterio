from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# --- MODELOS DO CEMITÉRIO ---

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
        ordering = ['numero'] # Garante ordem 1, 2, 3...
    
    def __str__(self): return f"Q{self.quadra.numero}-L{self.numero}"

    @property
    def esta_cheio(self):
        # Otimização de memória
        gavetas_lista = list(self.gavetas.all())
        total = len(gavetas_lista)
        if total == 0: return False
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
        # Regra de 2 anos (730 dias)
        libera = self.data + timedelta(days=730) 
        if hoje >= libera: return True, "✅ Exumação Autorizada"
        return False, f"⛔ Bloqueado até {libera.strftime('%d/%m/%Y')}"

class Historico(models.Model):
    gaveta = models.ForeignKey(Gaveta, on_delete=models.CASCADE, related_name='historico')
    nome = models.CharField(max_length=200)
    data_falecimento = models.DateField(blank=True, null=True)
    data_exumacao = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta: ordering = ['-data_exumacao']

# --- ESTOQUE ---

class Produto(models.Model):
    CATEGORIAS = [
        ('Urna', 'Urna Funerária'),
        ('Quimico', 'Produtos Químicos'),
        ('EPI', 'EPI / Proteção'),
        ('Outros', 'Outros'),
    ]
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='Outros')
    quantidade = models.IntegerField(default=0)
    minimo = models.IntegerField(default=5, verbose_name="Estoque Mínimo")

    def __str__(self): return self.nome
    
    @property
    def alerta_baixo(self):
        return self.quantidade <= self.minimo
