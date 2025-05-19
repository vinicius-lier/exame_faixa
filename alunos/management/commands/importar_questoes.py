from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Questao, Faixa
import pandas as pd

class Command(BaseCommand):
    help = 'Importa questões do arquivo Excel'

    def handle(self, *args, **options):
        try:
            # Lê o arquivo Excel
            df = pd.read_excel('banco_questoes_judo.xlsx')
            
            # Mapeamento de faixas
            faixa_map = {
                'branca/cinza': 'Ponta Cinza',
                'cinza': 'Cinza',
                'cinza/azul': 'Ponta Azul',
                'azul': 'Azul',
                'azul/roxa': 'Ponta Roxa',
                'roxa': 'Roxa',
                'roxa/marrom': 'Ponta Marrom',
                'marrom': 'Marrom',
                'marrom/preta': 'Ponta Preta',
                'preta': 'Preta',
                'azul/amarela': 'Ponta Amarela',
                'amarela/laranja': 'Ponta Laranja',
            }

            # Lista de faixas cadastradas (normalizadas)
            faixas_cadastradas = {f.nome.strip().casefold(): f for f in Faixa.objects.all()}

            with transaction.atomic():
                # Limpa questões existentes
                Questao.objects.all().delete()
                
                # Processa cada linha do Excel
                for _, row in df.iterrows():
                    faixa_raw = str(row['Faixa']).strip().casefold()
                    faixa_nome = faixa_map.get(faixa_raw, faixa_raw)
                    faixa_obj = faixas_cadastradas.get(faixa_nome.strip().casefold())
                    if not faixa_obj:
                        raise Exception(f'Faixa não encontrada: {row["Faixa"]}')
                    # Cria a questão
                    Questao.objects.create(
                        texto=row['Pergunta'],
                        faixa=faixa_obj,
                        natureza=str(row['Tipo']).strip().casefold(),
                        pontuacao=str(row['Pontuação']) if 'Pontuação' in row else '',
                        categoria=str(row['Categoria']) if 'Categoria' in row else '',
                        prioritaria=(str(row['Prioritária']).strip().lower() in ['sim', 'true', '1']),
                        descricao_execucao=str(row['Descrição da Execução']) if 'Descrição da Execução' in row else '',
                        ativa=True
                    )

            self.stdout.write(self.style.SUCCESS('Questões importadas com sucesso!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar questões: {str(e)}')) 