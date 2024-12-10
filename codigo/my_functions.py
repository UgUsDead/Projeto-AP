import os

def caminho_ficheiro(nome_ficheiro):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path).replace("codigo", "dados")
    if not os.path.exists(dir):
        os.makedirs(dir)  # Certifique-se de que o diretório "dados" exista
    return os.path.join(dir, nome_ficheiro)

def validar_numero(valor, tipo="float"):
    if tipo == "int":
        return valor.isdigit()
    try:
        float(valor)
        return True
    except ValueError:
        return False

def estacao_existe(codigo):
    estacoes = listar_estacoes()
    for estacao in estacoes:
        if estacao[0] == codigo:
            return True
    return False

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
    """Verifica se existe um caminho entre duas estações usando BFS."""
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

def adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico):
    if not estacao_existe(estacao_partida) or not estacao_existe(estacao_chegada):
        print("Erro: Estações de partida ou chegada não existem.")
        return False
    if not existe_caminho(estacao_partida, estacao_chegada):
        print("Erro: Não há carris conectando as estações especificadas.")
        return False
    caminho = caminho_ficheiro("linhas.txt")
    linha = codigo_linha + ";" + nome + ";" + estacao_partida + ";" + estacao_chegada + ";" + tipo_servico + "\n"
    ficheiro = open(caminho, "a")
    ficheiro.write(linha)
    ficheiro.close()
    return True

def listar_linhas():
    caminho = caminho_ficheiro("linhas.txt")
    if not os.path.exists(caminho):
        return []
    linhas = []
    ficheiro = open(caminho, "r")
    conteudo = ficheiro.readlines()
    ficheiro.close()
    for linha in conteudo:
        linhas.append(linha.strip().split(";"))
    return linhas
