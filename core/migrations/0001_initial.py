from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        # 1. QUADRA
        migrations.CreateModel(
            name='Quadra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
            ],
            options={'ordering': ['numero']},
        ),
        # 2. PRODUTO (ESTOQUE)
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('Urna', 'Urna Funerária'), ('Quimico', 'Produtos Químicos'), ('EPI', 'EPI / Proteção'), ('Outros', 'Outros')], default='Outros', max_length=20)),
                ('quantidade', models.IntegerField(default=0)),
                ('minimo', models.IntegerField(default=5, verbose_name='Estoque Mínimo')),
            ],
        ),
        # 3. LOTE
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('proprietario', models.CharField(blank=True, max_length=200, null=True, verbose_name='Comprador')),
                ('quadra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lotes', to='core.quadra')),
            ],
            options={'ordering': ['numero'], 'unique_together': {('quadra', 'numero')}},
        ),
        # 4. GAVETA
        migrations.CreateModel(
            name='Gaveta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('status', models.CharField(choices=[('Livre', 'Livre'), ('Ocupado', 'Ocupado')], default='Livre', max_length=20)),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('data', models.DateField(blank=True, null=True)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gavetas', to='core.lote')),
            ],
            options={'ordering': ['numero'], 'unique_together': {('lote', 'numero')}},
        ),
        # 5. HISTÓRICO
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('data_falecimento', models.DateField(blank=True, null=True)),
                ('data_exumacao', models.DateField(auto_now_add=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('gaveta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico', to='core.gaveta')),
            ],
            options={'ordering': ['-data_exumacao']},
        ),
    ]
