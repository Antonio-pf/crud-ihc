# Dicionário com a tabela de Código Morse
morse_code = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z"
}

def possibilidades(signals):
    # Função auxiliar para gerar todas as combinações substituindo '?' por '.' e '-'
    def gerar_combinacoes(sinais):
        if '?' not in sinais:
            return [sinais]  # Se não houver '?', retorne a string original como a única opção
        
        # Se houver '?', substituímos por '.' e '-' e continuamos recursivamente
        combinacoes = []
        for substituicao in ['.', '-']:
            combinacoes.extend(gerar_combinacoes(sinais.replace('?', substituicao, 1)))  # Substitui uma única '?' por '.' ou '-'
        return combinacoes

    # Gera todas as combinações possíveis para o sinal dado
    combinacoes = gerar_combinacoes(signals)
    
    # Busca as letras correspondentes no dicionário de código Morse
    letras_possiveis = []
    for combinacao in combinacoes:
        if combinacao in morse_code:
            letras_possiveis.append(morse_code[combinacao])
    
    return sorted(letras_possiveis)

# Exemplos de uso
print(possibilidades("?"))    # Deve retornar ["E", "T"]
print(possibilidades("?."))   # Deve retornar ["I", "N"]
print(possibilidades(".?"))   # Deve retornar ["I", "A"]
