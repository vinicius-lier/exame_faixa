from django.core.management.base import BaseCommand
from alunos.models import Faixa, Questao

FAIXAS = [
    'Ponta Cinza',
    'Cinza',
    'Ponta Azul',
    'Azul',
    'Ponta Roxa',
    'Roxa',
    'Ponta Marrom',
    'Marrom',
    'Ponta Preta',
    'Preta',
]

VARIACOES_QUESTOES = [
    # Saudações
    {'texto': 'Explique o significado de RITSU-REI.', 'natureza': 'historia'},
    {'texto': 'O que representa a saudação em pé (RITSU-REI) no judô?', 'natureza': 'historia'},
    {'texto': 'Por que é importante realizar o RITSU-REI antes do treino?', 'natureza': 'filosofia'},
    {'texto': 'Mostre como se faz o RITSU-REI corretamente.', 'natureza': 'tecnica'},
    {'texto': 'Demonstre a saudação ajoelhado (ZA-REI).', 'natureza': 'tecnica'},
    {'texto': 'Em que situações usamos o ZA-REI?', 'natureza': 'regras'},
    # Amortecimentos
    {'texto': 'Mostre como se executa o USHIRO-UKEMI.', 'natureza': 'tecnica'},
    {'texto': 'Quais os cuidados ao fazer o amortecimento para trás (USHIRO-UKEMI)?', 'natureza': 'regras'},
    {'texto': 'Explique a importância do YOKO-UKEMI.', 'natureza': 'filosofia'},
    {'texto': 'Demonstre o amortecimento para o lado (YOKO-UKEMI).', 'natureza': 'tecnica'},
    {'texto': 'Como é feito o ZENPO-KAITEN-UKEMI?', 'natureza': 'tecnica'},
    {'texto': 'Para que serve o rolamento à frente (ZENPO-KAITEN-UKEMI)?', 'natureza': 'filosofia'},
    # Técnicas de Projeção
    {'texto': 'Demonstre a técnica O-SOTO-GARI.', 'natureza': 'tecnica'},
    {'texto': 'Quais são os principais pontos para executar o O-SOTO-GARI?', 'natureza': 'tecnica'},
    {'texto': 'Explique o movimento do O-UCHI-GARI.', 'natureza': 'tecnica'},
    {'texto': 'Mostre como se faz o O-UCHI-GARI.', 'natureza': 'tecnica'},
    {'texto': 'Qual a diferença entre O-SOTO-GARI e O-UCHI-GARI?', 'natureza': 'regras'},
    # Técnicas de Imobilização
    {'texto': 'Demonstre a técnica KESA-GATAME.', 'natureza': 'tecnica'},
    {'texto': 'Explique como escapar do KESA-GATAME.', 'natureza': 'tecnica'},
    {'texto': 'Mostre a técnica KUZURE-KESA-GATAME.', 'natureza': 'tecnica'},
    {'texto': 'Qual a diferença entre KESA-GATAME e KUZURE-KESA-GATAME?', 'natureza': 'regras'},
    {'texto': 'Para que serve a imobilização KESA-GATAME?', 'natureza': 'filosofia'},
    # Vocabulário
    {'texto': 'O que significa TATAMI?', 'natureza': 'historia'},
    {'texto': 'Explique o termo JUDOGI.', 'natureza': 'historia'},
    {'texto': 'Para que serve o TATAMI no judô?', 'natureza': 'regras'},
    {'texto': 'Qual a função do JUDOGI?', 'natureza': 'regras'},
]

class Command(BaseCommand):
    help = 'Gera o máximo de questões variadas para todas as faixas do cronograma.'

    def handle(self, *args, **options):
        total_criadas = 0
        for faixa_nome in FAIXAS:
            faixa = Faixa.objects.filter(nome=faixa_nome).first()
            if not faixa:
                maior_ordem = Faixa.objects.all().order_by('-ordem').first()
                proxima_ordem = (maior_ordem.ordem + 1) if maior_ordem else 1
                faixa = Faixa.objects.create(nome=faixa_nome, ordem=proxima_ordem)
            criadas = 0
            for q in VARIACOES_QUESTOES:
                if not Questao.objects.filter(faixa=faixa, texto=q['texto'], natureza=q['natureza']).exists():
                    Questao.objects.create(faixa=faixa, texto=q['texto'], natureza=q['natureza'])
                    criadas += 1
            self.stdout.write(self.style.SUCCESS(f'{criadas} questões criadas para a faixa {faixa_nome}.'))
            total_criadas += criadas
        self.stdout.write(self.style.SUCCESS(f'Total de {total_criadas} questões criadas para todas as faixas.')) 