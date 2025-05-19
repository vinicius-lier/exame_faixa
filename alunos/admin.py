from django.contrib import admin
from .models import Aluno, Faixa, Questao, Avaliacao, RespostaAvaliacao, Certificado

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'nome_bordado', 'faixa_atual', 'faixa_proxima', 'data_inscricao')
    list_filter = ('faixa_atual', 'faixa_proxima')
    search_fields = ('nome_completo', 'nome_bordado', 'email')

@admin.register(Faixa)
class FaixaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'preco', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('nome',)
    ordering = ('ordem',)

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('texto', 'faixa', 'natureza')
    list_filter = ('faixa', 'natureza')
    search_fields = ('texto',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data', 'faixa_atual', 'faixa_proxima', 'conceito']
    list_filter = ['data', 'faixa_atual', 'faixa_proxima', 'conceito']
    search_fields = ['aluno__nome_completo']
    date_hierarchy = 'data'

@admin.register(RespostaAvaliacao)
class RespostaAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('avaliacao', 'questao', 'conceito')
    list_filter = ('conceito',)
    search_fields = ('avaliacao__aluno__nome_completo', 'questao__texto')

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'avaliacao', 'data_emissao')
    list_filter = ('data_emissao',)
    search_fields = ('aluno__nome_completo',)
