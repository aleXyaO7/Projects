import numpy as np
import pandas as pd

df = pd.read_csv('Data.csv')
x = df[['Glucose','BloodPressure']]
y = df['Outcome']

def sigmoid(input):    
    output = 1 / (1 + np.exp(-input))
    return output

def sigmoid_derivative(input):
    return sigmoid(input) * (1.0 - sigmoid(input))

def train_network(features,label,weights,bias,learning_rate,epochs):                                         
    for epoch in range(epochs):
        dot_prod = np.dot(features, np.transpose(*weights)) + bias
        preds = sigmoid(dot_prod)
        errors = preds - label                
        deriva_cost_funct = errors
        deriva_preds = sigmoid_derivative(preds)
        deriva_product = deriva_cost_funct * deriva_preds
        weights = weights -  np.dot(features, deriva_product) * learning_rate        
        loss = errors.sum()
    for i in deriva_product:
        bias = bias -  i * learning_rate

np.random.seed(10)
features  = x
label = y.values.reshape(y.shape[0],1)
weights = np.random.rand(2,1)
bias = np.random.rand(1)
learning_rate = 0.0000004
epochs = 100
weights_final, bias_final = train_network(features,label,weights,bias,learning_rate,epochs)

inputs = [[86,104]]
dot_prod = np.dot(inputs, weights_final) + bias_final
preds = sigmoid(dot_prod) >= 1/2
print(preds)