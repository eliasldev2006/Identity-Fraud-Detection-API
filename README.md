# Identity Fraud Detection API

Sistema de detecção de fraude em cadastros utilizando **FastAPI**, **Machine Learning (Random Forest)** e validação de dados com **Pydantic**.

## Objetivo

O projeto analisa tentativas de cadastro e identifica possíveis fraudes com base em:

* Uso de e-mails temporários
* Múltiplas tentativas utilizando o mesmo CPF
* Incompatibilidade entre nome e e-mail
* Predição realizada por um modelo de Machine Learning treinado com dados sintéticos

---

## Tecnologias Utilizadas

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Machine Learning

* Pandas
* Scikit-Learn
* Random Forest Classifier
* Joblib

### Utilitários

* Python Dotenv
* Email Validator

---

## Estrutura do Projeto

```text
IDENTITY-FRAUD-DETECTION/
│
├── data/
│   └── training_records.csv
│
├── models/
│   └── fraud_detector_model.pkl
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── predict.py
│   ├── schemas.py
│   ├── train_model.py
│   └── testes_api.py
│
├── data_generator.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instalação

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd IDENTITY-FRAUD-DETECTION
```

### 2. Criar Ambiente Virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## Geração da Base de Dados

Gerar o conjunto de dados sintético:

```bash
python data_generator.py
```

Arquivo gerado:

```text
data/training_records.csv
```

---

## Treinamento do Modelo

Treinar o modelo de Machine Learning:

```bash
python src/train_model.py
```

Ao final será criado:

```text
models/fraud_detector_model.pkl
```

---

## Executando a API

Iniciar o servidor FastAPI:

```bash
uvicorn src.main:app --reload
```

Servidor disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Endpoint Principal

### POST /api/v1/cadastro

Exemplo de requisição:

```json
{
  "nome": "Joao Pedro",
  "email": "joao@gmail.com",
  "cpf": "12345678901",
  "idade": 22
}
```

Exemplo de resposta:

```json
{
  "score_risco": 0,
  "status": "aprovado",
  "motivos": []
}
```

---

## Como Testar

### Opção 1 — Swagger

Acesse:

```text
http://127.0.0.1:8000/docs
```

1. Selecione o endpoint `POST /api/v1/cadastro`
2. Clique em **Try it out**
3. Insira um JSON de teste
4. Clique em **Execute**

---

### Opção 2 — Script Automatizado

Executar:

```bash
python src/testes_api.py
```

O script realiza diversos cenários de teste automaticamente.

---

## Casos de Teste

### Usuário Legítimo

```json
{
  "nome": "Joao Pedro",
  "email": "joao@gmail.com",
  "cpf": "12345678901",
  "idade": 22
}
```

Resultado esperado:

```json
{
  "score_risco": 0,
  "status": "aprovado"
}
```

---

### Email Temporário

```json
{
  "nome": "Joao Silva",
  "email": "joao@mailinator.com",
  "cpf": "98765432100",
  "idade": 25
}
```

Resultado esperado:

```json
{
  "status": "suspeito"
}
```

---

### Múltiplas Tentativas com o Mesmo CPF

Enviar diversas vezes:

```json
{
  "nome": "Teste Fraudador",
  "email": "teste@mailinator.com",
  "cpf": "99999999999",
  "idade": 20
}
```

Resultado esperado:

```json
{
  "status": "fraude"
}
```

Retorno HTTP:

```text
403 Forbidden
```

---

## Regras de Negócio

* Score de risco calculado entre 0 e 100.
* Score maior que 75 resulta em bloqueio automático.
* E-mails temporários aumentam o score de risco.
* Múltiplas tentativas com o mesmo CPF aumentam o score de risco.
* Incompatibilidade entre nome e e-mail aumenta o score de risco.
* O modelo de Machine Learning contribui para a classificação final.

---

## Autores

* Elias — Engenharia de Prompt, Dados e Modelo
* Erick — API, Rotas FastAPI, Integração e Testes

```
```
