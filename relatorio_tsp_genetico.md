# Relatório: Algoritmo Genético para o Problema do Caixeiro Viajante

Foram utilizadas três instâncias do TSPLIB com diferentes tamanhos:

- **burma14**: 14 cidades
- **kroA100**: 100 cidades
- **pcb442**: 442 cidades

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

| Instância | Cidades | Melhor Distância | Ótimo Conhecido | Erro (%) | Tempo (s) |
|-----------|---------|------------------|-----------------|----------|----------|
| burma14 | 14 | 3346.00 | 3323 | 0.69 | 0.48 |
| kroA100 | 100 | 115120.00 | 21282 | 440.93 | 2.07 |
| pcb442 | 442 | 677410.00 | 50778 | 1234.06 | 9.70 |
**burma14 (14 cidades)**:

- Distância inicial: 4849.00
- Distância final: 3346.00
- Melhoria nas primeiras 10 gerações: 792.00 (16.33%)
- Melhoria nas gerações restantes: 711.00 (17.53%)
- A convergência foi mais gradual, com melhorias significativas mesmo em gerações avançadas.

**kroA100 (100 cidades)**:

- Distância inicial: 149020.00
- Distância final: 115120.00
- Melhoria nas primeiras 10 gerações: 10930.00 (7.33%)
- Melhoria nas gerações restantes: 22970.00 (16.63%)
- A convergência foi mais gradual, com melhorias significativas mesmo em gerações avançadas.

**pcb442 (442 cidades)**:

- Distância inicial: 731168.00
- Distância final: 677410.00
- Melhoria nas primeiras 10 gerações: 10801.00 (1.48%)
- Melhoria nas gerações restantes: 42957.00 (5.96%)
- A convergência foi mais gradual, com melhorias significativas mesmo em gerações avançadas.

- O tempo de execução aumentou 20.17x ao passar de 14 para 442 cidades.
- O número de cidades aumentou 31.57x.
- O algoritmo demonstrou boa escalabilidade, com crescimento do tempo próximo ao linear em relação ao tamanho da instância.



## 6. Referências

- TSPLIB: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
- Valores ótimos para instâncias simétricas: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/STSP.html
