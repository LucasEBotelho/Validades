import pandas as pd
import streamlit as st
from datetime import datetime
import subprocess

# Função para carregar os dados dos produtos
def carregar_produtos():
    try:
        return pd.read_excel("produtos.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Codigo Produto", "Nome Produto"])

# Função para carregar os dados de validade
def carregar_dados_validades():
    try:
        return pd.read_excel("dados_validades.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Codigo Produto", "Nome Produto", "Data Validade", "Unidade", "Quantidade",
            "Valor", "Observacao", "Valor Sem Promoção", "Promocao", "Perda", "Valor Promocional", "Perda Pós Promoção"
        ])

# Função para salvar as informações na planilha de dados_validades e realizar commit no GitHub
def salvar_dados_validades(dados):
    # Exibindo os dados antes de salvar para depuração
    st.write("Dados a serem salvos:", dados)
    
    dados = pd.DataFrame([dados])
    dados_df = carregar_dados_validades()
    dados_df = pd.concat([dados_df, dados], ignore_index=True)
    
    # Salvando o arquivo Excel
    dados_df.to_excel("dados_validades.xlsx", index=False)
    
    # Exibindo mensagem para garantir que o arquivo foi salvo
    st.write("Arquivo 'dados_validades.xlsx' salvo com sucesso.")
    
    # Commit no GitHub
    subprocess.run(["git", "add", "dados_validades.xlsx"])  # Adiciona o arquivo alterado
    subprocess.run(["git", "commit", "-m", "Atualização de dados de validade"])  # Commit das mudanças
    subprocess.run(["git", "push"])  # Envia para o repositório no GitHub

# Função para cadastrar um novo produto
def cadastrar_produto():
    produtos_df = carregar_produtos()
    
    produto_selecionado = st.selectbox("Escolha o produto", produtos_df['Nome Produto'])
    
    if produto_selecionado == "Adicionar Novo Produto":
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        
        if st.button("Salvar Novo Produto"):
            novo_produto = {"Codigo Produto": codigo_produto, "Nome Produto": nome_produto}
            produtos_df = produtos_df.append(novo_produto, ignore_index=True)
            produtos_df.to_excel("produtos.xlsx", index=False)
            st.success("Produto salvo com sucesso!")
    
    else:
        data_validade = st.date_input("Data de Validade", min_value=datetime.today())
        unidade = st.selectbox("Unidade", ["Betelitas", "Lojinha", "Commulter"])
        quantidade = st.number_input("Quantidade", min_value=0)
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        observacao = st.text_input("Observação")
        promocao = st.checkbox("Promoção?")
        perda = st.checkbox("Perda?")
        
        valor_promocional = 0.0
        perda_pos_promocao = 0.0
        
        if promocao:
            valor_promocional = st.number_input("Valor Promocional", min_value=0.0, format="%.2f")
            perda_pos_promocao = (valor - valor_promocional) * quantidade
        
        valor_sem_promocao = valor * quantidade
        
        dados_validades = {
            "Codigo Produto": produtos_df.loc[produtos_df['Nome Produto'] == produto_selecionado, 'Codigo Produto'].values[0],
            "Nome Produto": produto_selecionado,
            "Data Validade": data_validade,
            "Unidade": unidade,
            "Quantidade": quantidade,
            "Valor": valor,
            "Observacao": observacao,
            "Valor Sem Promoção": valor_sem_promocao,
            "Promocao": promocao,
            "Perda": perda,
            "Valor Promocional": valor_promocional,
            "Perda Pós Promoção": perda_pos_promocao
        }
        
        if st.button("Salvar Cadastro"):
            salvar_dados_validades(dados_validades)
            st.success("Produto cadastrado com sucesso!")

# Página de seleção
st.title("Controle de Validade dos Produtos")

opcao = st.radio("O que você deseja fazer?", ("Consultar Produtos", "Cadastrar Novo Produto"))

if opcao == "Consultar Produtos":
    dados_df = carregar_dados_validades()
    st.dataframe(dados_df)

elif opcao == "Cadastrar Novo Produto":
    cadastrar_produto()