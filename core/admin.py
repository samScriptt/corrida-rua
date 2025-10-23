from django.contrib import admin  # importa o admin do Django
from .models import Equipe, Piloto, Carro, Pista, Corrida, Inscricao  # importa nossos modelos


# ----------------------------
# Admin da Equipe
# ----------------------------
@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "patrocinador")  # mostra essas colunas na listagem
    search_fields = ("nome", "cidade", "patrocinador")  # campo de busca
    ordering = ("nome",)  # ordenação padrão


# ----------------------------
# Admin do Piloto
# ----------------------------
@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "equipe")
    list_filter = ("categoria", "equipe")  # filtros laterais
    search_fields = ("nome", "documento")
    autocomplete_fields = ("equipe",)  # campo de seleção com busca


# ----------------------------
# Admin do Carro
# ----------------------------
@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("modelo", "placa", "ano", "equipe")
    list_filter = ("ano", "equipe")
    search_fields = ("modelo", "placa")
    autocomplete_fields = ("equipe",)


# ----------------------------
# Admin da Pista
# ----------------------------
@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "extensao_km")
    search_fields = ("nome", "cidade")


# ----------------------------
# Inline de Inscrição (pra aparecer dentro da Corrida)
# ----------------------------
class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 0  # não mostra linhas vazias a mais
    autocomplete_fields = ("piloto", "carro")  # busca rápida


# ----------------------------
# Admin da Corrida
# ----------------------------
@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    list_display = ("nome", "data", "categoria", "status", "pista")
    list_filter = ("categoria", "status", "pista")
    search_fields = ("nome",)
    date_hierarchy = "data"  # cria navegação por data no topo
    autocomplete_fields = ("pista",)
    inlines = [InscricaoInline]  # mostra as inscrições dentro da corrida


# ----------------------------
# Admin da Inscrição (caso queira acessar separadamente)
# ----------------------------
@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ("corrida", "numero_largada", "piloto", "carro", "situacao")
    list_filter = ("situacao", "corrida")
    search_fields = ("piloto__nome", "carro__placa")  # "__" faz busca por relação
    autocomplete_fields = ("corrida", "piloto", "carro")

