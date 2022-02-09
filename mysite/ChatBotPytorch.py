import nltk
import torch

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






#tesztelések
"""
teszt_szoveg = "How long does shipping take?"
print(teszt_szoveg)
teszt_szoveg = tokenize(teszt_szoveg)
print(teszt_szoveg)
teszt_lista = ["Organize", "organizes", "organizing"]
teszt_levagva = [stem(w) for w in teszt_lista]
print(teszt_levagva)
"""
