# src/train_model.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1. Load dataset
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(base_dir, "data", "training_records.csv")
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please run generate_data.py first.")

print(f"📂 Loading dataset from: {dataset_path}")
df = pd.read_csv(dataset_path)

# Verificar balanceamento
print(f"\n📊 Distribuição das classes:")
print(df['target'].value_counts())
print(f"Taxa de fraude: {df['target'].mean()*100:.2f}%")

# 2. Split features (X) and target (y)
X = df.drop('target', axis=1)
y = df['target']

# Adicionar feature engineering simples
X['age_squared'] = X['user_age'] ** 2  # Feature polinomial
X['risk_score'] = (X['is_disposable_email'] * 2 + 
                   X['recent_cpf_attempts'] * 1.5 + 
                   X['name_email_mismatch'] * 1.2)  # Score composto

print(f"\n🔧 Features utilizadas: {list(X.columns)}")

# 3. Variações do Random Forest com parâmetros mais conservadores
rf_variations = {
    "RandomForest_Conservador": {
        "n_estimators": 50,
        "max_depth": 5,
        "min_samples_split": 20,
        "min_samples_leaf": 10,
        "max_features": 'sqrt',
        "random_state": 42
    },
    "RandomForest_Moderado": {
        "n_estimators": 100,
        "max_depth": 8,
        "min_samples_split": 10,
        "min_samples_leaf": 5,
        "max_features": 'sqrt',
        "random_state": 42
    },
    "RandomForest_Agressivo": {
        "n_estimators": 150,
        "max_depth": 12,
        "min_samples_split": 5,
        "min_samples_leaf": 2,
        "max_features": 'sqrt',
        "random_state": 42
    },
    "GradientBoosting": {
        "n_estimators": 100,
        "max_depth": 3,
        "learning_rate": 0.1,
        "min_samples_split": 10,
        "min_samples_leaf": 5,
        "random_state": 42
    }
}

# 4. Splits para teste
test_sizes = {
    "80/20": 0.20,
    "70/30": 0.30,
    "60/40": 0.40
}

# 5. Cross-validation estratificada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 6. Armazenar resultados
resultados = []

print("\n" + "=" * 80)
print("🔬 COMPARATIVO DE MODELOS - COM VALIDAÇÃO RIGOROSA")
print("=" * 80)

for model_name, params in rf_variations.items():
    for split_name, test_size in test_sizes.items():
        print(f"\n{'='*60}")
        print(f"📊 Modelo: {model_name} | Split: {split_name}")
        print(f"{'='*60}")
        
        # Split estratificado
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Criar modelo apropriado
        if model_name == "GradientBoosting":
            model = GradientBoostingClassifier(**params)
        else:
            model = RandomForestClassifier(**params)
        
        # Treinar
        model.fit(X_train, y_train)
        
        # Previsões
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        y_test_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Métricas detalhadas
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        overfitting_gap = train_accuracy - test_accuracy
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        # Matriz de confusão
        tn, fp, fn, tp = confusion_matrix(y_test, y_test_pred).ravel()
        
        # Métricas por classe
        precision_fraud = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall_fraud = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_fraud = 2 * (precision_fraud * recall_fraud) / (precision_fraud + recall_fraud) if (precision_fraud + recall_fraud) > 0 else 0
        
        # AUC-ROC
        if y_test_proba is not None and len(np.unique(y_test)) > 1:
            auc_roc = roc_auc_score(y_test, y_test_proba)
        else:
            auc_roc = 0.5
        
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(X.columns, model.feature_importances_))
        else:
            feature_importance = {}
        
        resultado = {
            "modelo": model_name,
            "split": split_name,
            "parametros": params,
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "overfitting_gap": overfitting_gap,
            "cv_mean": cv_mean,
            "cv_std": cv_std,
            "auc_roc": auc_roc,
            "precision_fraud": precision_fraud,
            "recall_fraud": recall_fraud,
            "f1_fraud": f1_fraud,
            "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
            "feature_importance": feature_importance
        }
        resultados.append(resultado)
        
        # Exibir resultados
        print(f"\n📈 MÉTRICAS:")
        print(f"  • Acurácia Treino:     {train_accuracy*100:.2f}%")
        print(f"  • Acurácia Teste:      {test_accuracy*100:.2f}%")
        print(f"  • Gap Overfitting:     {overfitting_gap*100:.2f}%")
        print(f"  • CV Mean (5-fold):    {cv_mean*100:.2f}% (±{cv_std*100:.2f}%)")
        print(f"  • AUC-ROC:             {auc_roc*100:.2f}%")
        print(f"  • Precisão (Fraude):   {precision_fraud*100:.2f}%")
        print(f"  • Recall (Fraude):     {recall_fraud*100:.2f}%")
        print(f"  • F1-Score (Fraude):   {f1_fraud*100:.2f}%")
        
        print(f"\n📊 MATRIZ DE CONFUSÃO:")
        print(f"  • Verdadeiros Negativos:  {tn}")
        print(f"  • Falsos Positivos:       {fp}")
        print(f"  • Falsos Negativos:       {fn}")
        print(f"  • Verdadeiros Positivos:  {tp}")
        
        # Diagnóstico
        if overfitting_gap > 0.05:
            print(f"  ⚠️  OVERFITTING: Gap elevado ({overfitting_gap*100:.1f}%)")
        elif test_accuracy > 0.95:
            print(f"  ⚠️  POSSÍVEL DATA LEAKAGE: Acurácia muito alta ({test_accuracy*100:.1f}%)")
        else:
            print(f"  ✅ Modelo saudável")

# 7. Seleção do melhor modelo
print("\n" + "=" * 80)
print("🏆 SELEÇÃO DO MELHOR MODELO")
print("=" * 80)

resultados_df = pd.DataFrame(resultados)

# Score composto: penaliza overfitting e recompensa generalização
resultados_df['overfitting_penalty'] = np.where(
    resultados_df['overfitting_gap'] > 0.03, 
    resultados_df['overfitting_gap'] * 2,  # Penalidade dobrada se gap > 3%
    0
)

resultados_df['score_final'] = (
    resultados_df['test_accuracy'] * 0.25 +           # 25% acurácia
    resultados_df['cv_mean'] * 0.30 +                 # 30% cross-validation
    resultados_df['auc_roc'] * 0.15 +                 # 15% AUC-ROC
    resultados_df['f1_fraud'] * 0.15 +                # 15% F1-Score fraude
    (1 - resultados_df['overfitting_gap']) * 0.15 -   # 15% anti-overfitting
    resultados_df['overfitting_penalty']               # Penalidade extra
)

# Filtrar modelos com overfitting excessivo
modelos_validos = resultados_df[resultados_df['overfitting_gap'] <= 0.05]

if len(modelos_validos) == 0:
    print("\n⚠️  Nenhum modelo sem overfitting. Selecionando o melhor disponível...")
    modelos_validos = resultados_df

melhor = modelos_validos.loc[modelos_validos['score_final'].idxmax()]

print(f"\n✅ Melhor modelo: {melhor['modelo']}")
print(f"✅ Melhor split: {melhor['split']}")
print(f"✅ Acurácia teste: {melhor['test_accuracy']*100:.2f}%")
print(f"✅ CV Mean: {melhor['cv_mean']*100:.2f}%")
print(f"✅ Overfitting gap: {melhor['overfitting_gap']*100:.2f}%")
print(f"✅ F1-Score Fraude: {melhor['f1_fraud']*100:.2f}%")
print(f"✅ Score final: {melhor['score_final']:.4f}")

# 8. Treinar modelo final
print("\n" + "=" * 80)
print("🎯 TREINANDO MODELO FINAL PARA PRODUÇÃO")
print("=" * 80)

test_size_final = test_sizes[melhor['split']]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size_final, random_state=42, stratify=y
)

if melhor['modelo'] == "GradientBoosting":
    modelo_final = GradientBoostingClassifier(**melhor['parametros'])
else:
    modelo_final = RandomForestClassifier(**melhor['parametros'])

modelo_final.fit(X_train, y_train)

# Avaliação final detalhada
y_pred_final = modelo_final.predict(X_test)
y_proba_final = modelo_final.predict_proba(X_test)[:, 1] if hasattr(modelo_final, 'predict_proba') else None

print(f"\n📊 RELATÓRIO FINAL DETALHADO:")
print(classification_report(y_test, y_pred_final, 
                           target_names=['Legítimo', 'Fraude']))

# Feature importance final
if hasattr(modelo_final, 'feature_importances_'):
    print("\n🔑 IMPORTÂNCIA DAS FEATURES:")
    for name, importance in sorted(zip(X.columns, modelo_final.feature_importances_), 
                                   key=lambda x: x[1], reverse=True):
        print(f"  • {name}: {importance:.4f}")

# 9. Salvar modelo e pipeline
os.makedirs('models', exist_ok=True)

# Salvar modelo
model_output_path = os.path.join("models", "fraud_detector_model.pkl")
joblib.dump(modelo_final, model_output_path)
print(f"\n✅ Modelo salvo em: {model_output_path}")

# Salvar features usadas
features_path = os.path.join("models", "model_features.json")
with open(features_path, 'w') as f:
    json.dump(list(X.columns), f)
print(f"✅ Features salvas em: {features_path}")

# Salvar metadados
metadata = {
    "data_treinamento": datetime.now().isoformat(),
    "modelo_selecionado": melhor['modelo'],
    "split_selecionado": melhor['split'],
    "parametros": melhor['parametros'],
    "features": list(X.columns),
    "metricas": {
        "accuracy_teste": float(melhor['test_accuracy']),
        "cv_mean": float(melhor['cv_mean']),
        "cv_std": float(melhor['cv_std']),
        "overfitting_gap": float(melhor['overfitting_gap']),
        "auc_roc": float(melhor['auc_roc']),
        "f1_fraud": float(melhor['f1_fraud']),
        "precision_fraud": float(melhor['precision_fraud']),
        "recall_fraud": float(melhor['recall_fraud'])
    },
    "total_registros": len(df),
    "distribuicao_classes": df['target'].value_counts().to_dict(),
    "comparativo": resultados_df[['modelo', 'split', 'test_accuracy', 'overfitting_gap', 'cv_mean', 'f1_fraud', 'score_final']].to_dict('records')
}

metadata_path = os.path.join("models", "model_metadata.json")
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)
print(f"✅ Metadados salvos em: {metadata_path}")

# 10. Resumo visual
print("\n" + "=" * 80)
print("📊 RESUMO COMPARATIVO FINAL")
print("=" * 80)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
print(resultados_df[['modelo', 'split', 'test_accuracy', 'overfitting_gap', 'cv_mean', 'f1_fraud']].to_string())

print("\n✅ Treinamento concluído com sucesso!")