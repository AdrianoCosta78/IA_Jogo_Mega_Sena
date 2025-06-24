# mega_neural.py

import numpy as np
import random
from sklearn.neural_network import MLPClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.exceptions import NotFittedError

def to_one_hot(numbers):
    vec = np.zeros(60, dtype=int)
    vec[np.array(numbers) - 1] = 1
    return vec

def preparar_dados(df, N=5):
    """
    Monta X e Y usando as últimas N rodadas como histórico.
    Retorna X (features) e Y (targets) como numpy arrays.
    """
    colunas = [f'Bola{i}' for i in range(1,7)]
    X, Y = [], []
    for i in range(N, len(df)):
        prev = df.loc[i-N:i-1, colunas].values.tolist()
        feat = np.concatenate([to_one_hot(draw) for draw in prev])
        X.append(feat)
        Y.append(to_one_hot(df.loc[i, colunas].tolist()))
    return np.array(X), np.array(Y)

def treinar_modelo(X, Y, hidden_layer_sizes=(100,), max_iter=300, test_size=0.2, random_state=42):
    if len(X) < 2:
        # Treina direto sem split
        clf = MultiOutputClassifier(
            MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, random_state=random_state)
        )
        clf.fit(X, Y)
        return clf

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=test_size, random_state=random_state
    )

    clf = MultiOutputClassifier(
        MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, random_state=random_state)
    )
    clf.fit(X_train, Y_train)
    return clf

def prever_proximo(clf, df, N=5):
    """
    Usa o classificador treinado para prever as top‑6 dezenas do próximo sorteio.
    Trata corretamente o caso de classes únicas em alguns estimadores.
    """
    import numpy as np

    # Colunas de bolas
    colunas = [f'Bola{i}' for i in range(1,7)]
    # Índice do último sorteio
    ultimo_idx = len(df)
    # Prepara o vetor de features a partir dos N últimos sorteios
    last_draws = df.loc[ultimo_idx-N:ultimo_idx-1, colunas].values.tolist()
    feat = np.concatenate([to_one_hot(draw) for draw in last_draws]).reshape(1, -1)

    # Obtém lista de listas de probabilidades por estimador
    prob_list = clf.predict_proba(feat)

    # Extrai a probabilidade de "1" (presença) para cada dezena
    probs = []
    for i, probs_i in enumerate(prob_list):
        classes = clf.estimators_[i].classes_
        # Se existir rótulo 1, pega sua probabilidade; senão é zero
        if 1 in classes:
            idx1 = list(classes).index(1)
            probs.append(probs_i[0][idx1])
        else:
            probs.append(0.0)

    # Seleciona as 6 dezenas com maior probabilidade
    top6 = np.argsort(probs)[::-1][:6] + 1
    return sorted(top6.tolist())

def obter_probabilidades(clf, df, N=5):
    """
    Retorna lista de 60 probabilidades de cada dezena ser sorteada.
    """
    # igual ao prever_proximo, mas retornando o vetor de probs
    colunas = [f'Bola{i}' for i in range(1,7)]
    last = df.loc[len(df)-N:len(df)-1, colunas].values.tolist()
    feat = np.concatenate([to_one_hot(draw) for draw in last]).reshape(1, -1)
    prob_list = clf.predict_proba(feat)

    probs = []
    for i, probs_i in enumerate(prob_list):
        classes = clf.estimators_[i].classes_
        if 1 in classes:
            idx1 = list(classes).index(1)
            probs.append(probs_i[0][idx1])
        else:
            probs.append(0.0)
    return np.array(probs)

def gerar_varios_jogos(probabilidades, qtd_jogos=10):
    dezenas = list(range(1, 61))
    jogos = []

    for _ in range(qtd_jogos):
        jogo = sorted(random.choices(
            dezenas,
            weights=probabilidades,
            k=6
        ))

        # Garante que todas as dezenas sejam únicas dentro do jogo
        while len(set(jogo)) < 6:
            jogo = sorted(random.choices(
                dezenas,
                weights=probabilidades,
                k=6
            ))

        jogos.append(jogo)

    return jogos