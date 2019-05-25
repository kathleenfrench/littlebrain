# thanks to https://github.com/vzhou842/neural-network-from-scratch/blob/master/network.py
import numpy as np

def sigmoid(x):
  ## activation function : f(x) = 1 / (1 + e^(-x))
  return 1 / (1 + np.exp(-x))

def deriv_sigmoid(x):
  # derivative of sigmoid: f'(x) = f(x) * (1 - f(x))
  fx = sigmoid(x)
  return fx * (1 - fx)

## mean squared error (MSE)
def mse_loss(y_true, y_pred):
  # y_true and y_pred are numpy arrays of the same length
  return ((y_true - y_pred) ** 2).mean()

class Neuron:
  def __init__(self, weights, bias):
    self.weights = weights
    self.bias = bias

  def feed_forward(self, inputs):
    # weight inputs, add bias, then use the activation func
    total = np.dot(self.weights, inputs) + self.bias
    return sigmoid(total)

class NeuralNetwork:
  '''
  a neural network with:
    - 2 inputs
    - a hidden layer with 2 neurons (h1, h2)
    - an output layer with 1 neuron (o1)
  each neuron has the same weights and bias:
    - w = [0, 1]
    - b = 0
  '''
  def __init__(self):
    ## weights
    self.w1 = np.random.normal()
    self.w2 = np.random.normal()
    self.w3 = np.random.normal()
    self.w4 = np.random.normal()
    self.w5 = np.random.normal()
    self.w6 = np.random.normal()

    ## biases
    self.b1 = np.random.normal()
    self.b2 = np.random.normal()
    self.b3 = np.random.normal()

    # weights = np.array([0, 1])
    # bias = 0

    # self.h1 = Neuron(weights, bias)
    # self.h2 = Neuron(weights, bias)
    # self.o1 = Neuron(weights, bias)

  def feed_forward(self, x):
    # x is a numpy array with 2 elements
    h1 = sigmoid(self.w1 * x[0] + self.w2 * x[1] + self.b1)
    h2 = sigmoid(self.w3 * x[0] + self.w4 * x[1] + self.b2)
    o1 = sigmoid(self.w5 * h1 + self.w6 * h2 + self.b3)
    return o1

    # out_h1 = self.h1.feed_forward(x)
    # out_h2 = self.h2.feed_forward(x)

    ## the inputs for o1 are the outputs from h1 and h2
    # out_o1 = self.o1.feed_forward(np.array([out_h1, out_h2]))

    # return out_o1
  
  def train(self, data, all_y_trues):
    '''
    - data is a (n x 2) numpy array, n = # of samples in the dataset.
    - all_y_trues is a numpy array with n elements.
      Elements in all_y_trues correspond to those in data.
    '''
    learn_rate = 0.1
    epochs = 1000 # number of times to loop through the entire dataset

    for epoch in range(epochs):
      for x, y_true in zip(data, all_y_trues):
        # --- do a feedforward, use output values later
        sum_h1 = self.w1 * x[0] + self.w2 * x[1] + self.b1
        h1 = sigmoid(sum_h1)

        sum_h2 = self.w3 * x[0] + self.w4 * x[1] + self.b2
        h2 = sigmoid(sum_h2)

        sum_o1 = self.w5 * h1 + self.w6 * h2 + self.b3

        o1 = sigmoid(sum_o1)
        y_pred = o1

        ## calculate partial derivatives
        ## naming: d_L_d_w1 represents 'partial L / partial w1'
        d_L_d_ypred = -2 * (y_true - y_pred)

        # neuron o1
        d_ypred_d_w5 = h1 * deriv_sigmoid(sum_o1)
        d_ypred_d_w6 = h2 * deriv_sigmoid(sum_o1)
        d_ypred_d_b3 = deriv_sigmoid(sum_o1)

        d_ypred_d_h1 = self.w5 * deriv_sigmoid(sum_o1)
        d_ypred_d_h2 = self.w6 * deriv_sigmoid(sum_o1)

        # neuron h1
        d_h1_d_w1 = x[0] * deriv_sigmoid(sum_h1)
        d_h1_d_w2 = x[1] * deriv_sigmoid(sum_h1)
        d_h1_d_b1 = deriv_sigmoid(sum_h1)

        # nueron h2
        d_h2_d_w3 = x[0] * deriv_sigmoid(sum_h2)
        d_h2_d_w4 = x[1] * deriv_sigmoid(sum_h2)
        d_h2_d_b2 = deriv_sigmoid(sum_h2)

        ## update weights and biases

        # neuron h1
        self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w1
        self.w2 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w2
        self.b1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1

        # neuron h2
        self.w3 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w3
        self.w4 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w4
        self.b2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_b2

        # neuron o1
        self.w5 -= learn_rate * d_L_d_ypred * d_ypred_d_w5
        self.w6 -= learn_rate * d_L_d_ypred * d_ypred_d_w6
        self.b3 -= learn_rate * d_L_d_ypred * d_ypred_d_b3

      ## calculate  total loss at the end of each epoch
      if epoch % 10 == 0:
        y_preds = np.apply_along_axis(self.feed_forward, 1, data)
        loss = mse_loss(all_y_trues, y_preds)
        print("Epoch %d loss: %.3f" % (epoch, loss))

  def gender_check(self, pred):
    if pred < 0.5:
      print("Male")
    else:
      print("Female")

## testing outputs

# weights = np.array([0, 1]) # w1 = 0, w2 = 1 
# bias = 4 # b = 4
# n = Neuron(weights, bias)

# x = np.array([2, 3])

# print(n.feed_forward(x))
# print('')

# network = NeuralNetwork()
# z = np.array([2, 3])
# print(network.feed_forward(z))


# ## MSE loss tests
# print('')
# y_true = np.array([1, 0, 0, 1])
# y_pred = np.array([0, 0, 0, 0])

# print(mse_loss(y_true, y_pred)) # 0.5

'''
I arbitrarily chose the shift amounts (135 and 66) to make the 
numbers look nice. Normally, you’d shift by the mean.

Name	  Weight (lb)	Height (in)	Gender
Alice 	  133	        65	        F
Bob	      160	        72	        M
Charlie	  152	        70	        M
Diana	    120	        60	        F
Rachel    100         58          F
Doug      175         70          M
Lauren    140         62          F
Alex      122         55          F
Bertha    202         60          F
Leanne    142         60          F
Lee       256         68          M

mean weight: 154.72727272727
mean height: 63.636363636364


'''

# define dataset
data = np.array([
  [-2, -1],  # Alice
  [25, 6],   # Bob
  [17, 4],   # Charlie
  [-15, -6], # Diana
  [-18, -2], # Kathleen
  [30, 2], # Matt
  [3, -2] # Bertha
])

# define dataset 2
# data2 = np.array([
#   [−21.72727273, -1.363636364],
#   [5.272727273, 8.363636364],
#   [-2.727272727, 6.363636364],
  
# ])


all_y_trues = np.array([
  1, # Alice
  0, # Bob
  0, # Charlie
  1, # Diana
  1, # Kathleen
  0, # Matt
  1  # Bertha
])

# train our neural network!
network = NeuralNetwork()
network.train(data, all_y_trues)

emily = np.array([-7, -3]) # 128 pounds, 63 inches
frank = np.array([20, 2]) # 155 pounds, 68 inches
kieley = np.array([-15, -2]) 

emily_pred = network.feed_forward(emily)
frank_pred = network.feed_forward(frank)
kieley_pred = network.feed_forward(kieley)

# print("emily pred: ", emily_pred)
# print("frank pred: ", frank_pred)

network.gender_check(emily_pred)
network.gender_check(frank_pred)
network.gender_check(kieley_pred)


# print("Emily: %.3f" % network.feed_forward(emily)) 
# print("Frank: %.3f" % network.feed_forward(frank))