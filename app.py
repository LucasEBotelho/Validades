import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Função para inicializar o Firebase e mostrar mensagens no site
def inicializar_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("firebase-admin.json")  # Certifique-se de que o arquivo está correto
            firebase_admin.initialize_app(cred)
            st.write("Firebase inicializado com sucesso!")  # Exibe no site
        except Exception as e:
            st.error(f"Erro ao inicializar o Firebase: {e}")  # Exibe erro no site
    else:
        st.write("Firebase já foi inicializado.")  # Exibe no site

# Função para conectar ao Firestore
def conectar_firestore():
    try:
        db = firestore.client()  # Conecta ao Firestore
        st.write("Conectado ao Firestore com sucesso!")  # Exibe no site
        return db
    except Exception as e:
        st.error(f"Erro ao conectar ao Firestore: {e}")  # Exibe erro no site
        return None

# Inicializar Firebase e conectar ao Firestore
inicializar_firebase()
db = conectar_firestore()

# Função para carregar os dados dos produtos
def carregar_produtos():
    if db:
        produtos_ref = db.collection("produtos")
        produtos = produtos_ref.stream()
        produtos_lista = []
        for produto in produtos:
            produto_dict = produto.to_dict()
            produtos_lista.append(produto_dict["Nome Produto"])
        
        # Adicionando a opção de "Adicionar Novo Produto"
        produtos_lista.append("Adicionar Novo Produto")
        return produtos_lista
    else:
        st.error("Não foi possível carregar os produtos, pois não há conexão com o Firestore.")
        return []

# Função para carregar o estoque
def carregar_estoque():
    if db:
        estoque_ref = db.collection("estoque")
        estoque = estoque_ref.stream()
        estoque_lista = []
        for item in estoque:
            estoque_lista.append(item.to_dict())
        return estoque_lista
    else:
        st.error("Não foi possível carregar o estoque, pois não há conexão com o Firestore.")
        return []

# Função para salvar o estoque no Firebase
def salvar_estoque(dados):
    if db:
        estoque_ref = db.collection("estoque")
        estoque_ref.add(dados)
        st.success("Produto salvo com sucesso!")
    else:
        st.error("Não foi possível salvar o produto, pois não há conexão com o Firestore.")

# Função para cadastrar um novo produto
def cadastrar_produto():
    # Carregar os produtos
    produtos_lista = carregar_produtos()
    
    # Opção de escolher um produto
    produto_selecionado = st.selectbox("Escolha o produto", produtos_lista)
    
    # Se o produto não estiver na lista, adicionar um novo
    if produto_selecionado == "Adicionar Novo Produto":
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        
        # Salvar o novo produto
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
        
        # Estruturar os dados para salvar
        dados_estoque = {
            "Codigo Produto": codigo_produto,  # O código pode ser uma variável ou obtido do Firestore
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

# Tela inicial com botões
st.title("Controle de Validade dos Produtos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Consultar Produtos"):
        # Mostrar produtos cadastrados
        estoque_lista = carregar_estoque()
        st.write(estoque_lista)  # Exibir os produtos do estoque

with col2:
    if st.button("Cadastrar Novo Produto"):
        cadastrar_produto()