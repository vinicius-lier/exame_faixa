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
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    faixa_atual = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='alunos_atual')
    faixa_proxima = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='alunos_proxima')
    tamanho_faixa = models.CharField(max_length=10)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey('Turma', on_delete=models.PROTECT, related_name='alunos', null=True, blank=True)
    
    def __str__(self):
        return self.nome_completo

    class Meta:
        ordering = ['nome_completo']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        constraints = [
            models.UniqueConstraint(
                fields=['nome_completo'],
                name='unique_aluno_nome_completo'
            )
        ]

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    dias = models.CharField(max_length=100, blank=True)
    horarios = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.nome

class EventoExame(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    requisitos = models.TextField()
    def __str__(self):
        return f"{self.nome} - {self.data}" 

class Questao(models.Model):
    NATUREZA_CHOICES = [
        ('tecnica', 'Técnica'),
        ('historia', 'História'),
        ('regras', 'Regras'),
        ('filosofia', 'Filosofia'),
        ('etica', 'Ética'),
    ]

    texto = models.TextField()
    faixa = models.ForeignKey(Faixa, on_delete=models.CASCADE)
    natureza = models.CharField(max_length=20, choices=NATUREZA_CHOICES)
    pontuacao = models.CharField(max_length=20, blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    prioritaria = models.BooleanField(default=False)
    descricao_execucao = models.TextField(blank=True, null=True)
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faixa} - {self.natureza}"

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['faixa', 'natureza']

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='avaliacoes')
    data = models.DateField(null=True, blank=True)
    faixa_atual = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='avaliacoes_atual', null=True, blank=True)
    faixa_proxima = models.ForeignKey(Faixa, on_delete=models.PROTECT, related_name='avaliacoes_proxima', null=True, blank=True)
    avaliador = models.CharField(max_length=100, blank=True)
    conceito = models.ForeignKey('ConceitoAvaliacao', on_delete=models.PROTECT, null=True, blank=True)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    aprovado = models.BooleanField(default=False)
    nota_final = models.FloatField(null=True, blank=True)
    questoes = models.ManyToManyField(Questao, related_name='avaliacoes', blank=True)

    def save(self, *args, **kwargs):
        # Só permite nova avaliação se não houver aprovada para a faixa
        if self.aprovado:
            existe_aprovada = Avaliacao.objects.filter(
                aluno=self.aluno,
                faixa_atual=self.faixa_atual,
                aprovado=True
            ).exclude(pk=self.pk).exists()
            if existe_aprovada:
                raise Exception('Já existe uma avaliação aprovada para esta faixa.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Avaliação de {self.aluno} em {self.data}"

    def gerar_questoes(self, faixa=None):
        """Gera 10 questões aleatórias para a avaliação, evitando redundância de natureza."""
        from django.db.models import Q
        import random

        # Usa a faixa passada como parâmetro, ou a faixa_atual do aluno como fallback
        faixa_questao = faixa or self.faixa_atual

        # Obtém todas as questões ativas da faixa
        questoes_disponiveis = Questao.objects.filter(
            faixa=faixa_questao,
            ativa=True
        )

        # Agrupa questões por natureza
        questoes_por_natureza = {}
        for questao in questoes_disponiveis:
            if questao.natureza not in questoes_por_natureza:
                questoes_por_natureza[questao.natureza] = []
            questoes_por_natureza[questao.natureza].append(questao)

        # Seleciona questões
        questoes_selecionadas = []
        naturezas = list(questoes_por_natureza.keys())
        # Primeiro, seleciona uma questão de cada natureza
        for natureza in naturezas:
            if questoes_por_natureza[natureza]:
                questao = random.choice(questoes_por_natureza[natureza])
                questoes_selecionadas.append(questao)
                questoes_por_natureza[natureza].remove(questao)
        # Depois, completa até 10 questões
        while len(questoes_selecionadas) < 10:
            naturezas_disponiveis = [n for n in naturezas if questoes_por_natureza[n]]
            if not naturezas_disponiveis:
                break
            natureza = random.choice(naturezas_disponiveis)
            questao = random.choice(questoes_por_natureza[natureza])
            questoes_selecionadas.append(questao)
            questoes_por_natureza[natureza].remove(questao)
        # Atribui as questões à avaliação
        self.questoes.set(questoes_selecionadas)

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
