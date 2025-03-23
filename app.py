import pandas as pd
import streamlit as st
from datetime import datetime

# Função para carregar os dados dos produtos
def carregar_produtos():
    try:
        return pd.read_excel("produtos.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Codigo Produto", "Nome Produto"])

# Função para carregar o estoque
def carregar_estoque():
    try:
        return pd.read_excel("estoque.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Codigo Produto", "Nome Produto", "Data Validade", "Unidade", "Quantidade",
            "Valor", "Observacao", "Valor Total", "Promocao", "Perda", "Valor Promocional", "R$ Perdido"
        ])

# Função para salvar o estoque
def salvar_estoque(dados):
    # Garantir que dados seja um DataFrame
    dados = pd.DataFrame([dados])
    
    # Carregar o estoque atual
    estoque_df = carregar_estoque()
    
    # Concatenar os novos dados ao estoque
    estoque_df = pd.concat([estoque_df, dados], ignore_index=True)
    
    # Salvar o arquivo atualizado
    estoque_df.to_excel("estoque.xlsx", index=False)

# Função para cadastrar um novo produto
def cadastrar_produto():
    # Carregar os produtos
    produtos_df = carregar_produtos()
    
    # Opção de escolher um produto
    produto_selecionado = st.selectbox("Escolha o produto", produtos_df['Nome Produto'].tolist() + ["Adicionar Novo Produto"])
    
    # Se o produto não estiver na lista, adicionar um novo
    if produto_selecionado == "Adicionar Novo Produto":
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        
        # Salvar o novo produto
        if st.button("Salvar Novo Produto"):
            novo_produto = {"Codigo Produto": codigo_produto, "Nome Produto": nome_produto}
            produtos_df = produtos_df.append(novo_produto, ignore_index=True)
            produtos_df.to_excel("produtos.xlsx", index=False)
            st.success("Produto salvo com sucesso!")
    else:
        # Preencher os dados do estoque
        data_validade = st.date_input("Data de Validade", min_value=datetime.today())
        unidade = st.selectbox("Unidade", ["Betelitas", "Lojinha", "Commulter"])
        quantidade = st.number_input("Quantidade", min_value=0)
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        observacao = st.text_input("Observação")
        promocao = st.checkbox("Promoção?")
        perda = st.checkbox("Perda?")
        
        valor_promocional = 0.0
        valor_perdido = 0.0
        
        if promocao:
            valor_promocional = st.number_input("Valor Promocional", min_value=0.0, format="%.2f")
            valor_perdido = (valor - valor_promocional) * quantidade
        
        # Calcular o valor total
        valor_total = valor * quantidade - valor_perdido
        
        # Armazenar os dados para salvar
        dados_estoque = {
            "Codigo Produto": produtos_df.loc[produtos_df['Nome Produto'] == produto_selecionado, 'Codigo Produto'].values[0],
            "Nome Produto": produto_selecionado,
            "Data Validade": data_validade,
            "Unidade": unidade,
            "Quantidade": quantidade,
            "Valor": valor,
            "Observacao": observacao,
            "Valor Total": valor_total,
            "Promocao": promocao,
            "Perda": perda,
            "Valor Promocional": valor_promocional,
            "R$ Perdido": valor_perdido
        }
        
        # Botão para salvar os dados no estoque
        if st.button("Salvar Cadastro"):
            salvar_estoque(dados_estoque)
            st.success("Produto cadastrado com sucesso!")
    
# Página de seleção
st.title("Controle de Validade dos Produtos")

opcao = st.radio("O que você deseja fazer?", ("Consultar Produtos", "Cadastrar Novo Produto"))

if opcao == "Consultar Produtos":
    # Mostrar produtos cadastrados
    estoque_df = carregar_estoque()
    st.dataframe(estoque_df)

elif opcao == "Cadastrar Novo Produto":
    cadastrar_produto()