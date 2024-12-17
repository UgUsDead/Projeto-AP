import os
import qrcode
import folium 

def caminho_ficheiro(nome_ficheiro):
    #Buscar o path do ficheiro. Dados e codigo
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path).replace("codigo", "dados")
    if os.path.exists(dir)== False:
        os.makedirs(dir)  # Certifique-se de que o diretório "dados" exista
    return os.path.join(dir, nome_ficheiro)

def adicionar_estacao(codigo, nome, latitude, longitude):
    
    if validar_numero(latitude) == False or validar_numero(longitude) == False:
        print("Erro: Latitude e longitude devem ser números válidos.")
        return
    else:
        caminho = caminho_ficheiro("estacoes.txt")
        linha = codigo + ";" + nome + ";" + latitude + ";" + longitude + "\n"
        ficheiro = open(caminho, "a")
        ficheiro.write(linha)
        ficheiro.close()

# Carris
def adicionar_carril(estacao_a, estacao_b, distancia, vel_max):
    if validar_numero(distancia) == False or validar_numero(vel_max) == False:
        print("Erro: Distância e velocidade máxima devem ser números válidos.")
        return
    else:
        caminho = caminho_ficheiro("carris.txt")
        codigo_carril = estacao_a + "_" + estacao_b
        linha = codigo_carril + ";" + estacao_a + ";" + estacao_b + ";" + distancia + ";" + vel_max + "\n"
        ficheiro = open(caminho, "a")
        ficheiro.write(linha)
        ficheiro.close()

# Linha
def adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico):
    if estacao_existe(estacao_partida) == False or estacao_existe(estacao_chegada) == False:
        print("Erro: Estações de partida ou chegada não existem.")
        return False
    if existe_caminho(estacao_partida, estacao_chegada) == False:
        print("Erro: Não há carris conectando as estações especificadas.")
        return False
    if linha_existe(codigo_linha):
        print("Erro: Código da linha já existe.")
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

    # Adicionar a linha no ficheiro linhas.txt
    caminho = caminho_ficheiro("linhas.txt")
    ficheiro = open(caminho, "a")
    linha = codigo_linha + ";" + nome + ";" + estacao_partida + ";" + estacao_chegada + ";" + tipo_servico + "\n"
    ficheiro.write(linha)
    ficheiro.close()

    # Gerar o ID Paragem incrementando o último existente
    caminho_paragens = caminho_ficheiro("paragens.txt")
    ultimo_id = 0

    # Ler o último ID existente em paragens.txt
    if os.path.exists(caminho_paragens):
        ficheiro_paragens = open(caminho_paragens, "r")
        for linha in ficheiro_paragens:
            partes = linha.strip().split(";")
            if len(partes) >= 1 and partes[0].isdigit():
                ultimo_id = max(ultimo_id, int(partes[0]))  # Atualiza o último ID
        ficheiro_paragens.close()

    # Adicionar as paragens ao ficheiro paragens.txt
    ficheiro_paragens = open(caminho_paragens, "a")
    for parada in paradas:
        ultimo_id += 1  # Incrementa o ID
        linha_paragem = str(ultimo_id) + ";" + codigo_linha + ";" + parada + "\n"
        ficheiro_paragens.write(linha_paragem)
    ficheiro_paragens.close()

    return True


# Comboios
def adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico):
    if numero_serie.isdigit()==False or len(numero_serie) != 5:
        print("Erro: Número de série deve ser um número válido com 5 dígitos.")
        return False
    if validar_numero(vel_max)==False or validar_numero(capacidade)==False:
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

# Viagens
def adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros):
    if not validar_numero(identificador_viagem):
        print("Erro: Identificador da viagem deve ser um número válido.")
        return False
    if not validar_numero(numero_passageiros):
        print("Erro: Número de passageiros deve ser um número válido.")
        return False
    if not validar_data(dia, mes, ano):
        print("Erro: Data inválida.")
        return False

    # Check if viagem ID already exists
    viagens = listar_viagens()
    for viagem in viagens:
        if viagem[0] == identificador_viagem:
            print("Erro: Identificador da viagem já existe.")
            return False

    # Check if line and train exist
    linhas = listar_linhas()
    comboios = listar_comboios()

    linha_existe = any(linha[0] == codigo_linha for linha in linhas)
    comboio_existe = any(comboio[0] == numero_serie_comboio for comboio in comboios)

    if not linha_existe:
        print("Erro: Código da linha não existe.")
        return False
    if not comboio_existe:
        print("Erro: Número de série do comboio não existe.")
        return False

    # Save viagem to viagens.txt
    caminho_viagens = caminho_ficheiro("viagens.txt")
    ficheiro_viagens = open(caminho_viagens, "a")
    ficheiro_viagens.write(
        identificador_viagem + ";" + codigo_linha + ";" + numero_serie_comboio + ";" +
        hora_partida + ";" + hora_chegada + ";" + dia + ";" + mes + ";" + ano + ";" + numero_passageiros + "\n"
    )
    ficheiro_viagens.close()

    # Find stops (paragens) associated with the line and add to paragens_viagem.txt
    paragens = []
    caminho_paragens = caminho_ficheiro("paragens.txt")
    ficheiro_paragens = open(caminho_paragens, "r")
    linhas_paragens = ficheiro_paragens.readlines()
    ficheiro_paragens.close()

    for linha in linhas_paragens:
        partes = linha.strip().split(";")
        if len(partes) == 3 and partes[1] == codigo_linha:  # Match Line ID
            paragens.append(partes[2])  # Append Station ID only (3rd value)

    # Save stops to paragens_viagem.txt
    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    ficheiro_paragens_viagem = open(caminho_paragens_viagem, "a")
    index = 1
    for station_id in paragens:
        ficheiro_paragens_viagem.write(
            "PV" + identificador_viagem + "_" + str(index) + ";" + station_id + ";" + identificador_viagem + "\n"
        )
        index += 1
    ficheiro_paragens_viagem.close()

    return True




def adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar):
    # Verificar se a viagem existe
    viagens = listar_viagens()
    viagem_existe = False
    capacidade_maxima = 0
    codigo_linha = ""
    for viagem in viagens:
        if viagem[0] == identificador_viagem:
            viagem_existe = True
            capacidade_maxima = int(viagem[8])  # Capacidade máxima da viagem
            codigo_linha = viagem[1]  # Código da linha associada à viagem
            break
    
    if viagem_existe==False:
        print("Erro: Identificador da viagem não existe.")
        return False

    # Verificar o tipo de serviço da linha associada à viagem
    linhas = listar_linhas()
    for linha in linhas:
        if linha[0] == codigo_linha:
            tipo_servico = linha[4]  # Tipo de serviço da linha
            if tipo_servico == "U":
                print("Erro: Reservas não são permitidas para viagens urbanas.")
                return False
            break

    # Verificar se há vagas suficientes
    reservas = listar_reservas_por_viagem(identificador_viagem)
    if len(reservas) >= capacidade_maxima:
        print("Erro: Não há vagas suficientes na viagem.")
        return False

    # Verificar se o lugar já está ocupado
    for reserva in reservas:
        if reserva[3] == lugar:
            print("Erro: O lugar " + lugar + " já está reservado para esta viagem.")
            return False

    # Adicionar a reserva
    caminho = caminho_ficheiro("reservas_viagem.txt")
    linha = identificador_reserva_viagem + ";" + identificador_viagem + ";" + nome_passageiro + ";" + lugar + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def listar_estacoes():
    caminho = caminho_ficheiro("estacoes.txt")
    if os.path.exists(caminho) == True:
        estacoes = []
        ficheiro = open(caminho, "r")
        linhas = ficheiro.readlines()
        ficheiro.close()
        for linha in linhas:
            partes = linha.strip().split(";")
            if len(partes) == 4:  # Verificar se a linha está corretamente formatada
                estacoes.append(partes)
        return estacoes
    return []

def listar_carris():
    caminho = caminho_ficheiro("carris.txt")
    if os.path.exists(caminho) == True:
        carris = []
        ficheiro = open(caminho, "r")
        linhas = ficheiro.readlines()
        ficheiro.close()
        for linha in linhas:
            partes = linha.strip().split(";")
            if len(partes) == 5:  # Verificar se a linha tem o número correto de campos
                carris.append(partes)
        return carris
    return []

def listar_linhas():
    caminho = caminho_ficheiro("linhas.txt")
    if os.path.exists(caminho)==False:
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

def listar_comboios():
    caminho = caminho_ficheiro("comboios.txt")
    if os.path.exists(caminho)==False:
        return []
    comboios = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        comboios.append(linha.strip().split(";"))
    return comboios

def listar_viagens():
    caminho = caminho_ficheiro("viagens.txt")
    if os.path.exists(caminho)==False:
        return []
    viagens = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        viagens.append(linha.strip().split(";"))
    return viagens

def listar_viagens_por_linha(codigo_linha):
    caminho = caminho_ficheiro("viagens.txt")
    if os.path.exists(caminho)==False:
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

def listar_paragens_por_linha(codigo_linha):
    caminho = caminho_ficheiro("paragens.txt")
    if os.path.exists(caminho)==False:
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

def listar_reservas_por_viagem(identificador_viagem):
    caminho = caminho_ficheiro("reservas_viagem.txt")
    if os.path.exists(caminho)==False:
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

def listar_horario_viagem(identificador_viagem):
    caminho_viagens = caminho_ficheiro("viagens.txt")
    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    
    # Verificar se a viagem existe
    if not os.path.exists(caminho_viagens):
        print("Erro: Nenhuma viagem encontrada.")
        return False

    viagem_encontrada = None
    ficheiro_viagens = os.fdopen(os.open(caminho_viagens, os.O_RDONLY))
    linhas_viagens = ficheiro_viagens.readlines()
    ficheiro_viagens.close()

    for linha in linhas_viagens:
        partes = linha.strip().split(";")
        if partes[0] == identificador_viagem:
            viagem_encontrada = partes
            break

    if not viagem_encontrada:
        print("Erro: Identificador da viagem não existe.")
        return False

    # Listar paragens associadas à viagem
    paragens_viagem = []
    if os.path.exists(caminho_paragens_viagem):
        ficheiro_paragens_viagem = os.fdopen(os.open(caminho_paragens_viagem, os.O_RDONLY))
        linhas_paragens_viagem = ficheiro_paragens_viagem.readlines()
        ficheiro_paragens_viagem.close()

        for linha in linhas_paragens_viagem:
            partes = linha.strip().split(";")
            if partes[2] == identificador_viagem:  # Match the trip ID
                paragens_viagem.append(partes[1])  # Store stop names

    # Exibir informações da viagem
    print("Identificador: "+viagem_encontrada[0])
    print("Código da Linha: "+viagem_encontrada[1])
    print("Número de Série do Comboio: "+viagem_encontrada[2])
    print("Hora de Partida: "+viagem_encontrada[3])
    print("Hora de Chegada: "+viagem_encontrada[4])
    print("Data: "+viagem_encontrada[5]+"/"+viagem_encontrada[6]+"/" +viagem_encontrada[7])
    print("Número de Passageiros: "+viagem_encontrada[8])

    # Exibir paragens da viagem
    if paragens_viagem:
        print("Paragens da Viagem:")
        for idx, paragem in enumerate(paragens_viagem, start=1):
            print("{}. {}".format(idx, paragem))
    else:
        print("Nenhuma paragem associada a esta viagem.")

    return True

def estacao_existe(codigo):
    estacoes = listar_estacoes()
    for estacao in estacoes:
        if estacao[0] == codigo:
            return True
    return False

def carril_existe(esta, estb):
    carril = listar_carris()
    for carris in carril:
        if carris[0] == esta + "_" + estb:
            return True
    return False

def linha_existe(codlin):
    linhas = listar_linhas()
    for linha in linhas:
        if linha[0] == codlin:
            return True
    return False

def existe_caminho(estacao_a, estacao_b):  #https://www.youtube.com/watch?v=HZ5YTanv5QE (Explicação do nosso algoritmo de procura (não é dijkstras é BFS))
    #Algoritmo de procura de caminho mais curto
    conexoes = obter_conexoes()
    #Caso estaçao a ou estacao B nao tenham caminho uma para a outra, retorna falso. 
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

def mapa():
    ests=listar_estacoes()
    carris=listar_carris()

    m = folium.Map(location=(38.736946, -9.142685), zoom_start=7)

    for est in ests:
        station_name = est[0]
        city = est[1]
        latitude = est[2]
        longitude = est[3]
        station_coords = {est[0]: (float(est[2]), float(est[3])) for est in ests}
        # Add a marker to the map for each station
        folium.Marker(
            location=(latitude, longitude),
            popup=f"{station_name}, {city}",
            tooltip=station_name
        ).add_to(m)

        for carril in carris:
            start_code = carril[1]  # Starting station code
            end_code = carril[2]    # Ending station code

            if start_code in station_coords and end_code in station_coords:
                start_coords = station_coords[start_code]
                end_coords = station_coords[end_code]

                # Draw a line between the start and end stations
                folium.PolyLine(
                    locations=[start_coords, end_coords],
                    color="blue",
                    weight=2.5,
                    opacity=0.8
                ).add_to(m)

    m.save("Mapa.html")

def codigo_qr(identificador_viagem,nome_passageiro,lugar):

    identificador_viagem=str(identificador_viagem)
    nome_passageiro=str(nome_passageiro)
    lugar=str(lugar)
    img = qrcode.make(identificador_viagem + ";\n" + nome_passageiro + ";\n" + lugar)
    type(img)
    img.save(identificador_viagem + "_" + nome_passageiro + "_" + lugar + ".png")

def obter_conexoes():
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

def validar_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def validar_data(dia, mes, ano):
    dia = int(dia)
    mes = int(mes)
    ano = int(ano)
    # Verificar se o mês é válido
    if mes < 1 or mes > 12:
        return False
    
    # Definir o número de dias por mês para anos não bissextos
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Verificar se o ano é bissexto
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        dias_por_mes[1] = 29  # Fevereiro tem 29 dias em anos bissextos
    
    # Verificar se o dia é válido para o mês e ano
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False
    
    return True


def procurar_comboio(tipo, valor):
   
    comboios = listar_comboios()
    resultado = []

    if tipo == "SN":  # Search by Serial Number
        for comboio in comboios:
            if comboio[0] == valor:  # Exact match with serial number
                resultado.append(comboio)

    elif tipo == "CAP":  # Search by Capacity
        try:
            max_passageiros = int(valor)  # Convert to integer
            for comboio in comboios:
                capacidade = int(comboio[3])  # Passenger capacity
                if capacidade <= max_passageiros:
                    resultado.append(comboio)
        except ValueError:
            print("Erro: A capacidade máxima deve ser um número válido.")
    else:
        print("Erro: Tipo inválido. Use 'SN' para número de série ou 'CAP' para capacidade.")

    return resultado


def procurar_linhas_por_estacao(estacao_id):
    """
    Procura todas as linhas que passam por uma estação específica.
    - estacao_id: O ID da estação (por exemplo, 'LISB').
    """
    linhas = listar_linhas()  # Lista todas as linhas em linhas.txt
    paragens = listar_paragens()  # Lista todas as paragens em paragens.txt
    resultado = []

    # Verificar se a estação aparece como estação inicial, final ou paragem
    for linha in linhas:
        linha_id = linha[0]
        estacao_partida = linha[2]
        estacao_chegada = linha[3]

        # Verificar se a estação é partida ou chegada
        if estacao_id == estacao_partida or estacao_id == estacao_chegada:
            resultado.append(linha)
            continue

        # Verificar se a estação aparece como paragem
        for paragem in paragens:
            if paragem[1] == linha_id and paragem[2] == estacao_id:  # Line ID and Station ID match
                resultado.append(linha)
                break

    return resultado

def listar_paragens():
    caminho = caminho_ficheiro("paragens.txt")
    paragens = []

    if os.path.exists(caminho):
        with open(caminho, "r") as ficheiro:
            for linha in ficheiro:
                partes = linha.strip().split(";")
                if len(partes) == 3:  # Ensure valid stop format
                    paragens.append(partes)

    return paragens