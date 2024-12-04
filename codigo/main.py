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
            
            if (dadoslist[0]==cod_est):
                print("Código de estação já existe, por favor insira outro")
            else:
                check=True
            count=count+1


    nome_est= input("Por favor insira o nome da estação: ")

    lati= float(input("Por favor insira a Latitude da estação: "))

    longi=float(input("Por favor insira a longitude da estação: "))

    my_functions.estacao(cod_est,nome_est,lati,longi)

if (resp=="2"):
    check=False
    while check==False:
        cod_car=input("Por favor insira o codigo do carril: ")
        path = os.path.realpath(__file__) 
        dir = os.path.dirname(path) 
        dir = dir.replace('codigo', 'dados') 
        os.chdir(dir) 
        ficheiro= open("tabela_carril.txt","r")
        dados=ficheiro.readlines()
        ficheiro.close()
        
        count=0
        for i in dados:
            dadoslist=dados[count].split(";")
            
            
            if (dadoslist[0]==cod_car):
                print("Código de carril já existe, por favor insira outro")
            else:
                
                check=True
            count=count+1


    check=False
    while check==False:

        estA= input("Por favor insira o nome de uma das estações ligadas por este carril: ")

        estB= input("Por favor insira o nome da outra estação ligada por este carril: ")

        ficheiro= open("tabela_estacoes.txt","r")
        dados=ficheiro.readlines()
        ficheiro.close()
       
        count=0
        estcheck=0
        for i in dados:
            dadoslist=dados[count].split(";")
            print(dadoslist[0])
            print(estcheck)
            print(check)

            if (dadoslist[0]==estA or dadoslist[0]==estB):
                estcheck=estcheck+1
              

            
                
            count=count+1
           

            if estcheck>=2:
                check=True
                
            else:
                print("Uma das estações não existe. Certifique-se que essa é criada antes de criar um carril")

    dist= float(input("Por favor insira a distancia entre as estações: "))

    maxvel=float(input("Por favor insira a velocidade maxima entre as estações: "))

    my_functions.carril(cod_car,estA,estB,dist,maxvel)