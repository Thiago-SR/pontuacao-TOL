import pytest
from main import (
    movimentos_minimos,
    string_para_estado,
    normalizar_estados,
    EstadoInvalidoError
)

def test_string_para_estado():
    """Testa a conversão de string para estado."""
    # Teste básico
    assert string_para_estado('|A|B|C|') == [['A'], ['B'], ['C']]
    
    # Teste com pinos vazios
    assert string_para_estado('|A||C|') == [['A'], [], ['C']]
    
    # Teste com múltiplas bolas
    assert string_para_estado('|AB|C|D|') == [['A', 'B'], ['C'], ['D']]
    
    # Teste com string inválida
    with pytest.raises(EstadoInvalidoError):
        string_para_estado('A|B|C|')
    
    with pytest.raises(EstadoInvalidoError):
        string_para_estado('')

def test_normalizar_estados():
    """Testa a normalização de estados."""
    # Teste com estados já normalizados
    estado1 = [['A'], ['B'], ['C']]
    estado2 = [['C'], ['B'], ['A']]
    assert normalizar_estados(estado1, estado2) == (estado1, estado2)
    
    # Teste com estados não normalizados
    estado1 = [['A'], ['B']]
    estado2 = [['C']]
    norm1, norm2 = normalizar_estados(estado1, estado2)
    assert len(norm1) == 3
    assert len(norm2) == 3
    assert norm1 == [['A'], ['B'], []]
    assert norm2 == [['C'], [], []]

def test_movimentos_minimos():
    """Testa o cálculo de movimentos mínimos."""
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
        
        # Teste 8: caso com altura máxima 1
        ([['A'], ['B'], ['C']], [['C'], ['A'], ['B']], 1, -1),
        
        # Teste 9: caso com altura máxima 3 e 4 bolas (impossível por exceder altura máxima)
        ([['A', 'B', 'C', 'D'], [], []], [[], [], ['A', 'B', 'C', 'D']], 3, -1),
        
        # Teste 10: caso com altura máxima 4 e 4 bolas (possível)
        ([['A', 'B', 'C', 'D'], [], []], [[], [], ['A', 'B', 'C', 'D']], 4, 7),
    ]
    
    for i, (ini, fim, alt, esperado) in enumerate(testes, 1):
        resultado = movimentos_minimos(ini, fim, alt)
        assert resultado == esperado, f"Teste {i} falhou: esperado {esperado}, obtido {resultado}"

def test_movimentos_minimos_limite():
    """Testa o limite máximo de movimentos."""
    # Cria um caso que exige muitos movimentos
    estado_inicial = [['A', 'B', 'C', 'D', 'E'], [], []]
    estado_final = [[], [], ['A', 'B', 'C', 'D', 'E']]
    altura_max = 5
    
    resultado = movimentos_minimos(estado_inicial, estado_final, altura_max)
    assert resultado == 9, "Deveria retornar 9 movimentos para este caso"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
