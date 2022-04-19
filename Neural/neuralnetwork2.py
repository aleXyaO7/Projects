def hadamard(v1, v2):
    return [v1[i]*v2[i] for i in range(len(v1))]

def dot(v1, v2):
    return sum(hadamard(v1, v2))

def sigmoid(x):
    return 
