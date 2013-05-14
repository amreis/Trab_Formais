#-*- coding: utf-8 -*-
import sys
from formaisFuncoes import *


regras = { }
terminais = [ ]
variaveis = [ ]
arquivo = []
inicial = None
# { S > NP , VP }
# [ 'S > NP VP' ]
# { "S" : "NP VP" }

gramatica = (variaveis,terminais,regras,inicial)


formataArquivo(sys.stdin)

rang = range(len(arquivo))
for i in rang:

    if arquivo[i] == "Terminais":
        achaTerminais(arquivo[i+1])


    elif arquivo[i] == "Variaveis":
        achaVariaveis(arquivo[i+1])

    elif arquivo[i] == "Inicial":
        inicial = arquivo[i+1].strip('{ ,}\n').split(', ')[0] #OMG
    
    elif arquivo[i] == "Regras":
        processaRegras(i+1)
        break
        
#### AWWWWWWW  YEAAAAAAAA
print [key for key, value in regras.items() if found("barks", value)]


