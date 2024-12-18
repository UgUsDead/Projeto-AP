import os
import qrcode
import folium 

def caminho_ficheiro(nome_ficheiro):  
    # Função para obter o caminho completo de um ficheiro de dados
    path = os.path.realpath(__file__) # Obter o diretório principal do ficheiro atual
    dir = os.path.dirname(path).replace("codigo", "dados") # Substituir 'codigo' por 'dados'
    if os.path.exists(dir)== False:
        os.makedirs(dir)  
    return os.path.join(dir, nome_ficheiro)

def adicionar_estacao(codigo, nome, latitude, longitude):
    
    if validar_numero(latitude) == False or validar_numero(longitude) == False: 
        print("Erro: Latitude e longitude devem ser números válidos.")
        return
    else:
        # Adicionar a estação ao ficheiro estacoes.txt
        caminho = caminho_ficheiro("estacoes.txt")
        linha = codigo + ";" + nome + ";" + latitude + ";" + longitude + "\n"
        ficheiro = open(caminho, "a")
        ficheiro.write(linha)
        ficheiro.close()

def adicionar_carril(estacao_a, estacao_b, distancia, vel_max): 
    if validar_numero(distancia) == False or validar_numero(vel_max) == False: # Verificar se a distância e a velocidade máxima são números válidos
        print("Erro: Distância e velocidade máxima devem ser números válidos.")
        return
    else:
        # Adicionar o carril ao ficheiro carris.txt
        caminho = caminho_ficheiro("carris.txt")
        codigo_carril = estacao_a + "_" + estacao_b
        linha = codigo_carril + ";" + estacao_a + ";" + estacao_b + ";" + distancia + ";" + vel_max + "\n"
        ficheiro = open(caminho, "a")
        ficheiro.write(linha)
        ficheiro.close()

def adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico):
    if estacao_existe(estacao_partida) == False or estacao_existe(estacao_chegada) == False: # Verificar se as estações de partida e chegada existem
        print("Erro: Estações de partida ou chegada não existem.")
        return False
    if existe_caminho(estacao_partida, estacao_chegada) == False: # Verificar se há um caminho entre as estações
        print("Erro: Não há carris conectando as estações especificadas.")
        return False
    if linha_existe(codigo_linha): # Verificar se o código da linha já existe
        print("Erro: Código da linha já existe.")
        return False

    # Obter o caminho entre as estações
    caminho_estacoes = obter_caminho(estacao_partida, estacao_chegada)
    
    if len(caminho_estacoes) > 2: # Se houver estações intermediárias, perguntar ao utilizador se deseja adicioná-las
        print("O caminho passa pelas seguintes estações intermediárias:")
        for estacao in caminho_estacoes[1:-1]:
            print(estacao)
        resposta = input("Deseja adicionar paragens nas estações intermediárias? (s/n): ").strip().lower()
        if resposta == 's':
            paragens = caminho_estacoes[1:-1]
        else:
            paragens = []
    else:
        paragens = []

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
        for linha in ficheiro_paragens: # Percorrer todas as linhas do ficheiro paragens.txt para encontrar o último ID
            detalhes = linha.strip().split(";") # Separar os detalhes da linha
            if len(detalhes) >= 1 and detalhes[0].isdigit(): # Verificar se o ID é um número válido 
                ultimo_id = max(ultimo_id, int(detalhes[0]))  # Atualiza o último ID
        ficheiro_paragens.close()

    # Adicionar as paragens ao ficheiro paragens.txt
    ficheiro_paragens = open(caminho_paragens, "a")
    for paragem in paragens:
        ultimo_id += 1  # Incrementa o ID
        linha_paragem = str(ultimo_id) + ";" + codigo_linha + ";" + paragem + "\n"
        ficheiro_paragens.write(linha_paragem)
    ficheiro_paragens.close()

    return True

def adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico):
    # Verificar se os dados são válidos
    if numero_serie.isdigit()==False or len(numero_serie) != 5: # Verificar se o número de série é um número válido com 5 dígitos 
        print("Erro: Número de série deve ser um número válido com 5 dígitos.")
        return False
    if validar_numero(vel_max)==False or validar_numero(capacidade)==False: # Verificar se a velocidade máxima e a capacidade são números válidos
        print("Erro: Velocidade máxima e capacidade devem ser números válidos.")
        return False
    if tipo_servico not in ["U", "R", "I", "A"]: # Verificar se o tipo de serviço é válido
        print("Erro: Tipo de serviço deve ser 'U' (urbano), 'R' (regional), 'I' (intercidades) ou 'A' (Alfa-Pendular).")
        return False
    
    comboios = listar_comboios()
    for comboio in comboios: # Verificar se o número de série já existe
        if comboio[0] == numero_serie:
            print("Erro: Número de série já existe!")
            return False
    
    caminho = caminho_ficheiro("comboios.txt")
    linha = numero_serie + ";" + modelo + ";" + vel_max + ";" + capacidade + ";" + tipo_servico + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros):
    # Verificar inputs básicos
    if not validar_numero(identificador_viagem):
        print("Erro: Identificador da viagem deve ser um número válido.")
        return False
    if not validar_numero(numero_passageiros):
        print("Erro: Número de passageiros deve ser um número válido.")
        return False
    if not validar_data(dia, mes, ano):
        print("Erro: Data inválida.")
        return False

    # Verificar se o identificador da viagem já existe
    viagens = listar_viagens() 
    for viagem in viagens:
        if viagem[0] == identificador_viagem:
            print("Erro: Identificador da viagem já existe.")
            return False

    # Verificar existência do comboio e linha, bem como compatibilidade de tipos e capacidade
    comboios = listar_comboios()
    tipo_servico_comboio = None
    comboio_existe = False

    for comboio in comboios:
        if comboio[0] == numero_serie_comboio:
            comboio_existe = True
            # Verificar capacidade
            if int(comboio[3]) < int(numero_passageiros):
                print("Erro: O número de passageiros excede a capacidade do comboio.")
                return False
            tipo_servico_comboio = comboio[4]
            break

    if not comboio_existe:
        print("Erro: Número de série do comboio não existe.")
        return False

    linhas = listar_linhas()
    linha_encontrada = None
    for linha in linhas:
        if linha[0] == codigo_linha:
            linha_encontrada = linha
            break

    if linha_encontrada is None:
        print("Erro: Código da linha não existe.")
        return False

    # Verificar se o tipo de serviço do comboio corresponde ao da linha
    if linha_encontrada[4] != tipo_servico_comboio:
        print("Erro: O tipo de serviço do comboio não corresponde ao tipo de serviço da linha.")
        return False

    # Verificar se existe caminho entre as estações da linha
    if not existe_caminho(linha_encontrada[2], linha_encontrada[3]):
        print("Erro: Não há carris conectando as estações especificadas.")
        return False

    # Todas as verificações passaram, então adiciona a viagem
    caminho_viagens = caminho_ficheiro("viagens.txt")
    ficheiro_viagens = open(caminho_viagens, "a")
    linha = identificador_viagem + ";" + codigo_linha + ";" + numero_serie_comboio + ";" + hora_partida + ";" + hora_chegada + ";" + dia + ";" + mes + ";" + ano + ";" + numero_passageiros + "\n"
    ficheiro_viagens.write(linha)
    ficheiro_viagens.close()

    # Adicionar paragens da linha à viagem
    paragens = []
    caminho_paragens = caminho_ficheiro("paragens.txt")
    if os.path.exists(caminho_paragens):
        with open(caminho_paragens, "r") as ficheiro_paragens:
            linhas_paragens = ficheiro_paragens.readlines()
        for lin in linhas_paragens:
            detalhes = lin.strip().split(";")
            # detalhes: [id_paragem, codigo_linha, estacao_paragem]
            # Procurar paragens para a linha em questão
            if len(detalhes) == 3 and detalhes[1] == codigo_linha:
                paragens.append(detalhes[2])

    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    with open(caminho_paragens_viagem, "a") as ficheiro_paragens_viagem:
        index = 1
        for station_id in paragens:
            ficheiro_paragens_viagem.write(
                "PV" + identificador_viagem + "_" + str(index) + ";" + station_id + ";" + identificador_viagem + "\n"
            )
            index += 1

    return True


def adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar):
    # Verificar se a viagem existe
    viagens = listar_viagens()
    viagem_existe = False
    capacidade_maxima = 0
    codigo_linha = ""
    reservas = listar_reservas_por_viagem(identificador_viagem)
    for reserva in reservas:
        if reserva[0] == identificador_reserva_viagem:
            print("Erro: Já existe uma reserva com este identificador.")
            return False
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
            detalhes = linha.strip().split(";")
            if len(detalhes) == 4:  # Verificar se a linha está corretamente formatada
                estacoes.append(detalhes)
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
            detalhes = linha.strip().split(";")
            if len(detalhes) == 5:  # Verificar se a linha tem o número correto de campos
                carris.append(detalhes)
        return carris
    return []

def listar_linhas():
    #Ler ficheiro linhas
    caminho = caminho_ficheiro("linhas.txt")
    if os.path.exists(caminho)==False:
        return []
    linhas = []
    ficheiro = open(caminho, "r")
    conteudo = ficheiro.readlines()
    ficheiro.close()

    #Ler ficheiro paragens
    caminho_paragens = caminho_ficheiro("paragens.txt")
    paragens_dict = {}
    if os.path.exists(caminho_paragens):
        ficheiro_paragens = open(caminho_paragens, "r")
        for linha in ficheiro_paragens:
            detalhes = linha.strip().split(";")
            codigo_linha = detalhes[1]
            paragem = detalhes[2]
            if codigo_linha not in paragens_dict:
                paragens_dict[codigo_linha] = []
            paragens_dict[codigo_linha].append(paragem)
        ficheiro_paragens.close()

    for linha in conteudo:
        detalhes = linha.strip().split(";")
        codigo_linha = detalhes[0]
        nome = detalhes[1]
        estacao_partida = detalhes[2]
        estacao_chegada = detalhes[3]
        tipo_servico = detalhes[4]
        paragens = paragens_dict.get(codigo_linha, [])
        linhas.append((codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico, paragens))
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
        detalhes = linha.strip().split(";")
        if detalhes[1] == codigo_linha:
            viagens.append(detalhes)
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
        detalhes = linha.strip().split(";")
        if detalhes[1] == codigo_linha:
            paragens.append(detalhes)
    return paragens

def listar_reservas_por_viagem(identificador_viagem): #Lista reservas de uma viagem
    caminho = caminho_ficheiro("reservas_viagem.txt")
    if os.path.exists(caminho)==False:
        return []
    reservas = []
    ficheiro = open(caminho, "r")
    linhas = ficheiro.readlines()
    ficheiro.close()
    for linha in linhas:
        detalhes = linha.strip().split(";")
        if detalhes[1] == identificador_viagem: 
            reservas.append(detalhes)
    return reservas

def listar_horario_viagem(identificador_viagem):
    caminho_viagens = caminho_ficheiro("viagens.txt")
    caminho_paragens_viagem = caminho_ficheiro("paragens_viagem.txt")
    
    # Verificar se a viagem existe
    if os.path.exists(caminho_viagens)==False:
        print("Erro: Nenhuma viagem encontrada.")
        return False

    viagem_encontrada = None
    ficheiro_viagens = open(caminho_viagens,"r")
    linhas_viagens = ficheiro_viagens.readlines()
    ficheiro_viagens.close()

    for linha in linhas_viagens:
        detalhes = linha.strip().split(";")
        if detalhes[0] == identificador_viagem:
            viagem_encontrada = detalhes
            break

    if  viagem_encontrada==None:
        print("Erro: Identificador da viagem não existe.")
        return False

    #Ler informação acerca das paragens
    paragens_viagem = []
    if os.path.exists(caminho_paragens_viagem):
        ficheiro_paragens_viagem = open(caminho_paragens_viagem, "r")
        linhas_paragens_viagem = ficheiro_paragens_viagem.readlines()
        ficheiro_paragens_viagem.close()

        for linha in linhas_paragens_viagem:    
            detalhes = linha.strip().split(";")
            if detalhes[2] == identificador_viagem:  
                paragens_viagem.append(detalhes[1])  #Guardar info se corresponder

    #Mostar info da viagem
    print("Identificador: "+viagem_encontrada[0])
    print("Código da Linha: "+viagem_encontrada[1])
    print("Número de Série do Comboio: "+viagem_encontrada[2])
    print("Hora de Partida: "+viagem_encontrada[3])
    print("Hora de Chegada: "+viagem_encontrada[4])
    print("Data: "+viagem_encontrada[5]+"/"+viagem_encontrada[6]+"/" +viagem_encontrada[7])
    print("Número de Passageiros: "+viagem_encontrada[8])

    #Listar paragens

    if paragens_viagem:
        print("Paragens da Viagem:")
        idx = 1
        for paragem in paragens_viagem:
            print(str(idx) + ". " + paragem)
            idx += 1
    else:
        print("Nenhuma paragem associada a esta viagem.")
    input("Pressione Enter para continuar...")
    return True

def estacao_existe(codigo): #Verifica se a estação já existe
    estacoes = listar_estacoes()
    for estacao in estacoes:
        if estacao[0] == codigo:
            return True
    return False

def carril_existe(esta, estb): #Verifica se a carril já existe
    carril = listar_carris()
    for carris in carril:
        if carris[0] == esta + "_" + estb:
            return True
    return False

def linha_existe(codlin):  #Verifica se a linha já existe
    linhas = listar_linhas()
    for linha in linhas:
        if linha[0] == codlin:
            return True
    return False

def existe_caminho(estacao_a, estacao_b):  #https://www.youtube.com/watch?v=HZ5YTanv5QE Video a explicar o algoritmo BFS (Ajuda de CoPilot)
    
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

def mapa():
    ests=listar_estacoes()
    carris=listar_carris()

    m = folium.Map(location=(38.736946, -9.142685), zoom_start=7) #Define as coordenadas e foca em Portugal

    for est in ests:
        station_name = est[0]
        city = est[1]
        latitude = est[2]
        longitude = est[3]
        station_coords = {est[0]: (float(est[2]), float(est[3])) for est in ests} #Procura no dicionario pelas coordenadas e transforma em float
        
        folium.Marker(                              #Adiciona informação ao mapa para os markers
            location=(latitude, longitude),
            popup=f"{station_name}, {city}",
            tooltip=station_name
        ).add_to(m)

        for carril in carris:
            start_code = carril[1]  
            end_code = carril[2]    

            if start_code in station_coords and end_code in station_coords:
                start_coords = station_coords[start_code]
                end_coords = station_coords[end_code]

                
                folium.PolyLine(                         #Adiciona informação ao mapa para as linhas (Carris)
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
    img = qrcode.make("Id Viagem: " + identificador_viagem + ";\n" + "Nome Passageiro: " + nome_passageiro + ";\n" +"Lugar: " + lugar)
    img.save(identificador_viagem + "_" + nome_passageiro + "_" + lugar + ".png")

def obter_conexoes(): #Algoritmo BFS (Ajuda de CoPilot)
    conexoes = {}  # Dicionário de conexões vazio
    carris = listar_carris() 
    for carril in carris:  
        estacao_a, estacao_b = carril[1], carril[2]
        if estacao_a not in conexoes:  # Se a estação de partida não estiver no dicionário, adicionar a estação de partida ao dicionário com uma lista vazia
            conexoes[estacao_a] = []  
        if estacao_b not in conexoes:
            conexoes[estacao_b] = []
        conexoes[estacao_a].append(estacao_b)  # Adicionar a estação de chegada à lista de conexões da estação de partida
        conexoes[estacao_b].append(estacao_a)  # Adicionar a estação de partida à lista de conexões da estação de chegada
    return conexoes  # Retornar o dicionário de conexões

def obter_caminho(estacao_a, estacao_b): #Algoritmo BFS (Ajuda de CoPilot)
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
    
    if mes < 1 or mes > 12:
        return False
    
    
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Verificar se o ano é bissexto (Ajuda de CoPilot)
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        dias_por_mes[1] = 29  
    
    # Verificar se o dia é válido para o mês e ano
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False
    
    return True


def procurar_comboio(tipo, valor):
   
    comboios = listar_comboios()
    resultado = []

    if tipo == "NS":  #Procura por nº de série
        for comboio in comboios:
            if comboio[0] == valor:  
                resultado.append(comboio)

    elif tipo == "CAP":  #Procura pela capacidade máxima
        try:
            max_passageiros = int(valor)  
            for comboio in comboios:
                capacidade = int(comboio[3])  
                if capacidade <= max_passageiros:
                    resultado.append(comboio)
        except ValueError:
            print("Erro: A capacidade máxima deve ser um número válido.")
    else:
        print("Erro: Tipo inválido. Por favor use 'NS' para procurar o número de série ou 'CAP' para capacidade.")

    return resultado


def procurar_linhas_por_estacao(estacao_id):
   
    linhas = listar_linhas()  
    paragens = listar_paragens()  
    resultado = []
    if estacao_existe(estacao_id)==False:
        print("Erro: Estação não existe.")
        return []
    # Verifica se a estação aparece como estação inicial, final ou paragem
    for linha in linhas:
        linha_id = linha[0]
        estacao_partida = linha[2]
        estacao_chegada = linha[3]

        # Verifica se a estação é partida ou chegada
        if estacao_id == estacao_partida or estacao_id == estacao_chegada:
            resultado.append(linha)
            continue

        # Verifica se a estação é uma paragem
        for paragem in paragens:
            if paragem[1] == linha_id and paragem[2] == estacao_id:  
                resultado.append(linha)
                break

    return resultado

def listar_paragens(): #Lista paragens
    
    caminho = caminho_ficheiro("paragens.txt")
    paragens = []
    if os.path.exists(caminho):
        with open(caminho, "r") as ficheiro:
            for linha in ficheiro:
                detalhes = linha.strip().split(";")
                if len(detalhes) == 3:  
                    paragens.append(detalhes)

    return paragens

def procurar_viagens_por_estacao(estacao_id):
   
    viagens = listar_viagens()  
    linhas = listar_linhas()    
    resultado = []
    if estacao_existe(estacao_id)==False:
        print("Erro: Estação não existe.")
        return []
    # Encontrar as linhas que têm a estação como partida ou chegada
    linhas_relevantes = []
    for linha in linhas:
        estacao_partida = linha[2]
        estacao_chegada = linha[3]
        if estacao_id == estacao_partida or estacao_id == estacao_chegada:
            linhas_relevantes.append(linha[0])  

    # Comparar viagens que usam as linhas encontradas
    for viagem in viagens:
        if viagem[1] in linhas_relevantes:  # Verifica se a viagem pertence à linha
            resultado.append(viagem)

    return resultado
