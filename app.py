import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred)

# Referência para o Firestore
db = firestore.client()

# Função para carregar os produtos do Firestore
def carregar_produtos():
    produtos_ref = db.collection("produtos")
    produtos = produtos_ref.stream()
    
    # Criando uma lista para armazenar os produtos
    produtos_lista = []
    for produto in produtos:
        produtos_lista.append(produto.to_dict())
    
    # Se não houver produtos, retorna um dataframe vazio
    if not produtos_lista:
        return pd.DataFrame(columns=["Codigo Produto", "Nome Produto"])
    
    return pd.DataFrame(produtos_lista)

# Função para carregar o estoque do Firestore
def carregar_estoque():
    estoque_ref = db.collection("estoque")
    estoque = estoque_ref.stream()
    
    # Criando uma lista para armazenar o estoque
    estoque_lista = []
    for item in estoque:
        estoque_lista.append(item.to_dict())
    
    # Se não houver estoque, retorna um dataframe vazio
    if not estoque_lista:
        return pd.DataFrame(columns=[
            "Codigo Produto", "Nome Produto", "Data Validade", "Unidade", "Quantidade",
            "Valor", "Observacao", "Valor Total", "Promocao", "Perda", "Valor Promocional", "R$ Perdido"
        ])
    
    return pd.DataFrame(estoque_lista)

# Função para salvar o estoque no Firestore
def salvar_estoque(dados):
    # Adicionando os dados ao Firestore
    estoque_ref = db.collection("estoque")
    estoque_ref.add(dados)

# Função para cadastrar um novo produto
def cadastrar_produto():
    # Carregar os produtos do Firestore
    produtos_df = carregar_produtos()
    
    # Opção de escolher um produto
    produto_selecionado = st.selectbox("Escolha o produto", produtos_df['Nome Produto'])
    
    # Se o produto não estiver na lista, adicionar um novo
    if produto_selecionado == "Adicionar Novo Produto":
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        
        # Salvar o novo produto no Firestore
        if st.button("Salvar Novo Produto"):
            novo_produto = {"Codigo Produto": codigo_produto, "Nome Produto": nome_produto}
            # Salvar no Firestore
            db.collection("produtos").add(novo_produto)
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

# Tela inicial com botões
st.title("Controle de Validade dos Produtos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Consultar Produtos"):
        # Mostrar produtos cadastrados
        produtos_df = carregar_produtos()
        st.dataframe(produtos_df)

with col2:
    if st.button("Cadastrar Novo Produto"):
        cadastrar_produto()