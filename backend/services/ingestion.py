import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

db_path = BASE_DIR.parent.parent / "database" / "gym.db"
file_path = BASE_DIR.parent / "data" / "raw" / "workouts.csv"

def get_connection():
    return sqlite3.connect(db_path)

# garante pasta do banco
db_path.parent.mkdir(parents=True, exist_ok=True)


# leitura
df = pd.read_csv(file_path)

# conexão
conn = sqlite3.connect(db_path)

# cria tabela e insere dados
df.to_sql("workouts", conn, if_exists="replace", index=False)

# fechar conexão
conn.close()

print("Dados inseridos com sucesso!")