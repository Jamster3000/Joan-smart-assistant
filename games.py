'''
This is for all the games that the user can play.
The play of the games do not take place in this file.
The actual code for playing games are found in interactions.play
Mostly for when the user asks to play a specific game, or something related to playing a game
'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression

from user_interaction import *
from tools import *
from conversations import *
from interactions import *
from tools import *

class Games():
    def get_game_intent(self, entity, vectorizer, classifier, user_input, user_data):
        if entity == "wiki game": self.wiki_game(vectorizer, classifier, user_input)
        elif entity == "akinator": self.akinator(vectorizer, classifier, user_input)
        elif entity == "play blackjack again": self.play_blackjack_again(vectorizer, classifier, user_input, user_data)
        elif entity == "play number guess again": self.play_number_guess_again(vectorizer, classifier, user_input, user_data)
        else: return 0
    
    def wiki_game(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            games.open_wiki_game()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def akinator(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            games.akinator()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def play_blackjack_again(self, vectorizer, classifier, user_input, user_data):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            games.blackjack('')
        else:
            audio(chatbot_tools.random_output('no worries game').replace('<user-name>', user_data['first name']))
            
    def play_number_guess_again(self, vectorizer, classifier, user_input, user_data):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            games.numberGuess()
        else:
            audio(chatbot_tools.random_output('no worries').replace('<user-name>', user_data['first name']))