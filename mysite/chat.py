import random
import json
import torch
from model import NeuralNet 
from ChatBotPytorch import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')#ha CUDA támogatott cpu van akkor 'cuda' különben 'cpu' az értéke

with open("intents.json", "r") as f:#intents.json betöltése
    intents = json.load(f)

FILE = "data.pth"
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

bot_name = "Petra"
print("Beszélgessünk írd, hogy 'kilépés', ha nem szeretnél:(")
while True:
    sentence = input("Te: ")
    if sentence == "kilépés":
        break
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim = 1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim = 1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75: #Ha 75 százalékig egyezik az egyik lehetőséggel akkor fut le
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: Nem értem!!!!")