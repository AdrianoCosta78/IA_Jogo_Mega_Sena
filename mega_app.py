
import streamlit as st
import pandas as pd
import random
import time
from collections import Counter
from itertools import combinations
from mega_neural import (
    preparar_dados,
    treinar_modelo,
    prever_proximo,
    obter_probabilidades,
    gerar_varios_jogos
)
import plotly.express as px

# Carregar dados
@st.cache_data
def carregar_dados():
    # 1) lê o Excel sem parâmetros de data
    df = pd.read_excel("Mega-Sena.xlsx")
    # 2) converte a coluna de data corretamente, informando dayfirst
    df['Data do Sorteio'] = pd.to_datetime(df['Data do Sorteio'], dayfirst=True)
    # 3) extrai o ano
    df['Ano'] = df['Data do Sorteio'].dt.year
    return df

df = carregar_dados()



st.title("Mega-Sena Análise e Simulação")

with st.sidebar:
    st.image("Cicinho.png", use_container_width=True)
    st.markdown("### Escolha uma funcionalidade:")
    menu = st.selectbox("", [
        "1 - Simular Jogos",
        "2 - Frequência por Ano",
        "3 - Pares de Dezenas Mais Comuns",
        "4 - Sugestão de Dezenas Frequentes",
        "5 - Comparar Jogo com Histórico",
        "6 - Download Jogos Gerados",
        "7 - Previsão Neural"
    ])

# Função para gerar jogos
def gerar_jogo(pares_min=2, pares_max=4):
    while True:
        jogo = random.sample(range(1, 61), 6)
        pares = len([x for x in jogo if x % 2 == 0])
        if pares_min <= pares <= pares_max:
            return sorted(jogo)

# Função para frequência de dezenas num ano específico
def frequencia_ano(df, ano):
    df_ano = df[df['Ano'] == ano]
    dezenas = []
    for i in range(1,7):
        dezenas += df_ano[f'Bola{i}'].tolist()
    freq = pd.Series(dezenas).value_counts().sort_index()
    return freq

# Função pares mais comuns
def pares_mais_comuns(df):
    pares = []
    for _, row in df.iterrows():
        bolas = [row[f'Bola{i}'] for i in range(1,7)]
        pares += list(combinations(sorted(bolas), 2))
    contagem = Counter(pares)
    return contagem.most_common(10)

# Função para sugestão de dezenas frequentes nos últimos N concursos
def dezenas_frequentes(df, ultimos=100):
    df_recente = df.tail(ultimos)
    dezenas = []
    for i in range(1,7):
        dezenas += df_recente[f'Bola{i}'].tolist()
    freq = pd.Series(dezenas).value_counts()
    freq = freq.sort_values(ascending=False)
    return freq

# Função para comparar jogo com histórico (quantas dezenas já saíram)
def comparar_jogo(jogo, df):
    count = 0
    for _, row in df.iterrows():
        bolas = [row[f'Bola{i}'] for i in range(1,7)]
        intersec = set(jogo).intersection(set(bolas))
        if len(intersec) >= 3:  # Exemplo: já saiu com 3 ou mais dezenas iguais
            count += 1
    return count

# Lista para armazenar jogos gerados (para download)
if "jogos_gerados" not in st.session_state:
    st.session_state.jogos_gerados = []

# --- Funcionalidades ---

if menu == "1 - Simular Jogos":
    st.header("Simular jogos aleatórios com filtro de pares/ímpares")
    pares_min = st.slider("Mínimo de dezenas pares", 0, 6, 2)
    pares_max = st.slider("Máximo de dezenas pares", 0, 6, 4)
    gerar = st.button("Gerar jogo")
    if gerar:
        jogo = gerar_jogo(pares_min, pares_max)
        st.write("Jogo gerado:", jogo)
        st.session_state.jogos_gerados.append(jogo)

elif menu == "2 - Frequência por Ano":
    st.header("Frequência das dezenas por ano")
    anos = sorted(df['Ano'].unique())
    ano_selecionado = st.selectbox("Selecione o ano", anos)
    freq = frequencia_ano(df, ano_selecionado)
    fig = px.bar(x=freq.index, y=freq.values,
                 labels={"x":"Dezena", "y":"Frequência"},
                 title=f"Frequência das dezenas em {ano_selecionado}")
    st.plotly_chart(fig)

elif menu == "3 - Pares de Dezenas Mais Comuns":
    st.header("Pares de dezenas que mais saíram juntos")
    pares = pares_mais_comuns(df)
    pares_df = pd.DataFrame(pares, columns=["Par de Dezenas", "Ocorrências"])
    st.table(pares_df)

elif menu == "4 - Sugestão de Dezenas Frequentes":
    st.header("Dezenas mais frequentes nos últimos concursos")
    ultimos = st.slider("Número de concursos recentes para analisar", 10, 200, 100)
    freq = dezenas_frequentes(df, ultimos)
    st.write(freq)
    fig = px.bar(x=freq.index, y=freq.values,
                 labels={"x":"Dezena", "y":"Frequência"},
                 title=f"Dezenas frequentes nos últimos {ultimos} concursos")
    st.plotly_chart(fig)

elif menu == "5 - Comparar Jogo com Histórico":
    st.header("Comparar um jogo gerado com o histórico da Mega-Sena")
    jogo_input = st.text_input("Digite 6 dezenas separadas por vírgula", "1, 2, 3, 4, 5, 6")
    if st.button("Comparar"):
        try:
            jogo = sorted([int(x.strip()) for x in jogo_input.split(",")])
            if len(jogo) != 6:
                st.error("Digite exatamente 6 dezenas.")
            elif any(d < 1 or d > 60 for d in jogo):
                st.error("Dezenas devem estar entre 1 e 60.")
            else:
                ocorrencias = comparar_jogo(jogo, df)
                st.write(f"O jogo {jogo} já teve {ocorrencias} concursos com 3 ou mais dezenas iguais.")
        except Exception as e:
            st.error(f"Erro: {e}")

elif menu == "6 - Download Jogos Gerados":
    st.header("Download dos jogos gerados")
    if st.session_state.jogos_gerados:
        df_jogos = pd.DataFrame(st.session_state.jogos_gerados, columns=[f"Dezena {i}" for i in range(1,7)])
        csv = df_jogos.to_csv(index=False)
        st.download_button("Baixar CSV dos jogos", csv, file_name="jogos_mega_sena.csv", mime="text/csv")
        st.table(df_jogos)
    else:
        st.info("Nenhum jogo gerado ainda. Vá para a opção 1 para gerar jogos.")

elif menu == "7 - Previsão Neural":
    st.header("🔮 Previsão Neural: gerar múltiplos jogos")

    # Limita N para não ultrapassar 100 (evita explosão de features)
    max_N = min(len(df) - 2, 100)
    N = st.slider(
        "Histórico (últimas N rodadas):",
        min_value=5,
        max_value=max_N,
        value=10
    )

    # Quantidade de jogos a gerar
    qtd_jogos = st.number_input(
        "Quantos jogos a IA deve gerar?",
        min_value=1,
        max_value=100,
        value=10
    )

    if N > 50:
        st.warning("⚠️ Usar N muito grande pode tornar o treinamento muito lento.")

    if st.button("Treinar modelo e gerar jogos"):
        start_time = time.time()

        try:
            st.info("📊 Preparando dados...")
            X, Y = preparar_dados(df, N=N)
            st.write(f"✔️ Dimensão dos dados de entrada: X = {X.shape}, Y = {Y.shape}")

            if X.shape[0] < 10:
                st.error("Dados insuficientes para treinamento. Tente diminuir o N.")
            else:
                with st.spinner("🤖 Treinando rede neural..."):
                    clf = treinar_modelo(
                        X, Y,
                        hidden_layer_sizes=(100,),
                        max_iter=50,  # menor para agilizar
                        test_size=0.2,
                        random_state=42
                    )

                with st.spinner("🎰 Gerando jogos..."):
                    probs = obter_probabilidades(clf, df, N=N)
                    jogos = gerar_varios_jogos(probs, qtd_jogos)

                end_time = time.time()
                duracao = round(end_time - start_time, 2)

                st.success(f"✅ {len(jogos)} jogos gerados em {duracao} segundos!")

                jogos_df = pd.DataFrame(jogos, columns=[f"Dezena {i}" for i in range(1, 7)])
                st.table(jogos_df)

                csv = jogos_df.to_csv(index=False)
                st.download_button(
                    "📥 Baixar CSV dos jogos",
                    data=csv,
                    file_name="jogos_previsao_neural.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"❌ Ocorreu um erro durante o processamento: {e}")


