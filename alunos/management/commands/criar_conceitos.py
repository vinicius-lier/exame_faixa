from django.core.management.base import BaseCommand
from alunos.models import ConceitoAvaliacao

class Command(BaseCommand):
    help = 'Cria os conceitos de avaliação padrão'

    def handle(self, *args, **kwargs):
        conceitos = [
            ('ND', 'Necessário Desenvolvimento'),
            ('R', 'Regular'),
            ('B', 'Bom'),
            ('MB', 'Muito Bom'),
            ('E', 'Excelente'),
        ]

        for sigla, descricao in conceitos:
            ConceitoAvaliacao.objects.get_or_create(
                sigla=sigla,
                defaults={'descricao': descricao}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Conceito criado: {sigla} - {descricao}')
            ) 