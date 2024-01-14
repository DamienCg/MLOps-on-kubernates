from io import BytesIO
import torch
from model import model


import torch

def predict(input_data, checkpoint_binary):
    # Load the model
    checkpoint_stream = BytesIO(checkpoint_binary)
    checkpoint = torch.load(checkpoint_stream)

    # Check the keys in the checkpoint dictionary
    if 'state_dict' in checkpoint:
        model.load_state_dict(checkpoint['state_dict'])
    else:
        # If the 'state_dict' key is not present, assume the checkpoint directly contains the model state_dict
        model.load_state_dict(checkpoint)

    model.eval()

    # Convert the list to a PyTorch tensor
    input_tensor = torch.tensor(input_data, dtype=torch.float32).view(1, -1)

    with torch.no_grad():
        # Make the prediction
        print("EFFETTUO PREVISIONE")
        prediction = model(input_tensor)
        predicted_class = torch.argmax(prediction).item()

    return predicted_class
