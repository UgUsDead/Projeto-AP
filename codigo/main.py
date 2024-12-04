import my_functions
print("Bem vindo à CP!! \n\n 1-Adicionar estação \n\n 2-Adicionar carril \n\n 3-Adicionar Linha \n\n 4- Adicionar Comboio\n\n 5-Adicionar Viagem \n\n 6-Reservar viagem \n\n")

resp=input("Por favor escolha uma opção: ")

if (resp=="1"):
    print(my_functions.estacao(1,2,3,4))