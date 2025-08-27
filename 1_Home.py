import streamlit as st

# --- CONFIGURAÇÃO INICIAL E ESTILO ---

st.set_page_config(
    page_title="Início",
    layout="wide"
)


# --- CONTEÚDO DA PÁGINA ---

st.title("Dashboard de Análise de Dados da Olist")
st.write("""
Bem-vindo ao dashboard de análise de dados da Olist! Este dashboard foi desenvolvido para apresentar insights valiosos sobre dados reais da empresa.
""")
st.markdown("---")

# Seção de introdução pessoal e objetivo profissional com foto
with st.container():
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("me.jpg", caption="Caio Alexandre", use_container_width=True)
    with col2:
        st.markdown('<h2 class="intro-title" style="text-align: left;">Olá, me chamo <span class="highlight">Caio Alexandre dos Santos</span>.</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="intro-text" style="text-align: left;">Como estudante do 4º semestre de <span class="highlight">Engenharia de Software na FIAP</span>, busco unir a paixão pela tecnologia com a análise de dados para transformar informações complexas em soluções práticas e de impacto. Meu objetivo é atuar em um ambiente que me permita aplicar meus conhecimentos em desenvolvimento e dados para resolver problemas reais e contribuir para o crescimento de projetos inovadores.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
