from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Aluno, Faixa, Questao, Avaliacao, RespostaAvaliacao, Certificado
from .forms import AlunoForm, FaixaForm, QuestaoForm, AvaliacaoForm, RespostaAvaliacaoFormSet

# Views para Alunos
class AlunoListView(ListView):
    model = Aluno
    template_name = 'alunos/aluno_list.html'
    context_object_name = 'alunos'
    ordering = ['nome_completo']

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

    def form_valid(self, form):
        form.instance.aluno = get_object_or_404(Aluno, pk=self.kwargs['pk'])
        messages.success(self.request, 'Avaliação iniciada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('alunos:avaliacao_detail', kwargs={'pk': self.object.pk})

class AvaliacaoDetailView(DetailView):
    model = Avaliacao
    template_name = 'alunos/avaliacao_detail.html'
    context_object_name = 'avaliacao'

class AvaliacaoResponderView(UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'alunos/avaliacao_responder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['respostas'] = RespostaAvaliacaoFormSet(self.request.POST, instance=self.object)
        else:
            context['respostas'] = RespostaAvaliacaoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        respostas = context['respostas']
        if respostas.is_valid():
            self.object = form.save()
            respostas.instance = self.object
            respostas.save()
            messages.success(self.request, 'Respostas salvas com sucesso!')
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
        total_peso = 0
        total_pontos = 0
        for resposta in avaliacao.respostas.all():
            total_peso += resposta.questao.peso
            total_pontos += resposta.conceito * resposta.questao.peso
        
        if total_peso > 0:
            nota_final = total_pontos / total_peso
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
