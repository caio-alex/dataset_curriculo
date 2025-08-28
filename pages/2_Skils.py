import streamlit as st

# --- CONFIGURAÇÃO INICIAL E ESTILO ---

st.set_page_config(
    page_title="Habilidades",
    layout="wide"
)

# Adicionando um bloco de CSS personalizado para estilização
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Estiliza o título principal do dashboard com cor branca */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Estiliza os cabeçalhos de seção com cor branca */
    h2, h3, h4 {
        color: #ffffff;
        font-weight: 600;
        margin-top: 1.5rem;
    }

    /* Estiliza o contêiner e o texto dentro dele com fundo escuro e texto branco */
    .stContainer {
        border-radius: 10px;
        padding: 40px;
        margin-top: 50px;
        background-color: #333333;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #555555;
    }

    .intro-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #ffffff; /* Cor branca para o texto introdutório */
    }

    .skill-list {
        font-size: 1rem;
        line-height: 1.8;
        color: #f0f0f0; /* Cor branca para o texto da lista */
    }

    .highlight {
        color: #00bfff; /* Cor de destaque em um tom de azul claro */
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# --- CONTEÚDO DA PÁGINA ---

st.title("Habilidades Técnicas e Pessoais 👨‍💻")

st.markdown("""
<div class="intro-text">
    Aqui estão as minhas principais habilidades e as tecnologias com as quais tenho experiência, divididas em categorias para facilitar a visualização.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção de Tecnologias de Programação
st.header("Tecnologias de Programação")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <ul class="skill-list">
            <li><span class="highlight">Front-end:</span> HTML/Css, Sass, Bootstrap, Tailwind, JavaScript, TypeScript, React</li>
            <li><span class="highlight">Back-end:</span> Java, SpringBoot, Python, PHP</li>
        </ul>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <ul class="skill-list">
            <li><span class="highlight">Banco de Dados:</span> SQL</li>
            <li><span class="highlight">Sistemas:</span> Linux</li>
            <li><span class="highlight">Linguagens:</span> C++</li>
        </ul>
        """, unsafe_allow_html=True)

st.markdown("---")

# Seção de Ferramentas
st.header("Ferramentas")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <ul class="skill-list">
            <li>GitHub</li>
            <li>Trello</li>
            <li>Figma</li>
        </ul>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <ul class="skill-list">
            <li>Watson IBM</li>
            <li>Maya</li>
            <li>Selenium</li>
        </ul>
        """, unsafe_allow_html=True)

st.markdown("---")

# Seção de Metodologias
st.header("Metodologias")
st.markdown("""
<div class="skill-list">
    Minha experiência acadêmica me proporcionou a vivência com metodologias ágeis e de design, essenciais para o trabalho em equipe e a solução de problemas.
</div>
<ul class="skill-list">
    <li>Scrum</li>
    <li>Design Thinking</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção de Idiomas
st.header("Idiomas")
st.markdown("""
<ul class="skill-list">
    <li><span class="highlight">Inglês:</span> Bom domínio de inglês técnico</li>
    <li><span class="highlight">Espanhol:</span> Básico</li>
</ul>
""", unsafe_allow_html=True)
