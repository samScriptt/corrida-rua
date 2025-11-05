# core/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Equipe, Carro, Pista, Corrida, Inscricao, Piloto # Importar Piloto

# =================================================================
# --- 1. FORMS DE CRUD ---
# =================================================================

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ["nome", "cidade", "patrocinador"] 

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        # O campo 'equipe' é preenchido automaticamente pela view
        fields = ["modelo", "placa", "ano", "cor"] 

class PistaForm(forms.ModelForm):
    class Meta:
        model = Pista
        fields = ["nome", "cidade", "extensao_km"]

class CorridaForm(forms.ModelForm):
    class Meta:
        model = Corrida
        fields = ["nome", "data", "status", "categoria", "pista"]

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        # Campos de 'piloto', 'corrida' e 'situacao' são preenchidos pela View
        fields = ["carro", "numero_largada"]

# =================================================================
# --- 2. FORM DE REGISTRO UNIFICADO ---
# =================================================================

class RegistroPilotoForm(forms.Form):
    # --- CAMPOS DO USUÁRIO (User) ---
    username = forms.CharField(label="Nome de Usuário", max_length=150)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email", required=True)

    # --- CAMPOS DO PILOTO (Piloto) ---
    nome_piloto = forms.CharField(label="Nome Completo do Piloto", max_length=120)
    # Garante que as choices do form correspondam ao Piloto.CATEGORIAS
    CATEGORIAS_CHOICES = Piloto.CATEGORIAS
    
    data_nascimento = forms.DateField(
        label="Data de Nascimento (AAAA-MM-DD)", 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    documento = forms.CharField(label="Documento", max_length=30, required=False)
    categoria = forms.ChoiceField(label="Categoria Inicial", choices=CATEGORIAS_CHOICES)

    # --- CAMPOS DE EQUIPE (Vinculação ou Criação) ---
    equipe_existente = forms.ModelChoiceField(
        queryset=Equipe.objects.all().order_by('nome'),
        label="Equipe Existente (Selecione)",
        required=False,
        empty_label="--- Selecione ou Crie uma Nova ---"
    )
    
    nova_equipe_nome = forms.CharField(label="Nome da Nova Equipe", max_length=120, required=False)
    nova_equipe_cidade = forms.CharField(label="Cidade da Nova Equipe", max_length=80, required=False)
    nova_equipe_patrocinador = forms.CharField(label="Patrocinador da Nova Equipe", max_length=120, required=False)

    # Validação customizada
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        equipe_existente = cleaned_data.get("equipe_existente")
        nova_equipe_nome = cleaned_data.get("nova_equipe_nome")

        # 1. Validação de Senhas
        if password and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

        # 2. Validação de Equipe
        if not equipe_existente and not nova_equipe_nome:
            # Erro que aparece acima de todos os campos
            raise forms.ValidationError(
                "Você deve selecionar uma equipe existente OU fornecer um nome para uma nova equipe."
            )
        
        # 3. Validação de User
        if User.objects.filter(username=cleaned_data.get("username")).exists():
             self.add_error('username', "Este nome de usuário já está em uso.")

        return cleaned_data

    def save(self):
        # 1. Lida com a criação/vinculação da Equipe
        equipe = self.cleaned_data.get('equipe_existente')
        if not equipe:
            # Cria a nova equipe se nenhuma existente foi selecionada
            equipe = Equipe.objects.create(
                nome=self.cleaned_data['nova_equipe_nome'],
                cidade=self.cleaned_data['nova_equipe_cidade'],
                patrocinador=self.cleaned_data['nova_equipe_patrocinador']
            )

        # 2. Cria o Usuário (User)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        # 3. Cria o Perfil de Piloto e o vincula ao User e à Equipe
        Piloto.objects.create(
            usuario=user,
            nome=self.cleaned_data['nome_piloto'],
            data_nascimento=self.cleaned_data['data_nascimento'],
            documento=self.cleaned_data['documento'],
            categoria=self.cleaned_data['categoria'],
            equipe=equipe
        )

        return user