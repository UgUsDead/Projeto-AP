import my_functions as mf
import random
def menu_principal():
    
    print('''  
╔═══════════════════════════════════════════════════╗
║         Bem-vindo á CP Comboios Portugal!         ║
╠═══════════════════════════════════════════════════╣
║  1. Adicionar Estação                             ║
║  2. Adicionar Carril                              ║
║  3. Adicionar Linha                               ║
║  4. Adicionar Comboio                             ║
║  5. Adicionar Viagem                              ║
║  6. Listar Estações                               ║
║  7. Listar Carris                                 ║
║  8. Listar Linhas                                 ║
║  9. Listar Comboios                               ║
║ 10. Listar Viagens por Linha                      ║
║ 11. Adicionar Reserva de Viagem                   ║
║ 12. Listar Horário de uma Viagem e suas Paragens  ║
║ 13. Mostrar Mapa                                  ║
║ 14. Procurar por comboio                          ║
║ 15. Procurar linhas a partir de estação           ║
║ 16. Pesquisar viagens por est de partida/chegada  ║             
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
                    print("O Código tem de ter 4 letras(apenas letras aceites)!")
                    input("Pressione Enter para continuar...")
                else:
                    if mf.estacao_existe(codigo)==True: 
                        print("Erro: A estação já existe!")
                        input("Pressione Enter para continuar...")
                    else:
                        mf.adicionar_estacao(codigo, nome, latitude, longitude) 
                        print("Estação adicionada com sucesso!")
                        input("Pressione Enter para continuar...")
            
            case "2": 
                estacao_a = input("Código da estação A: ").strip().upper()
                estacao_b = input("Código da estação B: ").strip().upper()
                distancia = input("Distância (km): ").strip()
                vel_max = input("Velocidade máxima permitida (km/h): ").strip()
                if estacao_a != estacao_b:
                    if mf.carril_existe(estacao_a, estacao_b)==False: 
                        if mf.estacao_existe(estacao_a)==True and mf.estacao_existe(estacao_b)==True: 
                            mf.adicionar_carril(estacao_a, estacao_b, distancia, vel_max)
                            print("Carril adicionado com sucesso!")
                            input("Pressione Enter para continuar...")
                        else:
                            print("Erro: Uma ou ambas as estações não existem!")
                            input("Pressione Enter para continuar...")
                    else:
                        print("Erro: O carril já existe!")
                        input("Pressione Enter para continuar...")
                else:
                    print("Estações têm de ser diferentes!")
                    input("Pressione Enter para continuar...")
            case "3": 
                codigo_linha = input("Código da linha: ").strip().upper()
                nome = input("Nome da linha: ").strip()
                estacao_partida = input("Código da estação de partida: ").strip().upper()
                estacao_chegada = input("Código da estação de chegada: ").strip().upper()
                tipo_servico = input("Tipo de serviço (U, R, I, A): ").strip().upper()
                #Inputs
                if estacao_partida != estacao_chegada:
                    if (tipo_servico!="U" or tipo_servico!="R" or tipo_servico!="I"or tipo_servico!="A" ):
                        if mf.adicionar_linha(codigo_linha, nome, estacao_partida, estacao_chegada, tipo_servico)==True:
                            print("Linha adicionada com sucesso!")
                            input("Pressione Enter para continuar...")
                        else:
                            print("Erro ao adicionar linha, por favor verifique os dados submetidos.")
                            input("Pressione Enter para continuar...")
                    else:
                        print("Tipo de serviço não existe! Por favor introduza um tipo de serviço válido(U ,R ,I ,A).")
                        input("Pressione Enter para continuar...")
                else:
                    print("Estações têm de ser diferentes!")
                    input("Pressione Enter para continuar...")
            case "4":
                numero_serie = input("Número de Série (5 números): ").strip()
                modelo = input("Modelo: ").strip()
                vel_max = input("Velocidade Máxima (km/h): ").strip()
                capacidade = input("Capacidade: ").strip()
                tipo_servico = input("Tipo de Serviço (U, R, I, A): ").strip().upper()
                #Inputs 
                
                if mf.adicionar_comboio(numero_serie, modelo, vel_max, capacidade, tipo_servico)==True:
                    print("Comboio adicionado com sucesso!")
                    input("Pressione Enter para continuar...")
                else:
                    print("Erro ao adicionar comboio, por favor verifique os dados submetidos.")
                    input("Pressione Enter para continuar...")
            
            case "5":
                identificador_viagem = input("Id. da Viagem: ").strip()
                codigo_linha = input("Código da Linha: ").strip().upper()
                numero_serie_comboio = input("Número de Série do Comboio: ").strip()
                hora_partida = input("Hora de Partida (HH:MM): ").strip()
                dia=input("Dia da Viagem: ").strip()
                mes=input("Mês da Viagem: ").strip()
                ano=input("Ano da Viagem: ").strip()
                
                #Inputs
                if len(hora_partida.split(":")) != 2 or hora_partida.split(":")[0].isdigit()==False or hora_partida.split(":")[1].isdigit()==False or (0 <= int(hora_partida.split(":")[0]) < 24)==False or (0 <= int(hora_partida.split(":")[1]) < 60)==False: #Validação de hora de partida
                    print("Erro: Hora de partida inválida!")
                    input("Pressione Enter para continuar...")
                    continue
               
                hora_chegada = input("Hora de Chegada (HH:MM): ").strip()
                if len(hora_chegada.split(":")) != 2 or hora_chegada.split(":")[0].isdigit()==False or hora_chegada.split(":")[1].isdigit()==False or (0 <= int(hora_chegada.split(":")[0]) < 24)==False or (0 <= int(hora_chegada.split(":")[1]) < 60)==False: #Validação hora de chegada
                    print("Erro: Hora de chegada inválida!")
                    input("Pressione Enter para continuar...")
                    continue
                numero_passageiros = input("Número de Passageiros: ").strip()
                if numero_passageiros.isdigit()==False or int(numero_passageiros) < 0:
                    print("Erro: Número de passageiros inválido!")
                    input("Pressione Enter para continuar...")
                    continue
                
                if mf.adicionar_viagem(identificador_viagem, codigo_linha, numero_serie_comboio, hora_partida, hora_chegada, dia, mes, ano, numero_passageiros)==True:
                    print("Viagem adicionada com sucesso!")
                    input("Pressione Enter para continuar...")
                else:
                    
                    input("Pressione Enter para continuar...")

            case "6":
                estacoes = mf.listar_estacoes()
                if estacoes:
                    print("Estações registados:")
                    for estacao in estacoes:
                        print("Código: " + estacao[0] + " | Nome: " + estacao[1] + " | Latitude: " + estacao[2] + " | Longitude: " + estacao[3])
                    input("Pressione Enter para continuar...")
                else:
                    print("Não existem estações registadas.")
                    input("Pressione Enter para continuar...")
            
            case "7":
                carris = mf.listar_carris()
                if carris:
                    print("Carris registados:")
                    for carril in carris:
                        print("Código: " + carril[0] + " | Estação A: " + carril[1] + " | Estação B: " + carril[2] + " | Distância: " + carril[3] + " | Velocidade Máxima: " + carril[4])
                    input("Pressione Enter para continuar...")
                else:
                    print("Nao existem carris registados.")
                    input("Pressione Enter para continuar...")
            
            case "8":
                linhas = mf.listar_linhas()
                if linhas:
                    print("Linhas registadas:")
                    for linha in linhas:
                        codigo, nome, partida, chegada, tipo, paragens = linha
                        print("Código: " + codigo + " | Nome: " + nome + " | Partida: " + partida + " | Chegada: " + chegada + " | Tipo de Serviço: " + tipo)
                        if paragens:
                            print("paragens intermédias: " + ", ".join(paragens))
                    input("Pressione Enter para continuar...")
                else:
                    print("Não existem linhas registadas.")
                    input("Pressione Enter para continuar...")
            
            case "9":
                comboios = mf.listar_comboios()
                if comboios:
                    print("Comboios registados:")
                    for comboio in comboios:
                        print("Número de Série: " + comboio[0] + " | Modelo: " + comboio[1] + " | Velocidade Máxima: " + comboio[2] + " | Capacidade: " + comboio[3] + " | Tipo de Serviço: " + comboio[4])
                    input("Pressione Enter para continuar...")
                else:
                    print("Não exitem comboios registados.")
                    input("Pressione Enter para continuar...")
            
            case "10":
                codigo_linha = input("Código da Linha: ").strip().upper()
                viagens = mf.listar_viagens_por_linha(codigo_linha)
                if viagens:
                    print("Viagens registadas para a linha " + codigo_linha + ":")
                    for viagem in viagens:
                        print("Id: " + viagem[0] + " | Código da Linha: " + viagem[1] + " | Número de Série do Comboio: " + viagem[2] + " | Hora de Partida: " + viagem[3] + " | Hora de Chegada: " + viagem[4] + " | Data: " + viagem[5] + "/" + viagem[6] + "/" + viagem[7] + " | Número de Passageiros: " + viagem[8])
                    input("Pressione Enter para continuar...")
                else:
                    print("Nenhuma viagem registada para a linha " + codigo_linha + ".")
                    input("Pressione Enter para continuar...")
            
            case "11":
                identificador_reserva_viagem = input("Id da Reserva de Viagem: ").strip()
                identificador_viagem = input("Id da Viagem: ").strip()
                nome_passageiro = input("Nome do Passageiro: ").strip()
                lugar = input("Lugar: ").strip()

                if mf.adicionar_reserva_viagem(identificador_reserva_viagem, identificador_viagem, nome_passageiro, lugar)==True:
                    mf.codigo_qr(identificador_viagem,nome_passageiro,lugar)
                    print("Reserva de viagem adicionada com sucesso!")
                    input("Pressione Enter para continuar...")

                else:
                    print("Erro ao adicionar reserva de viagem.")
                    input("Pressione Enter para continuar...")
            
            case "12":
                identificador_viagem = input("Id da Viagem: ").strip()
                if mf.listar_horario_viagem(identificador_viagem)==False:
                    print("Erro ao listar o horário da viagem.")
                    input("Pressione Enter para continuar...")

            case "13":
                mf.mapa()
                print("Mapa impresso com sucesso!")
                input("Pressione Enter para continuar...")

            case "14":
                print("Procurar Comboio:")
                print("1. Procurar por Número de Série")
                print("2. Procurar por Quantidade Máxima de Passageiros")
                escolha = input("Escolha uma opção (1 ou 2): ").strip()

                if escolha == "1":
                    tipo = "NS"
                    valor = input("Introduza o Número de Série do Comboio: ").strip()
                elif escolha == "2": 
                    tipo = "CAP"
                    valor = input("Introduza a Capacidade Máxima (número): ").strip()
                    if valor.isdigit()==False:
                        print("Erro: Capacidade deve ser um número válido.")
                        input("Pressione Enter para continuar...")
                        continue
                else:
                    print("Opção inválida.")
                    input("Pressione Enter para continuar...")
                    continue

                resultado = mf.procurar_comboio(tipo, valor)

                if resultado:
                    print("Comboios encontrados:")
                    for comboio in resultado:
                        print("Número de Série: " + comboio[0] + " | Nome: " + comboio[1] + " | Velocidade Máxima: " + comboio[2] + " | Capacidade: " + comboio[3] + " | Tipo de Serviço: " + comboio[4])
                    input("Pressione Enter para continuar...")
                else:
                    print("Nenhum comboio encontrado.")
                    input("Pressione Enter para continuar...")

            case "15":  
                estacao_id = input("Introduza o ID da Estação (ex: LISB, PORT): ").strip().upper()
                resultado = mf.procurar_linhas_por_estacao(estacao_id)

                if resultado:
                    print("Linhas que passam pela estação " + estacao_id + ":")
                    for linha in resultado:
                        print("ID: " + linha[0] + " | Nome: " + linha[1] + " | Tipo de Serviço: " + linha[4])
                    input("Pressione Enter para continuar...")
                else:
                    print("Nenhuma linha encontrada para a estação " + estacao_id + ".")
                    input("Pressione Enter para continuar...")

            case "16":  # Procurar viagens por estação
                estacao_id = input("Introduza o ID da Estação (ex: LISB): ").strip().upper()
                resultado = mf.procurar_viagens_por_estacao(estacao_id)

                if resultado:
                    print("Viagens que começam ou terminam na estação " + estacao_id + ":")
                    for viagem in resultado:
                        print("ID Viagem: " + viagem[0] + " | Linha ID: " + viagem[1] +" | Comboio: " + viagem[2] + " | Hora de Partida: " + viagem[3] +" | Hora de Chegada: " + viagem[4] + " | Data: "+viagem[5]+"/"+viagem[6]+"/"+ viagem[7] + " | Passageiros: " + viagem[8])
                    input("Pressione Enter para continuar...")
                else:
                    print("Nenhuma viagem encontrada para a estação " + estacao_id + ".")
                    input("Pressione Enter para continuar...")

            case "0":
                print("A CP vai encerrar, muito obrigado por escolher o nosso serviço extremamente mediocre!")
                break
        if opcao not in [str(i) for i in range(17)]: 
            print("Opção inválida! Tente novamente.")
else:
    print("A CP hoje está de greve. Pedimos desculpa por qualquer incomodo que esta situação possa ter causado :c")
    print("Thats all folks")