import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

import plotly.express as px

# --- CONFIGURAÇÃO INICIAL E CARREGAMENTO DE DADOS ---

st.set_page_config(
    page_title="Dashboard de Análise Olist",
    layout="wide",
)

# Adicionando um bloco de CSS personalizado para estilização
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Estiliza o título principal do dashboard */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        color: #007bff; /* Cor primária do tema */
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Estiliza os cabeçalhos de seção */
    h2, h3, h4 {
        color: #333333;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Estiliza os contêineres e cards de métricas */
    .stContainer {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }

    /* Estiliza os cards de métricas */
    .stMetric > div:first-child {
        font-size: 1.25rem;
        font-weight: 600;
        color: #555;
    }
    .stMetric > div:nth-child(2) {
        font-size: 2rem;
        font-weight: 700;
        color: #007bff;
    }

    /* Ajuste para o espaçamento dos elementos de texto */
    .stMarkdown p {
        line-height: 1.6;
        text-align: justify;
    }

    /* Ajuste para botões e inputs */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)


# Função para carregar e preparar os dados
@st.cache_data
def load_data():
    try:
        # Carregando os datasets
        df = pd.read_csv('olist_analise_completa.csv')
        df_payments = pd.read_csv('olist_order_payments_dataset.csv')
        
        # Unindo os dataframes
        df_merged = pd.merge(df, df_payments, on='order_id', how='left')
        
        # Convertendo colunas de data
        df_merged['order_purchase_timestamp'] = pd.to_datetime(df_merged['order_purchase_timestamp'])
        df_merged['order_delivered_customer_date'] = pd.to_datetime(df_merged['order_delivered_customer_date'])
        
        return df_merged
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar os dados: O arquivo '{e.filename}' não foi encontrado. Certifique-se de que todos os arquivos CSV estão na mesma pasta.")
        return None

# Carrega os dados
df_final = load_data()

if df_final is None:
    st.stop()

st.title('Dashboard de Análise de Vendas e Clientes Olist 📊')

# --- NAVEGAÇÃO NA BARRA LATERAL (ASIDE) ---
st.sidebar.title("Navegação")
lista_de_paginas = [
    "Conhecendo o Dataset",
    "Análise Descritiva Geral",
    "Hábitos de Compra por Estado",
    "Padrões Sazonais de Vendas",
    "Avaliação por Categoria Popular",
    "Satisfação por Tipo de Pagamento",
    "Qualidade do Anúncio vs. Satisfação",
    "Qui-Quadrado (Categoria vs. Estado)"
]
pagina_selecionada = st.sidebar.radio("Selecione uma análise:", lista_de_paginas)

# --- EXIBIÇÃO CONDICIONAL DAS PÁGINAS ---

# --- Página 1: Conhecendo o Dataset ---
if pagina_selecionada == "Conhecendo o Dataset":
    st.header("Apresentação do Conjunto de Dados")
    
    st.markdown("""
    Este dashboard foi construído a partir de um conjunto de dados públicos da **Olist**. Os dados referem-se a cerca de 100.000 pedidos realizados na plataforma entre 2016 e 2018, e foram unidos a partir de múltiplas fontes para criar um dataset analítico completo.
    """)

    st.write("Link do DataSet: ","https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    
    st.markdown("---")

    # --- SEÇÃO DE PERGUNTAS DE ANÁLISE ---
    st.subheader("Principais Perguntas Respondidas neste Dashboard")
    st.markdown("""
    Cada aba deste dashboard foi projetada para responder a uma pergunta de negócio específica, utilizando os dados disponíveis:

    1.  **Análise Descritiva Geral:** Qual é o perfil geral das transações da Olist em termos de preço, frete e satisfação do cliente?
    2.  **Hábitos de Compra por Estado:** O comportamento de compra e as preferências de produtos variam entre os diferentes estados do Brasil?
    3.  **Padrões Sazonais de Vendas:** Como o volume de vendas se comporta ao longo dos meses do ano e dos dias da semana?
    4.  **Avaliação por Categoria Popular:** Qual é o nível de satisfação dos clientes com as categorias de produtos mais vendidas na plataforma?
    5.  **Satisfação por Tipo de Pagamento:** O método de pagamento escolhido pelo cliente tem alguma relação com a sua avaliação final da compra?
    6.  **Qualidade do Anúncio vs. Satisfação:** A quantidade de fotos em um anúncio de produto impacta a nota de avaliação do cliente?
    7.  **Qui-Quadrado (Categoria vs. Estado):** Existe uma associação estatisticamente significativa entre o estado do cliente e a categoria de produto que ele compra?
    """)

    st.markdown("---")
    
    st.subheader("Classificação das Variáveis do Projeto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Variáveis Qualitativas")
        st.markdown("Representam uma qualidade, característica ou categoria.")
        
        st.markdown("#### Nominal")
        st.markdown("""
        Categorias que não possuem uma ordem ou hierarquia natural.
        - **`order_status`**: Situação atual do pedido.
        - **`product_category_name_english`**: Categoria do produto.
        - **`customer_state`** / **`seller_state`**: Estado do cliente/vendedor.
        - **`payment_type`**: Método de pagamento utilizado.
        - **(Identificadores)** `order_id`, `customer_unique_id`, `product_id`, `seller_id`, `review_id`: Códigos únicos que funcionam como "nomes" para cada registro.
        """)

        st.markdown("#### Ordinal")
        st.markdown("""
        Categorias que possuem uma ordem ou ranking claro.
        - **`review_score`**: Nota da avaliação (1 é pior que 2, etc.).
        """)

    with col2:
        st.markdown("### Variáveis Quantitativas")
        st.markdown("Representam uma quantidade numérica mensurável.")

        st.markdown("#### Discreta (Cardinal)")
        st.markdown("""
        Valores que resultam de uma contagem (geralmente números inteiros).
        - **`product_photos_qty`**: Quantidade de fotos no anúncio.
        - **`payment_installments`**: Número de parcelas no pagamento.
        """)

        st.markdown("#### Contínua (Cardinal)")
        st.markdown("""
        Valores que podem assumir qualquer número dentro de um intervalo.
        - **`price`**: Preço do produto.
        - **`freight_value`**: Custo do frete.
        - **`product_weight_g`**: Peso do produto em gramas.
        - **(Datas)** `order_purchase_timestamp`, `order_delivered_customer_date`: Pontos específicos em uma linha do tempo contínua.
        """)
    
    with st.expander("Ver amostra dos dados"):
        st.dataframe(df_final.head())

# --- Página 1: Análise Descritiva Geral ---
if pagina_selecionada == "Análise Descritiva Geral":
    st.header('Análise Descritiva dos Dados')
    
    # Criando um contêiner para os cards de métricas
    with st.container():
        st.subheader("Nota de Avaliação")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Média", value=f"{df_final['review_score'].mean():.2f}")
        with col2:
            st.metric(label="Mediana", value=f"{df_final['review_score'].median():.2f}")
        with col3:
            st.metric(label="Moda", value=f"{df_final['review_score'].mode()[0]:.2f}")
        st.dataframe(df_final['review_score'].describe())

    st.markdown("---")

    with st.container():
        st.subheader("Preço do Produto e Valor do Frete")
        p1, p2 = st.columns(2)
        with p1:
            st.metric(label="Preço Médio", value=f"R$ {df_final['price'].mean():.2f}")
            st.dataframe(df_final['price'].describe())
        with p2:
            st.metric(label="Frete Médio", value=f"R$ {df_final['freight_value'].mean():.2f}")
            st.dataframe(df_final['freight_value'].describe())
    
    st.markdown("""
        A análise da **review_score** mostra um cenário predominantemente positivo. A média de avaliação de 4.0 sugere uma boa satisfação geral. No entanto, uma análise mais profunda revela uma nuance crucial: a mediana (nota que divide a amostra ao meio) e a moda (nota mais frequente) são 5.0.
        
        No perfil de **Preços e Fretes**, tanto para o preço dos produtos quanto para o valor do frete, observamos que a média é consideravelmente maior que a mediana. Isso indica que o volume de vendas da Olist está concentrado em produtos de baixo e médio custo. Alguns itens muito caros e/ou fretes para locais distantes e de produtos pesados inflam a média, mas não representam a realidade da maioria das transações. A Olist é, predominantemente, um marketplace de produtos com ticket médio acessível.
    """)
    st.markdown("---")
    
    st.subheader('Distribuição e Correlação')
    col_dist, col_corr = st.columns(2)
    with col_dist:
        st.subheader('Distribuição da Nota de Avaliação')
        fig = px.histogram(df_final.dropna(subset=['review_score']), x='review_score', 
                            title='Distribuição da Nota de Avaliação do Cliente',
                            marginal='box',
                            color_discrete_sequence=['#636EFA'])
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)

    with col_corr:
        st.subheader('Correlação entre Preço e Frete')
        quantile_threshold = 0.99
        correlation = df_final['price'].corr(df_final['freight_value'])
        st.metric(label="Correlação (Pearson)", value=f"{correlation:.2f}")
        df_filtered_corr = df_final.dropna(subset=['price', 'freight_value'])
        df_filtered_corr = df_filtered_corr[(df_filtered_corr['price'] < df_filtered_corr['price'].quantile(quantile_threshold)) & 
                                         (df_filtered_corr['freight_value'] < df_filtered_corr['freight_value'].quantile(quantile_threshold))]
        
        fig = px.scatter(df_filtered_corr, x='price', y='freight_value', 
                          title='Correlação entre Preço do Produto e Valor do Frete',
                          trendline="ols",
                          trendline_color_override="red",
                          labels={'price': 'Preço do Produto (R$)', 'freight_value': 'Valor do Frete (R$)'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        O gráfico de dispersão e o coeficiente de correlação de aproximadamente **+0.44** confirmam que existe uma relação positiva moderada entre o preço do produto e o valor do frete. Isso faz sentido, pois produtos mais caros tendem a ser maiores e mais pesados, impactando o custo de envio.
    """)

# --- Página 2: Hábitos de Compra por Estado ---
elif pagina_selecionada == "Hábitos de Compra por Estado":
    st.header("Análise Geográfica dos Hábitos de Compra")
    df_state_value = df_final.groupby('customer_state')['total_order_value'].mean().sort_values(ascending=False).reset_index()
    top_categories_geral = df_final['product_category_name_english'].value_counts().nlargest(15).reset_index()
    top_categories_geral.columns = ['Categoria', 'Número de Pedidos']
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Valor Médio do Pedido por Estado (Top 15)")
        fig = px.bar(df_state_value.head(15), 
                      y='customer_state', x='total_order_value',
                      orientation='h', title='Valor Médio do Pedido por Estado (Top 15)',
                      color='customer_state',
                      labels={'customer_state': 'Estado', 'total_order_value': 'Valor Médio do Pedido (R$)'})
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Top 15 Categorias Mais Populares (Geral)")
        fig = px.bar(top_categories_geral, 
                      y='Categoria', x='Número de Pedidos',
                      orientation='h', title='Top 15 Categorias Mais Populares (Geral)',
                      color='Categoria',
                      color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        O gráfico de 'Valor Médio do Pedido por Estado' evidencia uma clara distinção econômica entre as regiões. Estados como Paraíba (PB), Rondônia (RO) e Piauí (PI) lideram com os tickets médios mais altos. Surpreendentemente, os estados com maior volume de vendas, como São Paulo (SP) e Rio de Janeiro (RJ), não estão no topo desta lista. O valor do frete para essas regiões é geralmente mais elevado, inflando o **total_order_value** (valor total do pedido).

        A análise das categorias mais vendidas em todo o país desenha um perfil claro do consumidor médio da Olist. Categorias como **cama_mesa_banho**, **beleza_saude**, **esporte_lazer**, **informatica_acessorios** e **moveis_decoracao** dominam o ranking. Isso demonstra que a Olist atua fortemente no varejo de bens de consumo do dia a dia e de uso pessoal.
    """)

# --- Página 3: Padrões Sazonais de Vendas ---
elif pagina_selecionada == "Padrões Sazonais de Vendas":
    st.header("Análise de Sazonalidade das Vendas")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vendas Médias por Mês (Padrão Sazonal)")
        df_final['year'] = df_final['order_purchase_timestamp'].dt.year
        df_final['month_name'] = df_final['order_purchase_timestamp'].dt.month_name()
        monthly_sales_raw = df_final.groupby(['year', 'month_name'])['order_id'].nunique().reset_index()
        average_monthly_sales = monthly_sales_raw.groupby('month_name')['order_id'].mean().reset_index()
        months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        average_monthly_sales['month_name'] = pd.Categorical(average_monthly_sales['month_name'], categories=months_order, ordered=True)
        average_monthly_sales = average_monthly_sales.sort_values('month_name')
        fig = px.line(average_monthly_sales, x='month_name', y='order_id', markers=True,
                      title='Média de Pedidos por Mês (Padrão Sazonal Agregado)',
                      labels={'month_name': 'Mês', 'order_id': 'Média de Pedidos Únicos'})
        fig.update_traces(line_color='#EF553B')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Vendas por Dia da Semana")
        df_final['day_of_week'] = df_final['order_purchase_timestamp'].dt.day_name()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_daily_sales = df_final.groupby('day_of_week')['order_id'].nunique().reindex(days_order).reset_index()
        fig = px.bar(df_daily_sales, x='day_of_week', y='order_id',
                      title='Número de Pedidos por Dia da Semana',
                      color='day_of_week',
                      color_discrete_sequence=px.colors.qualitative.Bold,
                      labels={'day_of_week': 'Dia da Semana', 'order_id': 'Número de Pedidos'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        Os gráficos desta aba mostram que as vendas da Olist são fortemente influenciadas tanto por um macro-ciclo anual, impulsionado por datas comemorativas, quanto por um micro-ciclo semanal, que reflete a rotina do consumidor.
        
        Embora haja flutuações ao longo do ano, com picos menores em datas como Dia das Mães (Maio), o destaque absoluto é o mês de **Novembro**. Este pico é inequivocamente impulsionado pela Black Friday. Este evento se consolidou como a data mais importante para o varejo online no Brasil, antecipando grande parte das compras de fim de ano.

        As vendas são consistentemente mais altas durante os dias úteis (Segunda a Sexta-feira), com um pico geralmente na **Terça-feira**. Este padrão sugere que os consumidores podem usar o fim de semana para pesquisar produtos e navegar, mas a decisão e o ato da compra são frequentemente concretizados durante a semana.
    """)

# --- Página 4: Avaliação por Categoria Popular ---
elif pagina_selecionada == "Avaliação por Categoria Popular":
    st.header('Distribuição da Nota de Avaliação para as Categorias Mais Populares')
    st.markdown("O boxplot mostra a distribuição das notas para as 10 categorias com **maior volume de vendas**. O losango branco representa a **média**.")
    
    # 1. Preparar os dados
    df_categoria = df_final[['product_category_name_english', 'review_score']].copy().dropna()
    num_categories = 10
    top_10_popular_cats = df_categoria['product_category_name_english'].value_counts().nlargest(num_categories).index
    df_plot = df_categoria[df_categoria['product_category_name_english'].isin(top_10_popular_cats)]
    
    # (Opcional, mas recomendado) Ordenar o gráfico pela mediana para melhor visualização
    median_order = df_plot.groupby('product_category_name_english')['review_score'].median().sort_values(ascending=False).index
    
    # 2. Visualização com Boxplot
    fig = px.box(df_plot, x='review_score', y='product_category_name_english',
                  orientation='h',
                  color='product_category_name_english',
                  category_orders={'product_category_name_english': median_order},
                  title='Distribuição das Avaliações para as 10 Categorias Mais Populares',
                  labels={'review_score': 'Nota de Avaliação', 'product_category_name_english': 'Categoria do Produto'})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. Tabela Descritiva
    st.markdown("---")
    st.subheader("Estatísticas Descritivas por Categoria")
    
    # Calculando as estatísticas solicitadas: média, desvio padrão e variância
    descriptive_stats = df_plot.groupby('product_category_name_english')['review_score'].agg(['mean', 'std', 'var']).reset_index()
    
    # Renomeando as colunas
    descriptive_stats.columns = ['Categoria', 'Média', 'Desvio Padrão', 'Variância']
    
    # Ordenando pela média para melhor visualização
    descriptive_stats_sorted = descriptive_stats.sort_values(by="Média", ascending=False)
    
    st.dataframe(descriptive_stats_sorted)

    st.markdown("""
        Categorias como **'beleza_saude'** e **'esporte_lazer'** se destacam. Seus boxplots mostram uma mediana alta (geralmente em 5.0) e uma 'caixa' (o intervalo interquartil) relativamente compacta e posicionada na parte superior do gráfico.
        
        Por outro lado, categorias como **'cama_mesa_banho'** ou **'informatica_acessorios'**, apesar de serem extremamente populares, exibem um boxplot muito mais 'largo'. Além disso, elas frequentemente apresentam uma quantidade significativa de outliers (os pontos individuais) com notas muito baixas (1 e 2).
    """)

# --- Página 5: Satisfação por Tipo de Pagamento ---
elif pagina_selecionada == "Satisfação por Tipo de Pagamento":
    st.header("Análise de Satisfação por Tipo de Pagamento")
    df_payment_reviews = df_final[['review_score', 'payment_type']].copy().dropna()
    main_payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card']
    df_payment_reviews = df_payment_reviews[df_payment_reviews['payment_type'].isin(main_payment_types)]
    agg_stats_payment = df_payment_reviews.groupby('payment_type')['review_score'].agg(['mean', 'count', 'sem']).reset_index()
    agg_stats_payment['confidence_margin'] = agg_stats_payment.apply(lambda row: stats.t.ppf(0.975, row['count'] - 1) * row['sem'] if row['count'] > 1 else 0, axis=1)
    
    fig = px.bar(agg_stats_payment, 
                  y='payment_type', x='mean',
                  error_x='confidence_margin',
                  orientation='h',
                  color='payment_type',
                  title='Avaliação Média e IC (95%) por Tipo de Pagamento',
                  labels={'payment_type': 'Tipo de Pagamento', 'mean': 'Média da Nota de Avaliação'})
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        O **cartão de crédito** é o método associado à maior média de satisfação. A análise sugere que sua popularidade e alta avaliação vêm da experiência fluida e de baixa fricção que proporciona.
        
        Por outro lado, o **voucher** é o método que apresenta a pior avaliação média entre todos. A análise aponta que o uso de vouchers, que deveriam ser um incentivo, pode estar se tornando uma fonte de frustração. As causas prováveis incluem problemas técnicos na aplicação do código ou regras de promoção confusas que quebram a expectativa do cliente.
    """)

# --- Página 6: Qualidade do Anúncio vs. Satisfação ---
elif pagina_selecionada == "Qualidade do Anúncio vs. Satisfação":
    st.header("Impacto da Qualidade do Anúncio na Satisfação do Cliente")
    st.markdown("""
    Analisamos se a quantidade de fotos no anúncio de um produto tem relação com a nota de avaliação final.
    - **Hipótese Nula ($H_0$)**: A avaliação média é **igual** para produtos com poucas (1) e muitas (>3) fotos.
    - **Hipótese Alternativa ($H_1$)**: As médias são **diferentes**.
    """)
    st.markdown("---")

    df_cleaned = df_final.dropna(subset=['review_score', 'product_photos_qty'])
    df_few_photos = df_cleaned[df_cleaned['product_photos_qty'] == 1]
    df_many_photos = df_cleaned[df_cleaned['product_photos_qty'] > 3]
    if len(df_few_photos) < 2 or len(df_many_photos) < 2:
        st.warning("Não há dados suficientes para realizar a comparação.")
    else:
        mean_few = df_few_photos['review_score'].mean()
        mean_many = df_many_photos['review_score'].mean()
        t_stat, p_value = stats.ttest_ind(df_few_photos['review_score'], df_many_photos['review_score'], equal_var=False)
        
        st.subheader("Resultados do Teste")
        col1, col2, col3 = st.columns(3)
        col1.metric("Média (1 Foto)", f"{mean_few:.3f}")
        col2.metric("Média (>3 Fotos)", f"{mean_many:.3f}")
        col3.metric("Valor-p do Teste", f"{p_value:.4f}")
        
        st.markdown("---")
        if p_value < 0.05:
            st.success("**Conclusão:** Rejeitamos a hipótese nula. Existe uma diferença estatisticamente significativa entre as médias de avaliação.")
        else:
            st.warning("**Conclusão:** Não há evidência para rejeitar a hipótese nula. A diferença observada pode ser fruto do acaso.")

        ci_few = stats.t.interval(0.95, len(df_few_photos)-1, loc=mean_few, scale=stats.sem(df_few_photos['review_score']))
        ci_many = stats.t.interval(0.95, len(df_many_photos)-1, loc=mean_many, scale=stats.sem(df_many_photos['review_score']))
        err_few = (ci_few[1] - ci_few[0]) / 2
        err_many = (ci_many[1] - ci_many[0]) / 2
        
        data_to_plot = pd.DataFrame({'Grupo': ['1 Foto', '> 3 Fotos'], 'Média': [mean_few, mean_many], 'erro': [err_few, err_many]})
        fig = px.bar(data_to_plot, x='Grupo', y='Média', error_y='erro',
                      color='Grupo',
                      color_discrete_map={'1 Foto':'#FFA15A', '> 3 Fotos':'#00CC96'},
                      title='Comparativo da Média de Avaliação por Nº de Fotos no Anúncio',
                      labels={'Média': 'Média da Nota de Avaliação'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        A qualidade do anúncio, representada pelo número de fotos, tem um impacto positivo, mas marginal, na satisfação do cliente. Ela não é um dos principais fatores que levam a uma avaliação de 5 estrelas, nem é a causa principal de uma avaliação de 1 estrela, quando comparada a fatores como atraso na entrega ou defeitos no produto.
    """)

# --- Página 7: Qui-Quadrado (Categoria vs. Estado) (COM ANÁLISE) ---
elif pagina_selecionada == "Qui-Quadrado (Categoria vs. Estado)":
    st.header("Teste Qui-Quadrado: Relação entre Categoria do Produto e Estado do Cliente")
    st.markdown("""
    Analisamos se a preferência por uma categoria de produto é influenciada pelo estado do cliente.
    - **Hipótese Nula ($H_0$)**: A escolha da categoria é **independente** do estado do cliente.
    - **Hipótese Alternativa ($H_1$)**: A escolha da categoria **depende** do estado do cliente.
    """)
    st.markdown("---")

    df_chi = df_final.dropna(subset=['customer_state', 'product_category_name_english'])
    top_10_states = df_chi['customer_state'].value_counts().nlargest(10).index
    top_10_categories = df_chi['product_category_name_english'].value_counts().nlargest(10).index
    df_filtered = df_chi[(df_chi['customer_state'].isin(top_10_states)) & (df_chi['product_category_name_english'].isin(top_10_categories))]
    contingency_table = pd.crosstab(df_filtered['customer_state'], df_filtered['product_category_name_english'])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    st.subheader("Resultados do Teste")
    col1, col2 = st.columns(2)
    col1.metric("Estatística Qui-Quadrado (χ²)", f"{chi2:.2f}")
    col2.metric("Valor-p", f"{p_value:.4f}")
    
    # --- Análise do Resultado Adicionada ---
    st.subheader("Análise do Resultado")
    if p_value < 0.05:
        st.success("**Conclusão: Rejeitamos a Hipótese Nula.**")
        st.markdown("O Valor-p extremamente baixo indica que a associação observada entre o estado do cliente e a categoria do produto **não é uma coincidência**. Existem, de fato, preferências de consumo regionais estatisticamente significativas. O heatmap abaixo ajuda a visualizar onde essas preferências são mais fortes.")
    else:
        st.warning("**Conclusão: Não Rejeitamos a Hipótese Nula.**")
        st.markdown("Não há evidências suficientes para afirmar que existe uma associação entre o estado do cliente e a categoria do produto.")

    st.markdown("---")
    st.subheader("Heatmap da Contagem de Pedidos por Categoria e Estado")
    fig = px.imshow(contingency_table, text_auto=True,
                      color_continuous_scale='Plasma',
                      title='Contagem de Pedidos por Categoria e Estado (Top 10)',
                      labels={'x': 'Categoria do Produto', 'y': 'Estado do Cliente'})
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Ver Tabela de Contingência Completa (Dados do Gráfico)"):
        st.dataframe(contingency_table)

    st.markdown("""
        Vemos "hotspots" (células de cor clara) muito claros. São Paulo (SP), por ser o maior mercado, domina em volume absoluto em quase todas as top 10 categorias. No entanto, o interessante é observar as proporções. Por exemplo, a popularidade de **'cama_mesa_banho'** em SP é gigantesca, enquanto outros estados podem ter uma preferência maior por **'esporte_lazer'** ou **'beleza_saude'** em relação a sua própria base de clientes.
    """)
