import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_detector_model.pkl"
)

model = joblib.load(MODEL_PATH)


def analisar_cadastro(
    idade: int,
    email_descartavel: int,
    tentativas_cpf: int,
    nome_email_diferente: int
):

    entrada = pd.DataFrame([{
        "user_age": idade,
        "is_disposable_email": email_descartavel,
        "recent_cpf_attempts": tentativas_cpf,
        "name_email_mismatch": nome_email_diferente
    }])

    predicao = model.predict(entrada)[0]

    score = 0
    motivos = []

    # Regras de risco
    if email_descartavel:
        score += 40
        motivos.append("Email temporário detectado")

    if tentativas_cpf >= 3:
        score += 40
        motivos.append("Múltiplas tentativas utilizando o mesmo CPF")

    if nome_email_diferente:
        score += 20
        motivos.append("Nome incompatível com email informado")

    # Peso da previsão do modelo
    if predicao == 1:
        score += 30

    score = min(score, 100)

    # Define status baseado no score final
    if score > 75:
        status = "fraude"
    elif score >= 40:
        status = "suspeito"
    else:
        status = "aprovado"

    return {
        "score_risco": score,
        "status": status,
        "motivos": motivos
    }