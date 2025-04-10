# ========================================

import pandas as pd

import numpy as np

import random

from datetime import datetime, timedelta



# Criando um log fictício com timestamps, IPs e status de acesso

def gerar_logs_ficticios(qtd=1000):

  ips = [f"192.168.0.{i}" for i in range(1, 256)] # Simula 255 IPs

  status = ["200 OK", "403 Forbidden", "500 Internal Server Error"]

   

  logs = []

  data_inicial = datetime.now() - timedelta(days=7) # Últimos 7 dias

   

  for _ in range(qtd):

    timestamp = data_inicial + timedelta(seconds=random.randint(0, 604800)) # Semana aleatória

    ip = random.choice(ips)

    status_code = random.choice(status)

    logs.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), ip, status_code])

   

  return pd.DataFrame(logs, columns=["Timestamp", "IP", "Status"])



# Gerando e salvando log fictício em CSV

df_logs = gerar_logs_ficticios()

df_logs.to_csv("log_ficticio.csv", index=False)
# ========================================

# ETAPA 1: SIMULAÇÃO E COLETA DE LOGS

# ========================================

import pandas as pd

import numpy as np

import random

from datetime import datetime, timedelta

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.ensemble import IsolationForest



# Criando um log fictício com timestamps, IPs e status de acesso

def gerar_logs_ficticios(qtd=1000):

  ips = [f"192.168.0.{i}" for i in range(1, 256)] # Simula 255 IPs

  status = ["200 OK", "403 Forbidden", "500 Internal Server Error"]

   

  logs = []

  data_inicial = datetime.now() - timedelta(days=7) # Últimos 7 dias

   

  for _ in range(qtd):

    timestamp = data_inicial + timedelta(seconds=random.randint(0, 604800)) # Semana aleatória

    ip = random.choice(ips)

    status_code = random.choice(status)

    logs.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), ip, status_code])

   

  return pd.DataFrame(logs, columns=["Timestamp", "IP", "Status"])



# Gerando e salvando log fictício em CSV

df_logs = gerar_logs_ficticios()

df_logs.to_csv("log_ficticio.csv", index=False)



print("Arquivo de log fictício gerado com sucesso.")



# ========================================

# ETAPA 2: INGESTÃO DOS LOGS

# ========================================

# Carregando os logs do arquivo CSV

df_logs = pd.read_csv("log_ficticio.csv")



# Convertendo o campo Timestamp para formato de data

df_logs["Timestamp"] = pd.to_datetime(df_logs["Timestamp"])



# Exibir amostra dos dados carregados

print(df_logs.head())



# ========================================

# ETAPA 3: PRÉ-PROCESSAMENTO DOS DADOS

# ========================================

# Contagem de acessos por IP

df_ip_counts = df_logs["IP"].value_counts().reset_index()

df_ip_counts.columns = ["IP", "Acessos"]



# Normalizando a contagem de acessos

df_ip_counts["Acessos_Normalizados"] = (df_ip_counts["Acessos"] - df_ip_counts["Acessos"].mean()) / df_ip_counts["Acessos"].std()



print("\nPré-processamento concluído.")

print(df_ip_counts.head())



# ========================================

# ETAPA 4: ANÁLISE COM IA (Detecção de Anomalias)

# ========================================

# Usando Isolation Forest para identificar anomalias

modelo = IsolationForest(contamination=0.05, random_state=42)

df_ip_counts["Anomalia"] = modelo.fit_predict(df_ip_counts[["Acessos_Normalizados"]])



# Definição de categorias com base na predição da IA

df_ip_counts["Classificacao"] = df_ip_counts["Anomalia"].map({1: "Normal", -1: "Suspeito"})



print("\nAnálise com IA concluída.")

print(df_ip_counts["Classificacao"].value_counts())



# ========================================

# ETAPA 5: CLASSIFICAÇÃO DOS ACESSOS

# ========================================

# Definição de acessos críticos: IPs com alto volume de acessos classificados como suspeitos

limite_critico = df_ip_counts["Acessos"].quantile(0.95) # Pega o top 5% de acessos

df_ip_counts["Classificacao"] = df_ip_counts.apply(

  lambda x: "Crítico" if x["Classificacao"] == "Suspeito" and x["Acessos"] > limite_critico else x["Classificacao"],

  axis=1

)



print("\nClassificação dos acessos concluída.")

print(df_ip_counts["Classificacao"].value_counts())



# ========================================

# ETAPA 6: RESPOSTA AUTOMATIZADA (Geração de Alertas)

# ========================================

# Gerando alertas para acessos críticos

acessos_criticos = df_ip_counts[df_ip_counts["Classificacao"] == "Crítico"]



if not acessos_criticos.empty:

  print("\n⚠️ ALERTA: Acessos Críticos Detectados!")

  print(acessos_criticos)

  acessos_criticos.to_csv("alertas_criticos.csv", index=False)

else:

  print("\nNenhum acesso crítico detectado.")



# ========================================

# ETAPA 7: VISUALIZAÇÃO DOS RESULTADOS

# ========================================

# Gráfico de distribuição dos acessos

plt.figure(figsize=(12, 6))

sns.histplot(df_ip_counts["Acessos"], bins=30, kde=True)

plt.title("Distribuição de Acessos por IP")

plt.xlabel("Número de Acessos")

plt.ylabel("Frequência")

plt.show()



# Gráfico de Classificação de acessos

plt.figure(figsize=(12, 6))

sns.countplot(x=df_ip_counts["Classificacao"], palette="coolwarm")

plt.title("Classificação de Acessos")

plt.xlabel("Tipo de Acesso")

plt.ylabel("Quantidade")

plt.show()



print("\nProcessamento concluído com sucesso!")