# Generated by Django 5.2.1 on 2025-05-19 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questao',
            name='categoria',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='questao',
            name='descricao_execucao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questao',
            name='pontuacao',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='questao',
            name='prioritaria',
            field=models.BooleanField(default=False),
        ),
    ]
