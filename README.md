# 🗳 Voting API  
### FastAPI + SQLAlchemy 2.0 + MySQL

Sistema de votaciones desarrollado como prueba técnica aplicando buenas prácticas de arquitectura backend, separación por capas y validaciones de negocio.

---

## 🚀 Características Principales

✔ Registro de votantes  
✔ Registro de candidatos  
✔ Emisión de voto único por votante  
✔ Estadísticas en tiempo real  
✔ Validaciones de integridad de datos  
✔ Manejo adecuado de errores HTTP (404, 409)  
✔ Arquitectura en capas (Repository + Service Pattern)  

---

## 🛠 Stack Tecnológico

| Tecnología | Uso |
|------------|------|
| **Python 3.10+** | Lenguaje principal |
| **FastAPI** | Framework REST |
| **SQLAlchemy 2.0** | ORM moderno |
| **MySQL** | Base de datos relacional |
| **Pydantic** | Validación de datos |
| **Uvicorn** | Servidor ASGI |

---

## 🏗 Arquitectura del Proyecto

El proyecto está organizado siguiendo separación de responsabilidades:

```
app/
│
├── api/            → Endpoints (Controllers)
├── services/       → Lógica de negocio
├── repositories/   → Acceso a datos (CRUD)
├── models/         → Modelos ORM
├── schemas/        → Validaciones Pydantic
├── db/             → Configuración de base de datos
└── core/           → Configuración general
```

### 🔎 Principios aplicados

- Clean Architecture (adaptada)
- Repository Pattern
- Service Layer Pattern
- Validaciones de negocio centralizadas
- Transacciones controladas

---

# ⚙ Instalación y Ejecución

## 1️⃣ Clonar el repositorio

Abrir Git Bash o PowerShell:

```bash
git clone https://github.com/montoyarua/voting-api-fastapi.git
cd voting-api-fastapi
```

---

## 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

```bash
venv\Scripts\activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar Base de Datos

Abrir MySQL Workbench y ejecutar:

```sql
CREATE DATABASE IF NOT EXISTS voting_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'voting_user'@'localhost' IDENTIFIED BY 'voting_pass';
GRANT ALL PRIVILEGES ON voting_db.* TO 'voting_user'@'localhost';
FLUSH PRIVILEGES;
```

Si usas 127.0.0.1:

```sql
CREATE USER IF NOT EXISTS 'voting_user'@'127.0.0.1' IDENTIFIED BY 'voting_pass';
GRANT ALL PRIVILEGES ON voting_db.* TO 'voting_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

---

## 5️⃣ Configurar variables de entorno

Copiar `.env.example` y renombrarlo a `.env`

```env
APP_NAME=Voting API
DATABASE_URL=mysql+pymysql://voting_user:voting_pass@localhost:3306/voting_db
```

Si usas `127.0.0.1`, ajustar la URL:

```
DATABASE_URL=mysql+pymysql://voting_user:voting_pass@127.0.0.1:3306/voting_db
```

---

## 6️⃣ Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

Servidor disponible en:

```
http://127.0.0.1:8000
```

---

## 📘 Documentación Interactiva (Swagger)

Disponible en:

```
http://127.0.0.1:8000/docs
```

---

# 📌 Endpoints

## 👥 Voters

| Método | Endpoint |
|--------|----------|
| POST | /voters |
| GET | /voters |
| GET | /voters/{voter_id} |
| DELETE | /voters/{voter_id} |

---

## 🏛 Candidates

| Método | Endpoint |
|--------|----------|
| POST | /candidates |
| GET | /candidates |
| GET | /candidates/{candidate_id} |
| DELETE | /candidates/{candidate_id} |

---

## 🗳 Votes

| Método | Endpoint |
|--------|----------|
| POST | /votes |
| GET | /votes |
| GET | /votes/statistics |

---

# 📊 Estadísticas Incluyen

- Total de votos
- Total de votantes que han votado
- Votos por candidato
- Porcentaje por candidato

Ejemplo de respuesta:

```json
{
  "total_votes": 2,
  "total_voters_voted": 2,
  "by_candidate": [
    {
      "candidate_id": 1,
      "name": "Ana Perez",
      "party": "Verde",
      "votes": 2,
      "percentage": 100.0
    }
  ]
}
```

---

# 🔒 Validaciones Implementadas

✔ Un votante no puede votar más de una vez  
✔ Validación de existencia de voter_id y candidate_id  
✔ Restricción cruzada entre votantes y candidatos  
✔ Actualización automática de `has_voted`  
✔ Incremento automático del contador de votos  
✔ Manejo de errores con códigos HTTP adecuados  

---

# 📸 Evidencia de Funcionamiento

Capturas incluidas en:

```
Images/
```

Ejemplo:

```markdown
### Crear candidato
![Create Candidate](Images/01_postman_create_candidate.png)

### Crear votante
![Create Voter](Images/02_postman_create_voter.png)

### Emitir voto
![Cast Vote](Images/03_postman_cast_vote.png)

### Estadísticas
![Statistics](Images/04_postman_statistics.png)

### Error voto duplicado
![Vote Twice Error](Images/05_postman_vote_twice_error.png)
```

---

# 👨‍💻 Autor

**Juan Jose Montoya Rua**

