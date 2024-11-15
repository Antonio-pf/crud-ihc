def seven_segmentify(time_: str) -> str:
   ## definir os horários
    display = {
        '0': [' _ ', '| |', '|_|'],
        '1': ['   ', '  |', '  |'],
        '2': [' _ ', ' _|', '|_ '],
        '3': [' _ ', ' _|', ' _|'],
        '4': ['   ', '|_|', '  |'],
        '5': [' _ ', '|_ ', ' _|'],
        '6': [' _ ', '|_ ', '|_|'],
        '7': [' _ ', '  |', '  |'],
        '8': [' _ ', '|_|', '|_|'],
        '9': [' _ ', '|_|', ' _|'],
        ':': ['   ', ' . ', ' . '],
        ' ': ['   ', '   ', '   ']
    }
    
    hora, minutos = time_.split(":")
    if hora[0] == '0':
      hora = ' ' + hora[1]
    hora_minutos = hora + ':' + minutos
    
    display_segmento = ["", "", ""]
    for numero in hora_minutos:
      for i in range(3):
        display_segmento[i] += display[numero][i] 
        
    
    return "\n".join(display_segmento)

print(seven_segmentify("00:00"))

print(seven_segmentify("6:00"))

print(seven_segmentify("12:00"))