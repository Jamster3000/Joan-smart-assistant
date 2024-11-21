'''
This file is for all the user interations that would typically appaear in Joan.py context within the process_input function
'''

import pandas as pd
import webbrowser
from tools import *
from conversations import *

def open_expected_context():
    with open('data/expected context.txt', 'r') as f:
        context = f.read()
    return context

class UserInteraction():
    def __init__(self):
        # Emotion based on positive, neutral, and negative emotions
        self.positive_emotions = ['happy', 'love']
        self.neutral_emotions = ['surprise', 'pain', 'hungry', 'bored']
        self.negative_emotions = ['sad', 'anger', 'fear', 'unhappy']

        self.user_data = chatbot_tools.get_user_data()  # Only keeping user_data

    def how_are_you(self, er_vectorizer, er_classifier, user_input):
        query_er_vectorizer = er_vectorizer.transform([user_input])
        user_emotion = er_classifier.predict(query_er_vectorizer)[0]
        for emotion in self.positive_emotions:
            if user_emotion == emotion:
                audio(chatbot_tools.random_output('positive emotion').replace('<emotion>', emotion))
                return None
        for emotion in self.neutral_emotions:
            how_are_you_response.neutral_response(user_emotion, emotion)
            break      
        for emotion in self.negative_emotions:
            if user_emotion == emotion:
                audio(chatbot_tools.random_output('negative emotion').replace('<emotion>', emotion))
                return None
    
    def learn_favourite_food(self, user_input):
        user_favourite_food_extract = text_tools.find_food(str(user_input))
        self.user_data['F-food'] = user_favourite_food_extract  # Updated to use user_data
        self.user_data.to_csv('data/user data.csv', index=False)  # Assuming you still want to save this data
        audio(chatbot_tools.random_output('favourite food response')
              .replace('<F-food>', user_favourite_food_extract)
              .replace('<name>', self.user_data['first name'])
              .replace('-', 'and'))

    def bordem_play_game(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            audio(chatbot_tools.random_output('play which game'))
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def bordem_watch_video(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            bordem_entertainment.play_video()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def tell_joke(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            tell_joke()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def tell_riddle(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            tell_riddle()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def fun_fact(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            facts()
        else:
            audio(chatbot_tools.random_output('no worries general'))
    
    def phone_person(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            audio(chatbot_tools.random_output('phone person'))
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def xkcd(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            games.xkcd()
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def welcome_user(self, user_input):
        # Get the user's name from their input
        user_name = chatbot_tools.get_user_name(user_input)
        user_name = user_name[0].split(' ')
        if len(user_name) > 1:
            if len(user_name) >= 3:
                chatbot_tools.write_user_data(first_name=user_name[0], middle_name=user_name[1], surname=user_name[2])
            else:
                chatbot_tools.write_user_data(first_name=user_name[0], surname=user_name[1])
        else:
            chatbot_tools.write_user_data(first_name=user_name[0])

        chatbot_tools.get_user_data.cache_clear()
        user_data = chatbot_tools.get_user_data()
        audio(chatbot_tools.random_output('welcome users name').replace('<user-name>', user_data['first name']))
        
        # Get the user's gender based on their name using an API
        gender_call = requests.get(f"https://api.genderize.io?name={user_data['first name']}")
        
        if gender_call.status_code == 200:
            gender_call = gender_call.json()
            gender = gender_call['gender']
            chatbot_tools.write_user_data(gender=gender)

    def random_activity(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]

        if sentiment == 'positive':
            audio(chatbot_tools.random_output('bored activity attempt'))
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def info_food(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        
        if sentiment == 'positive':
            with open('data/tempFile.txt', 'r') as f:
                read = f.read()
                
            search_food_ingriedents(read)

    def choose_youtube(self, user_input):
        from youtubesearchpython import VideosSearch
        videoResults = VideosSearch(user_input, limit=1)
        webbrowser.open(videoResults.result()['result'][0]['link'])
        chatbot_tools.open_file('data/expected context.txt', file='w', text='')

class Passcode():
    def __init__(self):
        pass

    def speak_passcode(self, user_input):
        with open('data/user passcode.txt', 'w') as f:
            f.write(user_input)
        audio(chatbot_tools.random_output('speak passcode again'))

    def repeat_passcode(self, user_input):
        with open('data/user passcode.txt', 'r') as f:
            passcode = f.read()
        
        if user_input == passcode:
            audio(chatbot_tools.random_output('passcode accepted'))
        else:
            with open('data/user passcode.txt', 'w') as f:
                f.write('')
            audio(chatbot_tools.random_output('passcode denied'))

    def change_passcode(self, vectorizer, classifier, user_input):
        sr_vectorizer = vectorizer.transform([user_input])
        sentiment = classifier.predict(sr_vectorizer)[0]
        if sentiment == 'positive':
            audio(chatbot_tools.random_output('passcode before change'))
        else:
            audio(chatbot_tools.random_output('no worries general'))

    def passcode_before_change(self, user_input):
        with open('data/user passcode.txt', 'r') as f:
            passcode = f.read()
        
        if passcode == user_input:
            audio(chatbot_tools.random_output('blank passcode accept'))
            audio(chatbot_tools.random_output('speak replace passcode'))
            with open('data/expected context.txt', 'w') as f:
                f.write('speak passcode')
        else:
            audio(chatbot_tools.random_output('blank passcode denied'))

def user_intent(context, vectorizer, classifier, er_vectorizer, er_classifier, user_input):
    userInteraction = UserInteraction()
    passcode = Passcode()
    expected_context = open_expected_context()

    if context == 'how_are_you':
        userInteraction.how_are_you(er_vectorizer, er_classifier, user_input)
    elif context == "learn favourite food":
        userInteraction.learn_favourite_food(user_input)
    elif context == "bordem play game":
        userInteraction.bordem_play_game(vectorizer, classifier, user_input)
    elif context == "bordem watch video":
        userInteraction.bordem_watch_video(vectorizer, classifier, user_input)
    elif context == "tell joke":
        userInteraction.tell_joke(vectorizer, classifier, user_input)
    elif context == "tell riddle":
        userInteraction.tell_riddle(vectorizer, classifier, user_input)
    elif context == "fun fact":
        userInteraction.fun_fact(vectorizer, classifier, user_input)
    elif context == "phone person":
        userInteraction.phone_person(vectorizer, classifier, user_input)
    elif context == "xkcd":
        userInteraction.xkcd(vectorizer, classifier, user_input)
    elif context == "speak passcode":
        passcode.speak_passcode(user_input)
    elif context == "repeat passcode":
        passcode.repeat_passcode(user_input)
    elif context == "welcome user" or expected_context == "welcome user":
        userInteraction.welcome_user(user_input)
    elif context == "random activity":
        userInteraction.random_activity(vectorizer, classifier, user_input)
    elif context == "info food":
        userInteraction.info_food(vectorizer, classifier, user_input)
    elif context == "choose youtube":
        userInteraction.choose_youtube(user_input)
    elif context == "change passcode":
        passcode.change_passcode(vectorizer, classifier, user_input)
    elif context == "passcode before change":
        passcode.passcode_before_change(user_input)
            
#TODO: Move how_are_you_response to this file