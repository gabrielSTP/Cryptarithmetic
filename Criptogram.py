import random
import sys

def runIt(numVec, generations, muteRate):
    w1, w2, w3, unigram, size, cross, parent = recive()  # Função que recebe entrada do teclado
    vectors = generateVectors(numVec, size)
    
    # A partir daqui, o output será redirecionado para o arquivo
    original_stdout = sys.stdout  # Salva a referência da saída padrão original
    with open("saida.txt", "w") as f:
        sys.stdout = f  # Redireciona a saída para o arquivo

        if cross == 2:
            print("\n---Base Fitness---\n")
            fitness(vectors, w1, w2, w3, unigram, willPrint=1)
            for i in range(generations):
                mutedVecs = mutationFitness(vectors, muteRate)
                sortedVecs = fitness(mutedVecs, w1, w2, w3, unigram, willPrint=0)
                if parent == 2:
                    pais = torneio(sortedVecs, torneioSize=3)
                    filhos = cycleCrossover(pais, taxaCrossover=0.8)
                    print("\nGeneration Num.", i + 1, "\n")
                    fitness(filhos, w1, w2, w3, unigram, willPrint=1)
                elif parent == 1:
                    pais = roleta(sortedVecs)
                    filhos = cycleCrossover(pais, taxaCrossover=0.8)
                    print("\nGeneration Num.", i + 1, "\n")
                    fitness(filhos, w1, w2, w3, unigram, willPrint=1)
        elif cross == 1:
            print("\n---Base Fitness---\n")
            fitness(vectors, w1, w2, w3, unigram, willPrint=1)
            for i in range(generations):
                mutedVecs = mutationFitness(vectors, muteRate)
                sortedVecs = fitness(mutedVecs, w1, w2, w3, unigram, willPrint=0)
                if parent == 2:
                    pais = torneio(sortedVecs, torneioSize=3)
                    filhos = crossoverPopulation(pais, taxaCrossover=1.0)
                    print("\nGeneration Num.", i + 1, "\n")
                    fitness(filhos, w1, w2, w3, unigram, willPrint=1)
                elif parent == 1:
                    pais = roleta(sortedVecs)
                    filhos = crossoverPopulation(pais, taxaCrossover=1.0)
                    print("\nGeneration Num.", i + 1, "\n")
                    fitness(filhos, w1, w2, w3, unigram, willPrint=1)
    
    sys.stdout = original_stdout  # Restaura a saída padrão original
        
def recive():
    cross = int(input("Qual algoritmo de Crossover?\n 1= PMX\n 2= Ciclico\n "))
    parent = int(input("Qual algoritmo de seleção de pais?\n 1= Roleta\n 2= Torneiro de tamanho 3\n "))
    w1 = input("Digite o Criptograma!\nPrimeira palavra: ")
    w2 = input("Soma: ")
    w3 = input("Resultado: ")
    unigram = generateUnigram(w1, w2, w3)
    size = len(unigram)
    return w1, w2, w3, unigram, size, cross, parent

def generateUnigram(w1, w2, w3):
    join = w1 + w2 + w3
    unigram = ''.join(sorted(set(join), key=join.index))
    if len(unigram) > 10:
        raise ValueError("\033[91mErro: Palavras Inválidas!\033[0m")
    else:
        print("Unigrama: ", unigram)
        return unigram

def identify(w, unigram):
    position = []
    word = [char for char in w if char.isalpha()]
    for letter in word:
        for index, item in enumerate(unigram):
            if letter == item:
                position.append(index)
    return position

def generateVectors(num_vectors, vector_size, num_range=10):
    vectors = []
    for _ in range(num_vectors):
        vector = random.sample(range(num_range), vector_size)
        vectors.append(vector)
    return vectors

def convertToInt(vector, positions):
    selected_digits = [vector[pos] for pos in positions]
    concatenated_str = ''.join(map(str, selected_digits))
    resultInt = int(concatenated_str)
    return resultInt

def mutation(vector):
    vector_copy = vector.copy()
    i, j = random.sample(range(len(vector_copy)), 2)
    vector_copy[i], vector_copy[j] = vector_copy[j], vector_copy[i]
    return vector_copy

def fitness(vectors, w1, w2, w3, unigram, willPrint):
    w1Posi = identify(w1, unigram)
    w2Posi = identify(w2, unigram)
    w3Posi = identify(w3, unigram)

    results = []

    for idx, vector in enumerate(vectors):
        word1 = convertToInt(vector, w1Posi)
        word2 = convertToInt(vector, w2Posi)
        word3 = convertToInt(vector, w3Posi)
        VecFitness = word3 - (word1 + word2)
    
        results.append((VecFitness, vector))
    
    sortedResults = sorted(results, key=lambda x: abs(x[0]))
    for idx, (VecFitness, vector) in enumerate(sortedResults, start=1):
        if willPrint == 1:
            print(f"Vetor {idx}: {vector} Fitness: {VecFitness}")
    
    return sortedResults

def torneio(vetores, torneioSize=3):
    pais_selecionados = []

    for _ in range(len(vetores)):
        competidores = random.sample(vetores, torneioSize)
        melhor = min(competidores, key=lambda x: abs(x[0]))
        pais_selecionados.append(melhor[1])
    return pais_selecionados

def roleta(vetores):
    if not vetores:
        return []
    
    aptidoes, individuos = zip(*vetores)
    aptidao_total = sum(aptidoes)
    probabilidades = [apt / aptidao_total for apt in aptidoes]
    
    # Calcular os limites acumulados para a roleta
    limites_acumulados = []
    acumulado = 0
    for prob in probabilidades:
        acumulado += prob
        limites_acumulados.append(acumulado)
    
    pais_selecionados = []
    for _ in range(len(vetores)):
        r = random.random()
        for i, limite in enumerate(limites_acumulados):
            if r <= limite:
                pais_selecionados.append(individuos[i])
                break
    return pais_selecionados

def mutationFitness(vectors, muteRate):
    muteIndex = []
    muteRate = round((muteRate * len(vectors)) / 100)
    muteIndex = random.sample(range(len(vectors)), muteRate)
    for index in muteIndex:
        vectors[index] = mutation(vectors[index])
    return vectors

def cycleCrossover(pais, taxaCrossover):
    filhos = []

    for i in range(0, len(pais) - 1, 2):
        if random.random() < taxaCrossover:
            pai1 = pais[i]
            pai2 = pais[i + 1]
            filho1 = pai1.copy()
            filho2 = pai2.copy()
            
            ciclo = [0]
            while True:
                idx = ciclo[-1]
                if pai2[idx] in pai1:
                    idx = pai1.index(pai2[idx])
                    if idx in ciclo:
                        break
                    ciclo.append(idx)
                else:
                    break
            
            for idx in ciclo:
                filho1[idx], filho2[idx] = filho2[idx], filho1[idx]
            
            filhos.append(filho1)
            filhos.append(filho2)
        else:
            # Sem crossover, os filhos são cópias dos pais
            filhos.append(pais[i].copy())
            filhos.append(pais[i + 1].copy())
    
    return filhos

def pmxCrossover(parent1, parent2):
    size = len(parent1)
    cx_points = sorted(random.sample(range(size), 2))
    cx_start, cx_end = cx_points[0], cx_points[1]

    child1, child2 = parent1[:], parent2[:]

    mapping1 = {}
    mapping2 = {}

    for i in range(cx_start, cx_end):
        child1[i] = parent2[i]
        child2[i] = parent1[i]
        mapping1[parent2[i]] = parent1[i]
        mapping2[parent1[i]] = parent2[i]

    def repair(child, mapping):
        for i in range(size):
            if i < cx_start or i >= cx_end:
                while child[i] in mapping:
                    child[i] = mapping[child[i]]

    repair(child1, mapping1)
    repair(child2, mapping2)

    return child1, child2

def crossoverPopulation(selected_parents, taxaCrossover):
    next_generation = []
    for i in range(0, len(selected_parents), 2):
        if i+1 < len(selected_parents):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i+1]
            if random.random() < taxaCrossover:
                child1, child2 = pmxCrossover(parent1, parent2)
            else:
                # Sem crossover, os filhos são cópias dos pais
                child1, child2 = parent1[:], parent2[:]
            next_generation.extend([child1, child2])
    return next_generation



muteRate = 5
numVec = 137
genSize = 50
#MAIN
runIt(numVec, genSize, muteRate)