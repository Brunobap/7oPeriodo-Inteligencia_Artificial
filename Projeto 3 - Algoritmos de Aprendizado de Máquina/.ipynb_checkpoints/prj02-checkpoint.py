#!/usr/bin/env python
# coding: utf-8

# Base de dados 9 - "Breast cancer"
# 
# Título: Breast cancer data
# Fonte: 
#    -- Matjaz Zwitter & Milan Soklic (physicians)
#       Institute of Oncology 
#       University Medical Center
#       Ljubljana, Yugoslavia
#    -- Donors: Ming Tan and Jeff Schlimmer (Jeffrey.Schlimmer@a.gp.cs.cmu.edu)
#    -- Date: 11 July 1988
# 
# Número de entradas: 286 
# Número de atributos: 9 + atributo de classe (se é recorrência ou não)
# 
# Eventos de recorrência: 85 --> 201 são "inéditos"
# 
# Atributo principal (alvo): class (especificado no site)

# # Parte 1: Atributos, e seus tipos de valores:
# 1. Class (qualitativo nominal): no-recurrence-events, recurrence-events
# 2. age (qualitativo intervalar): 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80-89, 90-99.
# 3. menopause (qualitativo nominal): lt40, ge40, premeno.
# 4. tumor-size (qualitativo intervalar): 0-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59.
# 5. inv-nodes (qualitativo intervalar): 0-2, 3-5, 6-8, 9-11, 12-14, 15-17, 18-20, 21-23, 24-26, 27-29, 30-32, 33-35, 36-39.
# 6. node-caps (qualitativo nominal): yes, no.
# 7. deg-malig (qualitativo ordinal): 1, 2, 3.
# 8. breast (qualitativo nominal): left, right.
# 9. breast-quad (qualitativo nominal): left-up, left-low, right-up, right-low, central.
# 10. irradiat (qualitativo nominal): yes, no.

# In[1]:


# Parte 1: ler o arquivo e montar as linhas
entrada = open("breast+cancer/breast-cancer.data")
tabelaIni = [[],[],[],[],[],[],[],[],[],[]]

for linha in entrada:
    linha = str.split(linha, '\n')[0]
    itens = str.split(linha, ',')
    for i in range(0,10): tabelaIni[i].insert(i,itens[i])        
print("Dados carregados")

# Tabela com tipos de entradas possíveis
tiposEntr = [
    ["no-recurrence-events", 'recurrence-events'],
    ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"],
    ["lt40", "ge40", "premeno"],
    ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"],
    ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "18-20", "21-23", "24-26", "27-29", "30-32", "33-35", "36-39"],
    ["yes", "no"],
    ["1", "2", "3"],
    ["left", "right"],    
    ['left_up','left_low','right_up','right_low','central'],
    ['no', 'yes']
]
print(f"\nTipos de entrada possíveis por coluna:\n{tiposEntr}")


tiposAtr = {
    'Class': 'qualitativo nominal',
    'age': 'qualitativo intervalar',
    'menopause': 'qualitativo nominal',
    'tumor-size': 'qualitativo intervalar',
    'inv-nodes': 'qualitativo intervalar',
    'node-caps': 'qualitativo nominal',
    'deg-malig': 'qualitativo ordinal',
    'breast': 'qualitativo nominal',
    'breast-quad': 'qualitativo nominal',
    'irradiat': 'qualitativo nominal'
}
print(f"\nTipos de cada atributos:\n{tiposAtr}")


# # Parte 2: Medidas de Localidade (Média aritmética/ponderada, mediana, moda, ponto médio, frequência, quartis):
# 
# 1. Class: frequência, moda;
# 2. age: média ponderada, mediana, frequência, quartis;
# 3. menopause: frequência, moda;
# 4. tumor-size: média ponderada, mediana, frequência, quartis;
# 5. inv-nodes:  média ponderada, mediana, frequência, quartis;
# 6. node-caps: frequência, moda;
# 7. deg-malig: frequência, moda;
# 8. breast: frequência, moda;
# 9. breast-quad: frequência, moda;
# 10. irradiat: frequência, moda;

# In[2]:


# Parte 2.1: fazer as funções de medida de localidade
def frequencia(lista):
    dummy = lista.copy()
    dummy.sort()
    contagens = {}
    while len(dummy) != 0:
        item = dummy[0]
        contagens[item] = dummy.count(item)
        dummy = dummy[contagens[item]:]
    return contagens

def moda(lista, i):
    contagens = frequencia(lista)
    contagens = sorted(contagens.items(), key=lambda item: item[1])
    maior = contagens.pop()
    while maior[0] not in tiposEntr[i]: maior = contagens.pop()
    return maior[0]

# O peso da média é a frequência dos itens
def mediaInterv(lista, i):
    contagens = frequencia(lista)
    soma = 0
    usados = 0
    for item in contagens: 
        if item in tiposEntr[i]:
            soma += contagens[item] * acharMeio(item)
            usados += contagens[item]
    return soma/usados
    
def percentilInterv(lista, porcentagem):
    dummy = lista.copy()
    dummy.sort()
    np = porcentagem * len(lista)
    if np - int(np) != 0.0:
        r = int(np)+1
        return acharMeio(lista[r])
    else:
        r = int(np)        
        num1 = acharMeio(lista[r])  
        num2 = acharMeio(lista[r+1])
        return (num1+num2)/2
    
def quartilInterv(lista,nQuartil):
    nQuartil = 4 - nQuartil
    return percentilInterv(lista, nQuartil/4)

def medianaInterv(lista):
        return quartilInterv(lista,2)
    
# Função auxiliar para manipular os intervalos
def acharMeio(interv):
    metades = interv.split('-')        
    return (int(metades[0])+int(metades[1]))/2


# In[3]:


# Parte 2.2: usar as funções de medida de localidade
# 1. Class: frequência, moda;
print("Atributo 'Class':")
print(f"\tModa - {moda(tabelaIni[0],0)}")
print(f"\tFrequências - {frequencia(tabelaIni[0])}")

# 2. age: média ponderada, mediana, frequência, moda, quartis;
print("\nAtributo 'age':")
print(f"\tMédia ponderada - {mediaInterv(tabelaIni[1],1)}")
print(f"\tMediana - {medianaInterv(tabelaIni[1])}")
print(f"\tFrequências - {frequencia(tabelaIni[1])}")
print(f"\tQuartil 1 (25%) - {quartilInterv(tabelaIni[1],1)}")
print(f"\tQuartil 2 (50%) - {quartilInterv(tabelaIni[1],2)}")
print(f"\tQuartil 3 (75%) - {quartilInterv(tabelaIni[1],3)}")

# 3. menopause: frequência, moda;
print("\nAtributo 'menopause':")
print(f"\tModa - {moda(tabelaIni[2],2)}")
print(f"\tFrequências - {frequencia(tabelaIni[2])}")

# 4. tumor-size: média ponderada, mediana, frequência, quartis;
print("\nAtributo 'tumor-size':")
print(f"\tMédia ponderada - {mediaInterv(tabelaIni[3],3)}")
print(f"\tMediana - {medianaInterv(tabelaIni[3])}")
print(f"\tFrequências - {frequencia(tabelaIni[3])}")
print(f"\tQuartil 1 (25%) - {quartilInterv(tabelaIni[3],1)}")
print(f"\tQuartil 2 (50%) - {quartilInterv(tabelaIni[3],2)}")
print(f"\tQuartil 3 (75%) - {quartilInterv(tabelaIni[3],3)}")

# 5. inv-nodes:  média ponderada, mediana, frequência, quartis;
print("\nAtributo 'inv-nodes':")
print(f"\tMédia ponderada - {mediaInterv(tabelaIni[4],4)}")
print(f"\tMediana - {medianaInterv(tabelaIni[4])}")
print(f"\tFrequências - {frequencia(tabelaIni[4])}")
print(f"\tQuartil 1 (25%) - {quartilInterv(tabelaIni[4],1)}")
print(f"\tQuartil 2 (50%) - {quartilInterv(tabelaIni[4],2)}")
print(f"\tQuartil 3 (75%) - {quartilInterv(tabelaIni[4],3)}")

# 6. node-caps: frequência, moda;
print("\nAtributo 'node-caps':")
print(f"\tModa - {moda(tabelaIni[5],5)}")
print(f"\tFrequências - {frequencia(tabelaIni[5])}")

# 7. deg-malig: frequência, moda;
print("\nAtributo 'deg-malig':")
print(f"\tModa - {moda(tabelaIni[6],6)}")
print(f"\tFrequências - {frequencia(tabelaIni[6])}")

# 8. breast: frequência, moda;
print("\nAtributo 'breast':")
print(f"\tModa - {moda(tabelaIni[7],7)}")
print(f"\tFrequências - {frequencia(tabelaIni[7])}")

# 9. breast-quad: frequência, moda;
print("\nAtributo 'breast-quad':")
print(f"\tModa - {moda(tabelaIni[8],8)}")
print(f"\tFrequências - {frequencia(tabelaIni[8])}")

# 10. irradiat: frequência, moda;
print("\nAtributo 'irradiat':")
print(f"\tModa - {moda(tabelaIni[9],9)}")
print(f"\tFrequências - {frequencia(tabelaIni[9])}")


# # Parte 3: Medidas de Espalhamento (intervalo, amplitude, desvio-padrão, variância):
# 
# 2. age: intervalo, amplitude, desvio-padrão, variância;
# 4. tumor-size: intervalo, amplitude, desvio-padrão, variância;
# 5. inv-nodes: intervalo, amplitude, desvio-padrão, variância;
# 7. deg-malig: intervalo, amplitude;
# 
# Somente os dados com médias podem ter desvio-padrão e variância.

# In[4]:


import math


# In[5]:


# Parte 3.1: fazer as funções das medidas de espalhamento
# Essa função funciona tanto para os intervalares quantos para os discretos
def amplitude(lista):
    dummy = lista.copy()
    dummy.sort()
    itemMin = dummy[0]
    metades = itemMin.split('-')        
    nMin = int(metades[0])
    
    itemMax = dummy.pop()
    metades = itemMax.split('-')     
    if len(metades) == 1:
        nMax = int(metades[0]) +1
    else:
        nMax = int(metades[1]) +1
    return nMax - nMin

def intervalo(lista):
    amp = amplitude(lista)
    contagens = frequencia(lista)
    return amp / len(contagens)

# Auxiliar para o cálculo dos 3 últimos momentos centrais
def momentoInterv(lista,k,i):
    media = mediaInterv(lista,i)
    contagens = frequencia(lista)
    soma = 0
    for item in contagens:
        if item in tiposEntr[i]: soma += ((acharMeio(item) - media)**k) * contagens[item]
    return soma / (len(lista) - (lista.count('?') - 1))

def varianciaInterv(lista,i):
    return momentoInterv(lista,2,i)

def desvPadInterv(lista,i):
    vari = varianciaInterv(lista,i)
    return math.sqrt(vari)


# In[6]:


# Parte 3.2: aplicar as funções de medida de espalhamento nos dados
# 2. age: intervalo, amplitude, desvio-padrão, variância;
print("Atributo 'age':")
print(f"\tIntervalo - {intervalo(tabelaIni[1])}")
print(f"\tAmplitude - {amplitude(tabelaIni[1])}")
print(f"\tVariância - {varianciaInterv(tabelaIni[1],1)}")
print(f"\tDesvio-padrão - {desvPadInterv(tabelaIni[1],1)}")

#4. tumor-size: intervalo, amplitude, desvio-padrão, variância;
print("\nAtributo 'tumor-size':")
print(f"\tIntervalo - {intervalo(tabelaIni[3])}")
print(f"\tAmplitude - {amplitude(tabelaIni[3])}")
print(f"\tVariância - {varianciaInterv(tabelaIni[3],3)}")
print(f"\tDesvio-padrão - {desvPadInterv(tabelaIni[3],3)}")

#5. inv-nodes: intervalo, amplitude, desvio-padrão, variância;
print("\nAtributo 'inv-nodes':")
print(f"\tIntervalo - {intervalo(tabelaIni[4])}")
print(f"\tAmplitude - {amplitude(tabelaIni[4])}")
print(f"\tVariância - {varianciaInterv(tabelaIni[4],4)}")
print(f"\tDesvio-padrão - {desvPadInterv(tabelaIni[4],4)}")

#7. deg-malig: intervalo, amplitude;
print("\nAtributo 'deg-malig':")
print(f"\tIntervalo - {intervalo(tabelaIni[6])}")
print(f"\tAmplitude - {amplitude(tabelaIni[6])}")


# # Parte 4: Medidas de Distribuição (obliquidade, curtose):
# OBS: dos 4 momentos centrais, os 2 primeiros já foram calculados (média e variância)
# 
# Somente os dados com médias podem ter essas medidas, ou seja as colunas 2 (age), 4 (tumor-size) e 5 (inv-nodes).

# In[7]:


# Parte 4.1: fazer as funções das medidas de distribuição
def obliquidadeInterv(lista,i):
    return momentoInterv(lista,3,i)

def curtoseInterv(lista,i):
        return momentoInterv(lista,4,i)


# In[8]:


# Parte 4.2: aplicar as funções de medida distribuição nos dados
# 2. age: intervalo, amplitude, desvio-padrão, variância;
print("Atributo 'age':")
print(f"\tObliquidade - {obliquidadeInterv(tabelaIni[1],1)}")
print(f"\tCurtose - {curtoseInterv(tabelaIni[1],1)}")

#4. tumor-size: intervalo, amplitude, desvio-padrão, variância;
print("\nAtributo 'tumor-size':")
print(f"\tObliquidade - {obliquidadeInterv(tabelaIni[3],3)}")
print(f"\tCurtose - {curtoseInterv(tabelaIni[3],3)}")

#5. inv-nodes: intervalo, amplitude, desvio-padrão, variância;
print("\nAtributo 'inv-nodes':")
print(f"\tObliquidade - {obliquidadeInterv(tabelaIni[4],4)}")
print(f"\tCurtose - {curtoseInterv(tabelaIni[4],4)}")


# In[9]:


import random


# In[10]:


# Parte 5: separar os conjuntos de treinamento/avaliação e de teste dos modelo
# Proporção: 2/3 treino, 1/3 teste

tabTreino = []
tabTeste = []
def separarTabelas(tabIni):
	treino = []
	teste = []
    for col in tabIni:
		treino.append(col.copy())
	teste.append([])

    tam = len(tabIni[0])/3
    for i in range(0,int(tam)):
        # A escolha dos testes é aleatória
        rand = random.randrange(0,len(treino[1]))
        for j in range(0,10):
            teste[j].insert(0,treino[j].pop(i))
    return [treino, teste]
            
tabs = separarTabelas(tabelaIni)
tabTreino = tabs[0]
tabTeste = tabs[1]


# In[11]:


# caso a proporção da classe minoritária seja muito discrepante, refazer as tabelas
fTreino = frequencia(tabTreino[0])
pTreino = 100 * fTreino['recurrence-events'] / (fTreino['recurrence-events']+fTreino['no-recurrence-events'])

fOrig = frequencia(tabelaIni[0])
pOrig = 100 * fOrig['recurrence-events'] / (fOrig['recurrence-events']+fOrig['no-recurrence-events'])

pEsp = pOrig * .7
while (pTreino < pEsp - 5) or (pEsp + 5 < pTreino):
    tabs = separarTabelas(tabelaIni)
    tabTreino = tabs[0]
    tabTeste = tabs[1]
    
    fTreino = frequencia(tabTreino[0])
    pTreino = 100 * fTreino['recurrence-events'] / (fTreino['recurrence-events']+fTreino['no-recurrence-events'])


# # Parte 6: Identificação de atributos não necessários: usar uma técnica de cálculo de correlação
# OBS: fórmulas em https://sweet.ua.pt/andreia.hall/TEA/Capcorrel.pdf
# 
# - Coeficiente de Qui-Quadrado (X^2): Categórica x Categórica
# - Coeficiente de Cramér V (V): Categórica x Categórica
# - Coeficiente de correlação de Pearson (R): Numerica x Numerica
# - Coeficiente de correlação de Spearman (Rs): Ordinal x Ordinal
# - Coeficiente Φ/Fi (Tab. de contigência): Categorica x Categorica (ambas bidimensionais)
# 
# Cada dado usa um tipo de medida de correlação:
# 1. Class (qualitativo nominal): é o alvo, não precisa medir correlação
# 2. age (qualitativo intervalar): Crámer V
# 3. menopause (qualitativo nominal): Cramér V
# 4. tumor-size (qualitativo intervalar): Crámer V
# 5. inv-nodes (qualitativo intervalar): Crámer V
# 6. node-caps (qualitativo nominal): Coeficiente Fi, Crámer V
# 7. deg-malig (qualitativo ordinal): Cramér V
# 8. breast (qualitativo nominal): Coeficiente Fi, Cramér V
# 9. breast-quad (qualitativo nominal): Cramér V
# 10. irradiat (qualitativo nominal): Coeficiente V, Cramér V

# In[12]:


# Parte 6.1: fazer as funções de identificação de correlação
        
def tabConting(l1,l2):    
    f1 = frequencia(l1)
    f2 = frequencia(l2)
    mat = {}
    for item1 in f1:
        mat[item1] = {}
        for item2 in f2:
            mat[item1][item2] = 0
        mat[item1]['Total'] = 0
    mat['Total'] = {}
    for item2 in f2:
        mat['Total'][item2] = 0
    mat['Total']['Total'] = 0
    for i in range(0,len(l1)):
        x = l1[i]
        y = l2[i]
        mat[x][y] += 1
    for item1 in f1:
        for item2 in f2:
            mat[item1]['Total'] += mat[item1][item2]
    for item2 in f2:
        for item1 in f1:
            mat['Total'][item2] += mat[item1][item2]
    mat['Total']['Total'] = len(l1)
    return mat
            
def quiQuad(lTarget, lAtrib):
    f1 = frequencia(lTarget)
    f2 = frequencia(lAtrib)
    tam = len(lTarget)
    x = 0
    for ind in range(0,tam):
        Ei = f1[lTarget[ind]]/tam
        Oi = f2[lAtrib[ind]]/tam
        x += ((Oi-Ei)**2)/Ei
    return x

def cramerV(lTarget, lAtrib):
    X2 = quiQuad(lTarget,lAtrib)
    n = len(lTarget)    
    return math.sqrt(X2/(X2+n))
        
def coefFi(lTarget, lAtrib):
    tab = tabConting(lTarget, lAtrib)
    tipos1 = list(tab)
    tipos2 = list(tab[lTarget[1]])
    A = tab[tipos1[0]][tipos2[0]]
    B = tab[tipos1[0]][tipos2[1]]
    C = tab[tipos1[1]][tipos2[0]]
    D = tab[tipos1[1]][tipos2[1]]
    upper = (A*D-B*C)
    lower = math.sqrt((A+B)*(C+D)*(A+C)*(B+D))
    return upper/lower


# In[13]:


# Parte 6.2: identificar a correlação ou não dos atributos
# 1. Class (qualitativo nominal): é o alvo, não precisa medir correlação
lAlvo = tabTreino[0]

# 2. age (qualitativo intervalar): Cramér V
lAtrib = tabTreino[1]
print("Atributo 'age':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 3. menopause (qualitativo nominal): Cramér V
lAtrib = tabTreino[2]
print("\nAtributo 'menopause':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 4. tumor-size (qualitativo intervalar): Cramér V
lAtrib = tabTreino[3]
print("\nAtributo 'tumor-size':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 5. inv-nodes (qualitativo intervalar): Cramer V
lAtrib = tabTreino[4]
print("\nAtributo 'inv-nodes':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 6. node-caps (qualitativo nominal): Coeficiente Fi, Crámer V
lAtrib = tabTreino[5]
print("\nAtributo 'node-caps':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))
print("\tCoeficiente Fi - "+str(coefFi(lAlvo,lAtrib)))

# 7. deg-malig (qualitativo ordinal): Cramér V
lAtrib = tabTreino[6]
print("\nAtributo 'deg-malig':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 8. breast (qualitativo nominal): Coeficiente Fi, Cramér V
lAtrib = tabTreino[7]
print("\nAtributo 'breast':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))
print("\tCoeficiente Fi - "+str(coefFi(lAlvo,lAtrib)))

# 9. breast-quad (qualitativo nominal): Cramér V
lAtrib = tabTreino[8]
print("\nAtributo 'breast-quad':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))

# 10. irradiat (qualitativo nominal): Coeficiente V, Cramér V
lAtrib = tabTreino[9]
print("\nAtributo 'irradiat':")
print("\tCramér V - "+str(cramerV(lAlvo,lAtrib)))
print("\tCoeficiente Fi - "+str(coefFi(lAlvo,lAtrib)))


# Como o Grau de Liberdade é sempre 1 com as correlações do atributo-alvo temos o seguinte cenário em relação aos valores de Cramer:
# - Pequena = 0.10
# - Média = 0.30
# - Grande = 0.50
# 
# Observando os valores de Cramer acima podemos ver que nenhuma das colunas possui uma associação no nível pequeno. Logo, não é necessário remover nenhuma.

# # Parte 7: eliminar exemplos desnecessários
# Para linhas inteiras só é possível procurar redundâncias, pois os dados são todos independentes entre si e os quantitativos são todos intervalados, o que elimina situações de inconsistência de linhas inteiras.
# 
# Sobre somente a redundância das linhas para ser analisada.
# 
# Caso 2 linhas com os mesmos atributos, pelo menos a 1a delas é eliminada, caso o resultado delas seja diferente, ambas são eliminadas.

# In[14]:


# Parte 7.1: identificar linhas redundantes e inconsistentes
def eliminaLinha(tab,y):
    for x in range(0,9): tab[x].pop(y)

# 1o) retirar redundancias das linhas
def retRedun(tab):
    reducoes = 0
    i = 0
    while i < len(tab[1]):
        l1 = ''
        for x in range(1,9): l1 += tab[x][i]+' <--> '
        j = i+1
        while j < len(tabTreino[1]):
            l2 = ''
            for x in range(1,9): l2 += tab[x][j]+' <--> '
            if l1 == l2:
                # Caso o resultado for diferente, eliminar as 2 linhas
                if tab[0][i] != tab[0][j]:
                    eliminaLinha(tab,i)
                    eliminaLinha(tab,j-1) 
                    reducoes += 1
                else: eliminaLinha(tab,i)
                reducoes += 1                
            j += 1
        i += 1
    return reducoes

print('Foram feitas '+str(retRedun(tabTreino))+' reduções por redundância.')


# # Parte 8 (amostragem dos dados): não é necessária
# A amostragem de dados não é necessária, pois a base de dados já está em um tamanho razoável (com aproximadamente 300 linhas). Reduzir o tamanho da amostra pode comprometer desnecessariamente a acurácia do modelo, visto que o processamento dos dados já não é excessivo.

# # Parte 9: identificar desbalanceamentos
# Como a geração das bases de treinamento e teste são aleatórias, a verificação do desbalanceamento deve ser feita de maneira automática a partir de um intervalo de porcentagens definida.
# 
# Na base original: P = 100 * x(recorrentes)/total --> aprox. 30% (no arquivo original)
# 
# OBS: .7 vem da separação de 2/3 da base original
# 
# Minimo: (P * .7) - 2%
# 
# Máximo: (P * .7) + 2%
# 
# Caso já esteja dentro desse intervalo não fazer nada. Caso não esteja, gerar linhas 'aleatórias'.

# In[15]:


# Função para gerar as linhas novas semi-aleatórias
def gerarLinha(tab, resultado):
    # 1a coluna é o resultado, o resultado é preditado
    tab[0].append(resultado)
    
    # Preencher todos os outros atributos com valores aleatórios
    for i in range(1,9):
        atr = tab[i]                
        rand = random.randrange(0,len(tiposEntr[i])-1)
        choosen = tiposEntr[i][rand]
        tab[i].append(choosen)
        

fTreino = frequencia(tabTreino[0])
pTreino = 100 * fTreino['recurrence-events'] / (fTreino['recurrence-events']+fTreino['no-recurrence-events'])
print("Balanço inicial da tabela de teste: "+str(pTreino)+'% minoritária')

fOrig = frequencia(tabelaIni[0])
pOrig = 100 * fOrig['recurrence-events'] / (fOrig['recurrence-events']+fOrig['no-recurrence-events'])

pEsp = pOrig * .7
print("Balanço esperado: "+str(pEsp)+'% minoritária\n')
dif = pEsp - pTreino
print("Diferença: "+str(dif)+'%\n')

# Se a diferença estiver menor que -2%, situação de oversampling, fazer linhas minoritárias
# Se a diferença estiver maior que 2%, situação de undersampling, fazer linhas majoritárias
if dif < -2 or 2 < dif:
    nLinhas = int(math.fabs(dif)*len(tabTreino[1]))
    
    res = ''
    if dif < 0: res = 'recurrence-events'
    else: res = 'no-recurrence-events'
    print('Balanceamento necessário, foram geradas '+nLinhas+' do tipo '+res)
        
    for i in range(0,nLinhas): gerarLinhas(tabTreino, res)
        
else: print('Não foi preciso fazer o balanceamento da base.')


# # Parte 10: Limpeza dos dados
# Por conta de todos os dados numéricos serem intervalos pre-processados, não há possibilidade de haverem outliers nos seus valores.
# 
# Os dados inconsistentes e incompletos podem ser ambos analisados a partir da tabela de tipos de entrada por coluna (tiposEntr), e subistituidos aleatóriamente.
# 
# A verificação dos dados redundantes já aconteceu com a limpeza do número de exemplos (Parte 7).

# In[16]:


def limpar(tab):
    limpezas = 0
    faltantes = {}
    for y in range(0,len(tab[0])):
        # Caso a saída esteja com problema, apagar a linha
        if tab[0][y] not in tiposEntr[0]: 
            eliminaLinha(tab,y)
            limpezas += 1
        else:
            for x in range(1,9):
                # Tipo não válido, preencher
                if tab[x][y] not in tiposEntr[x]:
                    faltantes[tab[x][y]] = 1
                    rand = random.randrange(0,len(tiposEntr[x])-1)
                    choosen = tiposEntr[x][rand]
                    tab[x][y] = choosen
                    limpezas += 1
    return limpezas
                    
print("Foram feitas "+str(limpar(tabTreino))+" limpezas no basnco de dados.")


# # Parte 11: Conversões dos dados
# 
# - Os atributos 'class' (0), 'node-caps' (5), 'breast' (7) e 'irradiat' (9) podem ser convertidos para binário.
# 
# - Os atributos 'age' (1), 'tumor-size' (3) e 'inv-nodes' (4) podem ser convertidos categóricos ordinais semelhante ao atributo 'deg-malig' (6), facilitando a leitura tanto pra máquina quanto para humanos.
# 
# - Os atributos 'menopause' (2) e 'breast-quad' (8) em colunas separadas de valor binário para cada tipo de entrada, o que facilita o processamento dos dados pelo computador.

# In[17]:


# 1o) Converter os sim's e não's
classLine = []
nodeLine = []
breastLine = []
irradiatLine = []
for y in range(0,len(tabTreino[0])):
    if tabTreino[0][y] == 'recurrence-events': classLine.append(True)
    else: classLine.append(False)
        
    if tabTreino[5][y] == 'yes': nodeLine.append(True)
    else: nodeLine.append(False)
        
    if tabTreino[7][y] == 'right': breastLine.append(True)
    else: breastLine.append(False)
        
    if tabTreino[9][y] == 'yes': irradiatLine.append(True)
    else: irradiatLine.append(False)
        
tabTreino[0] = classLine
tabTreino[5] = nodeLine
tabTreino[7] = breastLine
tabTreino[9] = irradiatLine


# In[18]:


# 2o) Converter os intervalares em ordinais
ageLine = []
tumorLine = []
invLine = []
for y in range(0,len(tabTreino[0])):
    newAge = tiposEntr[1].index(tabTreino[1][y])
    ageLine.append(newAge)
    
    newTumor = tiposEntr[3].index(tabTreino[3][y])
    tumorLine.append(newTumor)
    
    newInv = tiposEntr[4].index(tabTreino[4][y])
    invLine.append(newInv)
    
tabTreino[1] = ageLine
tabTreino[3] = tumorLine
tabTreino[4] = invLine


# In[19]:


# 3o) Converter os categóricos em colunas
# Fazer as colunas novas
novoTreino = []
for i in range(0,len(tabTreino)): 
    if i == 2 or i == 8:
        print(tiposEntr[i])
        for j in range(0,len(tiposEntr[i])): novoTreino.append([])
    else: novoTreino.append(tabTreino[i].copy())

# Preencher do novo jeito
for y in range(0,len(tabTreino[0])):
    # Dados de 'menopause'
    meno = tabTreino[2][y]
    if meno == 'lt40': novoTreino[2].append(True)
    else: novoTreino[2].append(False)
    if meno == 'ge40': novoTreino[3].append(True)
    else: novoTreino[3].append(False)
    if meno == 'premeno': novoTreino[4].append(True)
    else: novoTreino[4].append(False)
    
    quad = tabTreino[8][y]
    if quad == 'left-up': novoTreino[10].append(True)
    else: novoTreino[10].append(False)
    if quad == 'left-low': novoTreino[11].append(True)
    else: novoTreino[11].append(False)
    if quad == 'right-up': novoTreino[12].append(True)
    else: novoTreino[12].append(False)
    if quad == 'right-low': novoTreino[13].append(True)
    else: novoTreino[13].append(False)
    if quad == 'central': novoTreino[14].append(True)
    else: novoTreino[14].append(False)


# In[20]:


# Os atributos e tipos de entrada mudaram
# Tabela com tipos de entradas possíveis
tiposEntr = [
    [True, False],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [True, False],
    [True, False],
    [True, False],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [True, False],
    [1, 2, 3],    
    [True, False],
    [True, False],
    [True, False],
    [True, False],
    [True, False],
    [True, False],
    [True, False]
]
print("Tipos de entrada possíveis por coluna:\n"+str(tiposEntr))


tiposAtr = {
    'Class': 'qualitativo binário',
    'age': 'qualitativo ordinal',
    'lt40': 'qualitativo binário',
    'ge40': 'qualitativo binário',
    'premeno': 'qualitativo binário',
    'tumor-size': 'qualitativo ordinal',
    'inv-nodes': 'qualitativo ordinal',
    'node-caps': 'qualitativo binário',
    'deg-malig': 'qualitativo ordinal',
    'breast': 'qualitativo binário',
    'left-up': 'qualitativo binário',
    'left-low': 'qualitativo binário',
    'right-up': 'qualitativo binário',
    'right-low': 'qualitativo binário',
    'central': 'qualitativo binário',
    'irradiat': 'qualitativo binário'
}
print("\nTipos de cada atributos:\n"+str(tiposAtr))

print("\nNúmero de atributos atual: "+str(len(novoTreino)))


# # Parte 12: Redução da dimensionalidade
# 
# Visto que o conjunto de treino final contêm um número de linhas da ordem de 200, e 16 colunas, não foi vista a necessidade de aplicar um algoritmo de redução de dimensão sobre essa base de dados.
# 
# Além disso, como os dados númericos são ou ordinais ou do tipo qualitativo ordinal, realizar operações matemáticas para a união das colunas associadas afetaria demais a veracidade dos dados.
