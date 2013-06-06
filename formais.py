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
    terminais.append(' ')
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

			for d in direita:
				if d in controle:
					regras[esquerda].remove(d)
					controle.remove(d)
					for x in regras[d]:
						if not (x in regras[esquerda]):
							regras[esquerda].append(x)
							if x in variaveis:
								controle.append(x)

## XGH RULEZ MANO ##


def tokenize(string):
	buff = ""
	tokens = []
	i = 0
	while True:

		if buff+string[i] in variaveis:
			while (i < len(string)) and (buff+string[i] in variaveis):
				buff = buff + string[i]
				i += 1
			tokens.append(buff)
			buff = ""
		elif buff+string[i] in terminais:
			while (i < len(string)) and (buff+string[i] in terminais):
				buff = buff + string[i]
				i += 1
			tokens.append(buff)
			buff = ""
		else:
			buff += string[i]
			i += 1
		if i >= len(string): return tokens
# Assumindo que a gramática está simplificada.
def isCNF(regras):
	print variaveis
	deliciaDeLista = []
	for esquerda, direita in regras.items():
		for d in direita:
			if d not in deliciaDeLista: deliciaDeLista.append(d)
	for x in deliciaDeLista:
		t = tokenize(x)
		if len(t) == 1: continue
		elif len(t) > 2 : return False
		else:
			quantasVar = [y for y in t if y in variaveis] # BLACK MAGICS
			if len(quantasVar) == 2: continue
			else: return False
	return True
## TODO : FNC ##
def transformToCNF(regras):
# PARTE FODA
	pass
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
print isCNF(regras)
#print [key for key, value in regras.items() if found("barks", value)]


