from main import movimentos_minimos



def testar_movimentos_minimos():
    print("\n--- Iniciando testes de validação ---")
    testes = [
        # (estado_inicial, estado_final, altura_max, esperado)
        # Teste 1: mover duas bolas de um pino para outro (mínimo 3 movimentos)
        ([['A', 'B'], [], []], [[], [], ['A', 'B']], 2, 3),
        
        # Teste 2: estado já resolvido (mínimo 0)
        ([[], [], ['A', 'B']], [[], [], ['A', 'B']], 2, 0),
        
        # Teste 3: mover uma bola (mínimo 1)
        ([['A'], [], []], [[], [], ['A']], 1, 1),
        
        # Teste 4: caso com 3 bolas (mínimo conhecido = 5)
        ([['R', 'G', 'B'], [], []], [[], [], ['R', 'G', 'B']], 3, 5),
        
        # Teste 5: impossível (excesso de bolas para a altura máxima)
        ([['A', 'B', 'C']], [[], [], ['A', 'B', 'C', 'D']], 3, -1),
        
        # Teste 6: troca de lugares entre dois pinos (mínimo 3)
        ([['A'], ['B'], []], [['B'], ['A'], []], 1, 3),
        
        # Teste 7: verificar simetria
        ([['A', 'B'], [], []], [[], [], ['A', 'B']], 2, 3),
        ([[], [], ['A', 'B']], [['A', 'B'], [], []], 2, 3),
    ]
    
    for i, (ini, fim, alt, esperado) in enumerate(testes):
        resultado = movimentos_minimos(ini, fim, alt)
        assert resultado == esperado, f"❌ Teste {i + 1} falhou: esperado {esperado}, obtido {resultado}"
        print(f"✅ Teste {i + 1} passou! ({esperado} movimentos)")

    print("--- Todos os testes passaram com sucesso! ---\n")

# Chamada dos testes
testar_movimentos_minimos()
