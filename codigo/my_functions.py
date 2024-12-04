import os.path

def estacao(cod_est,nome,lati,longi):
    path = os.path.realpath(__file__)
    dir=os.path.dirname(path)
    dir= dir.replace("codigo","dados")
    os.chdir(dir)
    tabela_estacoes = open ("tabela_estacoes.txt", "a")
    cod_est=str(cod_est)
    nome=str(nome)
    lati=str(lati)
    longi=str(longi)
    texto= cod_est + ";" + nome + ";" + lati + ";" + longi + "\n"
    myEstacoes = tabela_estacoes.writelines( texto )
    tabela_estacoes.close()


    


