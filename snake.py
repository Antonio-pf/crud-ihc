from typing import List

def find_snake_on_grid(grid: List[str]) -> List[List[int]]:
    cabeca = 'h'
    partes_da_cobra = ['>', '<', 'v', '^']
    posicoes = []

    # Encontrar a cabeça da cobra
    for linha_posicao in range(len(grid)):
        linha = grid[linha_posicao]
        for coluna in range(len(linha)):
            if linha[coluna] == cabeca:
                # Adicionar a cabeça na lista
                posicoes.append([coluna, linha_posicao])
                break
    
    # Direções correspondentes a cada parte da cobra
    direcoes = {
        '>': (0, 1),  # para a direita (mesma linha, próxima coluna)
        '<': (0, -1),  # para a esquerda (mesma linha, coluna anterior)
        'v': (1, 0),   # para baixo (próxima linha, mesma coluna)
        '^': (-1, 0),  # para cima (linha anterior, mesma coluna)
    }

    # Agora vamos percorrer as partes do corpo, começando da cabeça
    ultima_posicao = posicoes[0]
    while True:
        linha_posicao, coluna = ultima_posicao
        found = False

        # Percorrer o grid para encontrar a próxima parte do corpo
        for direcao in partes_da_cobra:
            delta_linha, delta_coluna = direcoes[direcao]
            nova_linha = linha_posicao + delta_linha
            nova_coluna = coluna + delta_coluna

            # Verifica se a nova posição está dentro do grid
            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[nova_linha]):
                # Verifica se a parte do corpo está na posição correta
                if grid[nova_linha][nova_coluna] == direcao:
                    ultima_posicao = [nova_coluna, nova_linha]
                    posicoes.append([nova_coluna, nova_linha])
                    found = True
                    break
        
        # Se não encontrar mais partes, significa que terminamos de construir a cobra
        if not found:
            break

    return posicoes

# Teste com o grid fornecido
grid = [
            "   ",
            " h<",
            " >^",
        ]
posicoes_da_cobra = find_snake_on_grid(grid)
print(posicoes_da_cobra)