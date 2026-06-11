# src/predict.py
import os
import joblib
import pandas as pd
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_detector_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "model_features.json")

model = joblib.load(MODEL_PATH)

# Carregar features usadas no treinamento
with open(FEATURES_PATH, 'r') as f:
    trained_features = json.load(f)

def analisar_cadastro(
    idade: int,
    email_descartavel: int,
    tentativas_cpf: int,
    nome_email_diferente: int
):
    # Criar DataFrame base
    entrada_dict = {
        "user_age": idade,
        "is_disposable_email": email_descartavel,
        "recent_cpf_attempts": tentativas_cpf,
        "name_email_mismatch": nome_email_diferente,
        "age_squared": idade ** 2,
        "risk_score": (email_descartavel * 2 + 
                      tentativas_cpf * 1.5 + 
                      nome_email_diferente * 1.2)
    }
    
    # Filtrar apenas features usadas no treinamento
    entrada_filtrada = {k: entrada_dict[k] for k in trained_features if k in entrada_dict}
    
    entrada = pd.DataFrame([entrada_filtrada])
    
    # Previsão do modelo
    predicao = model.predict(entrada)[0]
    
    # Probabilidade se disponível
    if hasattr(model, 'predict_proba'):
        probabilidade = model.predict_proba(entrada)[0][1]
    else:
        probabilidade = float(predicao)
    
    # Score baseado na probabilidade
    score_base = probabilidade * 100
    
    # Regras de negócio complementares
    score = 0
    motivos = []
    
    if email_descartavel:
        score += 30
        motivos.append("Email temporário detectado")
    
    if tentativas_cpf >= 3:
        score += 35
        motivos.append("Múltiplas tentativas com mesmo CPF")
    
    if nome_email_diferente:
        score += 20
        motivos.append("Nome incompatível com email")
    
    # Combinar score do modelo com regras
    score_final = (score_base * 0.6 + score * 0.4)
    score_final = min(score_final, 100)
    
    # Status
    if score_final > 75:
        status = "fraude"
    elif score_final >= 40:
        status = "suspeito"
    else:
        status = "aprovado"
    
    return {
        "score_risco": round(score_final, 2),
        "status": status,
        "motivos": motivos,
        "probabilidade_modelo": round(probabilidade * 100, 2),
        "predicao_modelo": int(predicao)
    }