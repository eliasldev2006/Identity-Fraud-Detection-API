from fastapi import FastAPI
from src.schemas import CadastroRequest

app = FastAPI()

@app.post("/api/v1/cadastro")
def cadastro(dados: CadastroRequest):
    return {
        "status": "recebido",
        "dados": dados.model_dump()
    }