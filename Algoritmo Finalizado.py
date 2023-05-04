import random

# Define o tamanho da chapa de metal
CHAPA_COMPRIMENTO = 600
CHAPA_LARGURA = 300

# Define as peças de metal (comprimento, largura)
#PECAS = [(50, 100), (75, 150), (100, 200), (125, 250), (600, 200)]
#PECAS = [(50, 100), (50, 100),  (75, 150), (100, 200), (125, 250), (300, 100), (300, 100)]
PECAS = [(70, 20), (50, 100),  (75, 150), (100, 10), (125, 250), (50, 20), (50, 20), (50, 10), (70, 30), (50, 10), (50, 25), (50, 70), (100, 40)]
#PECAS = [(10, 14), (12, 20),  (5, 16), (17, 9), (10, 10), (25, 25), (35, 70), (90, 100), (10, 50), (35, 35), (47, 50), (40, 40), (2, 1), (1, 2), (25, 25), (20, 10), (15, 25), (37, 37), (40, 40), (65, 65)]

# Define o número de indivíduos na população
POPULACAO = 500

# Define o número de gerações
GERACOES = 100

# Define a classe Individuo para representar um indivíduo da população
class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.avaliar()
    
    def avaliar(self):
        # Calcula o comprimento e largura total das peças selecionadas
        comprimento_total = sum([PECAS[i][0] for i in range(len(PECAS)) if self.genes[i] == 1])
        largura_total = sum([PECAS[i][1] for i in range(len(PECAS)) if self.genes[i] == 1])
        
        # Verifica se o comprimento e largura total das peças selecionadas não ultrapassam o tamanho da chapa de metal
        if comprimento_total <= CHAPA_COMPRIMENTO and largura_total <= CHAPA_LARGURA:
            # Retorna o valor da função objetivo (área total das peças selecionadas)
            return comprimento_total * largura_total
        else:
            # Retorna um valor baixo para penalizar soluções inválidas
            return 0

# Define a função para gerar um gene aleatório (0 ou 1)
def gene_aleatorio():
    return random.randint(0, 1)

# Define a função para criar um indivíduo
def criar_individuo():
    return Individuo([gene_aleatorio() for _ in range(len(PECAS))])

# Define a função para criar a população inicial
def criar_populacao():
    return [criar_individuo() for _ in range(POPULACAO)]

# Define a função para selecionar os pais para reprodução (seleção por torneio)
def selecionar(populacao):
    pais = []
    for _ in range(len(populacao)):
        competidores = random.sample(populacao, 3)
        competidores.sort(key=lambda ind: ind.fitness, reverse=True)
        pais.append(competidores[0])
    return pais

# Define a função para aplicar o cruzamento em dois indivíduos (cruzamento de dois pontos)
def cruzar(filho1, filho2):
    ponto1 = random.randint(1, len(filho1.genes) - 2)
    ponto2 = random.randint(ponto1 + 1, len(filho1.genes) - 1)
    filho1.genes[ponto1:ponto2], filho2.genes[ponto1:ponto2] = filho2.genes[ponto1:ponto2], filho1.genes[ponto1:ponto2]

# Define a função para aplicar a mutação em um indivíduo (mutação por bit flip)
def mutar(mutante):
    for i in range(len(mutante.genes)):
        if random.random() < 0.05:
            mutante.genes[i] = 1 - mutante.genes[i]

# Cria a população inicial
populacao = criar_populacao()

# Executa o algoritmo genético por GERACOES gerações
for g in range(GERACOES):
    # Seleciona os pais para reprodução
    pais = selecionar(populacao)
    
    # Clona os pais selecionados
    pais = [Individuo(pai.genes[:]) for pai in pais]
    
    # Aplica o cruzamento nos pais selecionados (em pares)
    for filho1, filho2 in zip(pais[::2], pais[1::2]):
        if random.random() < 0.5:
            cruzar(filho1, filho2)
    
    # Aplica a mutação nos filhos gerados
    for mutante in pais:
        if random.random() < 0.2:
            mutar(mutante)
    
    # Avalia os filhos gerados que sofreram mutação ou cruzamento
    for filho in pais:
        filho.fitness = filho.avaliar()
    
    # Substitui a população atual pela nova geração de filhos
    populacao = pais

# Imprime o melhor indivíduo encontrado (solução ótima)
melhor_individuo = max(populacao, key=lambda ind: ind.fitness)
print(f"Melhor Indivíduo: {melhor_individuo.genes}")
print(f"Valor da Função Objetivo: {melhor_individuo.fitness}")

# Calcula a área total da chapa de metal
area_chapa = CHAPA_COMPRIMENTO * CHAPA_LARGURA

# Calcula a área desperdiçada
area_desperdicada = area_chapa - melhor_individuo.fitness

# Calcula o percentual de aproveitamento da chapa
percentual_aproveitamento = (melhor_individuo.fitness / area_chapa) * 100

# Imprime as informações
print(f"Área Total da Chapa: {area_chapa}")
print(f"Área Total das Peças Selecionadas: {melhor_individuo.fitness}")
print(f"Área Desperdiçada: {area_desperdicada}")
print(f"Percentual de Aproveitamento: {percentual_aproveitamento:.2f}%")