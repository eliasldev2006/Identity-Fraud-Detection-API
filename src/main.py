from fastapi import FastAPI, HTTPException

from src.schemas import CadastroRequest
from src.predict import analisar_cadastro

app = FastAPI(
    title="Identity Fraud Detection API",
    version="1.0.0"
)

# contador simples para demonstração
cpf_tentativas = {}

DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "sharklasers.com",
    "getairmail.com",
    "tempmail.de"
}


def verificar_email_descartavel(email: str) -> int:
    dominio = email.split("@")[-1].lower()

    return 1 if dominio in DISPOSABLE_DOMAINS else 0


def verificar_nome_email(nome: str, email: str) -> int:

    usuario = email.split("@")[0].lower()

    for parte in nome.lower().split():
        if parte in usuario:
            return 0

    return 1


@app.get("/")
def home():
    return {
        "status": "online"
    }


@app.post("/api/v1/cadastro")
def cadastrar(dados: CadastroRequest):

    cpf = dados.cpf

    cpf_tentativas[cpf] = cpf_tentativas.get(cpf, 0) + 1

    resultado = analisar_cadastro(
        idade=dados.idade,
        email_descartavel=verificar_email_descartavel(
            dados.email
        ),
        tentativas_cpf=cpf_tentativas[cpf],
        nome_email_diferente=verificar_nome_email(
            dados.nome,
            dados.email
        )
    )

    if resultado["score_risco"] > 75:
        raise HTTPException(
            status_code=403,
            detail=resultado
        )

    return resultado