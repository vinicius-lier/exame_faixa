from django.core.management.base import BaseCommand
from alunos.models import Faixa, Questao

class Command(BaseCommand):
    help = 'Gera o máximo de questões para a Faixa Cinza conforme o cronograma.'

    def handle(self, *args, **options):
        faixa_nome = 'Cinza'
        faixa = Faixa.objects.filter(nome=faixa_nome).first()
        if not faixa:
            maior_ordem = Faixa.objects.all().order_by('-ordem').first()
            proxima_ordem = (maior_ordem.ordem + 1) if maior_ordem else 1
            faixa = Faixa.objects.create(nome=faixa_nome, ordem=proxima_ordem)
        questoes = [
            # Saudações
            {'texto': 'O que significa RITSU-REI?', 'natureza': 'historia'},
            {'texto': 'O que significa ZA-REI?', 'natureza': 'historia'},
            {'texto': 'Execute a saudação em pé (RITSU-REI).', 'natureza': 'tecnica'},
            {'texto': 'Execute a saudação ajoelhado (ZA-REI).', 'natureza': 'tecnica'},
            # Amortecimentos
            {'texto': 'Execute o amortecimento para trás (USHIRO-UKEMI).', 'natureza': 'tecnica'},
            {'texto': 'Execute o amortecimento para o lado (YOKO-UKEMI) a partir da posição agachado.', 'natureza': 'tecnica'},
            {'texto': 'Execute o amortecimento para frente com rolamento (ZENPO-KAITEN-UKEMI).', 'natureza': 'tecnica'},
            {'texto': 'Explique o que é USHIRO-UKEMI.', 'natureza': 'filosofia'},
            {'texto': 'Explique o que é YOKO-UKEMI.', 'natureza': 'filosofia'},
            {'texto': 'Explique o que é ZENPO-KAITEN-UKEMI.', 'natureza': 'filosofia'},
            # Técnicas de Projeção
            {'texto': 'Execute a técnica O-SOTO-GARI.', 'natureza': 'tecnica'},
            {'texto': 'Execute a técnica O-UCHI-GARI.', 'natureza': 'tecnica'},
            {'texto': 'Explique a técnica O-SOTO-GARI.', 'natureza': 'tecnica'},
            {'texto': 'Explique a técnica O-UCHI-GARI.', 'natureza': 'tecnica'},
            # Técnicas de Imobilização
            {'texto': 'Execute a técnica KESA-GATAME.', 'natureza': 'tecnica'},
            {'texto': 'Execute a técnica KUZURE-KESA-GATAME.', 'natureza': 'tecnica'},
            {'texto': 'Explique a técnica KESA-GATAME.', 'natureza': 'tecnica'},
            {'texto': 'Explique a técnica KUZURE-KESA-GATAME.', 'natureza': 'tecnica'},
            # Vocabulário
            {'texto': 'O que significa TATAMI?', 'natureza': 'historia'},
            {'texto': 'O que significa JUDOGI?', 'natureza': 'historia'},
        ]
        criadas = 0
        for q in questoes:
            if not Questao.objects.filter(faixa=faixa, texto=q['texto'], natureza=q['natureza']).exists():
                Questao.objects.create(faixa=faixa, texto=q['texto'], natureza=q['natureza'])
                criadas += 1
        self.stdout.write(self.style.SUCCESS(f'{criadas} questões criadas para a faixa {faixa_nome}.')) 