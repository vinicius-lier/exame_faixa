from django.core.management.base import BaseCommand
from alunos.models import Faixa

class Command(BaseCommand):
    help = 'Cria as faixas iniciais do sistema'

    def handle(self, *args, **kwargs):
        faixas = [
            {'nome': 'Branca', 'ordem': 1, 'preco': 0.00},
            {'nome': 'Pontas Cinza', 'ordem': 2, 'preco': 50.00},
            {'nome': 'Cinza', 'ordem': 3, 'preco': 50.00},
            {'nome': 'Pontas Azul', 'ordem': 4, 'preco': 100.00},
            {'nome': 'Azul', 'ordem': 5, 'preco': 100.00},
            {'nome': 'Pontas Amarela', 'ordem': 6, 'preco': 150.00},
            {'nome': 'Amarela', 'ordem': 7, 'preco': 150.00},
            {'nome': 'Pontas Laranja', 'ordem': 8, 'preco': 200.00},
            {'nome': 'Laranja', 'ordem': 9, 'preco': 200.00},
            {'nome': 'Verde', 'ordem': 10, 'preco': 250.00},
            {'nome': 'Roxa', 'ordem': 11, 'preco': 300.00},
            {'nome': 'Marrom', 'ordem': 12, 'preco': 350.00},
        ]

        for faixa_data in faixas:
            faixa, created = Faixa.objects.get_or_create(
                nome=faixa_data['nome'],
                defaults={
                    'ordem': faixa_data['ordem'],
                    'preco': faixa_data['preco'],
                    'descricao': f'Exame de faixa {faixa_data["nome"]}'
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Faixa "{faixa.nome}" criada com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Faixa "{faixa.nome}" já existe.')
                ) 