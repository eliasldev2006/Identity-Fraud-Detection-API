from fastapi import FastAPI
from src.schemas import CadastroRequest, CadastroResponse

app = FastAPI(
    title="Identity Fraud Detection API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "online",
        "api": "Identity Fraud Detection"
    }


@app.post(
    "/api/v1/cadastro",
    response_model=CadastroResponse
)
def cadastrar_usuario(dados: CadastroRequest):

    score_risco = 0
    motivos = []

    # Regras simples para teste
    if dados.idade < 21:
        score_risco += 10
        motivos.append("idade considerada de risco")

    if len(dados.cpf.replace(".", "").replace("-", "")) != 11:
        score_risco += 50
        motivos.append("cpf inválido")

    if score_risco >= 75:
        status = "fraude"
    elif score_risco >= 40:
        status = "suspeito"
    else:
        status = "aprovado"

    return CadastroResponse(
        score_risco=score_risco,
        status=status,
        motivos=motivos
    )