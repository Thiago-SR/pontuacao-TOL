import pandas as pd
from collections import deque
import copy

def string_para_estado(s):
    partes = s.split('|')[1:]  # Remove o primeiro item vazio antes do primeiro '|'
    
    # Remove o último elemento vazio apenas se ele for causado por um '|' final extra
    if len(partes) > 0 and partes[-1] == '':
        partes = partes[:-1]
    
    return [list(pino) for pino in partes]



# Transforma um estado em uma tupla imutável para poder usar em sets
def estado_para_tupla(estado):
    return tuple(tuple(pino) for pino in estado)

# Gera todos os próximos estados válidos
def movimentos_possiveis(estado, altura_max):
    estados = []
    for i in range(len(estado)):
        if not estado[i]:  # Pula pinos vazios
            continue
        bola = estado[i][-1]
        for j in range(len(estado)):
            if i != j and len(estado[j]) < altura_max:
                novo_estado = copy.deepcopy(estado)
                novo_estado[i].pop()
                novo_estado[j].append(bola)
                estados.append(novo_estado)
    return estados

# Normaliza o tamanho dos estados para que tenham exatamente 3 pinos, preservando a posição dos pinos vazios
def normalizar_estados(estado_inicial, estado_final):
    num_pinos = 3  # Número fixo de pinos

    # Verifica se o estado inicial tem menos de 3 pinos e adiciona pinos vazios na posição correta
    while len(estado_inicial) < num_pinos:
        estado_inicial.append([])

    # Verifica se o estado final tem menos de 3 pinos e adiciona pinos vazios na posição correta
    while len(estado_final) < num_pinos:
        estado_final.append([])

    # Garante que ambos os estados tenham exatamente 3 pinos
    if len(estado_inicial) != num_pinos or len(estado_final) != num_pinos:
        raise ValueError("Erro na normalização: o estado não tem exatamente 3 pinos!")

    return estado_inicial, estado_final
# def movimentos_minimos(estado_inicial, estado_objetivo, altura_max):
#     visitados = set()
#     fila = deque([(estado_inicial, 0, [])])  # Adiciona histórico de passos

#     while fila:
#         estado_atual, passos, caminho = fila.popleft()
#         estado_tupla = estado_para_tupla(estado_atual)
#         if estado_tupla in visitados:
#             continue
#         visitados.add(estado_tupla)

#         novo_caminho = caminho + [copy.deepcopy(estado_atual)]

#         if estado_tupla == estado_para_tupla(estado_objetivo):
#             print("\n🧩 Caminho encontrado em", passos, "passos:")
#             for i, est in enumerate(novo_caminho):
#                 print(f"Passo {i}: {est}")
#             return passos

#         for prox in movimentos_possiveis(estado_atual, altura_max):
#             fila.append((prox, passos + 1, novo_caminho))

#     return -1

# Calcula a quantidade mínima de movimentos usando BFS
def movimentos_minimos(estado_inicial, estado_objetivo, altura_max):
    

    visitados = set()
    fila = deque([(estado_inicial, 0)])

    while fila:
        estado_atual, passos = fila.popleft()
        estado_tupla = estado_para_tupla(estado_atual)
        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)

        if estado_tupla == estado_para_tupla(estado_objetivo):
            return passos

        for prox in movimentos_possiveis(estado_atual, altura_max):
            fila.append((prox, passos + 1))

    # print("Estado objetivo nunca alcançado:")
    # print("Inicial:", estado_para_tupla(estado_inicial))
    # print("Final:  ", estado_para_tupla(estado_objetivo))

    return -1

# Pontuação baseada na diferença entre movimentos feitos e mínimos
def calcular_pontuacao(row, min_movs):
    if (row['done'] != 1) or min_movs == -1:
        return 0  # Nenhuma pontuação se não acertou

    extra_movs = row['step'] - min_movs
    pontuacao = max(0, 10 - extra_movs)  # Pontuação inicial de 10, penalizada pelos movimentos extras

    return pontuacao

def main():
    # === MAIN ===
    df = pd.read_csv('C:/Users/thiag/OneDrive/Documentos/TOL/Scripts/pontuacao-TOL/pontuacao_min_movs/teste.xls', sep=',')

    # Inicializa listas para novas colunas
    col_minimos = []
    col_pontuacao = []

    # Variáveis auxiliares
    estado_inicial = None
    estado_final = None

    for idx, row in df.iterrows():
        if row['step'] == 0:
            estado_inicial = string_para_estado(row['current'])
            estado_final = string_para_estado(row['end'])
            print(f"Estado inicial: {estado_inicial}")
            print(f"Estado final: {estado_final}")
            

        if row['done'] == 1:
            min_movs = movimentos_minimos(estado_inicial, estado_final, altura_max=row['size'])
            print(f"Movimentos mínimos: {min_movs}")
            pontuacao = calcular_pontuacao(row, min_movs)
        else:
            min_movs = 0
            pontuacao = 0

        col_minimos.append(min_movs)
        col_pontuacao.append(pontuacao)

    # Adiciona colunas ao DataFrame
    df['movimentos_minimos'] = col_minimos
    df['pontuacao_acumulada'] = pd.Series(col_pontuacao).cumsum()

    # Salva novo CSV
    df.to_csv('C:/Users/thiag/OneDrive/Documentos/TOL/Scripts/pontuacao-TOL/pontuacao_min_movs/result_test.csv', index=False)
    print("Pontuação acumulada e movimentos mínimos calculados e salvos com sucesso!")
if __name__ == "__main__":
    main()