import datetime, csv, random
import pandas as pd
from tools import *
from interactions import *

class how_are_you_response():
    def neutral_response(user_emotion, emotion):
        if user_emotion == 'hungry':
            how_are_you_response.suggest_food()
        elif user_emotion == 'bored':
            how_are_you_response.bordem_fix()
            return None
        elif user_emotion == emotion:
            print(chatbot_tools.random_output('neutral emotion').replace('<emotion>', emotion))
            return None
    
    def bordem_fix():
        internet = check_internet()

        random_number = 14# random.randint(1, 15)

        user_data = chatbot_tools.get_user_data()
        if user_data['fix bordem'] == '':
            if random_number == 1:#play a game
                print(chatbot_tools.random_output('bordem play game suggestion'))
            elif random_number == 2:#play a video
                if internet == 0:
                    print(chatbot_tools.random_output('bordem watch video suggestion'))
                else:
                    how_are_you_response.bordem_fix()
            elif random_number == 3:
                print(chatbot_tools.random_output('bordem play music suggestion'))
            elif random_number == 4:
                print(chatbot_tools.random_output('tell joke suggestion'))
            elif random_number == 5:
                print(chatbot_tools.random_output('tell riddle suggestion'))
            elif random_number == 6:
                print(chatbot_tools.random_output('start trivia suggestion'))
            elif random_number == 7:
                print(chatbot_tools.random_output('fun fact suggestion'))
            elif random_number == 8:
                print(chatbot_tools.random_output('wiki game suggestion'))
            elif random_number == 9:
                print(chatbot_tools.random_output('phone person suggestion'))
            elif random_number == 10:
                print(chatbot_tools.random_output('xkcd suggestion'))
            elif random_number == 11:
                print(chatbot_tools.random_output('read wikihow suggestion'))
            elif random_number == 12:
                print(chatbot_tools.random_output('read wikipedia suggestion'))
            elif random_number == 13:
                print(chatbot_tools.random_output('play akinator suggestion'))
            elif random_number == 14:
                result = requests.get('https://www.boredapi.com/api/activity/')
                if result.status_code == 200:
                    result = result.json()
                    
                    print(f"How about you try to {result['activity']}")
                    
                    with open('data/expected context.txt', 'w') as w:
                        w.write('random activity')
        else:
            print(chatbot_tools.get_user_data()['fix bordem'])
        return None 
        
    def suggest_food():
        suggest_meal()
        '''user_data = chatbot_tools.get_user_data()

        if user_data['favourite food'] == '':
            print(chatbot_tools.random_output('unknown fix hunger').replace('<user-name>', user_data['first name']))
        else:
            print(chatbot_tools.random_output('fix hunger').replace('<F-food>', user_data['favourite food']).replace('<user-name>', user_data['first name']))
        
        return None'''

def greeting_response(user_input):
    current_hour = datetime.datetime.now().hour
    
    users_name = ''
    #read user data for name
    with open('data/user data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            users_name = row[1]
            
    if 'morning' in user_input.lower():
        print(chatbot_tools.random_output('morning greeting').replace('<user-name>', users_name))
    elif 'afternoon' in user_input.lower():
        print(chatbot_tools.random_output('afternoon greeting').replace('<user-name>', users_name))
    elif 'evening' in user_input.lower():
        print(chatbot_tools.random_output('evening greeting').replace('<user-name>', users_name))
    elif 'night' in user_input.lower():
         print(chatbot_tools.random_output('night greeting').replace('<user-name>', users_name))
    else:
        if current_hour >= 6 and current_hour < 12:
             #morning
             print(chatbot_tools.random_output('morning greeting').replace('<user-name>', users_name))
        elif current_hour >= 12 and current_hour < 17:
            #afternoon
            print(chatbot_tools.random_output('afternoon greeting').replace('<user-name>', users_name))
        elif current_hour >= 17 and current_hour <= 21:
            #evening
            print(chatbot_tools.random_output('evening greeting').replace('<user-name>', users_name))
        else:
            #night
            print(chatbot_tools.random_output('night greeting').replace('<user-name>', users_name))
    
def been_while():
    time_used_last = chatbot_tools.open_file('data/last time used.txt', file='r')
    print(chatbot_tools.random_output('been while').replace('<date>', time_used_last))

def how_are_you():
    print(chatbot_tools.random_output('how are you bot response'))
