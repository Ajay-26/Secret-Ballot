import tensorflow as tf
from tensorflow import keras
from keras.datasets import mnist
import numpy as np

def K(x, y, sigma):
  return np.exp(-1*np.square(np.linalg.norm(x-y))/(2.0*sigma*sigma))

(train_X, train_y), (test_X, test_y) = tf.keras.datasets.mnist.load_data()
train_X = train_X.astype(int)
train_y = train_y.astype(int)
test_X = test_X.astype(int)
test_y = test_y.astype(int)

train_X = np.reshape(train_X,[-1,784])/255.0
test_X = np.reshape(test_X,[-1,784])/255.0

sigmas = [1,2,4]
gammas = [1,1e-2,1e-4,1e-8,1e-10]

train_eg = 1000
test_eg = 100

m = min(train_X.shape[0],train_eg)
weights = []
for sigma in sigmas:
  for gamma in gammas:
    print((sigma,gamma))
    gram_matrix = np.zeros((m,m))
    for i in range(m):
      #print(i)
      for j in range(m):
        gram_matrix[i, j] = K(train_X[i], train_X[j], sigma)
    cur_weight = np.linalg.solve(m*gamma*np.identity(m) + gram_matrix, train_y[0:m])
    #cur_weight = np.dot(np.linalg.inv(m*gamma*np.identity(m) + gram_matrix), train_y[0:m])
    weights.append((cur_weight, sigma, gamma))

    n = m # no. of test examples
    predicted_vals = []
    for i in range(n):
      x = train_X[i]
      temp = np.zeros(m)
      for j in range(m):
        temp[j] = K(train_X[j], x, sigma)
      #print(x)
      regression_val = np.dot(cur_weight, temp)
      #print(regression_val)
      up = (np.ceil(regression_val))
      down = (np.floor(regression_val))
      if (regression_val-down < up - regression_val):
        predicted_vals.append((int(down),train_y[i]))
      else:
        predicted_vals.append((int(up),train_y[i]))
    y_hat = np.array(predicted_vals)
    acc = np.sum(y_hat[:,0] == y_hat[:,1])
    print(acc)

n = test_eg # no. of test examples
for weight in weights:
  predicted_vals = []
  cur_weight = weight[0]
  sigma = weight[1]
  for i in range(n):
    x = test_X[i]
    temp = np.zeros(m)
    for j in range(m):
      temp[j] = K(train_X[j], x, sigma)
    #print(x)
    regression_val = np.dot(cur_weight, temp)
    up = (np.ceil(regression_val))
    down = (np.floor(regression_val))
    if (regression_val-down < up - regression_val):
      predicted_vals.append((int(down),test_y[i]))
    else:
      predicted_vals.append((int(up),test_y[i]))
  y_hat = np.array(predicted_vals)
  acc = np.sum(y_hat[:,0] == y_hat[:,1])
  print(acc)
