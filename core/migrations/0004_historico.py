from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_produto'),
    ]

    operations = [
        # 1. Cria a Tabela de Histórico
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
            options={
                'ordering': ['-data_exumacao'],
            },
        ),
        # 2. Arruma a ordem dos Lotes (1, 2, 3...)
        migrations.AlterModelOptions(
            name='lote',
            options={'ordering': ['numero']},
        ),
    ]
