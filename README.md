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
      unique (corrida_id, numero_largada)
      unique (corrida_id, piloto_id)
    }
