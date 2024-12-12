import os
import my_functions as mf

def menu_principal():
    print("Bem-vindo ao Sistema de Gestão Ferroviária!")
    print("1. Adicionar Estação")
    print("2. Adicionar Carril")
    print("3. Adicionar Linha")
    print("4. Adicionar Comboio")
    print("5. Adicionar Viagem")
    print("6. Adicionar Paragem de Viagem")
    print("7. Listar Estações")
    print("8. Listar Carris")
    print("9. Listar Linhas")
    print("10. Listar Comboios")
    print("11. Listar Viagens por Linha")
    print("12. Adicionar Reserva de Viagem")
    print("13. Listar Horário de uma Viagem e suas Paragens")
    print("0. Sair")

while True:
    menu_principal()
    opcao = input("Escolha uma opção: ").strip()
    
    match opcao:
        case "1":
            codigo = input("Código da estação (4 letras): ").strip().upper()
            nome = input("Nome da estação: ").strip()
            latitude = input("Latitude: ").strip()
            longitude = input("Longitude: ").strip()

            if len(codigo) != 4:
                print("Código tem de ter 4 letras!")
            else:
                if mf.estacao_existe(codigo):
                    print("Erro: A estação já existe!")
                else:
                    mf.adicionar_estacao(codigo, nome, latitude, longitude)
                    print("Estação adicionada com sucesso!")
        
        case "2":
            estacao_a = input("Código da estação A: ").strip().upper()
            estacao_b = input("Código da estação B: ").strip().upper()
            distancia = input("Distância (km): ").strip()
            vel_max = input("Velocidade máxima permitida (km/h): ").strip()
            
            if not mf.carril_existe(estacao_a, estacao_b):
                if mf.estacao_existe(estacao_a) and mf.estacao_existe(estacao_b):
                    mf.adicionar_carril(estacao_a, estacao_b, distancia, vel_max)
                    print("Carril adicionado com sucesso!")
                else:
                    print("Erro: Uma ou ambas as estações não existem!")
            else:
                print("Erro: O carril já existe!")
        
        case "3":
            codigo_linha = input("Código da linha: ").strip().upper()
            nome = input("Nome da linha: ").strip()
            estacao_partida = input("Código da estação de partida: ").strip().upper()
            estacao_chegada = input("Código da estação de chegada: ").strip().upper()
            tipo_servico = input("Tipo de serviço (U, R, I, A): ").strip().upper()

            if mf.adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico):
                print("Linha adicionada com sucesso!")
            else:
                print("Falha ao adicionar linha.")
        
        case "4":
            numero_serie = input("Número de Série (5 dígitos): ").strip()
            modelo = input("Modelo: ").strip()
            vel_max = input("Velocidade Máxima (km/h): ").strip()
            capacidade = input("Capacidade: ").strip()
            tipo_servico = input("Tipo de Serviço (U, R, I, A): ").strip().upper()

            if mf.adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico):
                print("Comboio adicionado com sucesso!")
            else:
                print("Falha ao adicionar comboio.")
        
        case "5":
            identificador_viagem = input("Identificador da Viagem: ").strip()
            codigo_linha = input("Código da Linha: ").strip().upper()
            numero_serie_comboio = input("Número de Série do Comboio: ").strip()
            hora_partida = input("Hora de Partida (HH:MM): ").strip()
            hora_chegada = input("Hora de Chegada (HH:MM): ").strip()
            dia = input("Dia: ").strip()
            mes = input("Mês: ").strip()
            ano = input("Ano: ").strip()
            numero_passageiros = input("Número de Passageiros: ").strip()

            if mf.adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros):
                print("Viagem adicionada com sucesso!")
            else:
                print("Falha ao adicionar viagem.")
        
        case "6":
            identificador_paragem_viagem = input("Identificador da Paragem de Viagem: ").strip()
            identificador_paragem = input("Identificador da Paragem: ").strip()
            identificador_viagem = input("Identificador da Viagem: ").strip()
            hora_paragem = input("Hora da Paragem (HH:MM): ").strip()

            if mf.adicionar_paragem_viagem(identificador_paragem_viagem, identificador_paragem, identificador_viagem, hora_paragem):
                print("Paragem de viagem adicionada com sucesso!")
            else:
                print("Falha ao adicionar paragem de viagem.")
        
        case "7":
            estacoes = mf.listar_estacoes()
            if estacoes:
                print("Estações registadas:")
                for estacao in estacoes:
                    print("Código: " + estacao[0] + " | Nome: " + estacao[1] + " | Latitude: " + estacao[2] + " | Longitude: " + estacao[3])
            else:
                print("Nenhuma estação registada.")
        
        case "8":
            carris = mf.listar_carris()
            if carris:
                print("Carris registados:")
                for carril in carris:
                    print("Código: " + carril[0] + " | Estação A: " + carril[1] + " | Estação B: " + carril[2] + " | Distância: " + carril[3] + " | Velocidade Máxima: " + carril[4])
            else:
                print("Nenhum carril registado.")
        
        case "9":
            linhas = mf.listar_linhas()
            if linhas:
                print("Linhas registadas:")
                for linha in linhas:
                    codigo, nome, partida, chegada, tipo, paradas = linha
                    print("Código: " + codigo + " | Nome: " + nome + " | Partida: " + partida + " | Chegada: " + chegada + " | Tipo de Serviço: " + tipo)
                    if paradas:
                        print("Paradas intermédias: " + ", ".join(paradas))
            else:
                print("Nenhuma linha registada.")
        
        case "10":
            comboios = mf.listar_comboios()
            if comboios:
                print("Comboios registados:")
                for comboio in comboios:
                    print("Número de Série: " + comboio[0] + " | Modelo: " + comboio[1] + " | Velocidade Máxima: " + comboio[2] + " | Capacidade: " + comboio[3] + " | Tipo de Serviço: " + comboio[4])
            else:
                print("Nenhum comboio registado.")
        
        case "11":
            codigo_linha = input("Código da Linha: ").strip().upper()
            viagens = mf.listar_viagens_por_linha(codigo_linha)
            if viagens:
                print("Viagens registadas para a linha " + codigo_linha + ":")
                for viagem in viagens:
                    print("Identificador: " + viagem[0] + " | Código da Linha: " + viagem[1] + " | Número de Série do Comboio: " + viagem[2] + " | Hora de Partida: " + viagem[3] + " | Hora de Chegada: " + viagem[4] + " | Data: " + viagem[5] + "/" + viagem[6] + "/" + viagem[7] + " | Número de Passageiros: " + viagem[8])
            else:
                print("Nenhuma viagem registada para a linha " + codigo_linha + ".")
        
        case "12":
            identificador_reserva_viagem = input("Identificador da Reserva de Viagem: ").strip()
            identificador_viagem = input("Identificador da Viagem: ").strip()
            nome_passageiro = input("Nome do Passageiro: ").strip()
            lugar = input("Lugar: ").strip()

            if mf.adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar):
                print("Reserva de viagem adicionada com sucesso!")
            else:
                print("Falha ao adicionar reserva de viagem.")
        
        case "13":
            identificador_viagem = input("Identificador da Viagem: ").strip()
            if not mf.listar_horario_viagem(identificador_viagem):
                print("Erro ao listar o horário da viagem.")
        
        case "0":
            print("A encerrar o sistema. Até logo!")
            break
        
        case _:
            print("Opção inválida! Tente novamente.")
