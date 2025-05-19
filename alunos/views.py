from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Aluno, Faixa, Questao, Avaliacao, RespostaAvaliacao, Certificado, Turma, EventoExame
from .forms import AlunoForm, FaixaForm, QuestaoForm, AvaliacaoForm, RespostaAvaliacaoFormSet, InscricaoExameForm, TurmaForm, EventoExameForm
from random import sample
from django.core.files.storage import default_storage
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from django.utils import timezone

# Views para Alunos
class AlunoListView(ListView):
    model = Aluno
    template_name = 'alunos/aluno_list.html'
    context_object_name = 'alunos'
    ordering = ['nome_completo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alunos = context['alunos']
        alunos_info = []
        for aluno in alunos:
            ultima_avaliacao = (
                aluno.avaliacoes.filter(faixa_atual=aluno.faixa_atual)
                .order_by('-data')
                .first()
            )
            alunos_info.append({
                'aluno': aluno,
                'avaliacao': ultima_avaliacao,
                'nota': getattr(ultima_avaliacao, 'nota_final', None) if ultima_avaliacao else None,
                'aprovado': getattr(ultima_avaliacao, 'aprovado', None) if ultima_avaliacao else None,
            })
        context['alunos_info'] = alunos_info
        return context

class AlunoDetailView(DetailView):
    model = Aluno
    template_name = 'alunos/aluno_detail.html'
    context_object_name = 'aluno'

class AlunoCreateView(CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/aluno_form.html'
    success_url = reverse_lazy('alunos:aluno_list')

    def form_valid(self, form):
        messages.success(self.request, 'Aluno cadastrado com sucesso!')
        return super().form_valid(form)

class AlunoUpdateView(UpdateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/aluno_form.html'
    success_url = reverse_lazy('alunos:aluno_list')

    def form_valid(self, form):
        messages.success(self.request, 'Aluno atualizado com sucesso!')
        return super().form_valid(form)

class AlunoDeleteView(DeleteView):
    model = Aluno
    template_name = 'alunos/aluno_confirm_delete.html'
    success_url = reverse_lazy('alunos:aluno_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Aluno excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Faixas
class FaixaListView(ListView):
    model = Faixa
    template_name = 'alunos/faixa_list.html'
    context_object_name = 'faixas'
    ordering = ['ordem']

class FaixaCreateView(CreateView):
    model = Faixa
    form_class = FaixaForm
    template_name = 'alunos/faixa_form.html'
    success_url = reverse_lazy('alunos:faixa_list')

    def form_valid(self, form):
        messages.success(self.request, 'Faixa cadastrada com sucesso!')
        return super().form_valid(form)

class FaixaUpdateView(UpdateView):
    model = Faixa
    form_class = FaixaForm
    template_name = 'alunos/faixa_form.html'
    success_url = reverse_lazy('alunos:faixa_list')

    def form_valid(self, form):
        messages.success(self.request, 'Faixa atualizada com sucesso!')
        return super().form_valid(form)

class FaixaDeleteView(DeleteView):
    model = Faixa
    template_name = 'alunos/faixa_confirm_delete.html'
    success_url = reverse_lazy('alunos:faixa_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Faixa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Questões
class QuestaoListView(ListView):
    model = Questao
    template_name = 'alunos/questao_list.html'
    context_object_name = 'questoes'
    ordering = ['faixa__ordem', 'texto']

class QuestaoCreateView(CreateView):
    model = Questao
    form_class = QuestaoForm
    template_name = 'alunos/questao_form.html'
    success_url = reverse_lazy('alunos:questao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Questão cadastrada com sucesso!')
        return super().form_valid(form)

class QuestaoUpdateView(UpdateView):
    model = Questao
    form_class = QuestaoForm
    template_name = 'alunos/questao_form.html'
    success_url = reverse_lazy('alunos:questao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Questão atualizada com sucesso!')
        return super().form_valid(form)

class QuestaoDeleteView(DeleteView):
    model = Questao
    template_name = 'alunos/questao_confirm_delete.html'
    success_url = reverse_lazy('alunos:questao_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Questão excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Avaliações
class AvaliacaoCreateView(CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'alunos/avaliacao_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = get_object_or_404(Aluno, pk=self.kwargs['pk'])
        context['aluno'] = aluno
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        aluno = get_object_or_404(Aluno, pk=self.kwargs['pk'])
        kwargs['aluno'] = aluno
        return kwargs

    def form_valid(self, form):
        aluno = get_object_or_404(Aluno, pk=self.kwargs['pk'])
        form.instance.aluno = aluno
        
        # Se for a primeira submissão (gerar avaliação)
        if not form.instance.pk:
            response = super().form_valid(form)
            # Sorteia as questões usando a faixa escolhida no formulário
            self.object.gerar_questoes(faixa=form.cleaned_data['faixa_proxima'])
            messages.success(self.request, 'Avaliação gerada com sucesso! Agora você pode avaliar o aluno.')
            return redirect('alunos:avaliacao_responder', pk=self.object.pk)
        
        # Se for a submissão final (salvar avaliação)
        self.object = form.save()
        messages.success(self.request, 'Avaliação salva com sucesso!')
        return redirect('alunos:avaliacao_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('alunos:avaliacao_detail', kwargs={'pk': self.object.pk})

class AvaliacaoDetailView(DetailView):
    model = Avaliacao
    template_name = 'alunos/avaliacao_form.html'
    context_object_name = 'avaliacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona respostas para exibição no template
        context['avaliacao'] = self.object
        context['respostas'] = self.object.respostas.all()
        return context

class AvaliacaoResponderView(UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'alunos/avaliacao_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['respostas'] = RespostaAvaliacaoFormSet(self.request.POST, instance=self.object)
        else:
            context['respostas'] = RespostaAvaliacaoFormSet(instance=self.object)
        context['avaliacao'] = self.object
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        respostas = context['respostas']
        if respostas.is_valid():
            self.object = form.save()
            respostas.instance = self.object
            respostas.save()
            
            # Calcular nota final baseada apenas nos conceitos
            total_conceito = 0
            total_questoes = 0
            for resposta in self.object.respostas.all():
                if resposta.conceito is not None:
                    total_conceito += resposta.conceito
                    total_questoes += 1
            
            nota_final = 0
            if total_questoes > 0:
                nota_final = (total_conceito / (total_questoes * 3)) * 10  # 3 é o valor máximo do conceito
            
            self.object.nota_final = nota_final
            self.object.aprovado = nota_final >= 6
            self.object.save()
            
            messages.success(self.request, 'Avaliação finalizada com sucesso!')
            return redirect('alunos:avaliacao_detail', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data(form=form))

class AvaliacaoResultadoView(DetailView):
    model = Avaliacao
    template_name = 'alunos/avaliacao_resultado.html'
    context_object_name = 'avaliacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avaliacao = self.get_object()
        # Calcula a nota final
        total_conceito = 0
        total_questoes = 0
        for resposta in avaliacao.respostas.all():
            if resposta.conceito is not None:
                total_conceito += resposta.conceito
                total_questoes += 1
        if total_questoes > 0:
            nota_final = (total_conceito / (total_questoes * 3)) * 10
            avaliacao.nota_final = nota_final
            avaliacao.aprovado = nota_final >= 7.0
            avaliacao.save()
            # Envia e-mail com o resultado
            if avaliacao.aluno.email:
                context_email = {
                    'avaliacao': avaliacao,
                    'aluno': avaliacao.aluno,
                }
                html_message = render_to_string('alunos/email_resultado.html', context_email)
                send_mail(
                    'Resultado da Avaliação',
                    'Você recebeu o resultado da sua avaliação.',
                    settings.DEFAULT_FROM_EMAIL,
                    [avaliacao.aluno.email],
                    html_message=html_message,
                )
        return context

# Views para Certificados
class CertificadoDetailView(DetailView):
    model = Certificado
    template_name = 'alunos/certificado_detail.html'
    context_object_name = 'certificado'

class CertificadoGerarView(CreateView):
    model = Certificado
    template_name = 'alunos/certificado_gerar.html'
    fields = ['avaliacao']

    def form_valid(self, form):
        certificado = form.save()
        messages.success(self.request, 'Certificado gerado com sucesso!')
        return redirect('alunos:certificado_detail', pk=certificado.pk)

class LogoUploadView(View):
    def post(self, request, *args, **kwargs):
        logo = request.FILES.get('logo')
        if logo:
            import os
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                os.makedirs(media_root)
            logo_path = os.path.join(media_root, 'logo.png')
            with open(logo_path, 'wb+') as destination:
                for chunk in logo.chunks():
                    destination.write(chunk)
            # Atualiza a sessão para mostrar a nova logo
            request.session['logo_url'] = settings.MEDIA_URL + 'logo.png'
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('alunos:aluno_list')))

class DashboardAdminView(View):
    def get(self, request, *args, **kwargs):
        from .models import Aluno, Avaliacao, Faixa
        # Ranking geral
        try:
            ranking_geral = Avaliacao.objects.all().select_related('aluno')[:10]
        except Exception:
            ranking_geral = []
        # Turmas
        try:
            turmas = Aluno.objects.values_list('turma', flat=True).distinct()
        except Exception:
            turmas = []
        turma_selecionada = request.GET.get('turma')
        ranking_turma = None
        if turma_selecionada:
            try:
                ranking_turma = Avaliacao.objects.filter(aluno__turma=turma_selecionada).select_related('aluno')[:10]
            except Exception:
                ranking_turma = []
        # Faixas base/intermediárias
        try:
            faixas_base = Faixa.objects.filter(tipo='base') if hasattr(Faixa, 'tipo') else Faixa.objects.filter(ordem__lte=3)
            faixas_inter = Faixa.objects.filter(tipo='intermediaria') if hasattr(Faixa, 'tipo') else Faixa.objects.filter(ordem__gt=3)
            ranking_base = Avaliacao.objects.filter(aluno__faixa_atual__in=faixas_base).select_related('aluno')[:10]
            ranking_inter = Avaliacao.objects.filter(aluno__faixa_atual__in=faixas_inter).select_related('aluno')[:10]
        except Exception:
            ranking_base = []
            ranking_inter = []
        try:
            total_alunos = Aluno.objects.count()
        except Exception:
            total_alunos = 0
        try:
            total_turmas = len(turmas)
        except Exception:
            total_turmas = 0
        try:
            total_avaliacoes = Avaliacao.objects.count()
        except Exception:
            total_avaliacoes = 0
        context = {
            'ranking_geral': ranking_geral,
            'turmas': turmas,
            'turma_selecionada': turma_selecionada,
            'ranking_turma': ranking_turma,
            'ranking_base': ranking_base,
            'ranking_inter': ranking_inter,
            'total_alunos': total_alunos,
            'total_turmas': total_turmas,
            'total_avaliacoes': total_avaliacoes,
        }
        return render(request, 'alunos/dashboard_admin.html', context)

class InscricaoExameView(FormView):
    template_name = 'alunos/inscricao_exame_form.html'
    form_class = InscricaoExameForm
    success_url = reverse_lazy('alunos:inscricao_exame')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import EventoExame
        evento = EventoExame.objects.filter(data__gte=timezone.now().date()).order_by('data').first()
        context['evento'] = evento
        return context

    def form_valid(self, form):
        aluno = form.save(commit=False)
        comprovante = form.cleaned_data.get('comprovante_pagamento')
        if comprovante:
            aluno.comprovante_pagamento = comprovante
        aluno.save()
        messages.success(self.request, 'Inscrição enviada com sucesso!')
        return super().form_valid(form)

class TurmaListView(ListView):
    model = Turma
    template_name = 'alunos/turma_list.html'
    context_object_name = 'turmas'

class TurmaCreateView(CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'alunos/turma_form.html'
    success_url = reverse_lazy('alunos:turma_list')

class EventoExameListView(ListView):
    model = EventoExame
    template_name = 'alunos/eventoexame_list.html'
    context_object_name = 'eventos'

class EventoExameCreateView(CreateView):
    model = EventoExame
    form_class = EventoExameForm
    template_name = 'alunos/eventoexame_form.html'
    success_url = reverse_lazy('alunos:eventoexame_list')
