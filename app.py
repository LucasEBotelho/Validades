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

# Função para cadastrar um novo produto
def cadastrar_produto():
    # Carregar os produtos
    produtos_lista = ["Produto 1", "Produto 2", "Produto 3", "Adicionar Novo Produto"]
    
    # Opção de escolher um produto
    produto_selecionado = st.selectbox("Escolha o produto", produtos_lista)
    
    # Se o produto não estiver na lista, adicionar um novo
    if produto_selecionado == "Adicionar Novo Produto":
        st.write("Entrando na parte de adicionar novo produto...")  # Mensagem de depuração
        codigo_produto = st.text_input("Código do Produto")
        nome_produto = st.text_input("Nome do Produto")
        
        # Salvar o novo produto
        if st.button("Salvar Novo Produto"):
            if codigo_produto and nome_produto:
                novo_produto = {"Codigo Produto": codigo_produto, "Nome Produto": nome_produto}
                # Salvar no Firestore
                db.collection("produtos").add(novo_produto)
                st.success("Produto salvo com sucesso!")
            else:
                st.error("Preencha todos os campos antes de salvar o produto.")

    else:
        st.write(f"Produto selecionado: {produto_selecionado}")  # Mensagem de depuração

# Tela inicial com botões
st.title("Controle de Validade dos Produtos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Consultar Produtos"):
        st.write("Consultando produtos...")  # Mensagem de depuração

with col2:
    if st.button("Cadastrar Novo Produto"):
        st.write("Clicou em Cadastrar Novo Produto!")  # Mensagem de depuração
        cadastrar_produto()