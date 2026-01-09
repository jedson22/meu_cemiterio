from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quadra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
            ],
            options={'ordering': ['numero']},
        ),
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
    ]
