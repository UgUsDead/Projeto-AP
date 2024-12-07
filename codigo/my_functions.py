import os

# Caminho do ficheiro txt 
def caminho_ficheiro(nome_ficheiro):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path).replace("codigo", "dados")
    return os.path.join(dir, nome_ficheiro)

# Guardar dados num ficheiro
def guardar_em_ficheiro(nome_ficheiro, texto):
    caminho = caminho_ficheiro(nome_ficheiro)
    ficheiro = open(caminho, "a")
    ficheiro.writelines(texto + "\n")
    ficheiro.close()

# Adicionar uma estação em tabela_estacoes.txt
def estacao(cod_est, nome, lati, longi):
    texto = str(cod_est) + ";" + str(nome) + ";" + str(lati) + ";" + str(longi)
    guardar_em_ficheiro("tabela_estacoes.txt", texto)

# Adicionar um carril tabela_carril.txt
def carril(cod_carr, esta, estb, dist, velmaxperm):
    texto = str(cod_carr) + ";" + str(esta) + ";" + str(estb) + ";" + str(dist) + ";" + str(velmaxperm)
    guardar_em_ficheiro("tabela_carril.txt", texto)

# Adicionar um comboio em tabela_comboios.txt
def comboio(cod_comb, modelo_comb, velocidade_comb, capacidade_comb, tipo_servico):
    texto = str(cod_comb) + ";" + str(modelo_comb) + ";" + str(velocidade_comb) + ";" + str(capacidade_comb) + ";" + str(tipo_servico)
    guardar_em_ficheiro("tabela_comboios.txt", texto)

# Adicionar uma linha em tabela_linhas.txt. aqui nao temos de verificar ests e servi ne? a verificacao é feita no main.py?
def linha(cod_linh, nome_linh, ests, servi):
    texto = str(cod_linh) + ";" + str(nome_linh) + ";" + str(ests) + ";" + str(servi)
    guardar_em_ficheiro("tabela_linhas.txt", texto)
