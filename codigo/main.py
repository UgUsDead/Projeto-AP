import os
import my_functions as mf

def menu_principal():
    print("Bem-vindo ao Sistema de Gestão Ferroviária!")
    print("1. Adicionar Estação")
    print("2. Listar Estações")
    print("3. Adicionar Carril")
    print("4. Listar Carris")
    print("5. Adicionar Linha")
    print("6. Listar Linhas")
    print("0. Sair")

while True:
    menu_principal()
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        codigo = input("Código da estação (4 letras): ").strip().upper()
        nome = input("Nome da estação: ").strip()
        latitude = input("Latitude: ").strip()
        longitude = input("Longitude: ").strip()
        
        if mf.estacao_existe(codigo):
            print("Erro: A estação já existe!")
        else:
            mf.adicionar_estacao(codigo, nome, latitude, longitude)
            print("Estação adicionada com sucesso!")
    
    elif opcao == "2":
        estacoes = mf.listar_estacoes()
        if estacoes:
            print("Estações cadastradas:")
            for estacao in estacoes:
                print("Código:", estacao[0], "| Nome:", estacao[1], "| Lat:", estacao[2], "| Long:", estacao[3])
        else:
            print("Nenhuma estação cadastrada.")
    
    elif opcao == "3":
        estacao_a = input("Código da estação A: ").strip().upper()
        estacao_b = input("Código da estação B: ").strip().upper()
        distancia = input("Distância (km): ").strip()
        vel_max = input("Velocidade máxima permitida (km/h): ").strip()
        
        if mf.estacao_existe(estacao_a) and mf.estacao_existe(estacao_b):
            mf.adicionar_carril(estacao_a, estacao_b, distancia, vel_max)
            print("Carril adicionado com sucesso!")
        else:
            print("Erro: Uma ou ambas as estações não existem.")
    
    elif opcao == "4":
        carris = mf.listar_carris()
        if carris:
            print("Carris cadastrados:")
            for carril in carris:
                print("Código:", carril[0], "| Estação A:", carril[1], "| Estação B:", carril[2],
                      "| Distância:", carril[3], "km | Vel. Máx.:", carril[4], "km/h")
        else:
            print("Nenhum carril cadastrado.")
    
    elif opcao == "5":
        codigo_linha = input("Código da linha: ").strip().upper()
        nome = input("Nome da linha: ").strip()
        estacao_partida = input("Código da estação de partida: ").strip().upper()
        estacao_chegada = input("Código da estação de chegada: ").strip().upper()
        tipo_servico = input("Tipo de serviço (U, R, I, A): ").strip().upper()
        
        if mf.estacao_existe(estacao_partida) and mf.estacao_existe(estacao_chegada):
            sucesso = mf.adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico)
            if sucesso:
                print("Linha adicionada com sucesso!")
            else:
                print("Erro ao adicionar a linha.")
        else:
            print("Erro: Uma ou ambas as estações não existem.")
    
    elif opcao == "6":
        linhas = mf.listar_linhas()
        if linhas:
            print("Linhas cadastradas:")
            for linha in linhas:
                print("Código:", linha[0], "| Nome:", linha[1], "| Partida:", linha[2],
                      "| Chegada:", linha[3], "| Tipo de Serviço:", linha[4])
        else:
            print("Nenhuma linha cadastrada.")
    
    elif opcao == "0":
        print("Encerrando o sistema. Até logo!")
        break
    
    else:
        print("Opção inválida! Tente novamente.")
