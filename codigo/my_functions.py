import os.path

# Função d tabela da estação, entra na tabela de estações e introduz todos os dados na tabela
def estacao(cod_est,nome,lati,longi):
    pathest = os.path.realpath(__file__)
    dir=os.path.dirname(pathest)
    dir= dir.replace("codigo","dados")
    os.chdir(dir)
    tabela_estacoes = open ("tabela_estacoes.txt", "a")
    cod_est=str(cod_est)
    nome=str(nome)
    lati=str(lati)
    longi=str(longi)
    textoest= cod_est + ";" + nome + ";" + lati + ";" + longi + "\n"
    tabela_estacoes.writelines( textoest )
    tabela_estacoes.close()


#Tabela do carril

def carril(cod_carr,esta,estb,dist,velmaxperm):
    pathcarr = os.path.realpath(__file__)
    dir=os.path.dirname(pathcarr)
    dir= dir.replace("codigo","dados")
    os.chdir(dir)
    tabela_carril = open ("tabela_carril.txt", "a")
    cod_carr=str(cod_carr)
    esta=str(esta)
    estb=str(estb)
    dist=str(dist)
    velmaxperm= str (velmaxperm)
    textocarr= cod_carr + ";" + esta + ";" + estb + ";" + dist + ";" + velmaxperm + "\n"
    tabela_carril.writelines( textocarr )
    tabela_carril.close()

#tabela do comboio

def comboio(cod_comb,modelocomb,velocidadecomb,capacidadecomb,tiposervico):
    pathcarr = os.path.realpath(__file__)
    dir=os.path.dirname(pathcarr)
    dir= dir.replace("codigo","dados")
    os.chdir(dir)
    tabela_comboios = open ("tabela_comboios.txt", "a")
    cod_comb=str(cod_comb)
    modelocomb=str(modelocomb)
    velocidadecomb=str(velocidadecomb)
    capacidadecomb=str(capacidadecomb)
    
    tiposervico= str (tiposervico)
    textocarr= cod_comb + ";" + modelocomb + ";" + velocidadecomb + ";" + capacidadecomb + ";" + tiposervico + "\n"
    tabela_comboios.writelines( textocarr )
    tabela_comboios.close()

#Tabela das linhas

def linha(codlinh, nomelinh, ests,servi):
    pathcarr = os.path.realpath(__file__)
    dir=os.path.dirname(pathcarr)
    dir= dir.replace("codigo","dados")
    os.chdir(dir)
    tabela_comboios = open ("tabela_linhas.txt", "a")
    codlinh=str(codlinh)
    nomelinh=str(nomelinh)
    ests=str(ests)
    servi=str(servi)
    textolinha= codlinh + ";" + nomelinh + ";" + ests + ";" + servi + "\n"
    tabela_comboios.writelines( textolinha )
    tabela_comboios.close()





