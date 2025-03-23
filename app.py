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
            "Valor", "Observacao", "Valor Sem Promoção", "Promocao", "Perda", "Valor Promocional", "Perda Pós Promoção"
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
    produto_selecionado = st.selectbox("Escolha o produto", produtos_df['Nome Produto'])
    
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
        perda_pos_promocao = 0.0
        
        if promocao:
            valor_promocional = st.number_input("Valor Promocional", min_value=0.0, format="%.2f")
            # Cálculo da Perda Pós Promoção
            perda_pos_promocao = (valor - valor_promocional) * quantidade
        
        # Calcular o Valor Sem Promoção (simplesmente valor * quantidade)
        valor_sem_promocao = valor * quantidade
        
        # Armazenar os dados para salvar
        dados_estoque = {
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
        
        # Botão para salvar os dados no estoque
        if st.button("Salvar Cadastro"):
            salvar_estoque(dados_estoque)
            st.success("Produto cadastrado com sucesso!")

# Tela inicial com botões
st.title("Controle de Validade dos Produtos")

# Definindo layout para os botões
col1, col2 = st.columns(2)

with col1:
    if st.button("Consultar Produtos"):
        # Mostrar produtos cadastrados de forma mais bonita
        estoque_df = carregar_estoque()
        
        # Ajustando a formatação
        st.write("### Produtos Cadastrados")
        st.write("Abaixo estão os produtos e suas informações de validade.")

        # Exibindo o dataframe de forma mais amigável
        st.dataframe(estoque_df.style.format({
            "Valor": "R$ {:,.2f}",
            "Valor Sem Promoção": "R$ {:,.2f}",
            "Valor Promocional": "R$ {:,.2f}",
            "Perda Pós Promoção": "R$ {:,.2f}",
        }))

with col2:
    if st.button("Cadastrar Novo Produto"):
        cadastrar_produto()