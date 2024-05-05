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
import requests
from sklearn.preprocessing import StandardScaler
import joblib
import emosent
from emosent import get_emoji_sentiment_rank_multiple
from emosent import get_emoji_sentiment_rank
import emoji
from scipy.sparse import csr_matrix, hstack
from afinn import Afinn
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

def clean_emoji(text):
    return emoji.replace_emoji(text, replace='')

# Función para contar ocurrencias de las palabras/frases
first_person_terms = ['I',"i'm", 'me', 'myself', 'my', 'mine', 'to me', 'for me', 'I feel', 'I think', 'I believe', 'I am', ]
def count_first_person_terms(text):
    count = 0
    for term in first_person_terms:
        count += text.lower().count(term.lower())
    return count
# Función para calcular la normalización por longitud del tweet
def normalize_by_length(text):
    words = text.split()  # Dividir el texto en palabras
    return len(words)

def detectar_emojis_completo(tweet):
    sentiment_score_total = 0  # Iniciar el puntaje total en cero

    # Iterar sobre cada carácter en el tweet
    for char in tweet:
        # Verificar si el carácter es un emoji
        if char in emoji.EMOJI_DATA:  # Usar EMOJI_DATA para verificar si es un emoji
            # Obtener el valor de sentiment_score del emoji
            emoji_sentiment_rank = get_emoji_sentiment_rank(char)
            if emoji_sentiment_rank:
                sentiment_score = emoji_sentiment_rank['sentiment_score']
                sentiment_score_total += sentiment_score  # Sumar el puntaje al total

    return sentiment_score_total


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
    tweets = [tweet["text"] for tweet in text_only_tweets]
    tweets = [tweet.replace('\n', ' ') for tweet in tweets]
    tweets = ' '.join(tweets)
    df = pd.DataFrame({"text": tweets},index=[0])
    df['text'] = df['text'].str.replace(r'@\w+', '', regex=True)  # Elimina menciones
    df['text'] = df['text'].str.replace(r'#\w+', '', regex=True)  # Elimina hashtags
    df['text'] = df['text'].str.lower()
    df['Emojis_Sentimentscore'] = df['text'].apply(detectar_emojis_completo)
    df['first_person_count'] = df['text'].apply(count_first_person_terms)
    df['tweet_length'] = df['text'].apply(normalize_by_length)
    df['egocentrism_score'] = df['first_person_count'] / df['tweet_length']
    afinn = Afinn()
    df['clean_tweet'] = df['text'].apply(clean_emoji)
    df['sentiment_score'] = df['clean_tweet'].apply(afinn.score)
    df = df[['clean_tweet', 'Emojis_Sentimentscore','egocentrism_score', 'sentiment_score']]
    #importar el vectorizador y el scalador
    vectorizer = joblib.load('vectorizador_entrenado_xgb_emotion (1).pkl')
    x_vec= vectorizer.transform(df['clean_tweet'])
    # Escala las características de sentimiento
    sentiment_features = df[['Emojis_Sentimentscore', 'egocentrism_score',
       'sentiment_score']]
    scaler = StandardScaler()
    scaled_sentiment_features = scaler.fit_transform(sentiment_features)
    scaled_sentiment_features_sparse = csr_matrix(scaled_sentiment_features)
    # Combinar las características TF-IDF con las características de sentimiento escaladas
    X_combined = hstack([x_vec, scaled_sentiment_features_sparse])
    xgb_clf = joblib.load('MODELO_xgb_emotion.pkl')

    predictions = xgb_clf.predict(X_combined)



    return predictions