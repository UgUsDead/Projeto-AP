import os

def caminho_ficheiro(nome_ficheiro):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path).replace("codigo", "dados")
    if not os.path.exists(dir):
        os.makedirs(dir)  # Certifique-se de que o diretório "dados" exista
    return os.path.join(dir, nome_ficheiro)

# Estacoes
def adicionar_estacao(codigo, nome, latitude, longitude):
    if not validar_numero(latitude) or not validar_numero(longitude):
        print("Erro: Latitude e longitude devem ser números válidos.")
        return
    caminho = caminho_ficheiro("estacoes.txt")
    linha = codigo + ";" + nome + ";" + latitude + ";" + longitude + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()

def listar_estacoes():
    caminho = caminho_ficheiro("estacoes.txt")
    if not os.path.exists(caminho):
        return []
    estacoes = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        estacoes.append(linha.strip().split(";"))
    return estacoes

def estacao_existe(codigo):
    estacoes = listar_estacoes()
    for estacao in estacoes:
        if estacao[0] == codigo:
            return True
    return False

# Carris
def adicionar_carril(estacao_a, estacao_b, distancia, vel_max):
    if not validar_numero(distancia) or not validar_numero(vel_max):
        print("Erro: Distância e velocidade máxima devem ser números válidos.")
        return
    caminho = caminho_ficheiro("carris.txt")
    codigo_carril = estacao_a + "_" + estacao_b
    linha = codigo_carril + ";" + estacao_a + ";" + estacao_b + ";" + distancia + ";" + vel_max + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()

def listar_carris():
    caminho = caminho_ficheiro("carris.txt")
    if not os.path.exists(caminho):
        return []
    carris = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        carris.append(linha.strip().split(";"))
    return carris

def carril_existe(esta, estb):
    carril = listar_carris()
    for carris in carril:
        if carris[0] == esta + "_" + estb:
            return True
    return False

# Linha
def adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico):
    if not estacao_existe(estacao_partida) or not estacao_existe(estacao_chegada):
        print("Erro: Estações de partida ou chegada não existem.")
        return False
    if not existe_caminho(estacao_partida, estacao_chegada):
        print("Erro: Não há carris conectando as estações especificadas.")
        return False

    # Obter o caminho entre as estações
    caminho_estacoes = obter_caminho(estacao_partida, estacao_chegada)
    
    if len(caminho_estacoes) > 2:
        print("O caminho passa pelas seguintes estações intermediárias:")
        for estacao in caminho_estacoes[1:-1]:
            print(estacao)
        resposta = input("Deseja adicionar paradas nas estações intermediárias? (s/n): ").strip().lower()
        if resposta == 's':
            paradas = caminho_estacoes[1:-1]
        else:
            paradas = []
    else:
        paradas = []

    caminho = caminho_ficheiro("linhas.txt")
    linha = codigo_linha + ";" + nome + ";" + estacao_partida + ";" + estacao_chegada + ";" + tipo_servico + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()

    # Save paragens to paragens.txt
    caminho_paragens = caminho_ficheiro("paragens.txt")
    ficheiro_paragens = open(caminho_paragens, "a")
    for parada in paradas:
        ficheiro_paragens.write(codigo_linha + ";" + parada + "\n")
    ficheiro_paragens.close()

    return True

def listar_linhas():
    caminho = caminho_ficheiro("linhas.txt")
    if not os.path.exists(caminho):
        return []
    linhas = []
    ficheiro = open(caminho, "r")
    conteudo = ficheiro.readlines()
    ficheiro.close()

    # Read paragens from paragens.txt
    caminho_paragens = caminho_ficheiro("paragens.txt")
    paragens_dict = {}
    if os.path.exists(caminho_paragens):
        ficheiro_paragens = open(caminho_paragens, "r")
        for linha in ficheiro_paragens:
            partes = linha.strip().split(";")
            codigo_linha = partes[1]
            parada = partes[2]
            if codigo_linha not in paragens_dict:
                paragens_dict[codigo_linha] = []
            paragens_dict[codigo_linha].append(parada)
        ficheiro_paragens.close()

    for linha in conteudo:
        partes = linha.strip().split(";")
        codigo_linha = partes[0]
        nome = partes[1]
        estacao_partida = partes[2]
        estacao_chegada = partes[3]
        tipo_servico = partes[4]
        paradas = paragens_dict.get(codigo_linha, [])
        linhas.append((codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico, paradas))
    return linhas

def linha_existe(codlin):
    linhas = listar_linhas()
    for linha in linhas:
        if linha[0] == codlin:
            return True
    return False

# Comboios
def adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico):
    if not numero_serie.isdigit() or len(numero_serie) != 5:
        print("Erro: Número de série deve ser um número válido com 5 dígitos.")
        return False
    if not validar_numero(vel_max) or not validar_numero(capacidade):
        print("Erro: Velocidade máxima e capacidade devem ser números válidos.")
        return False
    if tipo_servico not in ["U", "R", "I", "A"]:
        print("Erro: Tipo de serviço deve ser 'U' (urbano), 'R' (regional), 'I' (intercidades) ou 'A' (Alfa-Pendular).")
        return False
    
    comboios = listar_comboios()
    for comboio in comboios:
        if comboio[0] == numero_serie:
            print("Erro: Número de série já existe!")
            return False
    
    caminho = caminho_ficheiro("comboios.txt")
    linha = numero_serie + ";" + modelo + ";" + vel_max + ";" + capacidade + ";" + tipo_servico + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def listar_comboios():
    caminho = caminho_ficheiro("comboios.txt")
    if not os.path.exists(caminho):
        return []
    comboios = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        comboios.append(linha.strip().split(";"))
    return comboios

# Viagens
def adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros):
    if not validar_numero(identificador_viagem):
        print("Erro: Identificador da viagem deve ser um número válido.")
        return False
    if not validar_numero(numero_passageiros):
        print("Erro: Número de passageiros deve ser um número válido.")
        return False
    if not validar_numero(dia) or not validar_numero(mes) or not validar_numero(ano):
        print("Erro: Dia, mês e ano devem ser números válidos.")
        return False
    
    viagens = listar_viagens()
    for viagem in viagens:
        if viagem[0] == identificador_viagem:
            print("Erro: Identificador da viagem já existe.")
            return False
    
    linhas = listar_linhas()
    comboios = listar_comboios()
    
    linha_existe = False
    comboio_existe = False
    
    for linha in linhas:
        if linha[0] == codigo_linha:
            linha_existe = True
            break
    
    for comboio in comboios:
        if comboio[0] == numero_serie_comboio:
            comboio_existe = True
            break
    
    if not linha_existe:
        print("Erro: Código da linha não existe.")
        return False
    if not comboio_existe:
        print("Erro: Número de série do comboio não existe.")
        return False
    
    caminho = caminho_ficheiro("viagens.txt")
    linha = identificador_viagem + ";" + codigo_linha + ";" + numero_serie_comboio + ";" + hora_partida + ";" + hora_chegada + ";" + dia + ";" + mes + ";" + ano + ";" + numero_passageiros + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()

    # Adicionar paragens associadas à linha
    paragens = listar_paragens_por_linha(codigo_linha)
    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    ficheiro_paragens_viagem = open(caminho_paragens_viagem, "a")
    for i, paragem in enumerate(paragens):
        identificador_paragem_viagem = f"PV{identificador_viagem}_{i+1}"
        ficheiro_paragens_viagem.write(identificador_paragem_viagem + ";" + paragem[0] + ";" + identificador_viagem + ";" + hora_partida + "\n")
    ficheiro_paragens_viagem.close()

    return True

def listar_viagens_por_linha(codigo_linha):
    caminho = caminho_ficheiro("viagens.txt")
    if not os.path.exists(caminho):
        return []
    viagens = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        partes = linha.strip().split(";")
        if partes[1] == codigo_linha:
            viagens.append(partes)
    return viagens

def adicionar_paragem_viagem(identificador_paragem_viagem, identificador_paragem, identificador_viagem, hora_paragem):
    caminho = caminho_ficheiro("paragens_viagem.txt")
    linha = identificador_paragem_viagem + ";" + identificador_paragem + ";" + identificador_viagem + ";" + hora_paragem + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def listar_paragens_por_linha(codigo_linha):
    caminho = caminho_ficheiro("paragens.txt")
    if not os.path.exists(caminho):
        return []
    paragens = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        partes = linha.strip().split(";")
        if partes[1] == codigo_linha:
            paragens.append(partes)
    return paragens

def adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar):
    # Verificar se a viagem existe
    viagens = listar_viagens()
    viagem_existe = False
    capacidade_maxima = 0
    numero_passageiros = 0
    for viagem in viagens:
        if viagem[0] == identificador_viagem:
            viagem_existe = True
            capacidade_maxima = int(viagem[8])
            numero_passageiros = int(viagem[9])
            break
    
    if not viagem_existe:
        print("Erro: Identificador da viagem não existe.")
        return False
    
    # Verificar se há vagas suficientes
    reservas = listar_reservas_por_viagem(identificador_viagem)
    if len(reservas) >= capacidade_maxima:
        print("Erro: Não há vagas suficientes na viagem.")
        return False
    
    # Adicionar a reserva
    caminho = caminho_ficheiro("reservas_viagem.txt")
    linha = identificador_reserva_viagem + ";" + identificador_viagem + ";" + nome_passageiro + ";" + lugar + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def listar_reservas_por_viagem(identificador_viagem):
    caminho = caminho_ficheiro("reservas_viagem.txt")
    if not os.path.exists(caminho):
        return []
    reservas = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        partes = linha.strip().split(";")
        if partes[1] == identificador_viagem:
            reservas.append(partes)
    return reservas

def listar_viagens():
    caminho = caminho_ficheiro("viagens.txt")
    if not os.path.exists(caminho):
        return []
    viagens = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        viagens.append(linha.strip().split(";"))
    return viagens

def listar_horario_viagem(identificador_viagem):
    caminho_viagens = caminho_ficheiro("viagens.txt")
    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    
    # Verificar se a viagem existe
    if not os.path.exists(caminho_viagens):
        print("Erro: Nenhuma viagem encontrada.")
        return False
    
    viagem_encontrada = False
    viagem_info = None
    ficheiro_viagens = open(caminho_viagens, "r")
    linhas_viagens = ficheiro_viagens.readlines()
    ficheiro_viagens.close()
    
    for linha in linhas_viagens:
        partes = linha.strip().split(";")
        if partes[0] == identificador_viagem:
            viagem_encontrada = True
            viagem_info = partes
            break
    
    if not viagem_encontrada:
        print("Erro: Identificador da viagem não existe.")
        return False
    
    # Listar paragens da viagem
    if not os.path.exists(caminho_paragens_viagem):
        print("Erro: Nenhuma paragem encontrada.")
        return False
    
    paragens = []
    ficheiro_paragens_viagem = open(caminho_paragens_viagem, "r")
    linhas_paragens = ficheiro_paragens_viagem.readlines()
    ficheiro_paragens_viagem.close()
    
    for linha in linhas_paragens:
        partes = linha.strip().split(";")
        if partes[2] == identificador_viagem:
            paragens.append(partes)
    
    # Exibir informações da viagem e suas paragens
    print("Horário da Viagem:")
    print("Identificador: " + viagem_info[0])
    print("Código da Linha: " + viagem_info[1])
    print("Número de Série do Comboio: " + viagem_info[2])
    print("Hora de Partida: " + viagem_info[3])
    print("Hora de Chegada: " + viagem_info[4])
    print("Data: " + viagem_info[5] + "/" + viagem_info[6] + "/" + viagem_info[7])
    print("Número de Passageiros: " + viagem_info[8])
    
    if paragens:
        print("Paragens:")
        for paragem in paragens:
            print("Identificador da Paragem: " + paragem[1] + " | Hora da Paragem: " + paragem[3])
    else:
        print("Nenhuma paragem encontrada para esta viagem.")
    
    return True

# Conexoes
def obter_conexoes():
    """Cria um grafo com base nos carris disponíveis."""
    conexoes = {}
    carris = listar_carris()
    for carril in carris:
        estacao_a, estacao_b = carril[1], carril[2]
        if estacao_a not in conexoes:
            conexoes[estacao_a] = []
        if estacao_b not in conexoes:
            conexoes[estacao_b] = []
        conexoes[estacao_a].append(estacao_b)
        conexoes[estacao_b].append(estacao_a)
    return conexoes

def existe_caminho(estacao_a, estacao_b):
    #Algoritmo de procura de caminho mais curto
    conexoes = obter_conexoes()
    if estacao_a not in conexoes or estacao_b not in conexoes:
        return False
    
    visitados = set()
    fila = [estacao_a]

    while fila:
        atual = fila.pop(0)
        if atual == estacao_b:
            return True
        if atual not in visitados:
            visitados.add(atual)
            fila.extend(conexoes[atual])
    return False

def obter_caminho(estacao_a, estacao_b):
    conexoes = obter_conexoes()
    fila = [(estacao_a, [estacao_a])]
    visitados = set()

    while fila:
        (atual, caminho) = fila.pop(0)
        if atual in visitados:
            continue
        visitados.add(atual)
        for proximo in conexoes.get(atual, []):
            if proximo in visitados:
                continue
            if proximo == estacao_b:
                return caminho + [proximo]
            else:
                fila.append((proximo, caminho + [proximo]))
    return []

# Validations
def validar_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False
