# -*- coding: utf-8 -*-
"""
Algoritmo Genético para o Problema do Caixeiro Viajante (TSP)
Versão simplificada para Windows com geração de gráficos
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
    
    # Copia o segmento entre os pontos de corte
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
 
    # Inicializa a população
    populacao = inicializar_populacao(tamanho_populacao, cidades)
    melhor_rota_global = None
    melhor_distancia_global = float('inf')
    historico_distancias = []
    
    print(f"\nIniciando Algoritmo Genético...")
    print(f"Tamanho da População: {tamanho_populacao}, Número de Gerações: {num_geracoes}")
    print(f"Taxa de Crossover: {taxa_crossover}, Taxa de Mutação: {taxa_mutacao}, Elitismo: {tamanho_elitismo}\n")
    
    # Loop principal de gerações
    for geracao in range(num_geracoes):
        # Calcula o fitness de cada indivíduo
        valores_fitness = [calcular_fitness(rota, problema, num_cidades) for rota in populacao]
        
        # Encontra o melhor indivíduo da geração atual
        melhor_fitness_geracao = max(valores_fitness)
        indice_melhor_geracao = valores_fitness.index(melhor_fitness_geracao)
        melhor_rota_geracao = populacao[indice_melhor_geracao]
        melhor_distancia_geracao = calcular_distancia_rota(melhor_rota_geracao, problema, num_cidades)
        
        # Atualiza o melhor global se necessário
        if melhor_distancia_geracao < melhor_distancia_global:
            melhor_distancia_global = melhor_distancia_geracao
            melhor_rota_global = list(melhor_rota_geracao)
            print(f"Geração {geracao+1}: Nova melhor distância = {melhor_distancia_global:.2f}")
        
        # Armazena a melhor distância global desta geração
        historico_distancias.append(melhor_distancia_global)
        
        # Imprime progresso a cada 10 gerações
        if (geracao + 1) % 10 == 0:
            print(f"Geração {geracao+1}: Melhor distância atual = {melhor_distancia_global:.2f}")
        
        # Cria nova população
        nova_populacao = []
        
        # Aplica elitismo (mantém os melhores indivíduos)
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
            
            # Aplica crossover com probabilidade taxa_crossover
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
        
        # Substitui a população antiga pela nova
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
    
    # Adiciona rótulos com o número de cidades
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
    # Define semente para reprodutibilidade
    random.seed(semente)
    
    # Carrega a instância
    problema, cidades, num_cidades = carregar_instancia(arquivo_tsp)
    if not problema:
        print(f"Não foi possível carregar a instância {arquivo_tsp}.")
        return None, None, None, None, 0
    
    nome_instancia = problema.name
    
    # Executa o algoritmo genético e mede o tempo
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
    
    # Valores ótimos conhecidos para algumas instâncias comuns
    valores_otimos = {
        "burma14": 3323,
        "ulysses16": 6859,
        "berlin52": 7542,
        "kroA100": 21282,
        "pcb442": 50778
    }
    
    # Compara com o valor ótimo conhecido, se disponível
    erro_percentual = None
    if nome_instancia in valores_otimos:
        valor_otimo = valores_otimos[nome_instancia]
        erro_percentual = ((melhor_distancia - valor_otimo) / valor_otimo) * 100
        print(f"Valor ótimo conhecido para {nome_instancia}: {valor_otimo}")
        print(f"Erro percentual: {erro_percentual:.2f}%")
    
    # Gera o gráfico de convergência
    nome_grafico = gerar_grafico_convergencia(historico, nome_instancia)
    
    # Salva os resultados em um arquivo de texto
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

def gerar_relatorio(resultados):
    relatorio = """# Relatório: Algoritmo Genético para o Problema do Caixeiro Viajante

Foram utilizadas três instâncias do TSPLIB com diferentes tamanhos:

""" 
    # Adiciona informações sobre cada instância
    for resultado in resultados:
        nome, distancia, erro, _, tempo, num_cidades = resultado
        relatorio += f"- **{nome}**: {num_cidades} cidades\n"
    
    relatorio += """
## 3. Parâmetros do Algoritmo

Os seguintes parâmetros foram utilizados em todas as execuções:

- Tamanho da População: 50 indivíduos
- Número de Gerações: 100
- Taxa de Crossover: 0.8 (80%)
- Taxa de Mutação: 0.05 (5%)
- Tamanho do Elitismo: 2 indivíduos
- Semente Aleatória: 42 (para reprodutibilidade)

## 4. Resultados Obtidos

### 4.1 Qualidade das Soluções

"""
    
    # Adiciona tabela de resultados
    relatorio += "| Instância | Cidades | Melhor Distância | Ótimo Conhecido | Erro (%) | Tempo (s) |\n"
    relatorio += "|-----------|---------|------------------|-----------------|----------|----------|\n"
    
    for resultado in resultados:
        nome, distancia, erro, _, tempo, num_cidades = resultado
        # Valores ótimos conhecidos
        valores_otimos = {
            "burma14": 3323,
            "ulysses16": 6859,
            "berlin52": 7542,
            "kroA100": 21282,
            "pcb442": 50778
        }
        otimo = valores_otimos.get(nome, "N/A")
        erro_str = f"{erro:.2f}" if erro is not None else "N/A"
        
        relatorio += f"| {nome} | {num_cidades} | {distancia:.2f} | {otimo} | {erro_str} | {tempo:.2f} |\n"
    
   
    # Adiciona análise para cada instância
    for resultado in resultados:
        nome, distancia, erro, historico, tempo, num_cidades = resultado
        
        # Análise simplificada da convergência
        melhoria_inicial = historico[0] - historico[9]
        melhoria_final = historico[9] - historico[-1]
        percentual_melhoria_inicial = (melhoria_inicial / historico[0]) * 100
        percentual_melhoria_final = (melhoria_final / historico[9]) * 100
        
        relatorio += f"**{nome} ({num_cidades} cidades)**:\n\n"
        relatorio += f"- Distância inicial: {historico[0]:.2f}\n"
        relatorio += f"- Distância final: {distancia:.2f}\n"
        relatorio += f"- Melhoria nas primeiras 10 gerações: {melhoria_inicial:.2f} ({percentual_melhoria_inicial:.2f}%)\n"
        relatorio += f"- Melhoria nas gerações restantes: {melhoria_final:.2f} ({percentual_melhoria_final:.2f}%)\n"
        
        if percentual_melhoria_inicial > percentual_melhoria_final:
            relatorio += "- A convergência foi mais rápida no início e desacelerou nas gerações posteriores.\n\n"
        else:
            relatorio += "- A convergência foi mais gradual, com melhorias significativas mesmo em gerações avançadas.\n\n"
    
    # Adiciona análise do tempo de execução
    tempos = [resultado[4] for resultado in resultados]
    tamanhos = [resultado[5] for resultado in resultados]
    
    # Calcula a proporção de aumento
    if len(tempos) >= 3:
        proporcao_tempo = tempos[2] / tempos[0]
        proporcao_tamanho = tamanhos[2] / tamanhos[0]
        
        relatorio += f"- O tempo de execução aumentou {proporcao_tempo:.2f}x ao passar de {tamanhos[0]} para {tamanhos[2]} cidades.\n"
        relatorio += f"- O número de cidades aumentou {proporcao_tamanho:.2f}x.\n"
        
        if proporcao_tempo > proporcao_tamanho:
            relatorio += "- O crescimento do tempo é superlinear em relação ao tamanho da instância, o que é esperado para problemas NP-difíceis como o TSP.\n\n"
        else:
            relatorio += "- O algoritmo demonstrou boa escalabilidade, com crescimento do tempo próximo ao linear em relação ao tamanho da instância.\n\n"
    
    
    # Salva o relatório em um arquivo
    nome_arquivo = "relatorio_tsp_genetico.md"
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write(relatorio)
    
    print(f"Relatório detalhado salvo como {nome_arquivo}")
    return nome_arquivo

def main():
    # Lista de instâncias a serem executadas
    instancias = ["burma14.tsp", "kroA100.tsp", "pcb442.tsp"]
    
    # Parâmetros do algoritmo
    TAMANHO_POPULACAO = 50
    NUM_GERACOES = 100
    TAXA_CROSSOVER = 0.8
    TAXA_MUTACAO = 0.05
    TAMANHO_ELITISMO = 2
    SEMENTE = 42
    
    # Armazena resultados para cada instância
    resultados = []
    nomes_instancias = []
    tempos_execucao = []
    tamanhos_instancias = []
    
    # Executa o algoritmo para cada instância
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
        
        if resultado[0]:  # Se a execução foi bem-sucedida
            resultados.append(resultado)
            nomes_instancias.append(resultado[0])
            tempos_execucao.append(resultado[4])
            tamanhos_instancias.append(resultado[5])
    
    # Gera o gráfico de comparação de tempo de execução
    if len(nomes_instancias) > 1:
        gerar_grafico_tempo_execucao(nomes_instancias, tempos_execucao, tamanhos_instancias)
    
    # Gera o relatório detalhado
    if resultados:
        relatorio = gerar_relatorio(resultados)
        print(f"\nProcesso concluído! Foram gerados:")
        print(f"- Gráficos de convergência para cada instância")
        print(f"- Gráfico comparativo de tempo de execução")
        print(f"- Relatório detalhado: {relatorio}")
    else:
        print("Não foi possível gerar o relatório pois nenhuma instância foi executada com sucesso.")

if __name__ == "__main__":
    main()
