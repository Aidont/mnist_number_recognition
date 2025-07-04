# -*- coding: utf-8 -*-
"""MNIST number recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pJ5YtImBEk-qngWYmnLolajOOBsvv4bU
"""

import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader

"""The next part only works if you have a training csv file stored in a folder MNIST in your drive."""

data = pd.read_csv('drive/MyDrive/MNIST/mnist_train.csv')

data = torch.tensor(data.values, dtype=torch.float32)

Y_training = data[:,0]
X_training = data[:,1:]/255

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dataset = TensorDataset(X_training, Y_training)
training_sets = DataLoader(dataset, 64, True)

m, n = X_training.size()

def make_param(*shape):
  return torch.normal(0.01, 0.03, size=shape, device = device, requires_grad = True)

lr = 0.01

hidden1 = 20
hidden2 = 20


w1 = make_param(n, hidden1)
w2 = make_param(hidden1, hidden2)
w3 = make_param(hidden2, 10)

b1 = make_param(hidden1, )
b2 = make_param(hidden2, )
b3 = make_param(10, )

def model(x):
  l1 = x@w1 +b1
  l1 = torch.relu(l1)
  l2 = l1@w2 + b2
  l2 = torch.relu(l2)
  l3 = l2@w3 + b3
  return l3

loss = torch.nn.CrossEntropyLoss()

def update():
  global w1, w2, w3, b1, b2, b3

  with torch.no_grad():
    w1 -= lr*w1.grad
    w2 -= lr*w2.grad
    w3 -= lr*w3.grad
    b1 -= lr*b1.grad
    b2 -= lr*b2.grad
    b3 -= lr*b3.grad

  w1.grad.zero_()
  w2.grad.zero_()
  w3.grad.zero_()
  b1.grad.zero_()
  b2.grad.zero_()
  b3.grad.zero_()

for i in range(10):
  for img_data, label in training_sets:
    img_data = img_data.to(device)
    label = label.to(device)

    logits = model(img_data)
    l = loss(logits, label.long())
    l.backward()
    update() # Call update function

  print(l.item())

test_data = pd.read_csv('drive/MyDrive/MNIST/mnist_test.csv')

test_data = torch.tensor(test_data.values, dtype=torch.float32)

Y_test = test_data[:, 0]
X_test = test_data[:, 1:]/255

X_test.size()

test_data = TensorDataset(X_test, Y_test)
test_sets = DataLoader(test_data, 64, False)

correct = 0
total = 0
for img_data, label in test_sets:
  img_data = img_data.to(device)
  label = label.to(device)
  pred = torch.argmax(model(img_data), dim = 1)
  correct += (pred==label).sum().item()

  total += label.size(0)

print((correct/total)*100)
print(total, correct)

