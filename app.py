import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="SmartGrill 🥩", layout="wide")

# --- SIMULAÇÃO DE BANCO DE DADOS (SESSION STATE) ---
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

# --- MENU CARDÁPIO ---
menu = {
    "Picanha na Brasa": 89.90,
    "Costela Premium": 75.50,
    "Linguiça Cuiabana": 45.00,
    "Pão de Alho (Porção)": 25.00,
    "Cerveja Artesanal": 18.00
}

# --- INTERFACE ---
st.title("🔥 SmartGrill: Pedidos Automatizados")

# Criamos abas para simular as DUAS telas (Tablet da Mesa e Tela da Cozinha)
aba_cliente, aba_cozinha, aba_garcom = st.tabs(["📱 Tablet Cliente", "👨‍🍳 Tela da Cozinha", "🤵 Tela do Garçom"])

# --- 1. VISÃO DO CLIENTE (TABLET) ---
with aba_cliente:
    st.subheader("Faça seu pedido")
    st.info("Toque nos itens para adicionar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_selecionado = st.radio("Escolha o corte:", list(menu.keys()))
        obs = st.text_input("Observação (Ex: Mal passada, Sem sal):")
    
    with col2:
        preco = menu[item_selecionado]
        st.metric(label="Valor do Item", value=f"R$ {preco:.2f}")
        
        if st.button("🛒 Enviar Pedido para Cozinha", type="primary"):
            # Lógica de Backend: Cria o pedido
            novo_pedido = {
                "id": len(st.session_state.pedidos) + 1,
                "item": item_selecionado,
                "obs": obs,
                "valor": preco,
                "status": "Na Fila 🕒",
                "hora": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.pedidos.append(novo_pedido)
            st.success("Pedido enviado! O cozinheiro já recebeu.")
            time.sleep(1)
            st.rerun()

# --- 2. VISÃO DA COZINHA (FILA DE PEDIDOS) ---
with aba_cozinha:
    st.subheader("Monitor de Pedidos (KDS)")
    
    # Filtra só o que não está pronto
    pedidos_pendentes = [p for p in st.session_state.pedidos if p["status"] == "Na Fila 🕒"]
    
    if not pedidos_pendentes:
        st.success("Cozinha livre! Nenhum pedido pendente.")
    else:
        for pedido in pedidos_pendentes:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**#{pedido['id']} - {pedido['item']}**")
                c1.caption(f"Obs: {pedido['obs']}")
                c2.text(f"🕒 {pedido['hora']}")
                
                if c3.button("🔥 Preparar", key=f"prep_{pedido['id']}"):
                    pedido["status"] = "Pronto ✅"
                    st.toast(f"Pedido #{pedido['id']} marcado como PRONTO!")
                    time.sleep(1)
                    st.rerun()

# --- 3. VISÃO DO GARÇOM (PAGAMENTO) ---
with aba_garcom:
    st.subheader("Conferência e Pagamento")
    df = pd.DataFrame(st.session_state.pedidos)
    if not df.empty:
        st.dataframe(df)
        total = df["valor"].sum()
        st.metric("Total da Mesa", f"R$ {total:.2f}")
    else:
        st.info("Aguardando pedidos...")