from django.db import models  # importa o módulo de models do Django, que cria tabelas no banco

# ----------------------------
# Modelo da Equipe
# ----------------------------
class Equipe(models.Model):  # cada classe dessas vira uma tabela no banco
    nome = models.CharField("Nome da equipe", max_length=120)  # texto curto (até 120 caracteres)
    cidade = models.CharField("Cidade", max_length=80, blank=True)  # pode deixar em branco
    patrocinador = models.CharField("Patrocinador", max_length=120, blank=True)  # idem

    class Meta:
        ordering = ["nome"]  # ordena por nome quando listar no admin

    def __str__(self):  # define o que aparece como nome no admin
        return self.nome


# ----------------------------
# Modelo do Piloto
# ----------------------------
class Piloto(models.Model):
    CATEGORIAS = [
        ("A", "A"),  # opções fixas
        ("B", "B"),
        ("PRO-AM", "PRO-AM"),
    ]

    nome = models.CharField("Nome do piloto", max_length=120)
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    documento = models.CharField("Documento", max_length=30, blank=True)
    categoria = models.CharField("Categoria", max_length=10, choices=CATEGORIAS, default="A")  # cria um select no admin
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name="pilotos")
    # FK = chave estrangeira (liga o piloto à equipe)
    # SET_NULL = se apagar a equipe, o campo vira NULL (piloto não é apagado)
    # related_name = nome pra acessar do outro lado (ex: equipe.pilotos.all())

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.categoria})"  # exibe "Caio (A)" no admin


# ----------------------------
# Modelo do Carro
# ----------------------------
class Carro(models.Model):
    modelo = models.CharField("Modelo", max_length=120)
    placa = models.CharField("Placa", max_length=10, unique=True)  # placa tem que ser única
    ano = models.PositiveIntegerField("Ano")  # número inteiro positivo
    cor = models.CharField("Cor", max_length=40, blank=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name="carros")

    class Meta:
        ordering = ["modelo", "placa"]

    def __str__(self):
        return f"{self.modelo} - {self.placa}"


# ----------------------------
# Modelo da Pista
# ----------------------------
class Pista(models.Model):
    nome = models.CharField("Nome da pista", max_length=120)
    cidade = models.CharField("Cidade", max_length=80)
    extensao_km = models.DecimalField("Extensão (km)", max_digits=5, decimal_places=2)  # tipo 3.50 km

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.cidade}"


# ----------------------------
# Modelo da Corrida
# ----------------------------
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
    # PROTECT = não deixa apagar pista se ela tiver corrida

    class Meta:
        ordering = ["-data", "nome"]  # mostra corridas mais recentes primeiro

    def __str__(self):
        return f"{self.nome} ({self.data})"


# ----------------------------
# Modelo da Inscrição
# ----------------------------
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
        unique_together = [("corrida", "numero_largada"), ("corrida", "piloto")]
        # garante que número e piloto não se repitam na mesma corrida
        ordering = ["corrida", "numero_largada"]

    def __str__(self):
        return f"{self.corrida} - #{self.numero_largada} - {self.piloto}"
