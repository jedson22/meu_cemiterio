from django.db import models
from django.utils import timezone

# --- PARTE DO CEMITÉRIO ---
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
        ('exumado', 'Exumado (Ossário)'),
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

# --- PARTE DO ESTOQUE (NOVO) ---
class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('urna_bronze', 'Urna Bronze'),
        ('urna_prata', 'Urna Prata'),
        ('urna_ouro', 'Urna Ouro'),
        ('quimico', 'Produto Químico (Formol/Outros)'),
        ('diversos', 'Diversos'),
    ]
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    quantidade = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"

class Historico(models.Model):
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.acao}"
