#from gradio_client import Client #only needed if using hugging face spaces api
import csv, random, json, datetime, requests, re
from collections import Counter
import pandas as pd
from functools import lru_cache
import nltk
from nltk import RegexpParser, sent_tokenize, word_tokenize, pos_tag, Tree, ne_chunk
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('maxent_ne_chunker_tab')
#nltk.download('words')

#files
from mistral_Joan import *

client = ElevenLabs(
  api_key="af1726bdbe04b294ff49ba28316bbebb",
)

#finding food in text
patterns="""
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    {<NP><CC><NP>}
    {<RB><JJ>*<NN*>+}
    """
NPChunker = RegexpParser(patterns) 
    
class process_text_tools():
    def calculate_class_weights(y_train):
        '''
        calculates the class weights based on class frequencies
        y_train: a list of class labesl for training data
        '''
        
        class_counts = Counter(y_train)
        total_count = len(y_train)
        class_weights = {label: total_count/(count *len(set(y_train))) for label, count in class_counts.items()}
        
        return class_weights
    
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def fix_json(json_string):
        # Remove any extra characters and ensure JSON structure has the correct closing
        json_string = json_string.strip()
        
        # Attempt to add a missing closing brace if not present
        if not json_string.endswith("}"):
            json_string += "}"
            
        # Look for common formatting issues and correct them
        json_string = re.sub(r",\s*}", "}", json_string)  # Remove trailing commas before closing brace
        json_string = re.sub(r",\s*\]", "]", json_string)  # Remove trailing commas before closing bracket
        
        return json_string

class chatbot_tools():       
    def extract_website_name(url):
        pattern = re.compile(r'https?://([^/]+)')
        match = pattern.match(url)
        if match:
            return match.group(1)
        else:
            return None
    
    @staticmethod
    @lru_cache(maxsize=None)
    def big_guns(user_input):
        # This function is to use wolfram alpha.        
        audio('Big guns running')
        user_data = chatbot_tools.get_user_data()
        response = requests.get(f'https://api.wolframalpha.com/v2/query?input={user_input.replace(" ", "+")}&format=plaintext&output=JSON&appid=E96E34-TYEKWH2QKL')
        if response.status_code == 200:
            data = response.json()
            data_type = data['queryresult']['datatypes']

            try:
                if data_type == 'Math':#if it's a maths question format the output
                    audio("The answer to your math question is: " + str(data['queryresult']['pods'][1]['subpods'][0]['plaintext']))
                else: #if not maths question just output result
                    answer = (data['queryresult']['pods'][1]['subpods'][0]['plaintext'])
                    audio(answer)

                    ET_pd = pd.read_csv('data/datasets/ET.csv')#load csv file
                    
                    new_data = {'name': user_input.lower().lstrip().rstrip(), 'ET': answer.replace('\n', '\\n')}
                    
                    ET_pd.loc[len(ET_pd)] = new_data
                    ET_pd.to_csv('data/datasets/ET.csv', index=False)
            except KeyError:
                audio(chatbot_tools.random_output('Unable to respond').replace('<user-name>', user_data['first name']))
           
    def day_to_date(target_day):
        # Define a dictionary to map day names to corresponding integers
        day_to_int = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        current_date = datetime.datetime.now()
        current_day = current_date.weekday()
        days_to_target_day = (day_to_int[target_day.lower()] - current_day) % 7
        next_target_day = current_date + datetime.timedelta(days=days_to_target_day)
        formatted_date = next_target_day.strftime('%Y-%m-%d')

        return formatted_date

    def get_user_name(text):
        text = text.title()
        # Tokenize the text and perform part-of-speech tagging
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        # Use NLTK's NER to find names
        named_entities = ne_chunk(tagged)

        # Extract names from the named entities
        names = []
        for entity in named_entities:
            if isinstance(entity, nltk.Tree):
                name = " ".join([word for word, pos in entity.leaves()])
                names.append(name)

        return names
    
    def restart_program():
        import sys, subprocess
        
        python = sys.executable
        script = sys.argv[0]
        subprocess.Popen([python, script])
        sys.exit()
        
    def process_input_to_numbers(text):
        try:
            from word2number import w2n
            get_number = w2n.word_to_num(text)
            return get_number
        except ValueError:
            return 'unknown'
        
    @staticmethod
    @lru_cache(maxsize=None)
    def write_user_data(new_user="", first_name="", middle_name="", surname="", dob="", nickname="", age="", gender="",
                        hobby="", fix_boredom="", f_song="", f_music_genre="", f_film="", f_book="", 
                        f_food="", dislike_food="", disability="", pet_amount="", type_pet="", name_pet="",
                        education="", work="", visited_places="", living_place='', news_interest="", 
                        news_hate="", city='', country='', location_key='', band_news_site=''):
        
        file_path = 'data/user_data.json'  # Update the file path to point to your JSON file
        
        # Read the existing data
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"users": [{}]}  # Initialize a default structure if the file doesn't exist or is empty
        
        # Ensure we have a user at index 0
        user_data = data["users"][0] if data.get("users") else {}
        
        # Update user data with provided values
        user_data.update({
            "new user": new_user if new_user else user_data.get("new user", "false"),
            "first name": first_name or user_data.get("first name", ""),
            "middle name": middle_name or user_data.get("middle name", ""),
            "surname": surname or user_data.get("surname", ""),
            "dob": dob or user_data.get("dob", ""),
            "nickname": nickname or user_data.get("nickname", ""),
            "age": age or user_data.get("age", ""),
            "gender": gender or user_data.get("gender", ""),
            "fix boredom": fix_boredom or user_data.get("fix boredom", ""),
            "F-song": f_song or user_data.get("F-song", ""),
            "F-music genre": f_music_genre or user_data.get("F-music genre", ""),
            "F-film": f_film or user_data.get("F-film", ""),
            "F-book": f_book or user_data.get("F-book", ""),
            "F-food": f_food or user_data.get("F-food", ""),
            "disliked food": user_data.get("disliked food", []),
            "disabilities": disability or user_data.get("disabilities", ""),
            "amount of pets": pet_amount or user_data.get("amount of pets", ""),
            "type of pets": type_pet or user_data.get("type of pets", ""),
            "name of pets": user_data.get("name of pets", []),
            "education": education or user_data.get("education", ""),
            "work": work or user_data.get("work", ""),
            "visited places": user_data.get("visited places", []),
            "living location": living_place or user_data.get("living location", ""),
            "news interest": user_data.get("news interest", []),
            "news hate": user_data.get("news hate", []),
            "city": city or user_data.get("city", ""),
            "country": country or user_data.get("country", ""),
            "location key": location_key or user_data.get("location key", ""),
            "band news site": user_data.get("band news site", "")
        })

        # Handle appending multiple disliked food, names of pets, visited places, news interest, and news hate
        if dislike_food:
            food_data = user_data['disliked food']
            food_list = [food.strip() for food in dislike_food.split(',')]
            user_data['disliked food'] = list(set(food_data + food_list))

        if visited_places:
            visit_data = user_data['visited places']
            visit_list = [place.strip() for place in visited_places.split(',')]
            user_data['visited places'] = list(set(visit_data + visit_list))

        if news_interest:
            interest_data = user_data['news interest']
            interest_list = [news.strip() for news in news_interest.split(',')]
            user_data['news interest'] = list(set(interest_data + interest_list))

        if news_hate:
            hate_data = user_data['news hate']
            hate_list = [news.strip() for news in news_hate.split(',')]
            user_data['news hate'] = list(set(hate_data + hate_list))

        # Handle hobby data generation
        if hobby:
            # Check if the hobby already exists
            hobby_data = user_data.get('hobbies', [])
            
            duplicate_found = any(
                item.get("hobby", "").strip().lower() == hobby.strip().lower() for item in user_data["hobbies"]
            )

            if duplicate_found:
                return

            # Retry mechanism for generating hobby data
            #generated_data = generate(f"Provide a simple, informative JSON structure about the hobby '{hobby}' Include: description as a concise explanation of what the hobby involves, type as the category of this hobby (e.g., 'musical instrument'), and the skill level of this hobby (easy, medium, hard). Keep the description strictly relevant, clear, and avoid unrelated details or filler words.").replace('</s>', '')
            #print("=====\n", generated_data, "\n=====")

            generated_data = generate(
                f"Provide a JSON structure for the hobby '{hobby}' in the following format:\n\n"
                f"{{\n"
                f"    \"hobby\": \"{hobby}\",\n"
                f"    \"description\": \"[A concise explanation of what the hobby involves]\",\n"
                f"    \"type\": \"[Category of the hobby, e.g., 'Visual Art']\",\n"
                f"    \"skill_level\": \"[Skill level required: Easy, Medium, Hard]\"\n"
                f"}}\n\n"
                "Ensure the JSON structure is valid, and replace only the placeholder descriptions and values in brackets with actual details relevant to the hobby."
            )

            print(generated_data)#***

            # Clean the generated data
            cleaned_data = chatbot_tools.clean_json_data(generated_data)

            try:
                # Attempt to load the cleaned JSON data
                hobby_data = json.loads(cleaned_data)

                # Ensure hobby_data is a dictionary
                if isinstance(hobby_data, dict):
                    # Ensure 'hobbies' key exists
                    if 'hobbies' not in user_data:
                        user_data['hobbies'] = []

                    # Append the new hobby data
                    user_data['hobbies'].append(hobby_data)
                else:
                    print("Generated hobby data is not a valid dictionary.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for hobby: {e} - Data: {cleaned_data.strip()}")

        # Ensure the users list contains the updated user_data
        if "users" in data and data["users"]:
            data["users"][0] = user_data
        else:
            data["users"] = [user_data]

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def clean_json_data(json_data):
        """
        Clean the generated JSON data by removing newlines, non-printable characters, and formatting it.
        """
        cleaned_data = re.sub(r'[\r\n]+', '', json_data)  # Remove newlines
        cleaned_data = re.sub(r'[^\x20-\x7E]+', '', cleaned_data)  # Remove non-printable characters
        cleaned_data = re.sub(r'^\s*{', '{', cleaned_data)  # Remove leading whitespace before '{'
        cleaned_data = re.sub(r'\s*}$', '}', cleaned_data)  # Remove trailing whitespace after '}'
        cleaned_data = re.sub(r',\s*', ', ', cleaned_data)  # Add a single space after commas
        return cleaned_data

    @staticmethod
    @lru_cache(maxsize=None)
    def get_user_data():
        file_path = 'data/user_data.json'
        try:
            with open(file_path, 'r') as f:
                user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return empty dict if file does not exist or is unreadable

        # Access the user data within the "users" array
        user_info = user_data.get("users", [{}])[0]
        
        # Return both user-specific and top-level data
        memory_data = {
            'index': user_info.get('index', ''),
            'new user': user_info.get('new user', ''),
            'first name': user_info.get('first name', ''),
            'middle name': user_info.get('middle name', ''),
            'surname': user_info.get('surname', ''),
            'dob': user_info.get('dob', ''),
            'nickname': user_info.get('nickname', ''),
            'age': user_info.get('age', ''),
            'gender': user_info.get('gender', ''),
            'hobby': user_info.get('hobby', {}),
            'fix boredom': user_info.get('fix boredom', ''),
            'favourite song': user_info.get('F-song', ''),
            'favourite music genre': user_info.get('F-music genre', ''),
            'favourite food': user_info.get('F-food', ''),
            'favourite book': user_info.get('F-book', ''),
            'favourite film': user_info.get('F-film', ''),
            'disliked food': user_info.get('disliked food', ''),
            'disabilities': user_info.get('disabilities', ''),
            'number of pets': user_info.get('amount of pets', ''),
            'name of pets': user_info.get('name of pets', ''),
            'type of pets': user_info.get('type of pets', ''),
            'education': user_info.get('education', ''),
            'work': user_info.get('work', ''),
            'places visited': user_info.get('visited places', ''),
            'living location': user_info.get('living location', ''),
            'news interest': user_info.get('news interest', ''),
            'news hate': user_info.get('news hate', ''),
            'city': user_data.get('city', ''),
            'country': user_data.get('country', ''),
            'location key': user_data.get('location key', ''),
            'band news site': user_info.get('band news site', '')
        }

        return memory_data
    
    def open_file(filename, file='r', text=None):
        try:
            text = str(text)
            with open(filename, file) as f:
                if file == 'r':
                    read_file = f.read()
                    return read_file
                else:
                    f.write(text)
        except FileNotFoundError:
            raise FileNotFoundError
                
    def random_output(tag):
        try:
            df = pd.read_csv("data/datasets/responses.csv", encoding="utf-8")
        
            # find the matching row to the tag
            matching_rows = df[df["ET"] == tag]
            
            if matching_rows.empty:
                raise ValueError(f"No matching rows found for tag: {tag}")
            
            expected_context = matching_rows.iloc[0, 1]
            responses = matching_rows.iloc[0, 2:].dropna().tolist()
            
            if not responses:
                raise ValueError("No responses foudn for the given tag")
            
            random_response = random.choice(responses)
            print(expected_context)
            with open("data/expected context.txt", 'w') as f:
                f.write(expected_context)
                
            return random_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error has occurred and an output cannot be produced"

class text_tools():
    def prepare_text(text):
        sentences = sent_tokenize(text)#nltk
        sentences = [word_tokenize(sent) for sent in sentences]#nltk 
        sentences = [pos_tag(sent) for sent in sentences]#nltk
        sentences = [NPChunker.parse(sent) for sent in sentences]
        return sentences


    def parsed_text_to_NP(sentences):
        nps = []
        for sent in sentences:
            tree = NPChunker.parse(sent)
            #audio(tree)
            for subtree in tree.subtrees():
                if subtree.label() == 'NP':
                    t = subtree
                    t = ' '.join(word for word, tag in t.leaves())
                    nps.append(t)
        return nps


    def sent_parse(text):
        sentences = text_tools.prepare_text(text)
        nps = text_tools.parsed_text_to_NP(sentences)
        return '-'.join(nps).replace('favourite food', '').replace(text, '')
    
    def find_food(text):
        from inflect import engine
        text = "favourite food is " + text
        p = engine()#inflect
        
        singular_word = p.singular_noun(text)

        if singular_word == False:
            return text_tools.sent_parse(text).replace('-', '').replace("favoutie food is ", '')
        else:
            return text_tools.sent_parse(singular_word).replace('-', '').replace("favoutie food is ")
      
def audio(text):
    try:    
        audio = client.generate(
                text = text,
                model="eleven_multilingual_v2",
                voice=Voice(
                voice_id='r1E4x9gdvKI4ah2XK8th',
                settings=VoiceSettings(stability=0.55, similarity_boost=0.2, style=0.35, use_speaker_boost=True)            
            )
        )
    
        play(audio)
    except Exception as e:
        print(text)

def check_internet():
    try:
        import requests
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return 0
    except requests.ConnectionError:
        return 1
    
def get_ip_address():
    '''
    Gets the user's device IP address.
    This used to use https://api64.ipify.org but that had a limit of 1000 requests
    '''
    #import requests
    #response = requests.get('https://api64.ipify.org?format=json').json()
    #return response['ip']

    import requests

    url = 'https://api.ipify.org'
    response = requests.get(url)
    ip = response.text
    
    return ip


def get_location_key():
    '''
    Gets the location key from accuweather api which uses the user's IP address
    '''
    import requests
    
    weather_api_key = 'F7DxhfQx1EoPuopgN59Tq0OkGRJwVkWQ'
    user_data = chatbot_tools.get_user_data()
    city = user_data['city']
    
    # Define the city you want to get the location key for
    city_name = city  # Replace with your desired city

    # AccuWeather API endpoint for location search
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"

    # Parameters for the API request
    params = {
        'apikey': weather_api_key,
        'q': city_name,
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
    
        # Assuming you want the first result
        if data:
            location_key = data[0]['Key']
            return location_key
    else:
        pass

def get_ip_data():
    '''
    Gets data from the IP address including city and country the user's device is in
    '''
    import ipinfo
    internet = check_internet()
    if internet == 0:
        try:
            ip_address = get_ip_address()#get the device ip address
            handler = ipinfo.getHandler('')#no api key or token for limited info
            details = handler.getDetails(ip_address)
            city, country = details.city, details.country_name
            
            chatbot_tools.write_user_data(city=city, country=country)#write city and country to user data
            location_key = get_location_key()
            chatbot_tools.write_user_data(location_key=location_key)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        pass
    
def copy_website_url():
    from pyperclip import paste
    from pyautogui import hotkey, press
    
    hotkey('alt', 'tab')
    hotkey('ctrl', 'l')
    hotkey('ctrl', 'c')
    press('esc')
    hotkey('alt', 'tab')

    return paste()

def get_copied_text():
    from pyperclip import paste
    
    return paste()

def recipe_by_title(title):
    title = title.lower().rstrip().lstrip().replace('&', 'and')
    with open('data/datasets/recipies.json', 'r') as json_file:
        data_list = json.load(json_file)
        
        for data_dict in data_list:
            meals = data_dict.get('meals', [])
            try:
                meal = [m for m in meals if title in m.get('strMeal').lower().replace('&', 'and')]
                if meal != []:
                    return meal
            except TypeError:
                pass
    return None


#Ask the user for their hobby
#chatbot_tools.write_user_data.cache_clear()
#chatbot_tools.get_user_data.cache_clear()

#chatbot_tools.write_user_data(hobby='dancing')

