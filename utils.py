import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def predict_Link(data):

    #api porcesa y descarga informacion del link (tweets de el ultimo mes del usuario)
    
    #se prosesan los texto y se vectorizan 
    # Cargar el modelo previamente entrenado para predecir probabilidad de tendecias suicidas 
    # model = load_model(ubicaciondel modelo)
    # Realizar la predicción con los datos proporcionados
    porcentaje = np.random.randint(1,101)
    if porcentaje > 50 :
        texto = 'Teniendo en cuenta el resultado del analisis sobre el texto seleccionado recomendamos que se busque asistencia profesional.'
    elif porcentaje < 50 :
        texto = 'Teniendo en cuenta el resultado del análisis sobre el texto seleccionado no parece necesario buscar asistencia profesional, no obstante es conveniente estar alerta ante signos de ansiedad o depresión crónica'
    predictions = f"La probabilidad de que esta persona tenga tendencias suicidas es del {porcentaje}%. \n {texto}"
    return predictions

def preprocess(text):
  text = text.lower()
  text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
  text = re.sub(r'@\w+','',text)
  text = re.sub(r'#\w+','',text)
  text = re.sub(r'[^\w\s]|[\d]', ' ', text)
  text = re.sub(r'\s+',' ',text).strip()
  tokens = word_tokenize(text)
  # Eliminación de los acentos
  tokens = [unidecode(token) for token in tokens]
  stop_w = set([unidecode(w) for w in stopwords.words('english')])
  tokens = [token for token in tokens if token not in stop_w]
  lematizador = WordNetLemmatizer()
  tokens = [lematizador.lemmatize(token) for token in tokens if len(token)>=3]
  return ' '.join(tokens)


def obtener_datos_desde_api(link):
    # Dividir la URL por el carácter "/"
    parts = link.split("/")
    # Tomar el último elemento de la lista
    username = parts[-1]
    url = "https://twitter154.p.rapidapi.com/user/tweets"

    querystring = {"username":username,"limit":100,"include_replies":"false","include_pinned":"false"}

    headers = {
	"X-RapidAPI-Key": "f0d9654d37msh1ebeda66ce26c16p1e8b78jsnab0528aef7bb",
	"X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    respueta = response.json()

    tweets = respueta['results']
    text_only_tweets = []

    for tweet in tweets:
      text_only_tweets.append({'text': tweet['text']})

    df = pd.DataFrame(text_only_tweets)
    processed_tweets = []
    for tweet in tqdm(df['text']):
        processed_tweet = preprocess(tweet)
        processed_tweets.append(processed_tweet)
    
    df['tweets_preprocessed'] = processed_tweets
    df = df.drop_duplicates()
    df.fillna('', inplace=True)
    vectorizer = joblib.load('vectorizador_entrenado.pkl')
    text = vectorizer.transform(df['tweets_preprocessed'])
    loaded_mo = joblib.load('modelo_entrenado1.1.pkl')
    prediccion = loaded_mo.predict(text)
    porcentaje = float(sum(prediccion == 0)/len(prediccion))

    return porcentaje