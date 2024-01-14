import torch.nn as nn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Carica il dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Definisci un modello semplice
class TabularModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(TabularModel, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        x = self.fc(x)
        return x

# Inizializza il modello
input_size = X.shape[1]
output_size = len(set(y))
model = TabularModel(input_size, output_size)