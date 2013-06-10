#-*- coding: utf-8 -*-
import sys
#lalalallala


regras = { }
terminais = [ ]
variaveis = [ ]
arquivo = []
varsCriadas =  { }
inicial = None
index = 0
# { S > NP , VP }
# [ 'S > NP VP' ]
# { "S" : "NP VP" }

gramatica = (variaveis,terminais,regras,inicial)

def achaTerminais(linhaTerminais):
    global terminais
    terminais.append(' ')
    terminais.append('&')
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
        if word in tokenize(l): return True
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
	
def excluiVazioRegra(esquerda, lTokens, regras, lVazios):

    if len(lTokens) == 1: return []
    vaziosNaRegra = [t for t in lVazios if t in lTokens]
    direita = ''.join(lTokens)
    print direita
    matriz = [0 for x in vaziosNaRegra]
    print matriz
    for i in range(len(matriz)):
        s = direita.replace(vaziosNaRegra[i], '', 1)
        matriz[i] = s
    for x in matriz:
        for y in excluiVazioRegra(esquerda, tokenize(x), regras, lVazios):
            if y not in matriz:
                matriz.append(y)
    return matriz
    
def tiraVazios(regras):
    levamEmVazio = [key for key, value in regras.items() if found("&", value)]
    print levamEmVazio
    for x in levamEmVazio:
        regras[x].remove('&')
    for esquerda, direita in regras.items():
        for d in direita:
            print d
            t = tokenize(d)
            for x in levamEmVazio:
                if x in t:
                    for var in excluiVazioRegra(esquerda, t, regras, levamEmVazio):
                        if var not in regras[esquerda]:
                            regras[esquerda].append(var)
## DONE ##
def simplify(regras):
	# Produções vazias.
	tiraVazios(regras)
	controle = []
	for r,s in regras.items():
		for x in s:
			if x in variaveis:
				controle.append(x)


    # Produções que substituem variáveis.
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


def createVariable(token):
    var = "_" + token + "_"
    if var in variaveis: return var
    else:
        variaveis.append(var)
        regras[var] = token
        return var

def substTerminal(term, var):
    global regras
    for esquerda, direita in regras.items():
        for d in direita:
            t = tokenize(d)
            if len(t) >= 2:
                if term in t:
                    t[t.index(term)] = var
                    s = ''.join(t)
                    regras[esquerda].remove(d)
                    #print s
                    regras[esquerda].append(s)
            else: continue

def chomskyfy(esquerda, lTokens, regras):
    global index

    newVarName = ""
    oldVarName = ""
    while True:
        #print lTokens
        if len(lTokens) == 2:
            regras[esquerda].append(''.join(lTokens))
            return
        else:                        
            s = lTokens[-2] + lTokens[-1]
            newVarName = "_V" + str(index) + "_"
#AQUI ESTÃO MINHAS CAGADAS
            if (s not in varsCriadas.keys()):
                varsCriadas[s] = newVarName
                index += 1
            else:
                newVarName=varsCriadas[s]
            
            #print varsCriadas          
            del lTokens[-2]
            del lTokens[-1]
            lTokens.append(newVarName)
            try:
                if s not in regras[newVarName]:
                    regras[newVarName].append(s)
                else: index -= 1
            except KeyError:
                regras[newVarName] = [s]
                index -= 1
            variaveis.append(newVarName)
            oldVarName = newVarName
        index += 1
## TODO : FNC ##
def transformToCNF(regras):
	while not isCNF(regras):
	    for esquerda, direita in regras.items():
	        for d in direita:
	            t = tokenize(d)
	            if len(t) >= 2:
	                for token in t:
	                    if token in terminais:
	                        substTerminal(token, createVariable(token))
	    copy = regras.items()
	    for esquerda, direita in copy:
	        for d in direita:
	            t = tokenize(d)
	            if len(t) >= 3:
	                regras[esquerda].remove(d)
	                #print "CHOMSKYFY!"
	                chomskyfy(esquerda, t, regras)
	                #print regras
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
#print regras
transformToCNF(regras)

#print regras
#print [key for key, value in regras.items() if found("barks", value)]
for x in regras.keys():
    print x, ' :', regras[x] 

