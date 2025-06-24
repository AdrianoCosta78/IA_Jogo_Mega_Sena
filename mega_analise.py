import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from mega_neural import (
    preparar_dados,
    treinar_modelo,
    obter_probabilidades,
    gerar_varios_jogos
)
import random
import os

# Lê o arquivo Excel
df = pd.read_excel("Mega-Sena.xlsx")

# Define as colunas das dezenas
colunas_dezenas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']

# Junta todas as dezenas sorteadas em uma lista única
todas_dezenas = df[colunas_dezenas].values.flatten()
contador = Counter(todas_dezenas)
dezenas_mais_frequentes = contador.most_common()


def mostrar_estatisticas():
    print("\n📊 Estatísticas de frequência das dezenas:\n")
    for dezena, freq in dezenas_mais_frequentes:
        print(f"Dezena {int(dezena):02d}: {freq} vezes")

    numeros, frequencias = zip(*dezenas_mais_frequentes)
    plt.bar(numeros, frequencias, color="blue")
    plt.title("Frequência das dezenas sorteadas")
    plt.xlabel("Dezenas")
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.show()


def gerar_jogos_simples(qtd_jogos, top_n=20):
    top_dezenas = [int(dezena) for dezena, _ in dezenas_mais_frequentes[:top_n]]
    print(f"\n🎰 Gerando {qtd_jogos} jogos com base nas {top_n} dezenas mais sorteadas:\n")

    jogos_gerados = set()
    while len(jogos_gerados) < qtd_jogos:
        jogo = tuple(sorted(random.sample(top_dezenas, 6)))
        if jogo not in jogos_gerados:
            jogos_gerados.add(jogo)
            print(" -", jogo)

    salvar = input("\nDeseja salvar os jogos em um arquivo? (s/n): ").strip().lower()
    if salvar == "s":
        nome = input("Digite o nome do arquivo (ex: meus_jogos.txt): ")
        salvar_jogos_em_arquivo(jogos_gerados, nome)


def jogo_valido(jogo):
    pares = sum(1 for n in jogo if n % 2 == 0)
    soma = sum(jogo)

    consecutivas = 0
    max_consecutivas = 0
    for i in range(1, len(jogo)):
        if jogo[i] == jogo[i - 1] + 1:
            consecutivas += 1
            max_consecutivas = max(max_consecutivas, consecutivas)
        else:
            consecutivas = 0

    return (
        2 <= pares <= 4 and
        120 <= soma <= 200 and
        max_consecutivas < 2
    )


def gerar_jogos_filtrados(qtd_jogos, top_n=20):
    top_dezenas = [int(dezena) for dezena, _ in dezenas_mais_frequentes[:top_n]]
    print(f"\n🧠 Gerando {qtd_jogos} jogos filtrados com base nas {top_n} dezenas mais sorteadas:\n")

    jogos_gerados = set()
    tentativas = 0

    while len(jogos_gerados) < qtd_jogos and tentativas < 1000:
        tentativas += 1
        jogo = tuple(sorted(random.sample(top_dezenas, 6)))
        if jogo not in jogos_gerados and jogo_valido(jogo):
            jogos_gerados.add(jogo)
            print(" -", jogo)

    if len(jogos_gerados) < qtd_jogos:
        print("\n⚠️ Não foi possível gerar todos os jogos com os filtros definidos.")

    salvar = input("\nDeseja salvar os jogos em um arquivo? (s/n): ").strip().lower()
    if salvar == "s":
        nome = input("Digite o nome do arquivo (ex: jogos_filtrados.txt): ")
        salvar_jogos_em_arquivo(jogos_gerados, nome)

def salvar_jogos_em_arquivo(jogos, nome_arquivo="jogos_gerados.txt"):
    caminho = os.path.join("C:\\mega_ia", nome_arquivo)
    with open(caminho, "w") as f:
        for jogo in jogos:
            linha = ", ".join(f"{num:02d}" for num in jogo)
            f.write(linha + "\n")
    print(f"\n💾 Jogos salvos com sucesso em: {caminho}")

def menu():
    while True:
        print("\n=== MENU MEGA IA ===")
        print("1 - Ver estatísticas de frequência")
        print("2 - Gerar jogos simples")
        print("3 - Gerar jogos com filtros inteligentes")
        print("4 - Sair")
        print("5 - Frequência por década")
        print("6 - Estatísticas da soma das dezenas")
        print("7 - Distribuição de pares e ímpares")
        print("8 - Previsão Neural (IA)")
        

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_estatisticas()
        elif opcao == "2":
            qtd = int(input("Quantos jogos você deseja gerar? "))
            gerar_jogos_simples(qtd)
        elif opcao == "3":
            qtd = int(input("Quantos jogos você deseja gerar? "))
            gerar_jogos_filtrados(qtd)
        elif opcao == "4":
            print("Encerrando... Até logo!")
            break
        elif opcao == "5":
            frequencia_por_decada()
        elif opcao == "6":
            estatisticas_soma()
        elif opcao == "7":
            distribuicao_pares_impares()
        elif opcao == "8":
            # Nova funcionalidade
            max_N = len(df) - 1
            N = int(input(f"Use quantas últimas rodadas como histórico? (1–{max_N}): "))
            qtd = int(input("Quantos jogos a IA deve gerar? "))
            print("\nTreinando modelo, aguarde...") 
            X, Y = preparar_dados(df, N=N)
            clf = treinar_modelo(X, Y,
                                hidden_layer_sizes=(100,),
                                max_iter=300,
                                test_size=0.2,
                                random_state=42)
            print("Gerando jogos com base nas probabilidades previstas...")
            probs = obter_probabilidades(clf, df, N=N)
            jogos = gerar_varios_jogos(probs, qtd)
            print(f"\n-- {len(jogos)} jogos gerados pela IA --")
            for jogo in jogos:
                print(jogo)
        else:
            print("Opção inválida. Tente novamente.")
        

def frequencia_por_decada():
    df['Ano'] = pd.to_datetime(df['Data do Sorteio'], dayfirst=True).dt.year
    df['Década'] = (df['Ano'] // 10) * 10

    print("\n📅 Frequência das dezenas por década:\n")

    for decada in sorted(df['Década'].unique()):
        print(f"🕰️ Década de {decada}:")
        dezenas = df[df['Década'] == decada][colunas_dezenas].values.flatten()
        contagem = Counter(dezenas).most_common(10)
        for dezena, freq in contagem:
            print(f"  - {int(dezena):02d}: {freq} vezes")
        print()

def estatisticas_soma():
    df['Soma'] = df[colunas_dezenas].sum(axis=1)
    media = df['Soma'].mean()
    desvio = df['Soma'].std()

    print("\n➗ Estatísticas da soma das dezenas sorteadas:")
    print(f"🔹 Média das somas: {media:.2f}")
    print(f"🔸 Desvio padrão: {desvio:.2f}")


def distribuicao_pares_impares():
    print("\n⚖️ Distribuição pares x ímpares nos sorteios:\n")
    distribuicoes = Counter()

    for _, linha in df.iterrows():
        dezenas = [linha[col] for col in colunas_dezenas]
        pares = sum(1 for d in dezenas if d % 2 == 0)
        impares = 6 - pares
        distribuicoes[(pares, impares)] += 1

    for (pares, impares), qtd in sorted(distribuicoes.items()):
        print(f"{pares} pares e {impares} ímpares: {qtd} vezes")


# Inicia o programa
if __name__ == "__main__":
    menu()

