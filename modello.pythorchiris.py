import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

# Carica il dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Dividi il dataset in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Converte i dati in tensori PyTorch
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.LongTensor(y_train)

# Crea un DataLoader per il training
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

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

# Definisci la loss e l'ottimizzatore
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Addestra il modello
num_epochs = 50
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Salva il checkpoint
checkpoint_path = 'model_checkpoint.pth'
torch.save(model.state_dict(), checkpoint_path)

# Carica il modello da checkpoint
loaded_model = TabularModel(input_size, output_size)
loaded_model.load_state_dict(torch.load(checkpoint_path))
loaded_model.eval()

# Esegui una previsione con un singolo esempio Iris
sample_input = torch.FloatTensor(X_test[0])
with torch.no_grad():
    prediction = loaded_model(sample_input)
    predicted_class = torch.argmax(prediction).item()

print(f"Predicted class for the sample: {predicted_class}")
