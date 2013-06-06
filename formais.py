#-*- coding: utf-8 -*-
import sys
#lalalallala


regras = { }
terminais = [ ]
variaveis = [ ]
arquivo = []
inicial = None
# { S > NP , VP }
# [ 'S > NP VP' ]
# { "S" : "NP VP" }

gramatica = (variaveis,terminais,regras,inicial)

def achaTerminais(linhaTerminais):
    global terminais
    for ter in linhaTerminais.strip('{ ,}\n').split(', '):
        terminais.append(ter)

def achaVariaveis(linhaVariaveis):
    global variaveis
    for var in linhaVariaveis.strip('{ ,}\n').split(', '):
        variaveis.append(var)

def formataArquivo(arq):
    global arquivo
    for line in arq:
        arquivo.append(line.partition('#')[0].strip())

def processaRegras(linhaInicial):
    global arquivo
    for i in range(linhaInicial, len(arquivo)):
        linha = arquivo[i].strip('{ ,}\n').replace(',', '')
        regra = linha.partition('}')[0]
        esquerda, dummy,  direita = regra.partition(' > ')
        try:
            if (regras[esquerda] == None): regras[esquerda] = []
        except KeyError:
            regras[esquerda] = []
        if direita.strip() in regras[esquerda]:
            continue
        regras[esquerda].append(direita.strip())
        
def found(word, listOfLists):
    for l in listOfLists:
        if word in l: return True
    return False

#def fecho(var, regras):
#    parcial = []
#    total = []
#    for v in regras[var]:
#       if v in variaveis: parcial.append(v)
#        
#    for coisa in parcial:
#        if not (coisa in total):
#            total.append(coisa)
#            temp = fecho(coisa,regras)
#        if (temp != None): total.append(temp)
#    return total

def generatesVariable(var):
	for x in regras[var]:
		if x in variaveis: return True
	return False
## DONE ##
def simplify(regras):
	controle = []
	for r,s in regras.items():
		for x in s:
			if x in variaveis:
				controle.append(x)

	while controle != []:
		for esquerda, direita in regras.items():
			print controle
			for d in direita:
				if d in controle:
					regras[esquerda].remove(d)
					controle.remove(d)
					for x in regras[d]:
						if not (x in regras[esquerda]):
							regras[esquerda].append(x)
							if x in variaveis:
								controle.append(x)

	
	
## TODO : FNC ##
def transformToCNF(regras):
	
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
simplify(regras)
#print [key for key, value in regras.items() if found("barks", value)]


