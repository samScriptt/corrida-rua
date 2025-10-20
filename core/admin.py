from django.contrib import admin
from .models import Equipe, Piloto, Carro, Pista, Corrida, Inscricao

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "patrocinador")
    search_fields = ("nome", "cidade", "patrocinador")
    ordering = ("nome",)

@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "equipe")
    list_filter = ("categoria", "equipe")
    search_fields = ("nome", "documento")
    autocomplete_fields = ("equipe",)

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("modelo", "placa", "ano", "equipe")
    list_filter = ("ano", "equipe")
    search_fields = ("modelo", "placa")
    autocomplete_fields = ("equipe",)

@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "extensao_km")
    search_fields = ("nome", "cidade")

class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 0
    autocomplete_fields = ("piloto", "carro")

@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    list_display = ("nome", "data", "categoria", "status", "pista")
    list_filter = ("categoria", "status", "pista")
    search_fields = ("nome",)
    date_hierarchy = "data"
    autocomplete_fields = ("pista",)
    inlines = [InscricaoInline]

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ("corrida", "numero_largada", "piloto", "carro", "situacao")
    list_filter = ("situacao", "corrida")
    search_fields = ("piloto__nome", "carro__placa")
    autocomplete_fields = ("corrida", "piloto", "carro")
