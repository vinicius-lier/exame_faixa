from django.core.management.base import BaseCommand
from alunos.models import Faixa, Questao

class Command(BaseCommand):
    help = 'Cria as questões para cada faixa'

    def handle(self, *args, **kwargs):
        # Dicionário com as questões para cada faixa
        questoes_por_faixa = {
            'Cinza': [
                {
                    'pergunta': 'O que é o Judô?',
                    'opcoes': [
                        'Uma arte marcial japonesa',
                        'Um esporte de luta',
                        'Uma técnica de defesa pessoal',
                        'Todas as alternativas acima'
                    ],
                    'resposta_correta': 3
                },
                {
                    'pergunta': 'Quem foi o criador do Judô?',
                    'opcoes': [
                        'Mestre Funakoshi',
                        'Mestre Kano',
                        'Mestre Ueshiba',
                        'Mestre Oyama'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Qual o significado da palavra Judô?',
                    'opcoes': [
                        'Caminho da flexibilidade',
                        'Caminho suave',
                        'Caminho da força',
                        'Caminho da paz'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Quais são os princípios fundamentais do Judô?',
                    'opcoes': [
                        'Força e velocidade',
                        'Flexibilidade e agilidade',
                        'Máxima eficiência e bem-estar mútuo',
                        'Técnica e força'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que significa a faixa cinza no Judô?',
                    'opcoes': [
                        'Iniciante',
                        'Intermediário',
                        'Avançado',
                        'Mestre'
                    ],
                    'resposta_correta': 0
                }
            ],
            'Azul': [
                {
                    'pergunta': 'Qual é o objetivo principal do Judô?',
                    'opcoes': [
                        'Derrotar o oponente',
                        'Desenvolver o corpo e a mente',
                        'Aprender técnicas de luta',
                        'Ganhar competições'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'O que significa "Rei" no Judô?',
                    'opcoes': [
                        'Respeito',
                        'Força',
                        'Técnica',
                        'Vitória'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'Qual é a posição básica de combate no Judô?',
                    'opcoes': [
                        'Shizen-tai',
                        'Jigo-tai',
                        'Ambas as alternativas',
                        'Nenhuma das alternativas'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que é um "Randori"?',
                    'opcoes': [
                        'Um tipo de golpe',
                        'Um treino livre',
                        'Uma competição',
                        'Uma técnica de defesa'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Qual é a importância da faixa azul no Judô?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio básico',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 1
                }
            ],
            'Amarela': [
                {
                    'pergunta': 'O que é "Kuzushi"?',
                    'opcoes': [
                        'Uma técnica de projeção',
                        'O desequilíbrio do oponente',
                        'Uma posição de defesa',
                        'Um tipo de golpe'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Qual é a importância do "Tsukuri"?',
                    'opcoes': [
                        'Preparar a técnica',
                        'Executar o golpe',
                        'Defender o ataque',
                        'Finalizar o combate'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'O que é "Kake" no Judô?',
                    'opcoes': [
                        'A execução da técnica',
                        'O início do movimento',
                        'A defesa do ataque',
                        'O final do combate'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'Qual é a importância da faixa amarela?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio intermediário',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'O que significa "Seiryoku Zenyo"?',
                    'opcoes': [
                        'Máxima eficiência',
                        'Bem-estar mútuo',
                        'Força e técnica',
                        'Respeito e disciplina'
                    ],
                    'resposta_correta': 0
                }
            ],
            'Laranja': [
                {
                    'pergunta': 'O que é "Jita Kyoei"?',
                    'opcoes': [
                        'Máxima eficiência',
                        'Bem-estar mútuo',
                        'Força e técnica',
                        'Respeito e disciplina'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Qual é a importância da faixa laranja?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio intermediário',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que é "Uchi-komi"?',
                    'opcoes': [
                        'Treino de entrada',
                        'Treino de projeção',
                        'Treino de defesa',
                        'Treino de finalização'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'Qual é a importância do "Nage-komi"?',
                    'opcoes': [
                        'Treino de entrada',
                        'Treino de projeção',
                        'Treino de defesa',
                        'Treino de finalização'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'O que é "Kata"?',
                    'opcoes': [
                        'Forma preestabelecida de técnicas',
                        'Treino livre',
                        'Competição',
                        'Defesa pessoal'
                    ],
                    'resposta_correta': 0
                }
            ],
            'Verde': [
                {
                    'pergunta': 'O que é "Ne-waza"?',
                    'opcoes': [
                        'Técnicas em pé',
                        'Técnicas no solo',
                        'Técnicas de projeção',
                        'Técnicas de defesa'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'Qual é a importância da faixa verde?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio intermediário',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que é "Osae-komi"?',
                    'opcoes': [
                        'Imobilização',
                        'Projeção',
                        'Finalização',
                        'Defesa'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'O que é "Shime-waza"?',
                    'opcoes': [
                        'Técnicas de imobilização',
                        'Técnicas de estrangulamento',
                        'Técnicas de luxação',
                        'Técnicas de projeção'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'O que é "Kansetsu-waza"?',
                    'opcoes': [
                        'Técnicas de imobilização',
                        'Técnicas de estrangulamento',
                        'Técnicas de luxação',
                        'Técnicas de projeção'
                    ],
                    'resposta_correta': 2
                }
            ],
            'Roxa': [
                {
                    'pergunta': 'O que é "Randori-no-kata"?',
                    'opcoes': [
                        'Forma de treino livre',
                        'Forma de competição',
                        'Forma de defesa pessoal',
                        'Forma de demonstração'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'Qual é a importância da faixa roxa?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio intermediário',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que é "Ju-no-kata"?',
                    'opcoes': [
                        'Forma de flexibilidade',
                        'Forma de força',
                        'Forma de técnica',
                        'Forma de defesa'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'O que é "Itsutsu-no-kata"?',
                    'opcoes': [
                        'Forma dos cinco princípios',
                        'Forma das cinco técnicas',
                        'Forma das cinco projeções',
                        'Forma das cinco defesas'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'O que é "Koshiki-no-kata"?',
                    'opcoes': [
                        'Forma antiga',
                        'Forma moderna',
                        'Forma básica',
                        'Forma avançada'
                    ],
                    'resposta_correta': 0
                }
            ],
            'Marrom': [
                {
                    'pergunta': 'O que é "Kodokan"?',
                    'opcoes': [
                        'A escola de Judô fundada por Jigoro Kano',
                        'Um tipo de técnica',
                        'Um sistema de graduação',
                        'Um estilo de Judô'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'Qual é a importância da faixa marrom?',
                    'opcoes': [
                        'Representa o início do aprendizado',
                        'Representa o domínio intermediário',
                        'Representa o nível avançado',
                        'Representa o nível mestre'
                    ],
                    'resposta_correta': 2
                },
                {
                    'pergunta': 'O que é "Dan"?',
                    'opcoes': [
                        'Grau de faixa preta',
                        'Grau de faixa colorida',
                        'Sistema de graduação',
                        'Tipo de competição'
                    ],
                    'resposta_correta': 0
                },
                {
                    'pergunta': 'O que é "Kyu"?',
                    'opcoes': [
                        'Grau de faixa preta',
                        'Grau de faixa colorida',
                        'Sistema de graduação',
                        'Tipo de competição'
                    ],
                    'resposta_correta': 1
                },
                {
                    'pergunta': 'O que é "Shodan"?',
                    'opcoes': [
                        'Primeiro grau de faixa preta',
                        'Último grau de faixa colorida',
                        'Sistema de graduação',
                        'Tipo de competição'
                    ],
                    'resposta_correta': 0
                }
            ]
        }

        # Criar questões para cada faixa
        for nome_faixa, questoes in questoes_por_faixa.items():
            try:
                faixa = Faixa.objects.get(nome=nome_faixa)
                
                # Remover questões existentes da faixa
                Questao.objects.filter(faixa=faixa).delete()
                
                # Criar novas questões
                for questao in questoes:
                    Questao.objects.create(
                        faixa=faixa,
                        pergunta=questao['pergunta'],
                        opcoes=questao['opcoes'],
                        resposta_correta=questao['resposta_correta']
                    )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Questões criadas com sucesso para a faixa {nome_faixa}')
                )
            except Faixa.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Faixa {nome_faixa} não encontrada')
                ) 