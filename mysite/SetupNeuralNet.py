import torch
import json
from pathlib import Path
from .model import NeuralNet


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')#ha CUDA támogatott cpu van akkor 'cuda' különben 'cpu' az értéke

with open(Path(__file__).parent / 'intents.json', "r") as f:#intents.json betöltése
    intents = json.load(f)

FILE = Path(__file__).parent / 'data.pth'
data = torch.load(FILE)#data.pth betöltése

input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)#objekt létrehozás
model.load_state_dict(model_state)
model.eval()#értékelő módba kapcsolás
