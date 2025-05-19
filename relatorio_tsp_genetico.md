# Relat�rio: Algoritmo Gen�tico para o Problema do Caixeiro Viajante

Foram utilizadas tr�s inst�ncias do TSPLIB com diferentes tamanhos:

- **burma14**: 14 cidades
- **kroA100**: 100 cidades
- **pcb442**: 442 cidades

## 3. Par�metros do Algoritmo

Os seguintes par�metros foram utilizados em todas as execu��es:

- Tamanho da Popula��o: 50 indiv�duos
- N�mero de Gera��es: 100
- Taxa de Crossover: 0.8 (80%)
- Taxa de Muta��o: 0.05 (5%)
- Tamanho do Elitismo: 2 indiv�duos
- Semente Aleat�ria: 42 (para reprodutibilidade)

## 4. Resultados Obtidos

### 4.1 Qualidade das Solu��es

| Inst�ncia | Cidades | Melhor Dist�ncia | �timo Conhecido | Erro (%) | Tempo (s) |
|-----------|---------|------------------|-----------------|----------|----------|
| burma14 | 14 | 3346.00 | 3323 | 0.69 | 0.48 |
| kroA100 | 100 | 115120.00 | 21282 | 440.93 | 2.07 |
| pcb442 | 442 | 677410.00 | 50778 | 1234.06 | 9.70 |
**burma14 (14 cidades)**:

- Dist�ncia inicial: 4849.00
- Dist�ncia final: 3346.00
- Melhoria nas primeiras 10 gera��es: 792.00 (16.33%)
- Melhoria nas gera��es restantes: 711.00 (17.53%)
- A converg�ncia foi mais gradual, com melhorias significativas mesmo em gera��es avan�adas.

**kroA100 (100 cidades)**:

- Dist�ncia inicial: 149020.00
- Dist�ncia final: 115120.00
- Melhoria nas primeiras 10 gera��es: 10930.00 (7.33%)
- Melhoria nas gera��es restantes: 22970.00 (16.63%)
- A converg�ncia foi mais gradual, com melhorias significativas mesmo em gera��es avan�adas.

**pcb442 (442 cidades)**:

- Dist�ncia inicial: 731168.00
- Dist�ncia final: 677410.00
- Melhoria nas primeiras 10 gera��es: 10801.00 (1.48%)
- Melhoria nas gera��es restantes: 42957.00 (5.96%)
- A converg�ncia foi mais gradual, com melhorias significativas mesmo em gera��es avan�adas.

- O tempo de execu��o aumentou 20.17x ao passar de 14 para 442 cidades.
- O n�mero de cidades aumentou 31.57x.
- O algoritmo demonstrou boa escalabilidade, com crescimento do tempo pr�ximo ao linear em rela��o ao tamanho da inst�ncia.



## 6. Refer�ncias

- TSPLIB: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
- Valores �timos para inst�ncias sim�tricas: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/STSP.html
