import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Função para salvar dados no Firestore
def salvar_dados_validades(dados):
    db.collection("dados_validades").add(dados)

# Função para carregar os dados de validade
def carregar_dados_validades():
    docs = db.collection("dados_validades").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

# Função para cadastrar um novo produto
def cadastrar_produto():
    produto_selecionado = st.text_input("Nome do Produto")
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
        "Nome Produto": produto_selecionado,
        "Data Validade": str(data_validade),
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

# Página principal
st.title("Controle de Validade dos Produtos")

opcao = st.radio("O que você deseja fazer?", ("Consultar Produtos", "Cadastrar Novo Produto"))

if opcao == "Consultar Produtos":
    dados = carregar_dados_validades()
    st.dataframe(dados)
elif opcao == "Cadastrar Novo Produto":
    cadastrar_produto()
