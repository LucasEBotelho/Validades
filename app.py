import streamlit as st
import pandas as pd
from datetime import datetime

# Função para carregar os produtos cadastrados
def carregar_produtos():
    try:
        # Carregar a planilha de produtos
        produtos_df = pd.read_excel("produtos.xlsx")
        return produtos_df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Codigo Produto", "Nome Produto"])

# Função para carregar o banco de dados de estoque
def carregar_estoque():
    try:
        # Carregar a planilha de estoque
        estoque_df = pd.read_excel("estoque.xlsx")
        return estoque_df
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Codigo Produto", "Nome Produto", "Data Validade", "Unidade", "Quantidade", "Valor", 
            "Observação", "Valor Total", "Promoção", "Perda", "Valor Promocional", "R$ Perdido"
        ])

# Função para salvar no banco de dados (estoque)
def salvar_estoque(dados):
    # Carregar a planilha de estoque
    estoque_df = carregar_estoque()
    # Adicionar os novos dados
    estoque_df = pd.concat([estoque_df, dados], ignore_index=True)
    # Salvar a planilha
    estoque_df.to_excel("estoque.xlsx", index=False)

# Função para salvar no banco de dados (produtos)
def salvar_produto(codigo, nome):
    produtos_df = carregar_produtos()
    produtos_df = produtos_df.append({"Codigo Produto": codigo, "Nome Produto": nome}, ignore_index=True)
    produtos_df.to_excel("produtos.xlsx", index=False)

# Interface do usuário
st.title("Controle de Validade de Produtos")

# Opção para escolher entre consultar ou cadastrar
opcao = st.selectbox("O que você deseja fazer?", ["Consultar Itens", "Cadastrar Novo Produto"])

if opcao == "Consultar Itens":
    # Exibir itens cadastrados
    estoque_df = carregar_estoque()
    st.dataframe(estoque_df)

elif opcao == "Cadastrar Novo Produto":
    # Carregar produtos para exibição
    produtos_df = carregar_produtos()
    
    if produtos_df.empty:
        st.warning("Não há produtos cadastrados. Por favor, adicione um novo produto.")
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        if st.button("Cadastrar Produto"):
            salvar_produto(codigo_produto, nome_produto)
            st.success(f"Produto {nome_produto} cadastrado com sucesso!")
    else:
        produto_selecionado = st.selectbox("Escolha o produto", produtos_df['Nome Produto'])
        produto_info = produtos_df[produtos_df['Nome Produto'] == produto_selecionado].iloc[0]

        # Preenchimento do formulário de cadastro
        st.subheader("Cadastro de Estoque")
        validade = st.date_input("Data de Validade", min_value=datetime.today())
        unidade = st.selectbox("Unidade", ["Betelitas", "Lojinha", "Commulter"])
        quantidade = st.number_input("Quantidade", min_value=1)
        valor = st.number_input("Valor", min_value=0.01, format="%.2f")
        observacao = st.text_area("Observação")
        promocao = st.checkbox("Promoção?")
        perda = st.checkbox("Perda?")
        
        valor_promocional = 0
        valor_perdido = 0
        if promocao:
            valor_promocional = st.number_input("Valor Promocional", min_value=0.01, format="%.2f")
            valor_perdido = (valor - valor_promocional) * quantidade if promocao else 0

        valor_total = valor * quantidade
        dados_estoque = {
            "Codigo Produto": produto_info["Codigo Produto"],
            "Nome Produto": produto_info["Nome Produto"],
            "Data Validade": validade,
            "Unidade": unidade,
            "Quantidade": quantidade,
            "Valor": valor,
            "Observação": observacao,
            "Valor Total": valor_total,
            "Promoção": "Sim" if promocao else "Não",
            "Perda": "Sim" if perda else "Não",
            "Valor Promocional": valor_promocional,
            "R$ Perdido": valor_perdido
        }

        if st.button("Salvar Produto"):
            salvar_estoque(dados_estoque)
            st.success("Produto cadastrado no estoque com sucesso!")