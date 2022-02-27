#METHOD 2

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

weights = []
sigmas = [1,2,4]
gammas = [1,1e-2,1e-4,1e-8,1e-10]

train_eg = 1000
test_eg = 100

m = min(train_X.shape[0],train_eg)
for sigma in sigmas:
  for gamma in gammas:
    gram_matrix = np.zeros((m,m))
    for i in range(m):
      #print(i)
      for j in range(m):
        gram_matrix[i, j] = K(train_X[i], train_X[j], sigma)
    for k in range(10):
      print(k)
      y_tr = np.ones_like(train_y)
      y_tr[np.where(train_y != k)[0]] = -1
      cur_weight = np.linalg.solve(m*gamma*np.identity(m) + gram_matrix, y_tr[0:m])
      weights.append((cur_weight, sigma, gamma))

for idx in range(20):
  print(idx)
  preds = []
  for k in range(10):
    n = test_eg # no. of test examples
    predicted_vals = []
    #print(19*idx + k)
    curr_weight = weights[10*idx + k][0]
    sigma = weights[10*idx + k][1]
    for i in range(n):
      x = test_X[i]
      temp = np.zeros(m)
      for j in range(m):
        temp[j] = K(train_X[j], x, sigma)
      regression_val = np.dot(curr_weight, temp)
      predicted_vals.append(regression_val)
    preds.append(predicted_vals)
  y_hat = np.array(preds)
  pred_arr = np.argmax(y_hat, axis = 0)
  acc = np.sum(pred_arr == test_y[0:n])
  print(acc)