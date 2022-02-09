from django.shortcuts import render, redirect 
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from pathlib import Path

from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages
import json
import random
import torch
import torch.nn as nn
import nltk
#nltk.download('punkt')#punkt package letöltése, csak első alkalommal kell
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()#Stemmer object létrehozása szavak végének levágásához szükséges
def tokenize(sentence):#Mondat elemekre darabolása és egy listaként adja vissza
    return nltk.word_tokenize(sentence)

def stem(word):#Levágja a szavak végét, így nem kell annyi szót megtanítani neki
    return stemmer.stem(word.lower())#kis betűre is konvertálja a szavakat

def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence] #A tokenizált mondaton elvégezzük a levágást
    bag = np.zeros(len(all_words), dtype = np.float32)#Létrehozunk egy all_words hosszúságú listát nulákkal töltve
    for idx,w, in enumerate(all_words):#Végig loopolunk az all_words listán idx növekedik minden futással w a jelenlegi elem
        if w in tokenized_sentence:#Ha a szó szerepel a mondatban
            bag[idx] = 1.0 #nulla átírása annál a helynél 1-re
    return bag
class NeuralNet(nn.Module):#Neurális hálózat szerkezetének kiépítése
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet,self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2= nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self,x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        #no activation and no softmax
        return out

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

def home(request):
    if request.method == "POST":
        sentence = json.loads(request.body).get('data')
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
                    answer = random.choice(intent['responses'])
        else:
            answer = "Nem értem!!!!"
        return HttpResponse(str(answer))
    return render(request, 'mysite/home.html')
# Create your views here.
@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
	context = {'form':form}
	return render(request, 'mysite/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'mysite/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')
