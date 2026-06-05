import requests
import time

URL = "http://127.0.0.1:8000/api/v1/cadastro"

casos = [
    {
        "descricao": "Usuário legítimo",
        "dados": {
            "nome": "Joao Pedro",
            "email": "joao@gmail.com",
            "cpf": "12345678901",
            "idade": 22
        }
    },
    {
        "descricao": "Email temporário",
        "dados": {
            "nome": "Joao Silva",
            "email": "joao@mailinator.com",
            "cpf": "98765432100",
            "idade": 25
        }
    },
    {
        "descricao": "Nome incompatível com email",
        "dados": {
            "nome": "Maria Oliveira",
            "email": "carlos123@gmail.com",
            "cpf": "55544433322",
            "idade": 30
        }
    },
    {
        "descricao": "Email temporário + nome incompatível",
        "dados": {
            "nome": "Ana Costa",
            "email": "hacker@mailinator.com",
            "cpf": "11122233344",
            "idade": 28
        }
    },
    {
        "descricao": "Fraude potencial",
        "dados": {
            "nome": "Pedro Silva",
            "email": "fraudador@mailinator.com",
            "cpf": "11111111111",
            "idade": 19
        }
    }
]

print("=" * 70)
print("TESTES DA API DE DETECÇÃO DE FRAUDE")
print("=" * 70)

for i, caso in enumerate(casos, start=1):

    print(f"\nCASO {i} - {caso['descricao']}")
    print("-" * 70)

    resposta = requests.post(URL, json=caso["dados"])

    print("Status HTTP:", resposta.status_code)

    try:
        print("Resposta:")
        print(resposta.json())
    except:
        print(resposta.text)

    time.sleep(1)

# Teste especial de múltiplas tentativas com o mesmo CPF

print("\n")
print("=" * 70)
print("TESTE DE MÚLTIPLAS TENTATIVAS COM O MESMO CPF")
print("=" * 70)

cpf_repetido = {
    "nome": "Teste Fraudador",
    "email": "teste@mailinator.com",
    "cpf": "99999999999",
    "idade": 20
}

for tentativa in range(1, 6):

    print(f"\nTentativa {tentativa}")

    resposta = requests.post(URL, json=cpf_repetido)

    print("Status HTTP:", resposta.status_code)

    try:
        print(resposta.json())
    except:
        print(resposta.text)

    time.sleep(1)

print("\n")
print("=" * 70)
print("TESTES FINALIZADOS")
print("=" * 70)