import warnings

warnings.filterwarnings("ignore")

import string
import time
import joblib
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from fuzzywuzzy import process
from functools import lru_cache, wraps
import logging

#Sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

#file imports
from handle_intent import handle_entity
from news import *
from games import *
from trivia import *
from wikihow import *
from user_interaction import *
from tools import *
from conversations import *
from interactions import *

#empties expected context file
chatbot_tools.open_file('data/expected context.txt', file='w', text='')

#configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("Joan.log"),
        #logging.StreamHandler()
    ]
)

get_ip_data()

#decorator for logging the execution time of a function
# this is still new to me this feature of python  
def log_execution_time(func):
    """
    A decorator mesaures how long a function takes to execute and logs the duration in seconds using the `logging` module.
    It is useful for performance monitoring and debugging

    Args:
        - func (callable): The function to be wrapped and timed.

    Return:
        - callable: The wrapped function with execution time logging added.
    @wraps(func)
    def wraper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info("Function '%s' executed in %.4f seconds", func.__name__, execution_time)
        return result
    return wraper

class models():
    @log_execution_time       
    def process_input(user_input, vectorizer, classifier, er_vectorizer, er_classifier):
        """
        Processes the user's input, cleans it, and uses different functions to respond accurately.
        If no appropriate response is found, it relies on external AI sources like Mistral or Wolfram Alpha.
        
        Args:
            - user_input (str): The user's input to process.
            - vectorizer (TfidfVectorizer): The vectorizer used to transform text data.
            - classifier (LinearSVC): The classifier used to predict user input classification.
            - er_vectorizer (TfidfVectorizer): The vectorizer for emotion recognition.
            - er_classifier (SVC): The classifier for emotion recognition.
        
        Returns:
            - None: This function does not return a value, it handles user interaction and context.
        """
        
        with open('data/expected context.txt', 'r') as f:
            context = f.read()

        user_input = user_input.lower().translate(str.maketrans("","",string.punctuation))
        matched_keywords = models.find_matched_keywords(user_input, vectorizer, threshold=0.5)
    
        text = process_text_tools.preprocess_text(user_input)
        text_vectorized = vectorizer.transform([text])
        entity = classifier.predict(text_vectorized)[0]

        user_intent(entity, vectorizer, classifier, er_vectorizer, er_classifier, user_input) #This is for the user_interation.py

        #print("Entity: ", entity)#***

        #Try other modules first
        news = News()
        wikihow = Wikihow()
        trivia = Trivia()
        games = Games()

        news_intent = news.get_news_intent(entity, vectorizer, classifier)
        wikihow_intent = wikihow.get_wiki_intent(user_input)
        trivia_intent = trivia.get_quiz_intent(entity)
        games_intent = games.get_game_intent(entity, vectorizer, classifier, user_input, user_data)

        if news_intent == 0 or wikihow_intent == 0 or trivia_intent == 0 or games_intent == 0:
            intent = models.find_intent(user_input, ET_data)

            ##the main intent recognition
            #print("user's intent:", intent)#***
            try:
                ET_data.set_index('name', inplace=True)
            except KeyError:
                pass
            
            #print(entity)#***
            entity_response = handle_entity(entity, user_input)

            if entity_response[0] == "output":
                audio(entity_response[1])
            elif entity_response[0] == "function" and entity_response[1] == None:
                if entity == 'positive' or entity == 'negative':
                    chatbot_tools.big_guns(user_input)
                    return 'reload data'
                else:
                    audio(entity)
        else:
            print("One of the requested modules worked.")

    @log_execution_time
    def find_intent(user_input, ET_data):
        """
        Compares the user's input (string) to the entity tagging data it has in the ET.csv file.
        Uses fuzzywuzzy to find the best match to the user's input.

        Args:
            - user_input (str): The user's input
            - ET_data (pandas DataFrame): A dataframe for pandas to use effeciently.

        Returns:
            - str : Empty string or match[0] (the match with highest score).
        """
        
        try:
            user_input = user_input.lower()
            ET_data = ET_data.iloc[ET_data['name'].str.len().argsort()]
            ET_data.set_index('name', inplace=True)
        
            matches = process.extractOne(user_input, ET_data)

            if matches[1] > 90:
                return matches[0]
            else:
                return ''
        except KeyError:
            pass

    @staticmethod
    @lru_cache(maxsize=None)
    @log_execution_time
    def preprocess_data():
        """
        Reads all the data models (if they exist), and other data files into memory.
        Trains Machine Learning models on the data in memory.
    
        Args:
            None: Doesn't accept any parameters.
    
        Returns:
            tuple:
                - TfidfVectorizer: The vectorizer for sentiment analysis.
                - LinearSVC: The sentiment classifier.
                - TfidfVectorizer: The vectorizer for emotion recognition.
                - SVC: The emotion recognition classifier.
        """
        
        # Check if models are already saved
        try:
            vectorizer = joblib.load('Models/vectorizer.joblib')
            classifier = joblib.load('Models/classifier.joblib')
            er_vectorizer = joblib.load('Models/er_vectorizer.joblib')
            er_classifier = joblib.load('Models/er_classifier.joblib')
            return vectorizer, classifier, er_vectorizer, er_classifier
        except FileNotFoundError:
            pass  # If files don't exist, continue with training

        # Read data
        df = pd.read_csv('data/datasets/ET.csv')
        pos_neg_data = pd.read_csv('data/datasets/SR.csv')
        emotion_data = pd.read_csv('data/datasets/ER.csv')

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            combined_data1_future = executor.submit(
                pd.concat, [df['name'], pos_neg_data['text']], axis=0, ignore_index=True)
            combined_data2_future = executor.submit(
                pd.concat, [df['ET'], pos_neg_data['sentiment']], axis=0, ignore_index=True)

            combined_data1 = combined_data1_future.result()
            combined_data2 = combined_data2_future.result()

        # Preprocess data
        X_train = [process_text_tools.preprocess_text(text) for text in combined_data1.tolist()]
        y_train = combined_data2.tolist()

        # Vectorization
        vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b', max_features=10000)
        x_train_vectorized = vectorizer.fit_transform(X_train)

        # Classifier training
        class_weights = process_text_tools.calculate_class_weights(y_train)
        classifier = LinearSVC(class_weight=class_weights, loss="hinge", C=0.5)
        classifier.fit(x_train_vectorized, y_train)

        # Emotion recognizer
        er_vectorizer = TfidfVectorizer(max_features=5000)
        x_train_er_vectorized = er_vectorizer.fit_transform(emotion_data['text'])
        er_classifier = SVC(kernel='linear')
        er_classifier.fit(x_train_er_vectorized, emotion_data['emotion'])

        # Save models
        joblib.dump(vectorizer, 'Models/vectorizer.joblib')
        joblib.dump(classifier, 'Models/classifier.joblib')
        joblib.dump(er_vectorizer, 'Models/er_vectorizer.joblib')
        joblib.dump(er_classifier, 'Models/er_classifier.joblib')

        return vectorizer, classifier, er_vectorizer, er_classifier

    @staticmethod
    @lru_cache(maxsize=None)
    @log_execution_time
    def find_matched_keywords(user_input, vectorizer, threshold=0.7):
        """
        Uses the user's input to find their input with the data in the vectorizer

        Args:
            - user_input (str): the user's inputted text
            - vectorizer (TfidfVectorizer): The vectorizer used to transform text data
            - Threshold (float optional): The threshold to determine how close the user_input has to be to a keyword. Defaults to 0.7.

        Returns:
            - (str): string of the closest matching keyword or the user_input if no keyword matching was found.
        """
        try:
            keywords = ET_data.iloc[:, 0].tolist()

            preprocess_input = [process_text_tools.preprocess_text(user_input)]

            input_vectorized = vectorizer.transform(preprocess_input)
            similarity_scores = cosine_similarity(input_vectorized, vectorizer.transform(keywords))[0]

            matched_keywords = [keywords[i] for i, score in enumerate(similarity_scores) if score >= threshold]
            return matched_keywords
        except Exception as e:
            return user_input

#entity tag data
ET_data = pd.read_csv('data/datasets/ET.csv')

vectorizer, classifier, er_vectorizer, er_classifier = models.preprocess_data()

user_data = chatbot_tools.get_user_data()

if user_data['new user'] == 'true':
    chatbot_tools.write_user_data(new_user='false')
    print(chatbot_tools.random_output('welcome user'))

run_loop = True
            
while run_loop is True:
    user_input = input('Input >>> ')
    process = models.process_input(user_input, vectorizer, classifier, er_vectorizer, er_classifier)  

    if process == 'reload data': #if the bot learns from wolfram alpha then it returns 'reload data' for it load the data model in again (takes around 1.5 seconds)
        vectorizer, classifier, er_vectorizer, er_classifier = models.preprocess_data()

###for any code that is temp search for ***
