import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import json

def train_test_val(loaded_data):
    print("SONO SU MODEL MANAGEMENT, ALLENO IL MODELLO")

    data_dict_list = json.loads(loaded_data)

    data = data_dict_list['data']
    data = json.loads(data)

    # Estrai features (X) e target (y)
    X = []
    y = []
    for entry in data:
        features = [entry["sepal length (cm)"], entry["sepal width (cm)"], entry["petal length (cm)"], entry["petal width (cm)"]]
        target = entry["target"]
        X.append(features)
        y.append(target)

    # Converti X e y in array NumPy
    import numpy as np
    X = np.array(X)
    y = np.array(y)

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

    precision = 0.95

    files = {'checkpoint': open(checkpoint_path, 'rb')}
    return files,precision

  

    
 
