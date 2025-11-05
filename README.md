# 🏁 Sistema de Gestão de Corridas

Projeto desenvolvido em **Django** para gerenciar equipes, pilotos, carros, pistas e corridas, com interface administrativa integrada.

---

## 🚀 Como Executar o Projeto

### 1️⃣ Criar e ativar o ambiente virtual

Abra o terminal na pasta do projeto e execute:

#### Linux / Mac:
```bash
python -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2️⃣ Instalar dependências
```bash
pip install django
```

---

### 3️⃣ Rodar migrações iniciais
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Iniciar o servidor
```bash
python manage.py runserver
```

Depois abra no navegador:

👉 **http://127.0.0.1:8000/**

---

## 🧩 Diagrama Entidade-Relacionamento (ER)

```mermaid
erDiagram

    EQUIPE ||--o{ PILOTO : "tem"
    EQUIPE ||--o{ CARRO  : "tem"
    PILOTO ||--o{ INSCRICAO : "participa"
    CARRO  ||--o{ INSCRICAO : "é inscrito com"
    CORRIDA ||--o{ INSCRICAO : "recebe"
    PISTA  ||--o{ CORRIDA : "ocorre em"

    EQUIPE {
      int id PK
      string nome
      string cidade
      string patrocinador
    }

    PILOTO {
      int id PK
      string nome
      date data_nascimento
      string documento
      string categoria   "A/B/PRO-AM"
      int equipe_id FK
    }

    CARRO {
      int id PK
      string modelo
      string placa
      int ano
      string cor
      int equipe_id FK
    }

    PISTA {
      int id PK
      string nome
      string cidade
      decimal extensao_km
    }

    CORRIDA {
      int id PK
      string nome
      date data
      string status      "PLANEJADA/EM_ANDAMENTO/ENCERRADA"
      string categoria   "STREET/DRAG/DRIFT"
      int pista_id FK
    }

    INSCRICAO {
      int id PK
      int corrida_id FK
      int piloto_id  FK
      int carro_id   FK
      int numero_largada
      string situacao  "APROVADA/PENDENTE/INDEFERIDA"
      %% restrições únicas: (corrida_id, numero_largada), (corrida_id, piloto_id)
    }
```
