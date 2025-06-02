def base64Encode(octets):
    # Tabela de codificação Base64
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # Calcula o número de bytes faltantes para ser múltiplo de 3
    padding = (3 - len(octets) % 3) % 3
    
    # Adiciona bytes nulos para garantir múltiplo de 3
    octets += "\0" * padding
    
    sextets = []
    shiftRight, shiftLeft = 2, 6
    remainer, remainerPadding = 0, 4
    
    for i, char in enumerate(octets):
        sextets.append(remainer << shiftLeft | ord(char) >> shiftRight)
        remainer = ord(char) % remainerPadding
        
        if (i + 1) % 3 == 0:
            sextets.append(remainer)
            shiftRight, shiftLeft = 2, 6
            remainer, remainerPadding = 0, 4
        else:
            shiftRight += 2
            shiftLeft -= 2
            remainerPadding *= 4
    
    # Remove os sextetos adicionados pelo padding
    if padding:
        sextets = sextets[:-padding]
    
    # Converte sextetos em caracteres Base64
    encoded = ''.join(base64_chars[sextet] for sextet in sextets)
    
    # Adiciona os caracteres de padding =
    encoded += "=" * padding
    
    return encoded

def base64Decode(encoded):
    # Tabela de codificação Base64
    base64_sextets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # Remove caracteres de padding =
    encoded = encoded.replace('=', '')

    # Converte os caracteres Base64 de volta para sextetos
    sextets = [base64_sextets.index(sextet) for sextet in encoded]

    j = 1
    octets = []
    
    shiftLeft, shiftRight = 2, 4
    
    remainerPadding, remainer = 16, sextets[0]

    # Processa cada sexteto na string codificada
    while j < len(sextets):
        # Cria um caractere combinando o resto e o sexteto deslocado
        char_code = (remainer << shiftLeft) | (sextets[j] >> shiftRight)
        octets.append(char_code)
        
        # Atualiza o resto com os bits que não foram usados
        remainer = sextets[j] % remainerPadding

        if (j + 1) % 4 == 0:
            # Ajusta os valores de deslocamento após processar quatro sextetos
            shiftLeft, shiftRight = 2, 4
            remainerPadding = 16
            if j + 1 < len(sextets):
                remainer = sextets[j + 1]
            j += 2
        else:
            # Ajusta os valores de deslocamento para o próximo sexteto
            shiftLeft += 2
            shiftRight -= 2
            remainerPadding //= 4
            j += 1

    # Converte os códigos de caracteres de volta para a string original
    original = ''.join(chr(octet) for octet in octets).rstrip('\0')

    return original
