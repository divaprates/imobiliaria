import re

import requests
from bs4 import BeautifulSoup

with open("lista.txt", "r") as arquivo:
    lista = eval(arquivo.read())

lista_atual = []
lista_dif = []

imobiliarias = [
    {
        'nome': 'DIFERENCIAL',
        'url':'https://diferencialimoveis.com/consultar?empreendimento=&tipo=Casa%2CCasa%20Fundos%2CCobertura&para=locacao&refs=&_dorm=&cidade_bairros=&_valor=&caracteristicas=&valor=&dorm=&page=1',
        'find1': 'div',
        'find2': 'class',
        'find3': 'item-imovel-result-content',
        'Pfind1': 'div',
        'Pfind2': 'class',
        'Pfind3': 'item-imovel-result-footer',
        'Ifind': 'img',
        'Ifind2': 'data-src',
        'Cfind': '',
        'Cfind2': 'b',
        'Cposition': ''
    },
    {
        'nome': 'CERTA',
        'url':'https://certaimoveis.com.br/encontrar/789c7d924d6b02311086ffca10905548a9f6e8cdaa87a5cb16941e7a0a21893610936d3eec41fcefcd6437602f3dedcef3ce4cde99e446bc12ce4be1928d2279af6c1cf8599135ac283c8a4810a15ac14b49f94e2a607423515d06c3a3625e85642233ba0844381b73e3e7113fe98bbb2a1d48e9e639661827b8e08e9486a780a8fc735bbc902b37ce53e9fc8586a4a32ac5acd09afb2778303e8d43564b1484965c96b81d78d4f6cc91463d38645b1e38b967a0257ab0c918acf96f2f952e33fef952bef4def43bc0d1a06bdff6d0cca6f1660da0327aa85af531897398a31b687b9837e8a7592ce0fd0008030b4a242bb9d72ed47a86496ccd723d26eef60778fd0419591a64be0b688fd07f741d7d40bbfd715b626d8549b282d1178574a2e5b89c820b8771f9e3874da350c8f7049be3964c6f029fc3fd17667db9d0/0?referer=/encontrar/',
        'find1': 'article',
        'find2': 'class',
        'find3': 'item-imovel-result',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'a',
        'Ifind2': 'data-src',
        'Cfind': 'data-id',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'CERTA',
        'url':'https://certaimoveis.com.br/encontrar/?template_result_list=content/result-imoveis&range=valor,dorm,suites&para=locacao&refs=&cidade=Coronel%20Fabriciano&bairro=Amaro%20Lanari&tipo=Casa&valor=&_valor=',
        'find1': 'article',
        'find2': 'class',
        'find3': 'item-imovel-result',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'a',
        'Ifind2': 'data-src',
        'Cfind': 'data-id',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'JF CORRETOR',
        'url': 'https://www.jfcorretor.com.br/imobiliaria/locacao/cobertura-duplex-casa/imoveis/11248',
        'find1': 'article',
        'find2': 'class',
        'find3': 'card c49-property-card',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'a',
        'Ifind2': 'href',
        'Cfind': 'id',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'ALLEX',
        'url': 'https://www.alleximoveis.com.br/busca?estado%5B%5D=6&cidade%5B%5D=312&valor-min=&valor-max=&operacao=locacao&tipo-imovel%5B%5D=55&tipo-imovel%5B%5D=7&dormitorios%5B%5D=&area-min=&area-max=&page=1',
        'find1': 'a',
        'find2': 'class',
        'find3': 'imovel',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'img',
        'Ifind2': 'src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
    # {
    #     'nome': 'VALE',
    #     'url': 'https://www.valeimoveismg.com.br/imobiliaria/locacao/cobertura-duplex-casa/imoveis/646',
    #     'find1': 'article',
    #     'find2': 'class',
    #     'find3': 'card c49-property-card',
    #     'Pfind1': '',
    #     'Pfind2': '',
    #     'Pfind3': '',
    #     'Ifind': 'img',
    #     'Ifind2': 'src',
    #     'Cfind': 'id',
    #     'Cfind2': '',
    #     'Cposition': ''
    # },
    {
        'nome': 'SETA',
        'url': 'https://www.setaimoveis.com.br/busca?estado=6&cidade=312&bairro=&valor-min=&valor-max=&operacao=locacao&tipo-imovel=55&dormitorios=&area-min=&area-max=&page=1',
        'find1': 'div',
        'find2': 'class',
        'find3': 'box-imovel-resultado',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'img',
        'Ifind2': 'src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'PORTAL',
        'url': 'https://www.portalimoveisimobiliaria.com.br/localizar/localizar-imovel?filter%5Bsearch%5D=&filter%5Bcategoria_catid%5D=-39&filter%5Btipo_catid%5D%5B%5D=313&filter%5Btipo_catid%5D%5B%5D=345&filter%5Btipo_catid%5D%5B%5D=346&filter%5Bfaixa_valor_venda%5D=0.00-2000000.00&filter%5Bfaixa_valor_venda%5D%5Bmin%5D=0.00&filter%5Bfaixa_valor_venda%5D%5Bmax%5D=2000000.00&filter%5Bfaixa_valor_locacao%5D=0.00-5000.00&filter%5Bfaixa_valor_locacao%5D%5Bmin%5D=0.00&filter%5Bfaixa_valor_locacao%5D%5Bmax%5D=5000.00&filter%5Bquartos%5D=&filter%5Bsuites%5D=&filter%5Bbanheiros%5D=&filter%5Bgaragens%5D=&task=search',
        'find1': 'div',
        'find2': 'class',
        'find3': 'item',
        'Pfind1': 'div',
        'Pfind2': 'class',
        'Pfind3': 'float-left',
        'Ifind': 'img',
        'Ifind2': 'data-src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
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
    {
        'nome': 'CATEDRAL',
        'url': 'https://www.catedralimobiliaria.com/imobiliaria/locacao/coronel-fabriciano-mg/amaro-lanari/cobertura-casa-casa/imoveis/9752',
        'find1': 'article',
        'find2': 'class',
        'find3': 'card c49-property-card',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'a',
        'Ifind2': 'href',
        'Cfind': 'id',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'MORADIA',
        'url': 'https://moradiaimobiliaria.com.br/imoveis/?sku=&street=&location%5B%5D=512&location%5B%5D=453&location%5B%5D=640&location%5B%5D=513&location%5B%5D=473&location%5B%5D=467&location%5B%5D=679&location%5B%5D=454&location%5B%5D=474&location%5B%5D=532&location%5B%5D=464&location%5B%5D=462&location%5B%5D=465&location%5B%5D=466&location%5B%5D=463&location%5B%5D=671&location%5B%5D=607&location%5B%5D=469&location%5B%5D=824&location%5B%5D=665&location%5B%5D=470&location%5B%5D=541&location%5B%5D=455&location%5B%5D=468&location%5B%5D=711&location%5B%5D=471&location%5B%5D=826&location%5B%5D=760&location%5B%5D=475&location%5B%5D=663&location%5B%5D=833&location%5B%5D=536&location%5B%5D=544&location%5B%5D=814&location%5B%5D=680&location%5B%5D=688&contract_type%5B%5D=51&property_type%5B%5D=82&property_type%5B%5D=87&property_type%5B%5D=753&bedroom=1%3B6',
        'find1': 'div',
        'find2': 'class',
        'find3': 'properties__item',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'img',
        'Ifind2': 'src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'FERREIRA',
        'url': 'https://www.ferreiraimoveis.net/resultadobusca.asp?categoria=Aluguel&CIDADE=IPATINGA&BAIRRO=&TIPO=&subtipo=Casa&faixa_preco_menor=',
        'find1': 'div',
        'find2': 'class',
        'find3': 'text_lista_tabulares',
        'Pfind1': '',
        'Pfind2': '',
        'Pfind3': '',
        'Ifind': 'img',
        'Ifind2': 'src',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'TOTAL',
        'url': 'https://www.totalimob.com.br/imoveis/alugar/mg/ipatinga/casa?valor_min=&valor_max=&ordem=recentes',
        'find1': 'div',
        'find2': 'class',
        'find3': 'imovel-item',
        'Pfind1': 'div',
        'Pfind2': 'class',
        'Pfind3': 'imovel-badge',
        'Ifind': 'a',
        'Ifind2': 'href',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
    },
    {
        'nome': 'TOTAL',
        'url': 'https://www.totalimob.com.br/imoveis/alugar/mg/coronel-fabriciano/amaro-lanari?valor_min=&valor_max=&ordem=recentes',
        'find1': 'div',
        'find2': 'class',
        'find3': 'imovel-item',
        'Pfind1': 'div',
        'Pfind2': 'class',
        'Pfind3': 'imovel-badge',
        'Ifind': 'a',
        'Ifind2': 'href',
        'Cfind': '',
        'Cfind2': '',
        'Cposition': ''
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

    produtos = site.findAll(imobiliaria['find1'], attrs={imobiliaria['find2'] : imobiliaria['find3']})

    for produto in produtos:
        #allex/seta/vale
        codigo = ''
        if imobiliaria['Pfind1'] == '' and imobiliaria['Cfind'] != '':
            #certa/jfCorretor/catedral
            codigo = produto[imobiliaria['Cfind']]
        elif imobiliaria['Pfind1'] != '' and imobiliaria['Cfind'] == '':
            #correta
            if imobiliaria['Cposition'] != '':
                codigo = produto.find_all(imobiliaria['Pfind1'], attrs={imobiliaria['Pfind2'] : imobiliaria['Pfind3']})[imobiliaria['Cposition']]
            else:
                #diferencial/portal
                codigo = produto.find(imobiliaria['Pfind1'], attrs={imobiliaria['Pfind2'] : imobiliaria['Pfind3']})
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
#print(lista_atual)

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
