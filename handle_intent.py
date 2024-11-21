from elevenlabs import user
import pandas as pd

from tools import *
from conversations import *
from interactions import *

#below is a list of response functions.
#This is more effective than lots of if/elif statements
#Please see the very bottom of the file to see the handle_entity function

def greeting(user_input):
    greeting_response(user_input)
    
def factory_reset_function(user_input):
    with open('data/user passcode.txt', 'r') as f:
        passcode = f.read()
        
    if passcode == '' or passcode not in user_input:
        audio(chatbot_tools.random_output('factory reset unrecognized passcode'))
    else:
        audio(chatbot_tools.random_output('factory reset passcode accecpted'))
        factory_reset()

def how_to_function(user_input):
    with open('data/wiki links.txt', 'w') as f:
        f.write(user_input)
    audio(chatbot_tools.random_output('wikihow search read or open'))

def bye_function():
    remember_data = pd.read_csv('data/userRemember.csv')
    user_data = chatbot_tools.get_user_data()
    
    for index, row in remember_data.iterrows():
        if row['when'] == 'bye':
            if 'water' in row['remember']:
                audio('Remember', row['remember'])
                break
            else:
                remember_data = remember_data.drop(index, axis=0)
                remember_data.to_csv('data/userRemember.csv')
                audio('Remember', row['remember'])
                break
    
    audio(chatbot_tools.random_output('bye').replace('<user-name>', user_data['first name']))

def set_passcode_function():
    with open('data/user passcode.txt', 'r') as f:
        passcode = f.read()
        
    if passcode == '':
        audio(chatbot_tools.random_output('speak passcode'))
    else:
        audio(chatbot_tools.random_output('current passcode'))

def youtube_video_function():
    internet = check_internet()
    if internet == 0:
        audio(chatbot_tools.random_output('choose video'))
    else:
        audio(chatbot_tools.random_output('no internet'))

def advice_function():
    with open('data/datasets/advice.txt', 'r') as f:
        advice = f.readlines()
        
    audio(random.choice(advice))
    
def bot_version_function():
    with open('data/version.txt', 'r') as f:
        version = f.read()
    audio(chatbot_tools.random_output('version'))

def knowledge_user_function():
    user_data = chatbot_tools.get_user_data()
    audio('Here are the things that I know about you')
    if user_data['first name'] != '':
        audio(f"Your first name is {user_data['first name']}")
    if user_data['middle name'] != '':
        audio(f"Your middle name is {user_data['middle name']}")
    if user_data['surename'] != '':
        audio(f"Your surname is {user_data['surename']}")
    if user_data['dob'] != '':
        audio(f"Your date of birth is {user_data['dob']}")
    if user_data['nickname'] != '':
        audio(f"Your nickname is {user_data['nickname']}")
    if user_data['hobbies/interest'] != '':
        audio(f"These are your hobbies and interests {user_data['hobbies/interests']}")
    if user_data['favourite song'] != '':
        audio(f"Your favourite song is {user_data['favourite song']}")
    if user_data['favourite music genre'] != '':
        audio(f"Your favourite music genre is {user_data['favourite music genre']}")
    if user_data['favourite film'] != '':
        audio(f"Your favourite film is {user_data['favourite film']}")
    if user_data['favourite food'] != '':
        audio(f"Your favourite food is {user_data['favourite food']}")
    if user_data['favourite book'] != '':
        audio(f"Your favourite book is {user_data['favourite book']}")
    if user_data['disliked food'] != '':
        audio(f"You dislike {user_data['disliked food']}")
    if user_data['disabilities'] != '':
        audio(f"You have {user_data['disability']}")
    if user_data['number of pets'] != '':
        audio(f"You have {user_data}")
    if user_data['name of pets'] != '':
        audio(f"The name of your pets are {user_data['name of pets']}")
    if user_data['places visited'] != '':
        audio(f"The places you have visited are {user_data['places visited']}")

def weather_for_area_function(user_input):
    user_input = user_input.split('for ')
    weather_for_area(user_input[1])
    
def scan_url_function():
    website_url = copy_website_url()
    scan_url(website_url)

def scan_copied_url_function():
    website_url = get_copied_text()
    scan_url(website_url)
    
def remember_function(user_input):
    from Joan import memory
    memory.remember(user_input)
    return 'reload data'

def search_food_function(user_input):
    search_food(user_input.replace('show', '').replace('recipies', '').replace('search', '').replace('for', '').replace('how', '').replace('to', '').replace('bake', '').replace('cook', '').rstrip().lstrip())
    
def search_ingredients_function(user_input):
    search_food_ingriedents(user_input.replace('ingredients', '').replace('ingredients', '').replace('for', ''))

def where_object_function(user_input):
    remember = pd.read_csv('data/userRemember.csv')

    for index, row in remember.iterrows():
        keyword = row['output'].split('***')
        if keyword[0] in user_input:
            audio(keyword[1])#this is the sentence rather than the keyword
    
            #remove from the userRemember.csv
            remember = remember.drop(index, axis=0)
            remember.to_csv('data/userRemember.csv')
            
            ET = pd.read_csv('data/datasets/ET.csv')
            ET = ET[~ET['name'].str.contains(user_input.split()[-1], case=False)]
            ET.to_csv('data/datasets/ET.csv', index=False)
    return 'reload data'




#the keys in this are the entity that the machine learning returns not the user input.
#if the value is a string and not a function then this just needs a random output based on that string
#the handle_entity function at the bottom of this file deals with the passing of arguments
    
response_map = {
    "greeting": greeting,
    "been while": been_while,
    "how are you": how_are_you,
    "play blackjack": games.blackjack,
    "play guessing game": games.numberGuess,
    "play rps": games.rps,
    "tell joke": tell_joke,
    "tell riddle": tell_riddle,
    "fact": facts,
    "wiki game": games.open_wiki_game,
    "xkcd": games.xkcd,
    "random wikihow article": wikihow,
    "factory reset": factory_reset_function,
    "how to": how_to_function,
    "search wikihow": "wikihow search read or open",
    "akinator": games.akinator,
    "list games": games.game_list,
    "describe akinator": "explain akinator",
    "describe wiki game": "explain wiki game",
    "bye": bye_function,
    "thank": "thank",
    "set passcode": set_passcode_function,
    "play game": "suggest play game",
    "what is passcode": "explain passcode",
    "current weather": current_weather,
    "weather tomorrow": weather_tomorrow,
    "weather day": current_weather,
    "choose youtube video": youtube_video_function,
    "users name": "tell user name",
    "advice": advice_function,
    "question amount": "amount of questions data",
    "chewie": "chewie",
    "wax on": "wax off",
    "i get you pretty": "dog too",
    "mama says": "stupid",
    "father": "father",
    "who are you": "who are you",
    "call bot": "call bot",
    "why named": "why named",
    "love user": "love user",
    "robot": "not robot",
    "human": "not human",
    "change bot name": "change bot name",
    "real or not": "real or not",
    "last night": "last night",
    "what doing": "what doing",
    "what next": "what next",
    "collection": "bot collection",
    "bot hobby": "bot hobby",
    "talk request": "talk request",
    "question bot": "question",
    "something": "something",
    "not talking bot": "not talking bot",
    "bot live forever": "bot live forever",
    "bot favourite": "bot favourite",
    "created": "created",
    "gender": "gender",
    "bot version": bot_version_function,
    "user thinking": "user thinking",
    "knowledge about user": knowledge_user_function,
    "time": tell_time,
    "date": tell_date,
    "day": tell_day,
    "month": tell_month,
    "year": tell_year,
    "weather monday": lambda: weather_day('monday'),
    "weather tuesday": lambda: weather_day('tuesday'),
    "weather wednesday": lambda: weather_day("wednesday"),
    "weather thursday": lambda: weather_day('thursday'),
    "weather friday": lambda: weather_day("friday"),
    "weather saturday": lambda: weather_day("saturday"),
    "weather sunday": lambda: weather_day("sunday"),
    "weather hour": weather_hour_advanced,
    "specific weather location": weather_for_area_function,
    "latest news": read_latest_news,
    "scan open website": scan_url_function,
    "scan copied website": scan_copied_url_function,
    "space news": read_space_news,
    "remember": remember_function,
    "remember that": remember_function,
    "search": search_food_function,
    "ingredients": search_ingredients_function,
    "meal suggestion": suggest_meal,
    "where object": where_object_function
}

def handle_entity(entity, user_input):
    user_data = chatbot_tools.get_user_data()
    
    # this was originally being used to check whether arguments needed to be passed to a function that is being called, but a better way has been implimented so that arguments can be specified in the response_map
    try: #try to run as a function passing user_input argument to the function
        return "function", response_map.get(entity, lambda user_input: None)(user_input)
    except TypeError:#if the user_input cannot be passed
        try:#try calling function without passing anything
            return "function", response_map.get(entity, lambda: None)()
        except TypeError:#if function can't be called then it must be an output
            return "output", chatbot_tools.random_output(response_map.get(entity).replace('<user-name>', user_data['first name']))