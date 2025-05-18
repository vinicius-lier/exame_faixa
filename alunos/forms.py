from django import forms
from django.forms import inlineformset_factory
from .models import Aluno, Faixa, Questao, Avaliacao, RespostaAvaliacao

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome_completo', 'nome_bordado', 'email', 'telefone', 'faixa_atual', 'faixa_proxima', 'tamanho_faixa']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_bordado': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'tamanho_faixa': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Todas as faixas para faixa_atual
        self.fields['faixa_atual'].queryset = Faixa.objects.all().order_by('ordem')
        self.fields['faixa_atual'].widget.attrs['class'] = 'form-control'
        
        # Todas as faixas exceto Branca para faixa_proxima
        self.fields['faixa_proxima'].queryset = Faixa.objects.exclude(nome__icontains='Branca').order_by('ordem')
        self.fields['faixa_proxima'].widget.attrs['class'] = 'form-control'

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
        fields = ['faixa', 'texto', 'tipo', 'peso', 'prioritaria']
        widgets = {
            'faixa': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'prioritaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['data', 'faixa_atual', 'faixa_proxima', 'conceito', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

class RespostaAvaliacaoForm(forms.ModelForm):
    class Meta:
        model = RespostaAvaliacao
        fields = ['conceito', 'observacao']
        widgets = {
            'conceito': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formset para respostas de avaliação
RespostaAvaliacaoFormSet = inlineformset_factory(
    Avaliacao,
    RespostaAvaliacao,
    form=RespostaAvaliacaoForm,
    extra=0,
    can_delete=False,
) 