import torch
import json
import random
from .ChatBotPytorch import bag_of_words, tokenize
from .SetupNeuralNet import all_words, model, tags, intents
def makeAnswer(request):
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
                return answer
    else:
        answer = "Nem értem!!!!"
        return answer