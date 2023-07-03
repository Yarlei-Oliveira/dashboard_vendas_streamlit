import streamlit as st
import requests
import pandas as pd
import time


@st.cache_data

def converter_csv(df):
    return df.to_csv(index= False).encode('UTF-8')

def msg_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon = '✅')
    time.sleep(5)
    sucesso.empty()

st.title('Dados brutos')

url = 'https://labdados.com/produtos'
request = requests.get(url)

data = pd.DataFrame.from_dict(request.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format= '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Colunas', list(data.columns), list(data.columns))
    
    
st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione o produto', data['Produto'].unique(), data['Produto'].unique())
    
with st.sidebar.expander('Categoria'):
    categoria_produto = st.multiselect('Selecione a categoria do produto', data['Categoria do Produto'].unique(), data['Categoria do Produto'].unique())
    
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Preço', 0, int(data['Preço'].max()), (0, int(data['Preço'].max())))
    
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione uma data', (data['Data da Compra'].min(), data['Data da Compra'].max()))
    
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o(s) vendedores', data['Vendedor'].unique(), data['Vendedor'].unique())
    
with st.sidebar.expander('Local'):
    local_compra = st.multiselect('Selecione o local', data['Local da compra'].unique(), data['Local da compra'].unique())
    
with st.sidebar.expander('Avaliação'):
    avaliacao = st.radio('Selecione avaliação', list(sorted(data['Avaliação da compra'].unique())))
    avaliacao = int(avaliacao)
    
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', data['Tipo de pagamento'].unique(), data['Tipo de pagamento'].unique())

with st.sidebar.expander('Parcelas'):
    parcelas = st.slider('Parcelas', 0, int(data['Quantidade de parcelas'].max()), (0, int(data['Quantidade de parcelas'].max())))
    
query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
`Categoria do Produto` in @categoria_produto and \
Vendedor in @vendedor and \
`Local da compra` in @local_compra and \
`Avaliação da compra` == @avaliacao and \
`Tipo de pagamento` in @tipo_pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]
'''

dados_filtrados = data.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')

coluna1, coluna2 = st.columns(2)

with coluna1:
    nome_do_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_do_arquivo += '.csv'
    
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data= converter_csv(dados_filtrados), file_name=nome_do_arquivo, mime='text/csv', on_click=msg_sucesso)
