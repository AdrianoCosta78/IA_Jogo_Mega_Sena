# 🎯 Cicinho - Inteligência Artificial para Análise da Mega-Sena

**Cicinho** é uma aplicação interativa construída com Python e Streamlit que analisa os resultados da Mega-Sena. Ela oferece funcionalidades estatísticas, geração de jogos e previsão com rede neural, em homenagem a Cícero, meu pai, que adorava esse jogo.

## 🧠 Funcionalidades do Projeto

### 1 - Simular Jogos
Gera jogos aleatórios com controle de quantidade mínima e máxima de dezenas pares.

### 2 - Frequência por Ano
Visualiza quais dezenas mais saíram em cada ano com gráficos interativos.

### 3 - Pares de Dezenas Mais Comuns
Mostra os pares de dezenas que mais saíram juntos nos concursos da Mega-Sena.

### 4 - Sugestão de Dezenas Frequentes
Sugere as dezenas mais sorteadas nos últimos concursos (você escolhe quantos).

### 5 - Comparar Jogo com Histórico
Permite verificar se um jogo inserido já teve dezenas que saíram juntas em concursos anteriores.

### 6 - Download Jogos Gerados
Permite baixar os jogos simulados em CSV.

### 7 - Previsão Neural
Usa uma rede neural para prever dezenas com base nas últimas N rodadas e gera diversos jogos com base nas probabilidades aprendidas.

## 🧠 Como funciona a Rede Neural

A IA utiliza um `MultiOutputClassifier` com `MLPClassifier` do `scikit-learn`. Ela transforma os jogos passados em vetores one-hot e aprende a prever as dezenas futuras com base em históricos.

- **Treinamento:** Usa as últimas N rodadas para prever a próxima.
- **Predição:** Gera uma probabilidade de cada dezena aparecer.
- **Geração de jogos:** Sorteia dezenas com base nessas probabilidades.

## 🛠️ Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- Pacotes listados em `requirements.txt`

### Instalação

```bash
git clone https://github.com/seu-usuario/cicinho.git
cd cicinho
pip install -r requirements.txt
streamlit run mega_app.py
📁 Estrutura do Projeto
bash
Copiar
Editar
📦cicinho
 ┣ 📄mega_app.py           # Código principal da aplicação Streamlit
 ┣ 📄mega_neural.py        # Algoritmo de rede neural
 ┣ 📄Mega-Sena.xlsx        # Base de dados dos sorteios
 ┣ 📄requirements.txt      # Dependências
 ┗ 📄README.md             # Documentação do projeto
📷 Logo
O projeto conta com um logo exclusivo em homenagem a Cícero (Cicinho).

📃 Licença
Projeto livre para fins educacionais e não comerciais.

