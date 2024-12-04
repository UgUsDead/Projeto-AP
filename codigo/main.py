import my_functions
from pathlib import Path
import os
print("Bem vindo à CP!! \n\n 1-Adicionar estação \n\n 2-Adicionar carril \n\n 3-Adicionar Comboio \n\n 4- Adicionar Linha\n\n 5-Adicionar Viagem \n\n 6-Reservar viagem \n\n")

resp=input("Por favor escolha uma opção: ")

#input e verificação dos inputs das estações (feitas)
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
        dadoslist=[]
        for i in dados:
            dadoslist.append(dados[count].split(";"))
            count=count+1
        
        count=0
        check=True
        for i in dados:
            print (dadoslist[count][0])
            if dadoslist[count][0] == cod_est:
                print("Código de estação já existe, por favor insira outro!")
                check=False
                break
            count=count+1


    nome_est= input("Por favor insira o nome da estação: ")

    lati= float(input("Por favor insira a Latitude da estação: "))

    longi=float(input("Por favor insira a longitude da estação: "))

    my_functions.estacao(cod_est,nome_est,lati,longi)

#input e verificação dos inputs dos carris (feitas)
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
        dadoslist=[]
        for i in dados:
            dadoslist.append(dados[count])
            count=count+1

        count=0
        check=True
        for i in dados:
           
            if dadoslist[count][0] == cod_car:
                print("Código de carril já existe, por favor insira outro!")
                check=False
                break
            count=count+1

    path = os.path.realpath(__file__) 
    dir = os.path.dirname(path) 
    dir = dir.replace('codigo', 'dados') 
    os.chdir(dir) 
    ficheiro= open("tabela_estacoes.txt","r")
    dados=ficheiro.readlines()
    ficheiro.close()
    count=0
    dadoslist=[]
    for i in dados:
        dadoslist.append(dados[count].split(";"))
        count=count+1
            


        check=False
    while (check==False):

        estA= input("Por favor insira o nome de uma das estações ligadas por este carril: ")

        estB= input("Por favor insira o nome da outra estação ligada por este carril: ")

        count=0
        estcheck=0
        check=True
        for i in dados:
            
            
            if (dadoslist[count][0] == estA) or (dadoslist[count][0]==estB) :
               
                estcheck=estcheck+1
                
            count=count+1
        
        if estcheck<2:
            print("Pelo menos uma das estações não existe, certifique-se que ambas as estações que quer ligar existem antes de criar um carril!")
            check=False
            
            
    dist= float(input("Por favor insira a distancia entre as estações: "))

    maxvel=float(input("Por favor insira a velocidade maxima entre as estações: "))

    my_functions.carril(cod_car,estA,estB,dist,maxvel)

#input e verificação dos inputs dos comboios (feitas)
if (resp=="3"):
    cod_comb=""
    check=False
    while (check==False) or (len(cod_comb)!=5):
        cod_comb=input("Por favor insira o número de série do comboio: ")
       
            
        path = os.path.realpath(__file__) 
        dir = os.path.dirname(path) 
        dir = dir.replace('codigo', 'dados') 
        os.chdir(dir) 
        ficheiro= open("tabela_comboios.txt","r")
        dados=ficheiro.readlines()
        ficheiro.close()
        
        count=0
        check=True
        print(len(cod_comb))
        for i in dados:
            dadoslist=dados[count].split(";")
            
            
            if (dadoslist[0]==cod_comb):
                print("Código de comboio já existe, por favor insira outro")
                check=False
            count=count+1  
            print(check)
            
    modelocomb=input("Por favor insira o modelo do comboio: ")
    velocidadecomb=input("Por favor insira a velocidade máxima do comboio: ")
    capacidadecomb=input("Por favor insira a capacidade máxima do comboio: ")
    tiposervico=""
    while (tiposervico != "U" and tiposervico!="R" and tiposervico!="I" and tiposervico!="A"):
        tiposervico=input("Por favor insira o tipo de serviço (U, R, I ou A): ").upper()

    my_functions.comboio(cod_comb,modelocomb,velocidadecomb,capacidadecomb,tiposervico)

#input e verificação dos inputs das linhas (a fazer)

if (resp=="4"):
    path = os.path.realpath(__file__) 
    dir = os.path.dirname(path) 
    dir = dir.replace('codigo', 'dados') 
    os.chdir(dir) 
    ficheiro= open("tabela_linhas.txt","r")
    dados=ficheiro.readlines()
    ficheiro.close()

    codlinha=input("Por favor insira o codigo desta linha: ")
    count=0
    dadoslist=[]
    for i in dados:
        dadoslist.append(dados[count].split(";"))
        count=count+1

    count=0
    check=True
    for i in dados:
        print (dadoslist[count][0])
        if dadoslist[count][0] == codlinha:
            print("Código da linha já existe, por favor insira outro!")
            check=False
            break
        count=count+1
    nomelinha=input("Por favor insira o nome desta linha: ")

    quantests=quantests = int(input("Por favor insira quantas estações quer que façam parte desta linha: "))


    ests=[]
    listacarril=[]
    listaestacao=[]

    ficheiroest= open("tabela_estacoes.txt","r")
    dadosest=ficheiroest.readlines()
    ficheiroest.close()

    ficheirocar= open("tabela_carril.txt","r")
    dadoscar=ficheirocar.readlines()
    ficheirocar.close()

    count=0
    for i in dadosest:
        listaestacao.append(dadosest[count].split(";"))
        count=count+1

    count=0
    for i in dadoscar:
        listacarril.append(dadoscar[count].split(";"))
        count=count+1

    count=0

    while count < quantests:  
        estcheck = False
        carrilcheck = False

    
        est = input(f"Por favor diga qual vai ser a {count + 1}ª estação: ").upper()

   
        for i in listaestacao:
            if est == i[0]:
                estcheck = True
                break  

    
        for i in listacarril:
       
            if len(ests) == 0:
                print(i)
                if est == i[1] or est == i[2]:  
                    carrilcheck = True
                    break  

            elif len(ests) > 0:
                if est == i[1] or est == i[2]:  
                    if est == listaestacao[len(ests)][0] or est == listaestacao[len(ests)][0]:
                        carrilcheck = True
                        break  

    
        if estcheck and carrilcheck:
            ests.append(est)
            count += 1  
        else:
            print("A estação que pediu não existe ou não tem ligações com outras estações!")

    tiposervico=""
    while (tiposervico != "U" and tiposervico!="R" and tiposervico!="I" and tiposervico!="A"):
        tiposervico=input("Por favor insira o tipo de serviço (U, R, I ou A): ").upper()

    my_functions.linha(codlinha,nomelinha,ests,tiposervico)

                

