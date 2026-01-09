from django.db import models
from datetime import date


class Quadra(models.Model):
    numero = models.IntegerField(unique=True)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Quadra {self.numero}"


class Lote(models.Model):
    quadra = models.ForeignKey(
        Quadra,
        related_name='lotes',
        on_delete=models.CASCADE
    )
    numero = models.IntegerField()
    proprietario = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Comprador'
    )

    class Meta:
        ordering = ['numero']
        unique_together = ('quadra', 'numero')

    def __str__(self):
        return f"Lote {self.numero} - Quadra {self.quadra.numero}"

    @property
    def esta_cheio(self):
        total = self.gavetas.count()
        if total == 0:
            return False
        ocupadas = self.gavetas.filter(status='Ocupado').count()
        return ocupadas == total


class Gaveta(models.Model):
    STATUS_CHOICES = (
        ('Livre', 'Livre'),
        ('Ocupado', 'Ocupado'),
    )

    lote = models.ForeignKey(
        Lote,
        related_name='gavetas',
        on_delete=models.CASCADE
    )
    numero = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Livre'
    )
    nome = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    data = models.DateField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['numero']
        unique_together = ('lote', 'numero')

    def __str__(self):
        return f"Gaveta {self.numero} - Lote {self.lote.numero}"

    @property
    def situacao_exumacao(self):
        """
        Regra:
        - Admin sempre pode exumar
        - Outros usuários só após 2 anos
        """
        if not self.data:
            return False, "Gaveta vazia"

        hoje = date.today()
        anos = hoje.year - self.data.year - (
            (hoje.month, hoje.day) < (self.data.month, self.data.day)
        )

        if anos >= 2:
            return True, "Exumação permitida"

        return False, f"Exumação permitida apenas após 2 anos ({anos}/2)"


class Produto(models.Model):
    CATEGORIA_CHOICES = (
        ('Urna', 'Urna Funerária'),
        ('Quimico', 'Produtos Químicos'),
        ('EPI', 'EPI / Proteção'),
        ('Outros', 'Outros'),
    )

    nome = models.CharField(max_length=100)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='Outros'
    )
    quantidade = models.IntegerField(default=0)
    minimo = models.IntegerField(
        default=5,
        verbose_name='Estoque Mínimo'
    )

    def __str__(self):
        return self.nome


class Historico(models.Model):
    gaveta = models.ForeignKey(
        Gaveta,
        related_name='historico',
        on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=200)
    data_falecimento = models.DateField(
        blank=True,
        null=True
    )
    data_exumacao = models.DateField(
        auto_now_add=True
    )
    observacao = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-data_exumacao']

    def __str__(self):
        return f"{self.nome} ({self.data_exumacao})"
