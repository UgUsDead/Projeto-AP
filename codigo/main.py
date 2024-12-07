import my_functions
import os

# Defini funções iniciais de maneira a que o código fique mais limpo pois podes chamar apenas uma vez a função e não ter de repetir o código
def obter_diretorio_dados():
    # Mostrar onde estão guardados
    path = os.path.realpath(__file__)
    return os.path.join(os.path.dirname(path).replace('codigo', 'dados'))

def ler_ficheiro(nome_ficheiro):
    # Ler os dados do ficheiro
    dir_dados = obter_diretorio_dados()
    caminho_ficheiro = os.path.join(dir_dados, nome_ficheiro)
    f = open(caminho_ficheiro, "r")
    linhas = [linha.strip().split(";") for linha in f.readlines()]
    f.close()
    return linhas

def verificar_codigo_unico(nome_ficheiro, codigo, indice=0):
    # Verificação se é único
    dados = ler_ficheiro(nome_ficheiro)
    return all(linha[indice] != codigo for linha in dados)

# Menu inicial da CP, os comboios que nunca se atrasam
print("Bem vindo à CP!! \n\n 1-Adicionar estação \n\n 2-Adicionar carril \n\n 3-Adicionar Comboio \n\n 4- Adicionar Linha\n\n 5-Adicionar Viagem \n\n 6-Reservar viagem \n\n")

resp = input("Por favor escolha uma opção: ")

# Adicionar Estação
if resp == "1":
    check = False
    while not check:
        cod_est = input("Por favor insira o código da estação: ")
        if not verificar_codigo_unico("tabela_estacoes.txt", cod_est):
            print("Código de estação já existe, por favor insira outro!")
        else:
            check = True

    nome_est = input("Por favor insira o nome da estação: ")
    lati = float(input("Por favor insira a Latitude da estação: "))
    longi = float(input("Por favor insira a Longitude da estação: "))

    my_functions.estacao(cod_est, nome_est, lati, longi)

# Adicionar Carril
elif resp == "2":
    check = False
    while not check:
        cod_car = input("Por favor insira o código do carril: ")
        if not verificar_codigo_unico("tabela_carril.txt", cod_car):
            print("Código de carril já existe, por favor insira outro!")
        else:
            check = True

    estacoes = ler_ficheiro("tabela_estacoes.txt")
    check_estacoes = False
    while not check_estacoes:
        estA = input("Por favor insira o nome de uma das estações ligadas por este carril: ")
        estB = input("Por favor insira o nome da outra estação ligada por este carril: ")

        if any(e[0] == estA for e in estacoes) and any(e[0] == estB for e in estacoes):
            check_estacoes = True
        else:
            print("Pelo menos uma das estações não existe, certifique-se que ambas as estações que quer ligar existem antes de criar um carril!")

    dist = float(input("Por favor insira a distância entre as estações: "))
    maxvel = float(input("Por favor insira a velocidade máxima entre as estações: "))#lembrar que os comboios da cp nao podem ir muito rapido senao passam por cima de gajos de fones a ouvir musica

    my_functions.carril(cod_car, estA, estB, dist, maxvel)

# Adicionar Comboio
elif resp == "3":
    check = False
    cod_comb = ""
    while not check or len(cod_comb) != 5:
        cod_comb = input("Por favor insira o número de série do comboio (5 dígitos): ")
        if not verificar_codigo_unico("tabela_comboios.txt", cod_comb):
            print("Código de comboio já existe, por favor insira outro!")
            check = False
        else:
            check = True

    modelo_comb = input("Por favor insira o modelo do comboio: ")
    velocidade_comb = input("Por favor insira a velocidade máxima do comboio: ")
    capacidade_comb = input("Por favor insira a capacidade máxima do comboio: ")

    tiposervico = ""
    while tiposervico not in ["U", "R", "I", "A"]:
        tiposervico = input("Por favor insira o tipo de serviço (U, R, I ou A): ").upper()

    my_functions.comboio(cod_comb, modelo_comb, velocidade_comb, capacidade_comb, tiposervico)

# Adicionar Linha
elif resp == "4":
    check = False
    while not check:
        cod_linha = input("Por favor insira o código desta linha: ")
        if not verificar_codigo_unico("tabela_linhas.txt", cod_linha):
            print("Código da linha já existe, por favor insira outro!")
        else:
            check = True

    nome_linha = input("Por favor insira o nome desta linha: ")
    quant_ests = int(input("Por favor insira quantas estações quer que façam parte desta linha: "))

    estacoes = ler_ficheiro("tabela_estacoes.txt")
    carris = ler_ficheiro("tabela_carril.txt")
    ests = []

    count = 0
    while count < quant_ests:
        est_check = False
        carril_check = False

        est = input(f"Por favor diga qual vai ser a {count + 1}ª estação: ").upper()

        if any(e[0] == est for e in estacoes):
            est_check = True

        if len(ests) == 0:
            if any(est in (c[1], c[2]) for c in carris):
                carril_check = True
        else:
            ultima_est = ests[-1]
            if any((ultima_est in (c[1], c[2]) and est in (c[1], c[2])) for c in carris):
                carril_check = True

        if est_check and carril_check:
            ests.append(est)
            count += 1
        else:
            print("A estação que pediu não existe ou não tem ligações com outras estações!")

    tiposervico = ""
    while tiposervico not in ["U", "R", "I", "A"]:
        tiposervico = input("Por favor insira o tipo de serviço (U, R, I ou A): ").upper()

    my_functions.linha(cod_linha, nome_linha, ests, tiposervico)