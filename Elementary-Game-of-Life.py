from numpy import random as rand
import random
import matplotlib.pyplot as plt



def convert_to_index(neighborhood):
    temp = 0
    for i in range(len(neighborhood)):
        if neighborhood[i]:
            temp += 2**i
    return temp



def update_board(board, rules):
    newBoard = [0]*boardSize
    for i in range(boardSize):
        temp = (neighborhoodSize - 1)/2
        a=int(i-temp)
        b=int(i + temp)
        if a < 0:
            neighborhood = board[a:]
            neighborhood.extend(board[:b+1])
        elif b > len(board)-1:
            neighborhood = board[a:]
            neighborhood.extend(board[:b-(len(board)-1)])
        else:
            neighborhood = board[a:b+1]
        index = convert_to_index(neighborhood)
        newBoard[i] = rules[index]
    return newBoard


def initialize_agents(numAgents):
    agents = [0]*numAgents
    for i in range(numAgents):
        agents[i] = [random.randint(0,1) for _ in range(2**neighborhoodSize)]
    return agents

def calculate_fitness(agents, numTrials, trialLength):
    fitness = [0]*len(agents)
    for count, agent in enumerate(agents):
        successes = 0
        for _ in range(numTrials):
            board = [random.randint(0,1) for _ in range(boardSize)]
            initialBoard = sum(board)
            for __ in range(trialLength):
                temp = update_board(board, agent)
                if board==temp:
                    break
                board=temp
            if (initialBoard > boardSize/2 and sum(board) == boardSize) or (initialBoard < boardSize/2 and sum(board) == 0):
                successes += 1
        fitness[count] = successes/numTrials
    return fitness

def select_parents(agents, fitness, numParents, punchersChance):
    parents = []
    for _ in range(numParents):
        ##Tournament Selection
        # competitor1 = random.randint(0, len(agents)-1)
        # competitor2 = random.randint(0, len(agents)-1)
        # if fitness[competitor1] >= fitness[competitor2]:
        #     if rand.uniform(0,1) > punchersChance:
        #         parents.append(agents[competitor1])
        #     else:
        #         parents.append(agents[competitor2])

        #Elitism
        currMax = fitness.index(max(fitness))
        parents.append(agents[currMax])
        fitness[currMax]=0
    return parents

def mate(parent1, parent2, mutationRate):
    crossoverPoint = random.randint(0, len(parent1)-1)
    child = parent1[:crossoverPoint]
    child.extend(parent2[crossoverPoint:])
    for count, gene in enumerate(child):
        if rand.uniform(0,1)<mutationRate:
            if gene == 0:
                child[count]=1
            else: 
                child[count]=0
    return child

def create_next_generation(parents, numAgents, mutationRate):
    children = parents
    for i in range(len(parents), numAgents):
        children.append(mate(random.choice(parents), random.choice(parents), mutationRate))
    return children


   
boardSize=29
neighborhoodSize=7
numAgents=100
numGenerations=300
numTrials = 100
trialLength = 60


def evolve(numParents, punchersChance, mutationRate):
    avgFitnesses=[]
    agents = initialize_agents(numAgents)
    fitness = calculate_fitness(agents, numTrials, trialLength)
    bestAgent=agents[fitness.index(max(fitness))]
    bestFitness = max(fitness)
    for _ in range(numGenerations):
        print("Generation "+str(_)+":\n")
        fitness = calculate_fitness(agents, numTrials, trialLength)
        avgFitnesses.append(sum(fitness)/len(fitness))
        maxFitness = max(fitness)
        if maxFitness>bestFitness:
            bestFitness=maxFitness
            bestAgent=agents[fitness.index(maxFitness)]
        # print("Average Fitness: "+str(sum(fitness)/len(fitness))+"\n")
        # print("Max Fitness: "+str(maxFitness)+"\n")
        parents = select_parents(agents, fitness, numParents, punchersChance)
        agents = create_next_generation(parents, numAgents, mutationRate)

    print("Best Agent Achieved: " + str(bestAgent))
    print("\nAgent Fitness: "+str(maxFitness))
    board = [random.randint(0,1) for _ in range(boardSize)]
    history=[]
    history.append(board)
    for x in range(50):
        board = update_board(board, bestAgent)
        history.append(board)
    plt.imshow(history)
    plt.show()
    return avgFitnesses


# evolTrajectory=evolve(25, 0, 0.04)

# plt.plot(evolTrajectory)
# plt.xlabel('Generations')
# plt.ylabel('Average Fitness')
# plt.title("Elitism Selection with 25 Parents, Population 100, Mutation Rate 0.04")
# plt.savefig('bigBoardGraph')
# plt.show()
    
board = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
history=[]
history.append(board)
for x in range(50):
    board = update_board(board, [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 
0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1])
    history.append(board)
plt.imshow(history)
plt.show()



# numParents = 10
# punchersChance = 0.2
# mutationRate=0
# evolTrajectories = []
# for x in range(5):
#     print("trial "+str(x+1)+" of 5 of mutation rate")
#     evolTrajectories.append(evolve(numParents, punchersChance, mutationRate))
#     mutationRate += 0.01

# for count, evolTrajectory in enumerate(evolTrajectories):
#     plt.plot(evolTrajectory, label=str(count*0.05))
#     plt.xlabel('Generations')
#     plt.ylabel('Average Fitness')
#     plt.title("Mutation Rates with Parents=10, PC=0.2")
# plt.savefig('mutationRatesGraph')
# plt.close()


# evolTrajectories = []
# numParents = 0
# punchersChance = 0.2
# mutationRate=0.04
# for x in range(5):
#     print("trial "+str(x+1)+" of 4 of parents")
#     numParents += 5
#     evolTrajectories.append(evolve(numParents, punchersChance, mutationRate))

# for count, evolTrajectory in enumerate(evolTrajectories):
#     plt.plot(evolTrajectory, label=str((1+count)*5))
#     plt.xlabel('Generations')
#     plt.ylabel('Average Fitness')
#     plt.title("Number of Parents with PC=0.2, MR=0.05")
# plt.savefig('numParentsGraph')
# plt.close()

# evolTrajectories = []
# numParents = 10
# punchersChance = 0
# mutationRate=0.05
# for x in range(5):
#     print("trial "+str(x+1)+" of 5 of punchers chance")
#     evolTrajectories.append(evolve(numParents, punchersChance, mutationRate))
#     punchersChance += 0.05

# for count, evolTrajectory in enumerate(evolTrajectories):
#     plt.plot(evolTrajectory, label=str(count*.05))
#     plt.xlabel('Generations')
#     plt.ylabel('Average Fitness')
#     plt.title("Puncher's Chance with Parents=10, MR=0.05")
# plt.savefig('punchersChanceGraph')
# plt.close()
