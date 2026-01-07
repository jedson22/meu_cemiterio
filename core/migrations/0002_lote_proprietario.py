from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='proprietario',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Comprador'),
        ),
    ]
