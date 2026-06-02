import csv
import os
import random

os.makedirs("data", exist_ok=True)

# Common secure domains vs disposable/temporary fraud domains
trusted_domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
disposable_domains = ["mailinator.com", "sharklasers.com", "getairmail.com", "tempmail.de"]

print("Generating synthetic data for the AI model...")

with open("data/training_records.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f) 
    
    # Dataset Header (Features)
    # target: 0 = Legitimate User, 1 = Identity Fraud Attempt
    writer.writerow([
        "user_age", 
        "is_disposable_email", 
        "recent_cpf_attempts", 
        "name_email_mismatch", 
        "target"
    ])
    
    for _ in range(1000):
        # 85% of the data will simulate legitimate users
        if random.random() > 0.15:
            age = random.randint(18, 70)
            is_disposable = 0  # Uses a trusted domain
            cpf_attempts = random.randint(1, 2)
            mismatch = random.choice([0, 0, 0, 1])  # Low chance of mismatch
            target = 0
        # 15% of the data will simulate fraud patterns
        else:
            age = random.randint(16, 85)
            is_disposable = random.choice([0, 1, 1])  # High chance of temporary email
            cpf_attempts = random.randint(3, 8)       # Multiple sign-up attempts with same document
            mismatch = random.choice([0, 1, 1])      # Name doesn't align with email string
            target = 1
            
        writer.writerow([age, is_disposable, cpf_attempts, mismatch, target])

print("File 'data/training_records.csv' successfully generated with 1000 records!")