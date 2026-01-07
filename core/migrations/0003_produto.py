from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_lote_proprietario'),
    ]

    operations = [
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
    ]
