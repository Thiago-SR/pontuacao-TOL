import pandas as pd

# Função de pontuação
def calcular_pontuacao(done, step, size):
    if done == 0:
        return 0  # Errou: pontuação 0
    multiplicador = 6 - size  # quanto menos bolas, maior a penalização
    return step * multiplicador

# Lê a tabela original no formato CSV (mesmo com extensão .xls)
df = pd.read_csv('C:/Users/thiag/OneDrive/Documentos/TOL/Scripts/pontuacao_simples/dados.xls', sep=',')

# Calcula a pontuação e adiciona diretamente a coluna de pontuação acumulada
df['pontuacao_acumulada'] = df.apply(lambda row: calcular_pontuacao(row['done'], row['step'], row['size']), axis=1).cumsum()

# Salva o novo arquivo com apenas a coluna de pontuação acumulada
df.to_csv('C:/Users/thiag/OneDrive/Documentos/TOL/Scripts/pontuacao_simples/tabela_com_pontuacao_acumulada.csv', index=False)

print("Pontuação acumulada calculada e salva com sucesso!")
