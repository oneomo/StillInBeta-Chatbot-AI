import json
from pathlib import Path

from nltk import data
from nltk.grammar import is_nonterminal
from ChatBotPytorch import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open(Path(__file__).parent / 'intents.json','r') as f:#Json file megnyitása
    intents = json.load(f)

all_words = []
tags = []
xy = []
for intent in intents['intents']:#intents.json adatain való átfutás
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)#all_words listához hozzáadjuk a jelenlegi tokenizált pattenrt
        xy.append((w, tag))#xy listához hozzáadunk egy tupplet a szóval és a tag-jével

ignore_words = ['?','!','.',',']#ezeket mellőzzük az all_words listábából mert feleslegesek
all_words =  [stem(w) for w in all_words if w not in ignore_words]#szavak levágva bele az all_words listába
all_words = sorted(set(all_words))#set-té konvertálás, eltünteti a duplicate-eket illetve abc szerinti sorrendbe
tags = sorted(set(tags))
print(tags)

X_train = []
y_train = []
for (patters_sentence, tag) in xy:#tuple-ken való átloopolás az xy-ban
    bag = bag_of_words(patters_sentence, all_words)#Bag of words alkalmazásával bag változó létrehozása, felülírása
    X_train.append(bag)
    
    label = tags.index(tag)#A tag-je alapján kap egy szám értéket
    y_train.append(label) #CrossEntrophyLoss

X_train = np.array(X_train)#numpy-os tömbbé alakítás
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__(self):#objekt létrehozásakor fut le
        self.n_sample = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
    
    #dataset[index]
    def __getitem__(self, index):#.get() függvény hívásakor fut le
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):#len() függvény objekten való használatakor fut le
        return self.n_sample

#Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 1000#Ennyi alkalommal trainel


dataset = ChatDataset()#objekt létrehozás
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle= True)#objekt létrehozás

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')#ha CUDA támogatott cpu van akkor 'cuda' különben 'cpu' az értéke
model = NeuralNet(input_size, hidden_size, output_size).to(device)#objekt létrehozás

#loss and optimizer
criterion = nn.CrossEntropyLoss()#A pontosság méréséhez kellő object
optimizer = torch.optim.Adam(model.parameters(), lr= learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype = torch.long).to(device)

        #forward
        outputs = model(words)#Neural hálózat használata
        loss = criterion(outputs, labels)#Veszteség meghatározása

        #backward and optimizer steps
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if(epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch+1} / {num_epochs}], loss = {loss.item():.4f}')
print(f'final loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"#ez lesz a neve a fájlnak
torch.save(data, FILE)#a data szótárt eltároljuk FILE változó értékének nevén

print(f"Training completed. file saved to {FILE}")