from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Faixa(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)
    programa = models.FileField(upload_to='programas/', null=True, blank=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['ordem']
        verbose_name = 'Faixa'
        verbose_name_plural = 'Faixas'

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=200)
    nome_bordado = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    faixa_atual = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='alunos_atual')
    faixa_proxima = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='alunos_proxima')
    tamanho_faixa = models.CharField(max_length=10)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome_completo

    class Meta:
        ordering = ['nome_completo']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

class Questao(models.Model):
    TIPO_CHOICES = [
        ('teorica', 'Teórica'),
        ('pratica', 'Prática'),
        ('kata', 'Kata'),
        ('randori', 'Randori'),
    ]
    
    faixa = models.ForeignKey(Faixa, on_delete=models.CASCADE, related_name='questoes')
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    peso = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    prioritaria = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.faixa} - {self.texto[:50]}"

    class Meta:
        ordering = ['faixa__ordem', 'texto']
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='avaliacoes')
    data = models.DateField(null=True, blank=True)
    faixa_atual = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='avaliacoes_atual', null=True, blank=True)
    faixa_proxima = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='avaliacoes_proxima', null=True, blank=True)
    conceito = models.ForeignKey('ConceitoAvaliacao', on_delete=models.PROTECT, null=True, blank=True)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avaliação de {self.aluno} em {self.data}"

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data']

class RespostaAvaliacao(models.Model):
    CONCEITOS = [
        (0, 'Não Atende'),
        (1, 'Atende Parcialmente'),
        (2, 'Atende'),
        (3, 'Supera'),
    ]
    
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='respostas')
    questao = models.ForeignKey(Questao, on_delete=models.PROTECT)
    conceito = models.IntegerField(choices=CONCEITOS, null=True, blank=True)
    observacao = models.TextField(blank=True)
    
    def __str__(self):
        return f"Resposta de {self.avaliacao.aluno} para {self.questao}"

    class Meta:
        ordering = ['questao__faixa__ordem', 'questao__texto']
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

class Certificado(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='certificados')
    avaliacao = models.OneToOneField(Avaliacao, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='certificados/', null=True, blank=True)
    
    def __str__(self):
        return f"Certificado de {self.aluno} - {self.data_emissao.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-data_emissao']
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

class ConceitoAvaliacao(models.Model):
    SIGLAS = [
        ('ND', 'Necessário Desenvolvimento'),
        ('R', 'Regular'),
        ('B', 'Bom'),
        ('MB', 'Muito Bom'),
        ('E', 'Excelente'),
    ]
    
    sigla = models.CharField(max_length=2, choices=SIGLAS, unique=True)
    descricao = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.sigla} - {self.descricao}"
    
    class Meta:
        verbose_name = 'Conceito de Avaliação'
        verbose_name_plural = 'Conceitos de Avaliação'
