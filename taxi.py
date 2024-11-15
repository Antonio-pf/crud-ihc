def escolhe_taxi(tf1, vqr1, tf2, vqr2):
    """
    Escolhe a empresa de táxi mais vantajosa com base nas taxas.

    Args:
        tf1: Taxa fixa da empresa 1.
        vqr1: Valor por quilômetro rodado da empresa 1.
        tf2: Taxa fixa da empresa 2.
        vqr2: Valor por quilômetro rodado da empresa 2.

    Returns:
        Uma string indicando a melhor empresa ou a condição para escolha.
    """

    tf1 = float(tf1)
    vqr1 = float(vqr1)
    tf2 = float(tf2)
    vqr2 = float(vqr2)

    if tf1 == tf2 and vqr1 == vqr2:
        return "Tanto faz"

    distance_equal = (tf2 - tf1) / (vqr1 - vqr2)

    if distance_equal < 0:
        if vqr1 < vqr2:
            return "Empresa 1"
        else:
            return "Empresa 2"

    if distance_equal % 1 == 0:
        format_string = f"Empresa 1 quando a distância < {distance_equal:.1f}, Tanto faz quando a distância = {distance_equal:.1f}, Empresa 2 quando a distância > {distance_equal:.1f}"
    else:
        format_string = f"Empresa 1 quando a distância < {distance_equal:.2f}, Tanto faz quando a distância = {distance_equal:.2f}, Empresa 2 quando a distância > {distance_equal:.2f}"

    return format_string

print(escolhe_taxi("2.5","1.0","5.0","0.75"))


