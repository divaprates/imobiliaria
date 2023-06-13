import requests
import re
from bs4 import BeautifulSoup

with open("lista.txt", "r") as arquivo:
    lista = eval(arquivo.read())

lista_atual = []
lista_dif = []

imobiliarias = [
    {
        'nome': 'CORRETA',
        'url': 'https://www.corretaimoveismg.com/imoveis/aluguel',
        'find1': 'div',
        'find2': 'class',
        'find3': 'work wow fadeInDown',
        'Pfind1': 'p',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'img',
        'Ifind2': 'src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': 1
    },

]

#FERREIRA: cobertura e amaro lanari
#SETA: cobertura e amaro lanari
#TOTAL: cobertura


print('Pesquisando em ', len(imobiliarias)-2, ' imobiliárias...')

for imobiliaria in imobiliarias:
    print(imobiliaria['nome'] + '...')
    response = requests.get(imobiliaria['url'])
    site = BeautifulSoup(response.text, 'html.parser')
    # print(site)

    produtos = site.findAll(imobiliaria['find1'], attrs={imobiliaria['find2'] : imobiliaria['find3']})
    # print(produtos)

    for produto in produtos:
        #allex/seta/vale
        codigo = ''
        if imobiliaria['Pfind1'] == '' and imobiliaria['Cfind'] != '':
            #certa/jfCorretor/catedral
            codigo = produto[imobiliaria['Cfind']]
        elif imobiliaria['Pfind1'] != '' and imobiliaria['Cfind'] == '':
            #diferencial/portal/correta
            codigo = produto.find(imobiliaria['Pfind1'], attrs={imobiliaria['Pfind2'] : imobiliaria['Pfind3']})
            if imobiliaria['Cposition'] != '':
                codigo = produto.find_all(imobiliaria['Pfind1'], attrs={imobiliaria['Pfind2'] : imobiliaria['Pfind3']})[imobiliaria['Cposition']]
            if imobiliaria['Cfind2'] != '': #diferencial
                codigo = codigo.find(imobiliaria['Cfind2'])
            codigo = codigo.text
            codigo = codigo.strip()
        codigo = re.sub('[^0-9]', '', codigo) #apenas números

        imagem = produto.find(imobiliaria['Ifind'])
        imagem = imagem[imobiliaria['Ifind2']]

        inserir = 1
        if imobiliaria['nome'] == 'CATEDRAL':
            if 'venda' in imagem:
                inserir = 0

        if inserir == 1:
            p = (imobiliaria['nome'], codigo, imagem)
            lista_atual.append(p)

# ----------------------------------------------------------------
# comparando as listas
print(lista_atual)
'''
for e in lista_atual:
    if e not in lista:
        lista_dif.append(e)

# exibindo resultados encontrados
if len(lista_dif) == 0:
    print('Não foi encontrado nenhum resultado diferente!')
else:
    for l in lista_dif:
        print(l)

    salvar = input('Deseja atualizar a lista? S sim - N não: ')
    if salvar == 's':
        with open('lista.txt', 'w') as arquivo:
            arquivo.write(str(lista_atual))
        print("Lista atualizada!")
'''