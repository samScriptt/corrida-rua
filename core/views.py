# core/views.py (Verifique se estas linhas existem e estão corretas)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ( # Importar as classes baseadas em classe
    ListView, CreateView, UpdateView, DeleteView, DetailView 
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login # <-- ESSENCIAL para o registro

from .models import Equipe, Piloto, Carro, Pista, Corrida, Inscricao
from .forms import EquipeForm, CarroForm, PistaForm, CorridaForm, InscricaoForm, RegistroPilotoForm # <-- ESSENCIAL para o registro

from django.db.models import Max


# --- HOME ---
def home(request):
    return render(request, 'home.html')

# --- Funções Auxiliares de Segurança ---
def get_piloto_profile(request):
    """Retorna o objeto Piloto do usuário logado ou levanta um 404."""
    # O Piloto deve estar logado
    return get_object_or_404(Piloto, usuario=request.user)


# =================================================================
# --- CRUD: EQUIPE ---
# Lógica: O Piloto só vê/edita a equipe à qual ele está associado

class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = 'equipe_list.html'
    context_object_name = 'equipes'

    def get_queryset(self):
        try:
            piloto = get_piloto_profile(self.request)
        except Piloto.DoesNotExist:
            return Equipe.objects.none() 
        
        # Retorna a Equipe à qual esse Piloto pertence
        if piloto.equipe:
             return Equipe.objects.filter(pk=piloto.equipe.pk)
        return Equipe.objects.none()

class EquipeCreateView(LoginRequiredMixin, CreateView):
    model = Equipe
    form_class = EquipeForm 
    template_name = 'equipe_form.html'
    success_url = reverse_lazy('core:equipe_list') 

class EquipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipe
    form_class = EquipeForm
    template_name = 'equipe_form.html'
    success_url = reverse_lazy('core:equipe_list')
    
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            piloto = get_piloto_profile(self.request)
            if piloto.equipe:
                return qs.filter(pk=piloto.equipe.pk)
            return qs.none()
        except Piloto.DoesNotExist:
            return qs.none()

class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    template_name = 'equipe_confirm_delete.html'
    success_url = reverse_lazy('core:equipe_list')
    
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            piloto = get_piloto_profile(self.request)
            if piloto.equipe:
                return qs.filter(pk=piloto.equipe.pk)
            return qs.none()
        except Piloto.DoesNotExist:
            return qs.none()


# =================================================================
# --- CRUD: CARRO ---

class CarroListView(LoginRequiredMixin, ListView):
    model = Carro
    template_name = 'carro_list.html'
    context_object_name = 'carros'

    def get_queryset(self):
        piloto = get_piloto_profile(self.request)
        if piloto.equipe:
            return Carro.objects.filter(equipe=piloto.equipe)
        return Carro.objects.none()

class CarroCreateView(LoginRequiredMixin, CreateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('core:carro_list')

    def form_valid(self, form):
        piloto = get_piloto_profile(self.request)
        
        if not piloto.equipe:
            return redirect('core:equipe_list')
        
        # Vincula o Carro à Equipe do Piloto logado
        form.instance.equipe = piloto.equipe 
        return super().form_valid(form)

class CarroUpdateView(LoginRequiredMixin, UpdateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('core:carro_list')
    
    def get_queryset(self):
        piloto = get_piloto_profile(self.request)
        return Carro.objects.filter(equipe=piloto.equipe)

class CarroDeleteView(LoginRequiredMixin, DeleteView):
    model = Carro
    template_name = 'carro_confirm_delete.html'
    success_url = reverse_lazy('core:carro_list')
    
    def get_queryset(self):
        piloto = get_piloto_profile(self.request)
        return Carro.objects.filter(equipe=piloto.equipe)

# =================================================================
# --- CRUD: PISTA ---

class PistaListView(LoginRequiredMixin, ListView):
    model = Pista
    template_name = 'pista_list.html'
    context_object_name = 'pistas'

class PistaCreateView(LoginRequiredMixin, CreateView):
    model = Pista
    form_class = PistaForm
    template_name = 'pista_form.html'
    success_url = reverse_lazy('core:pista_list')

class PistaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pista
    form_class = PistaForm
    template_name = 'pista_form.html'
    success_url = reverse_lazy('core:pista_list')

class PistaDeleteView(LoginRequiredMixin, DeleteView):
    model = Pista
    template_name = 'pista_confirm_delete.html'
    success_url = reverse_lazy('core:pista_list')

# =================================================================
# --- CRUD: CORRIDA ---

class CorridaListView(LoginRequiredMixin, ListView):
    model = Corrida
    template_name = 'corrida_list.html'
    context_object_name = 'corridas'

class CorridaDetailView(LoginRequiredMixin, DetailView):
    model = Corrida
    template_name = 'corrida_detail.html'
    context_object_name = 'corrida'

class CorridaCreateView(LoginRequiredMixin, CreateView):
    model = Corrida
    form_class = CorridaForm
    template_name = 'corrida_form.html'
    success_url = reverse_lazy('core:corrida_list')

class CorridaUpdateView(LoginRequiredMixin, UpdateView):
    model = Corrida
    form_class = CorridaForm
    template_name = 'corrida_form.html'
    success_url = reverse_lazy('core:corrida_list')

class CorridaDeleteView(LoginRequiredMixin, DeleteView):
    model = Corrida
    template_name = 'corrida_confirm_delete.html'
    success_url = reverse_lazy('core:corrida_list')

# =================================================================
# --- CRUD: INSCRIÇÃO ---

class InscricaoCreateView(LoginRequiredMixin, CreateView):
    model = Inscricao
    form_class = InscricaoForm
    template_name = 'inscricao_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['corrida'] = get_object_or_404(Corrida, pk=self.kwargs['corrida_pk'])
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        piloto = get_piloto_profile(self.request)
        
        # Filtra os carros para mostrar APENAS os da equipe do piloto
        if piloto.equipe:
            form.fields['carro'].queryset = Carro.objects.filter(equipe=piloto.equipe)
        else:
            form.fields['carro'].queryset = Carro.objects.none()
            form.fields['carro'].help_text = "Você precisa estar em uma equipe para inscrever um carro."

        return form

    # core/views.py (Dentro da classe InscricaoCreateView)

    def form_valid(self, form):
        corrida = get_object_or_404(Corrida, pk=self.kwargs['corrida_pk'])
        piloto = get_piloto_profile(self.request)
        
        # --- 1. PREVENIR A DUPLICIDADE ---
        if Inscricao.objects.filter(corrida=corrida, piloto=piloto).exists():
            print("AVISO: Este piloto já está inscrito nesta corrida.")
            return redirect('core:corrida_detail', pk=corrida.pk)

        # --- 2. CALCULAR O PRÓXIMO NÚMERO DE LARGADA ---
        from django.db.models import Max # Ainda precisa desta importação no topo!
        
        max_numero = Inscricao.objects.filter(corrida=corrida).aggregate(Max('numero_largada'))['numero_largada__max']
        next_numero = (max_numero or 0) + 1

        # --- 3. ATRIBUIR E SALVAR MANUALMENTE (CORREÇÃO) ---
        
        # Atribui os campos necessários
        form.instance.corrida = corrida
        form.instance.piloto = piloto
        form.instance.numero_largada = next_numero
        
        # SALVA a instância diretamente (substituindo o super().form_valid)
        form.instance.save() 
        
        # Redireciona para o detalhe da Corrida após a inscrição
        return redirect('core:corrida_detail', pk=corrida.pk)

def registro_piloto_view(request):
    if request.method == 'POST':
        form = RegistroPilotoForm(request.POST)
        if form.is_valid():
            # A função save faz todo o trabalho: cria User, Piloto e Equipe (se necessário)
            user = form.save() 
            
            # Faz o login do novo usuário
            login(request, user) 
            
            # Redireciona para a Home
            return redirect('core:home') 
    else:
        form = RegistroPilotoForm()
        
    context = {'form': form}
    return render(request, 'registro.html', context)