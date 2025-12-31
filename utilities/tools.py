def number_to_char(zahl):
    if 0 <= zahl <= 25:
        return chr(65 + zahl)  # 65 ist der ASCII-Code für 'A'
    else:
        return "Ungültige Zahl (0-25 erlaubt)"