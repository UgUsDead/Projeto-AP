import my_functions
from pathlib import Path
import os
print("Bem vindo à CP!! \n\n 1-Adicionar estação \n\n 2-Adicionar carril \n\n 3-Adicionar Linha \n\n 4- Adicionar Comboio\n\n 5-Adicionar Viagem \n\n 6-Reservar viagem \n\n")

resp=input("Por favor escolha uma opção: ")

if (resp=="1"):
    check=False
    while check==False:
        cod_est=input("Por favor insira o codigo da estação: ")
        path = os.path.realpath(__file__) 
        dir = os.path.dirname(path) 
        dir = dir.replace('codigo', 'dados') 
        os.chdir(dir) 
        ficheiro= open("tabela_estacoes.txt","r")
        dados=ficheiro.readlines()
        ficheiro.close()
       
        count=0
        for i in dados:
            dadoslist=dados[count].split(";")
            print(dadoslist)
            if (dadoslist[0]==cod_est):
                print("Código de estação já existe, por favor insira outro")
            else:
                check=True
            count=count+1


    nome_est= input("Por favor insira o nome da estação: ")

    lati= float(input("Por favor insira a Latitude da estação: "))

    longi=float(input("Por favor insira a longitude da estação: "))

    my_functions.estacao(cod_est,nome_est,lati,longi)