import copy

characters=["A","B","C","D","E","J","K"]

A = []
B = []
C = []
D = []
E = []
J = []
K = []


weight=[]
b = []
target = [[1,-1,-1,-1,-1,-1,-1], # A
          [-1, 1, -1, -1, -1, -1, -1], #B
          [-1, -1, 1, -1, -1, -1, -1], #C
          [-1, -1, -1, 1, -1, -1, -1], #D
          [-1, -1, -1, -1, 1, -1, -1], #E
          [-1, -1, -1, -1, -1, 1, -1], #J
          [-1, -1, -1, -1, -1, -1, 1]] #K

alpha=0.9
teta=0

def initInputs():
    global A,B,C,D,E,J,K
    A.clear()
    B.clear()
    C.clear()
    D.clear()
    E.clear()
    J.clear()
    K.clear()

    A=[[],[],[]]
    B=[[],[],[]]
    C=[[],[],[]]
    D=[[],[],[]]
    E=[[],[],[]]
    J=[[],[],[]]
    K=[[],[],[]]


def initWeights():
    global weight
    global b
    weight.clear()
    b.clear()
    b=[1,1,1,1,1,1,1]
    weight = [[], [], [], [], [], [], []]
    for i in range(len(weight)):
        for j in range(0,64):
            weight[i].append(0.1)


def convertInputToBipolar(input):
    bipolarInpuit=[]
    for i in range(len(input)):
        if input[i]=="#":
            bipolarInpuit.append(1)
        elif input[i]==".":
            bipolarInpuit.append(-1)
        elif input[i] =="@":
            bipolarInpuit.append(0)
        elif input[i] == "o":
            bipolarInpuit.append(0)
    return  bipolarInpuit


def loadInputData(trainOrTest):
    initInputs()
    A[0] = open(trainOrTest + '/A1.txt').read().replace("\n","")
    A[1] = open(trainOrTest + '/A2.txt').read().replace("\n","")
    A[2] = open(trainOrTest + '/A3.txt').read().replace("\n","")
    B[0] = open(trainOrTest + '/B1.txt').read().replace("\n","")
    B[1] = open(trainOrTest + '/B2.txt').read().replace("\n","")
    B[2] = open(trainOrTest + '/B3.txt').read().replace("\n","")
    C[0] = open(trainOrTest + '/C1.txt').read().replace("\n","")
    C[1] = open(trainOrTest + '/C2.txt').read().replace("\n","")
    C[2] = open(trainOrTest + '/C3.txt').read().replace("\n","")
    D[0] = open(trainOrTest + '/D1.txt').read().replace("\n","")
    D[1] = open(trainOrTest + '/D2.txt').read().replace("\n","")
    D[2] = open(trainOrTest + '/D3.txt').read().replace("\n","")
    E[0] = open(trainOrTest + '/E1.txt').read().replace("\n","")
    E[1] = open(trainOrTest + '/E2.txt').read().replace("\n","")
    E[2] = open(trainOrTest + '/E3.txt').read().replace("\n","")
    J[0] = open(trainOrTest + '/J1.txt').read().replace("\n","")
    J[1] = open(trainOrTest + '/J2.txt').read().replace("\n","")
    J[2] = open(trainOrTest + '/J3.txt').read().replace("\n","")
    K[0] = open(trainOrTest + '/K1.txt').read().replace("\n","")
    K[1] = open(trainOrTest + '/K2.txt').read().replace("\n","")
    K[2] = open(trainOrTest + '/K3.txt').read().replace("\n","")


def convertAllInputsToBipolar():
    for i in range(len(A)):
        A[i] = convertInputToBipolar(A[i])
        B[i] = convertInputToBipolar(B[i])
        C[i] = convertInputToBipolar(C[i])
        D[i] = convertInputToBipolar(D[i])
        E[i] = convertInputToBipolar(E[i])
        J[i] = convertInputToBipolar(J[i])
        K[i] = convertInputToBipolar(K[i])
    return  1


def activationFunction(y_in,teta):
    Y=0
    if y_in > teta:
        Y=1
    elif (-1*teta)<=y_in<=teta:
        Y=0
    elif y_in<-teta:
        Y=-1
    return Y

epoch=0

def trainNetwork(inputVector,target):
    initWeights()
    global epoch
    global weight
    global alpha
    epoch=0
    weightsVector=weight
    y_in=0
    Y=[]

    stoppingCondition = False

    while stoppingCondition==False :
        weightsHistory=[]
        if epoch%5 == 0:
            alpha=alpha/2
        for sampleNo in range(len(inputVector)):
            sumXiWi=0
            Y.clear()
            for j in range(len(target)):
                    sumXiWi = 0
                    for i in range(len(inputVector[sampleNo])):
                        sumXiWi += inputVector[sampleNo][i]*weight[j][i]
                    y_in = b[j]+sumXiWi
                    Y.append(activationFunction(y_in,teta))

            for k in range(len(target[int(sampleNo/3)])):
                    if Y[k] != target[int(sampleNo/3)][k]:
                        b[k]+= alpha*(target[int(sampleNo/3)][k] - Y[k])
                        for i in range(len(inputVector[sampleNo])):
                            weight[k][i] +=  (alpha * (target[int(sampleNo / 3)][k] -Y[k] ) * inputVector[sampleNo][i])
                            weightsHistory.append((alpha * (target[int(sampleNo / 3)][k] -Y[k] ) * inputVector[sampleNo][i]))

        epoch += 1
        if len(weightsHistory)!=0:
            if max(weightsHistory) <0.02:
               stoppingCondition=True;
        else:
            stoppingCondition=True

    return weight


def testNetwork(input,weights,b,inputCharacter):
    sumXiWi=0
    Y=[]
    y_in=[]
    flag=True
    for j in range(len(target)):
        sumXiWi=0
        for i in range(len(input)):
            sumXiWi += input[i] * weights[j][i]

        y_in.append(b[j] + sumXiWi)
        Y.append(activationFunction(y_in[j], teta))
    countOne=0
    indexOfOnes=[]
    for j in range(len(Y)):
            if Y[j] == 1:
                countOne+=1
                indexOfOnes.append(j)

    if len(indexOfOnes) == 1:
        if characters[indexOfOnes[0] == inputCharacter]:
            return True
        else:
            return  False
    else:
        if len(indexOfOnes)  > 1 :
            max = y_in[indexOfOnes[0]]
            maxIndex = 0
            for k in range(len(indexOfOnes)):
                if abs(y_in[indexOfOnes[k]] - teta)>= max:
                    maxIndex =indexOfOnes[k]
            try:
                if characters[maxIndex]==inputCharacter:
                    return True
                else:
                    return False
            except:
                print(inputCharacter + " ---" + str(min))

    return False



def totalTest():
    numberOfTrue=0
    numberOfFalse=0
    for i in range (len(A)):
        if testNetwork(A[i], finalWeights, finalBias, "A"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

        if testNetwork(B[i], finalWeights, finalBias, "B"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

        if testNetwork(C[i], finalWeights, finalBias, "C"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

        if testNetwork(D[i], finalWeights, finalBias, "D"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

        if testNetwork(E[i], finalWeights, finalBias, "E"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

        if testNetwork(J[i], finalWeights, finalBias, "J"):
            numberOfTrue += 1
        else:
            numberOfFalse += 1

        if testNetwork(K[i], finalWeights, finalBias, "K"):
            numberOfTrue+=1
        else:
            numberOfFalse+=1

    errorRate = (numberOfFalse / (21)) * 100
    return errorRate


loadInputData("train_input")
convertAllInputsToBipolar()

input=[A[0],A[1],A[2],B[0],B[1],B[2],C[0],C[1],C[2],D[0],D[1],D[2],E[0],E[1],E[2],J[0],J[1],J[2],K[0],K[1],K[2]]
finalWeights = copy.deepcopy(trainNetwork(input, target))
finalBias=copy.deepcopy(b)

print("Error rate with training data : ")
print(totalTest())

print(epoch)

loadInputData("test_input")
convertAllInputsToBipolar()

print("\n Error rate with test data : ")
print(totalTest())
