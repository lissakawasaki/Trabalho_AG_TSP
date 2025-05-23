"""
    * Lissa Guirau Kawasaki, Theo Okagawa Rodrigues.
    * Algoritmos Genéticos_TSP - Caixeiro viajante.
    * INTELIGENCIA ARTIFICIAL - UNIVERSIDADE ESTADUAL DO PARANÁ.
"""
import tsplib95
import random
import time
import os
import matplotlib.pyplot as plt

def carregar_instancia(nome_arquivo):
    try:
        problema = tsplib95.load(nome_arquivo)
        cidades = list(problema.get_nodes())
        num_cidades = len(cidades)
        print(f"Instância '{problema.name}' carregada com sucesso.")
        print(f"Número de cidades: {num_cidades}")
        return problema, cidades, num_cidades
    except Exception as e:
        print(f"Erro ao carregar a instância: {e}")
        return None, [], 0

def criar_rota_aleatoria(cidades):
    rota = list(cidades)
    random.shuffle(rota)
    return rota

def inicializar_populacao(tamanho_populacao, cidades):
    return [criar_rota_aleatoria(cidades) for _ in range(tamanho_populacao)]

def calcular_distancia_rota(rota, problema, num_cidades):
    distancia_total = 0
    for i in range(num_cidades):
        cidade_origem = rota[i]
        cidade_destino = rota[(i + 1) % num_cidades]
        distancia_total += problema.get_weight(cidade_origem, cidade_destino)
    return distancia_total

def calcular_fitness(rota, problema, num_cidades):
    distancia = calcular_distancia_rota(rota, problema, num_cidades)
    return 1.0 / distancia if distancia > 0 else float('inf')

def selecao_roleta(populacao, valores_fitness):
    total_fitness = sum(valores_fitness)
    if total_fitness == 0:
        return random.choice(populacao)
    
    probabilidades = [fitness / total_fitness for fitness in valores_fitness]
    valor_aleatorio = random.random()
    soma_acumulada = 0
    
    for i, individuo in enumerate(populacao):
        soma_acumulada += probabilidades[i]
        if soma_acumulada > valor_aleatorio:
            return individuo
    
    return populacao[-1]  # Caso extremo

def crossover_ordenado(pai1, pai2):
    tamanho = len(pai1)
    filho1, filho2 = [-1] * tamanho, [-1] * tamanho
    
    # Seleciona dois pontos de corte aleatórios
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    
    filho1[inicio:fim+1] = pai1[inicio:fim+1]
    filho2[inicio:fim+1] = pai2[inicio:fim+1]
    
    # Preenche o resto do filho1 com genes do pai2
    posicao_filho = (fim + 1) % tamanho
    posicao_pai = (fim + 1) % tamanho
    
    while -1 in filho1:
        if pai2[posicao_pai] not in filho1:
            filho1[posicao_filho] = pai2[posicao_pai]
            posicao_filho = (posicao_filho + 1) % tamanho
        posicao_pai = (posicao_pai + 1) % tamanho
    
    # Preenche o resto do filho2 com genes do pai1
    posicao_filho = (fim + 1) % tamanho
    posicao_pai = (fim + 1) % tamanho
    
    while -1 in filho2:
        if pai1[posicao_pai] not in filho2:
            filho2[posicao_filho] = pai1[posicao_pai]
            posicao_filho = (posicao_filho + 1) % tamanho
        posicao_pai = (posicao_pai + 1) % tamanho
    
    return filho1, filho2

def mutacao_troca(rota, taxa_mutacao):
    rota_mutada = list(rota)
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(rota_mutada)), 2)
        rota_mutada[idx1], rota_mutada[idx2] = rota_mutada[idx2], rota_mutada[idx1]
    return rota_mutada

def algoritmo_genetico(problema, cidades, num_cidades, tamanho_populacao=50, num_geracoes=100, taxa_crossover=0.8, taxa_mutacao=0.05, tamanho_elitismo=2):
 
    populacao = inicializar_populacao(tamanho_populacao, cidades)
    melhor_rota_global = None
    melhor_distancia_global = float('inf')
    historico_distancias = []
    
    print(f"\nIniciando Algoritmo Genético...")
    print(f"Tamanho da População: {tamanho_populacao}, Número de Gerações: {num_geracoes}")
    print(f"Taxa de Crossover: {taxa_crossover}, Taxa de Mutação: {taxa_mutacao}, Elitismo: {tamanho_elitismo}\n")
    
    for geracao in range(num_geracoes):
        valores_fitness = [calcular_fitness(rota, problema, num_cidades) for rota in populacao]
        
        melhor_fitness_geracao = max(valores_fitness)
        indice_melhor_geracao = valores_fitness.index(melhor_fitness_geracao)
        melhor_rota_geracao = populacao[indice_melhor_geracao]
        melhor_distancia_geracao = calcular_distancia_rota(melhor_rota_geracao, problema, num_cidades)
        
        if melhor_distancia_geracao < melhor_distancia_global:
            melhor_distancia_global = melhor_distancia_geracao
            melhor_rota_global = list(melhor_rota_geracao)
            print(f"Geração {geracao+1}: Nova melhor distância = {melhor_distancia_global:.2f}")
        
        historico_distancias.append(melhor_distancia_global)
        
        if (geracao + 1) % 10 == 0:
            print(f"Geração {geracao+1}: Melhor distância atual = {melhor_distancia_global:.2f}")

        nova_populacao = []
        
        if tamanho_elitismo > 0:
            indices_ordenados = sorted(range(len(populacao)), 
                                      key=lambda k: valores_fitness[k], 
                                      reverse=True)
            for i in range(min(tamanho_elitismo, tamanho_populacao)):
                nova_populacao.append(populacao[indices_ordenados[i]])
        
        # Preenche o resto da população com novos indivíduos
        while len(nova_populacao) < tamanho_populacao:
            # Seleciona dois pais
            pai1 = selecao_roleta(populacao, valores_fitness)
            pai2 = selecao_roleta(populacao, valores_fitness)
            
            if random.random() < taxa_crossover:
                filho1, filho2 = crossover_ordenado(pai1, pai2)
            else:
                filho1, filho2 = list(pai1), list(pai2)
            
            # Aplica mutação
            filho1 = mutacao_troca(filho1, taxa_mutacao)
            filho2 = mutacao_troca(filho2, taxa_mutacao)
            
            # Adiciona filhos à nova população
            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)
        
        populacao = nova_populacao
    
    print(f"\nAlgoritmo Genético concluído após {num_geracoes} gerações.")
    print(f"Melhor rota encontrada: {melhor_rota_global}")
    print(f"Distância da melhor rota: {melhor_distancia_global:.2f}")
    
    return melhor_rota_global, melhor_distancia_global, historico_distancias

def gerar_grafico_convergencia(historico_distancias, nome_instancia):
    """Gera um gráfico de convergência (distância vs. geração)"""
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(historico_distancias) + 1), historico_distancias, 'b-')
    plt.title(f'Convergência do AG para a instância {nome_instancia}')
    plt.xlabel('Geração')
    plt.ylabel('Melhor Distância')
    plt.grid(True)
    nome_arquivo = f"{nome_instancia}_convergencia.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Gráfico de convergência salvo como {nome_arquivo}")
    return nome_arquivo

def gerar_grafico_tempo_execucao(instancias, tempos, tamanhos):
    """Gera um gráfico de barras comparando o tempo de execução das instâncias"""
    plt.figure(figsize=(10, 6))
    bars = plt.bar(instancias, tempos, color=['blue', 'green', 'red'])
    
    for i, (bar, tamanho) in enumerate(zip(bars, tamanhos)):
        plt.text(i, bar.get_height() + 0.1, f"{tamanho} cidades", 
                ha='center', va='bottom')
        plt.text(i, bar.get_height() / 2, f"{tempos[i]:.2f}s", 
                ha='center', va='center', color='white', fontweight='bold')
    
    plt.title('Tempo de Execução por Instância')
    plt.xlabel('Instância')
    plt.ylabel('Tempo (segundos)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    nome_arquivo = "comparacao_tempo_execucao.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Gráfico de comparação de tempo salvo como {nome_arquivo}")
    return nome_arquivo

def executar_instancia(arquivo_tsp, tamanho_populacao=50, num_geracoes=100, taxa_crossover=0.8, taxa_mutacao=0.05, tamanho_elitismo=2, semente=42):
    """Executa o algoritmo genético para uma instância específica e retorna os resultados"""
    random.seed(semente)
    
    problema, cidades, num_cidades = carregar_instancia(arquivo_tsp)
    if not problema:
        print(f"Não foi possível carregar a instância {arquivo_tsp}.")
        return None, None, None, None, 0
    
    nome_instancia = problema.name
    
    inicio = time.time()
    melhor_rota, melhor_distancia, historico = algoritmo_genetico(
        problema, cidades, num_cidades,
        tamanho_populacao=tamanho_populacao,
        num_geracoes=num_geracoes,
        taxa_crossover=taxa_crossover,
        taxa_mutacao=taxa_mutacao,
        tamanho_elitismo=tamanho_elitismo
    )
    fim = time.time()
    tempo_execucao = fim - inicio
    
    print(f"\nTempo de execução para {nome_instancia}: {tempo_execucao:.2f} segundos")
    
    valores_otimos = {
        "burma14": 3323,
        "ulysses16": 6859,
        "berlin52": 7542,
        "kroA100": 21282,
        "pcb442": 50778
    }
    
    # Compara com o valor ótimo conhecido
    erro_percentual = None
    if nome_instancia in valores_otimos:
        valor_otimo = valores_otimos[nome_instancia]
        erro_percentual = ((melhor_distancia - valor_otimo) / valor_otimo) * 100
        print(f"Valor ótimo conhecido para {nome_instancia}: {valor_otimo}")
        print(f"Erro percentual: {erro_percentual:.2f}%")
    
    nome_grafico = gerar_grafico_convergencia(historico, nome_instancia)
    

    nome_arquivo_resultado = f"{nome_instancia}_resultado.txt"
    with open(nome_arquivo_resultado, "w") as arquivo:
        arquivo.write(f"Instância: {nome_instancia}\n")
        arquivo.write(f"Número de cidades: {num_cidades}\n")
        arquivo.write(f"Melhor rota: {melhor_rota}\n")
        arquivo.write(f"Distância: {melhor_distancia:.2f}\n")
        arquivo.write(f"Tempo de execução: {tempo_execucao:.2f} segundos\n")
        if nome_instancia in valores_otimos:
            arquivo.write(f"Valor ótimo conhecido: {valores_otimos[nome_instancia]}\n")
            arquivo.write(f"Erro percentual: {erro_percentual:.2f}%\n")
    
    print(f"Resultados salvos em: {nome_arquivo_resultado}")
    
    return nome_instancia, melhor_distancia, erro_percentual, historico, tempo_execucao, num_cidades

def gerar_resultados(resultados):
    relatorio = """# Relatório: Algoritmo Genético para o Problema do Caixeiro Viajante

Foram utilizadas três instâncias do TSPLIB com diferentes tamanhos:

""" 
    for resultado in resultados:
        nome, distancia, erro, _, tempo, num_cidades = resultado
        relatorio += f"- **{nome}**: {num_cidades} cidades\n"

    relatorio += """

## 3. Parâmetros do Algoritmo

- Tamanho da população: 50  
- Número de gerações: 100  
- Taxa de crossover: 0.8  
- Taxa de mutação: 0.05  
- Elitismo: 2  

## 4. Resultados Obtidos

| Instância | Nº Cidades | Melhor Distância | Tempo (s) | Erro (%) |
|-----------|------------|------------------|-----------|----------|
"""

    for resultado in resultados:
        nome, distancia, erro, _, tempo, num_cidades = resultado
        erro_formatado = f"{erro:.2f}%" if erro is not None else "N/A"
        relatorio += f"| {nome} | {num_cidades} | {distancia:.2f} | {tempo:.2f} | {erro_formatado} |\n"
    
    with open("relatorio_resultados.md", "w", encoding="utf-8") as f:
        f.write(relatorio)
        print("Relatório salvo como 'relatorio_resultados.md'")
    
    return relatorio

def main():
    instancias = ["burma14.tsp", "kroA100.tsp", "pcb442.tsp"]
    
    TAMANHO_POPULACAO = 50
    NUM_GERACOES = 100
    TAXA_CROSSOVER = 0.8
    TAXA_MUTACAO = 0.05
    TAMANHO_ELITISMO = 2
    SEMENTE = 42

    resultados = []
    nomes_instancias = []
    tempos_execucao = []
    tamanhos_instancias = []

    for arquivo_tsp in instancias:
        print(f"\n{'='*50}")
        print(f"Executando para a instância: {arquivo_tsp}")
        print(f"{'='*50}\n")
        
        resultado = executar_instancia(
            arquivo_tsp,
            tamanho_populacao=TAMANHO_POPULACAO,
            num_geracoes=NUM_GERACOES,
            taxa_crossover=TAXA_CROSSOVER,
            taxa_mutacao=TAXA_MUTACAO,
            tamanho_elitismo=TAMANHO_ELITISMO,
            semente=SEMENTE
        )
        
        if resultado[0]: 
            resultados.append(resultado)
            nomes_instancias.append(resultado[0])
            tempos_execucao.append(resultado[4])
            tamanhos_instancias.append(resultado[5])
    

    if len(nomes_instancias) > 1:
        gerar_grafico_tempo_execucao(nomes_instancias, tempos_execucao, tamanhos_instancias)
    
    if resultados:
        resultados = gerar_resultados(resultados)
        print(f"\nProcesso concluído! Foram gerados:")
        print(f"- Gráficos de convergência para cada instância")
        print(f"- Gráfico comparativo de tempo de execução")
        print(f"- Relatório detalhado: {resultados}")
    else:
        print("Não foi possível gerar o relatório pois nenhuma instância foi executada com sucesso.")

if __name__ == "__main__":
    main()
