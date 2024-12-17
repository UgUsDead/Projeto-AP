import my_functions as mf
import random
def menu_principal():
    
    print('''  
╔═══════════════════════════════════════════════════╗
║    Bem-vindo ao Sistema de Gestão Ferroviária!    ║
╠═══════════════════════════════════════════════════╣
║  1. Adicionar Estação                             ║
║  2. Adicionar Carril                              ║
║  3. Adicionar Linha                               ║
║  4. Adicionar Comboio                             ║
║  5. Adicionar Viagem                              ║
║  6. Adicionar Paragem de Viagem                   ║
║  7. Listar Estações                               ║
║  8. Listar Carris                                 ║
║  9. Listar Linhas                                 ║
║ 10. Listar Comboios                               ║
║ 11. Listar Viagens por Linha                      ║
║ 12. Adicionar Reserva de Viagem                   ║
║ 13. Listar Horário de uma Viagem e suas Paragens  ║
║ 14. Mostrar Mapa                                  ║
║  0. Sair                                          ║
╚═══════════════════════════════════════════════════╝
''')

greve=random.randint(1,10)
if greve!=10:

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()
        
        match opcao:
            case "1": 
                codigo = input("Código da estação (4 letras): ").strip().upper()
                nome = input("Nome da estação: ").strip()
                latitude = input("Latitude: ").strip()
                longitude = input("Longitude: ").strip()
                #Inputs
                
                if len(codigo) != 4:
                    print("Código tem de ter 4 letras!")
                else:
                    if mf.estacao_existe(codigo)==True: #Check se codigo de estação já existe em algum ficheiro
                        print("Erro: A estação já existe!")
                    else:
                        mf.adicionar_estacao(codigo, nome, latitude, longitude) #Adiciona estação ao ficheiro
                        print("Estação adicionada com sucesso!")
            
            case "2": #checked
                estacao_a = input("Código da estação A: ").strip().upper()
                estacao_b = input("Código da estação B: ").strip().upper()
                distancia = input("Distância (km): ").strip()
                vel_max = input("Velocidade máxima permitida (km/h): ").strip()
                #Inputs
                
                if mf.carril_existe(estacao_a, estacao_b)==False: #Check se carril já existe
                    if mf.estacao_existe(estacao_a)==True and mf.estacao_existe(estacao_b)==True: #Check se ambas as estações existem
                        mf.adicionar_carril(estacao_a, estacao_b, distancia, vel_max) #Adiciona carril ao ficheiro
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
                #Inputs
                if (tipo_servico!="U" or tipo_servico!="R" or tipo_servico!="I"or tipo_servico!="A" ):
                    if mf.adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico)==True:  #Esta função tem as verificações "built-in". Adiciona linha ao ficheiro
                        print("Linha adicionada com sucesso!")
                    else:
                        print("Falha ao adicionar linha.")
                else:
                    print("Por favor selecione um tipo de serviço válido!")
            
            case "4":
                numero_serie = input("Número de Série (5 dígitos): ").strip()
                modelo = input("Modelo: ").strip()
                vel_max = input("Velocidade Máxima (km/h): ").strip()
                capacidade = input("Capacidade: ").strip()
                tipo_servico = input("Tipo de Serviço (U, R, I, A): ").strip().upper()
                #Inputs 
                
                if mf.adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico)==True: #Esta função tem as verificações "built-in". Adiciona comboio ao ficheiro
                    print("Comboio adicionado com sucesso!")
                else:
                    print("Falha ao adicionar comboio.")
            
            case "5":
                identificador_viagem = input("Identificador da Viagem: ").strip()
                codigo_linha = input("Código da Linha: ").strip().upper()
                numero_serie_comboio = input("Número de Série do Comboio: ").strip()
                hora_partida = input("Hora de Partida (HH:MM): ").strip()
                dia=input("Dia da Viagem: ").strip()
                mes=input("Mês da Viagem: ").strip()
                ano=input("Ano da Viagem: ").strip()
                
                #Inputs
                if len(hora_partida.split(":")) != 2 or hora_partida.split(":")[0].isdigit()==False or hora_partida.split(":")[1].isdigit()==False or (0 <= int(hora_partida.split(":")[0]) < 24)==False or (0 <= int(hora_partida.split(":")[1]) < 60)==False: #Validação de hora de partida
                    print("Erro: Hora de partida inválida!")
                    continue
               
                hora_chegada = input("Hora de Chegada (HH:MM): ").strip()
                if len(hora_chegada.split(":")) != 2 or hora_chegada.split(":")[0].isdigit()==False or hora_chegada.split(":")[1].isdigit()==False or (0 <= int(hora_chegada.split(":")[0]) < 24)==False or (0 <= int(hora_chegada.split(":")[1]) < 60)==False: #Validação hora de chegada
                    print("Erro: Hora de chegada inválida!")
                    continue
                numero_passageiros = input("Número de Passageiros: ").strip()
                if numero_passageiros.isdigit()==False or int(numero_passageiros) < 0: #Verificação do nº de passageiros
                    print("Erro: Número de passageiros inválido!")
                    continue
                
                if mf.adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros)==True: #função tem verificações "built-in". Verifica e adiciona info ao ficheiro
                    print("Viagem adicionada com sucesso!")
                else:
                    print("Falha ao adicionar viagem.")

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

                if mf.adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar)==True:
                    mf.codigo_qr(identificador_viagem,nome_passageiro,lugar)
                    print("Reserva de viagem adicionada com sucesso!")

                else:
                    print("Falha ao adicionar reserva de viagem.")
            
            case "13":
                identificador_viagem = input("Identificador da Viagem: ").strip()
                if mf.listar_horario_viagem(identificador_viagem)==False:
                    print("Erro ao listar o horário da viagem.")

            case "14":
                mf.mapa()
                print("Mapa impresso com sucesso!")
            
            case "0":
                print("A encerrar o sistema. Até logo!")
                break
            
            case _:
                print("Opção inválida! Tente novamente.")

        if opcao not in [str(i) for i in range(15)]:
            print("Opção inválida! Tente novamente.")
else:
    print("A CP hoje está de greve. Pedimos desculpa por qualquer incomodo que esta situação possa ter causado :c")
    print("Thats its folks")