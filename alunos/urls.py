from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    # Alunos
    path('', views.AlunoListView.as_view(), name='aluno_list'),
    path('novo/', views.AlunoCreateView.as_view(), name='aluno_create'),
    path('<int:pk>/', views.AlunoDetailView.as_view(), name='aluno_detail'),
    path('<int:pk>/editar/', views.AlunoUpdateView.as_view(), name='aluno_update'),
    path('<int:pk>/excluir/', views.AlunoDeleteView.as_view(), name='aluno_delete'),
    
    # Faixas
    path('faixas/', views.FaixaListView.as_view(), name='faixa_list'),
    path('faixas/criar/', views.FaixaCreateView.as_view(), name='faixa_create'),
    path('faixas/<int:pk>/editar/', views.FaixaUpdateView.as_view(), name='faixa_update'),
    path('faixas/<int:pk>/excluir/', views.FaixaDeleteView.as_view(), name='faixa_delete'),
    
    # Questões
    path('questoes/', views.QuestaoListView.as_view(), name='questao_list'),
    path('questoes/nova/', views.QuestaoCreateView.as_view(), name='questao_create'),
    path('questoes/<int:pk>/editar/', views.QuestaoUpdateView.as_view(), name='questao_update'),
    path('questoes/<int:pk>/excluir/', views.QuestaoDeleteView.as_view(), name='questao_delete'),
    
    # Avaliações
    path('<int:pk>/avaliar/', views.AvaliacaoCreateView.as_view(), name='avaliacao_create'),
    path('avaliacoes/<int:pk>/', views.AvaliacaoDetailView.as_view(), name='avaliacao_detail'),
    path('avaliacoes/<int:pk>/responder/', views.AvaliacaoResponderView.as_view(), name='avaliacao_responder'),
    path('avaliacoes/<int:pk>/resultado/', views.AvaliacaoResultadoView.as_view(), name='avaliacao_resultado'),
    
    # Certificados
    path('certificados/<int:pk>/', views.CertificadoDetailView.as_view(), name='certificado_detail'),
    path('certificados/<int:pk>/gerar/', views.CertificadoGerarView.as_view(), name='certificado_gerar'),
    
    # Upload da logo
    path('logo_upload/', views.LogoUploadView.as_view(), name='logo_upload'),
    
    # Dashboard admin
    path('dashboard/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    
    # Inscrição no exame
    path('inscricao-exame/', views.InscricaoExameView.as_view(), name='inscricao_exame'),
    
    # Turmas
    path('turmas/', views.TurmaListView.as_view(), name='turma_list'),
    path('turmas/nova/', views.TurmaCreateView.as_view(), name='turma_create'),
    
    # Eventos de Exame
    path('eventos-exame/', views.EventoExameListView.as_view(), name='eventoexame_list'),
    path('eventos-exame/novo/', views.EventoExameCreateView.as_view(), name='eventoexame_create'),
] 