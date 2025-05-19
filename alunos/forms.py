from django import forms
from django.forms import inlineformset_factory
from .models import Aluno, Faixa, Questao, Avaliacao, RespostaAvaliacao, Turma, EventoExame
from datetime import date
from django.utils import timezone

TAMANHO_FAIXA_CHOICES = [
    ("2,00M", "M000 - 2,00M"),
    ("2,15M", "M00/M0 - 2,15M"),
    ("2,30M", "M1/M2 - 2,30M"),
    ("2,60M", "M3 - 2,60M"),
    ("2,80M", "A1 - 2,80M"),
    ("3,00M", "A2 - 3,00M"),
    ("3,20M", "A3 - 3,20M"),
    ("3,40M", "A4 - 3,40M"),
]

class AlunoForm(forms.ModelForm):
    tamanho_faixa = forms.ChoiceField(choices=TAMANHO_FAIXA_CHOICES, required=False, label="Tamanho da Faixa")
    turma = forms.ModelChoiceField(queryset=Turma.objects.all(), required=False, label="Turma", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Aluno
        fields = ['nome_completo', 'nome_bordado', 'faixa_atual', 'faixa_proxima', 'tamanho_faixa', 'telefone', 'email', 'turma']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_bordado': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Todas as faixas para faixa_atual
        self.fields['faixa_atual'].queryset = Faixa.objects.all().order_by('ordem')
        self.fields['faixa_atual'].widget.attrs['class'] = 'form-control'
        
        # Todas as faixas exceto Branca para faixa_proxima
        self.fields['faixa_proxima'].queryset = Faixa.objects.exclude(nome__icontains='Branca').order_by('ordem')
        self.fields['faixa_proxima'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        nome_completo = cleaned_data.get('nome_completo')
        email = cleaned_data.get('email')

        if nome_completo:
            if Aluno.objects.filter(nome_completo=nome_completo).exclude(pk=self.instance.pk if self.instance else None).exists():
                self.add_error('nome_completo', 'Já existe um aluno cadastrado com este nome completo.')

        if email:
            if Aluno.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
                self.add_error('email', 'Já existe um aluno cadastrado com este e-mail.')

        return cleaned_data

class FaixaForm(forms.ModelForm):
    class Meta:
        model = Faixa
        fields = ['nome', 'ordem', 'preco', 'descricao', 'programa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'programa': forms.FileInput(attrs={'class': 'form-control'}),
        }

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['faixa', 'texto', 'natureza']
        widgets = {
            'faixa': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'natureza': forms.Select(attrs={'class': 'form-control'}),
        }

class AvaliacaoForm(forms.ModelForm):
    faixa_atual = forms.ModelChoiceField(queryset=Faixa.objects.all().order_by('ordem'), label='Faixa Atual', disabled=True)
    class Meta:
        model = Avaliacao
        fields = ['data', 'faixa_atual', 'faixa_proxima', 'avaliador', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'avaliador': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        aluno = kwargs.pop('aluno', None)
        super().__init__(*args, **kwargs)
        self.fields['data'].initial = timezone.now().date()
        if aluno:
            self.fields['faixa_atual'].initial = aluno.faixa_atual
            # Busca todas as faixas ordenadas
            faixas_ordenadas = list(Faixa.objects.all().order_by('ordem'))
            # Identifica a próxima faixa pela ordem
            try:
                idx_atual = faixas_ordenadas.index(aluno.faixa_atual)
                proxima = faixas_ordenadas[idx_atual + 1] if idx_atual + 1 < len(faixas_ordenadas) else None
            except ValueError:
                proxima = None
            # Exclui qualquer faixa com 'preta' no nome, exceto se ela for a próxima
            faixas_validas = [f for f in faixas_ordenadas if 'preta' not in f.nome.lower() or (proxima and f == proxima)]
            # Remove a faixa atual da lista
            faixas_validas = [f for f in faixas_validas if f != aluno.faixa_atual]
            self.fields['faixa_proxima'].queryset = Faixa.objects.filter(id__in=[f.id for f in faixas_validas]).order_by('ordem')
            if proxima:
                self.fields['faixa_proxima'].initial = proxima

class RespostaAvaliacaoForm(forms.ModelForm):
    class Meta:
        model = RespostaAvaliacao
        fields = ['conceito', 'observacao']
        widgets = {
            'conceito': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questao = getattr(self.instance, 'questao', None)
        if questao:
            if questao.natureza in ['teorica', 'filosofica']:
                self.fields['conceito'].choices = [
                    (1, 'Certo'),
                    (0, 'Errado'),
                ]
            else:
                self.fields['conceito'].choices = [
                    (0, 'Necessário desenvolvimento'),
                    (1, 'Regular'),
                    (2, 'Bom'),
                    (3, 'Muito Bom'),
                    (4, 'Excelente'),
                ]

# Formset para respostas de avaliação
RespostaAvaliacaoFormSet = inlineformset_factory(
    Avaliacao,
    RespostaAvaliacao,
    form=RespostaAvaliacaoForm,
    extra=0,
    can_delete=False,
)

class InscricaoExameForm(forms.ModelForm):
    responsavel = forms.CharField(label="Nome do Responsável", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    comprovante_pagamento = forms.FileField(label="Comprovante de Pagamento", required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    tamanho_faixa = forms.ChoiceField(choices=TAMANHO_FAIXA_CHOICES, required=False, label="Tamanho da Faixa")
    turma = forms.ModelChoiceField(queryset=Turma.objects.all(), required=False, label="Turma", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Aluno
        fields = ['nome_completo', 'nome_bordado', 'faixa_atual', 'faixa_proxima', 'tamanho_faixa', 'telefone', 'email', 'turma']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_bordado': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'dias', 'horarios']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'dias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segunda, Quarta, Sexta'}),
            'horarios': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 18:00 - 19:30'}),
        }

class EventoExameForm(forms.ModelForm):
    class Meta:
        model = EventoExame
        fields = ['nome', 'data', 'requisitos']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 