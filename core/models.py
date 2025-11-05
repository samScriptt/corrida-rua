from django.db import models
from django.contrib.auth.models import User 

class Equipe(models.Model):
    nome = models.CharField("Nome da equipe", max_length=120)
    cidade = models.CharField("Cidade", max_length=80, blank=True)
    patrocinador = models.CharField("Patrocinador", max_length=120, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Piloto(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="piloto_profile",
        null=True,  # Permite que o valor seja NULO no banco
        blank=True  # Permite que o campo fique em branco em formulários
    )
    CATEGORIAS = [
        ("A", "A"),
        ("B", "B"),
        ("PRO-AM", "PRO-AM"),
    ]
    nome = models.CharField("Nome do piloto", max_length=120)
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    documento = models.CharField("Documento", max_length=30, blank=True)
    categoria = models.CharField("Categoria", max_length=10, choices=CATEGORIAS, default="A")
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name="pilotos")

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.categoria})"


class Carro(models.Model):
    modelo = models.CharField("Modelo", max_length=120)
    placa = models.CharField("Placa", max_length=10, unique=True)
    ano = models.PositiveIntegerField("Ano")
    cor = models.CharField("Cor", max_length=40, blank=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name="carros")

    class Meta:
        ordering = ["modelo", "placa"]

    def __str__(self):
        return f"{self.modelo} - {self.placa}"


class Pista(models.Model):
    nome = models.CharField("Nome da pista", max_length=120)
    cidade = models.CharField("Cidade", max_length=80)
    extensao_km = models.DecimalField("Extensão (km)", max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.cidade}"


class Corrida(models.Model):
    STATUS = [
        ("PLANEJADA", "Planejada"),
        ("EM_ANDAMENTO", "Em andamento"),
        ("ENCERRADA", "Encerrada"),
    ]
    CATEGORIAS = [
        ("STREET", "Street"),
        ("DRAG", "Drag"),
        ("DRIFT", "Drift"),
    ]
    nome = models.CharField("Nome da corrida", max_length=120)
    data = models.DateField("Data")
    status = models.CharField("Status", max_length=20, choices=STATUS, default="PLANEJADA")
    categoria = models.CharField("Categoria", max_length=20, choices=CATEGORIAS, default="STREET")
    pista = models.ForeignKey(Pista, on_delete=models.PROTECT, related_name="corridas")

    class Meta:
        ordering = ["-data", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.data})"


class Inscricao(models.Model):
    SITUACAO = [
        ("APROVADA", "Aprovada"),
        ("PENDENTE", "Pendente"),
        ("INDEFERIDA", "Indeferida"),
    ]
    corrida = models.ForeignKey(Corrida, on_delete=models.CASCADE, related_name="inscricoes")
    piloto = models.ForeignKey(Piloto, on_delete=models.PROTECT, related_name="inscricoes")
    carro = models.ForeignKey(Carro, on_delete=models.PROTECT, related_name="inscricoes")
    numero_largada = models.PositiveIntegerField("Número de largada")
    situacao = models.CharField("Situação", max_length=10, choices=SITUACAO, default="PENDENTE")

    class Meta:
        unique_together = [
            ("corrida", "numero_largada"),
            ("corrida", "piloto"),
        ]
        ordering = ["corrida", "numero_largada"]

    def __str__(self):
        return f"{self.corrida} - #{self.numero_largada} - {self.piloto}"
