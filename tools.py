import re, csv, random, re, requests, sys, subprocess, json, datetime
import pandas as pd
from word2number import w2n
import nltk
from nltk import RegexpParser, sent_tokenize, word_tokenize, pos_tag, Tree, ne_chunk
from inflect import engine

#finding food in text
patterns="""
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    {<NP><CC><NP>}
    {<RB><JJ>*<NN*>+}
    """
NPChunker = RegexpParser(patterns)
    
class process_text_tools():
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def conversation_memory(user_input):
        with open('data/conversation.csv', 'r', newline='', encoding='utf8') as file:
            reader = csv.reader(file)
            next(reader)
            
            for row in reader:
                if row[0] == user_input:
                    return row[1]
        return None

class chatbot_tools():
    def big_guns(user_input):
        user_data = chatbot_tools.get_user_data()
        response = requests.get(f'https://api.wolframalpha.com/v2/query?input={user_input.replace(" ", "+")}&format=plaintext&output=JSON&appid=E96E34-TYEKWH2QKL')
        if response.status_code == 200:
            data = response.json()
            data_type = data['queryresult']['datatypes']

            try:
                if data_type == 'Math':
                    print("The answer to your math question is: " + str(data['queryresult']['pods'][1]['subpods'][0]['plaintext']))
                else:
                    print(data['queryresult']['pods'][1]['subpods'][0]['plaintext'])
            except KeyError:
                print(chatbot_tools.random_output('Unable to respond').replace('<user-name>', user_data['first name']))

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

        # Get the current date
        current_date = datetime.datetime.now()

        # Calculate the current day of the week (0 for Monday, 1 for Tuesday, etc.)
        current_day = current_date.weekday()

        # Calculate the number of days to the target day
        days_to_target_day = (day_to_int[target_day.lower()] - current_day) % 7

        # Calculate the date for the upcoming target day
        next_target_day = current_date + datetime.timedelta(days=days_to_target_day)

        # Format the date in the desired format (e.g., 'YYYY-MM-DD')
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
        python = sys.executable
        script = sys.argv[0]
        subprocess.Popen([python, script])
        sys.exit()
        
    def process_input_to_numbers(text):
        try:
            get_number = w2n.word_to_num(text)
            return get_number
        except ValueError:
            return 'unknown'
        
    def write_user_data(first_name="",middle_name="",surname="",dob="",nickname="",age="",gender="",interests="",fix_boredom="",f_song="",f_music_genre="",f_film="",f_book="",f_food="",dislike_food="",disability="",
                        pet_amount="",type_pet="",name_pet="",education="",work="",visited_places="",living_place='',news_interest="",news_hate="",city='',country='', location_key=''):

        file_path = 'data/user data.csv'
        data = []
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        
        if first_name != '':
            data[0]['first name'] = first_name
        if middle_name != '':
            data[0]['middle name'] = middle_name
        if surname != '':
            data[0]['surname'] = surname
        if dob != '':
            data[0]['dob'] = dob
        if nickname != '':
            data[0]['nickname'] = nickname
        if age != '':
            data[0]['age'] = age
        if gender != '':
            data[0]['gender'] = gender
        if interests != '':
            data[0]['interests/hobbies'] = interests
        if fix_boredom != '':
            data[0]['fix bordem'] = fix_boredom
        if f_song != '':
            data[0]['F-song'] = f_song
        if f_music_genre != '':
            data[0]['F-music genre'] = f_music_genre
        if f_film != '':
            data[0]['F-film'] = f_film
        if f_book != '':
            data[0]['F-book'] = f_book
        if f_food != '':
            data[0]['F-food'] = f_food
        if dislike_food != '':
            data[0]['disliked food'] = dislike_food
        if disability != '':
            data[0]['disabilities'] = disability
        if pet_amount != '':
            data[0]['amount of pets'] = pet_amount
        if type_pet != '':
            data[0]['type of pets'] = type_pet
        if name_pet != '':
            data[0]['name of pets'] = name_pet
        if education != '':
            data[0]['education'] = education
        if work != '':
            data[0]['work'] = work
        if visited_places != '':
            data[0]['visited places'] = visited_places
        if living_place != '':
            data[0]['living location'] = living_place
        if news_interest != '':
            data[0]['news interest'] = news_interest
        if news_hate != '':
            data[0]['news hate'] = news_hate
        if city != '':
            data[0]['city'] = city
        if country != '':
            data[0]['country'] = country
        if location_key != '':
            data[0]['location key'] = location_key

        with open(file_path, mode='w', newline='') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(data[0])

            
    def get_user_data():      
        user_data = pd.read_csv('data/user data.csv', )

        #user info from csv file
        index = user_data['index'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        first_name = user_data['first name'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        middle_name = user_data['middle name'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        surename = user_data['surname'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        dob = user_data['dob'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        nickname = user_data['nickname'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        age = user_data['age'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        gender = user_data['gender'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        interests_hobbies = user_data['interests/hobbies'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        fix_bordem = user_data['fix bordem'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        F_song = user_data['F-song'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        F_song_genre = user_data['F-music genre'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        F_food = user_data['F-food'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        F_book = user_data['F-book'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        F_film = user_data['F-film'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        disliked_food = user_data['disliked food'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        disabilities = user_data['disabilities'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        amount_of_pets = user_data['amount of pets'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        name_of_pets = user_data['name of pets'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        type_of_pets = user_data['type of pets'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        education = user_data['education'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        work = user_data['work'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        visited_places = user_data['visited places'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        living_location = user_data['living location'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        news_interest = user_data['news interest'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        news_hate = user_data['news hate'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        city = user_data['city'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '').replace('0', '')
        country = user_data['country'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')
        location_key = user_data['location key'].to_string().replace('0    ', '').replace('Series([], )', '').replace('0   NaN', '').replace('   NaN', '')

        memory_data = {'index': index,'first name': first_name,'middle name': middle_name,'surename': surename,
                       'dob': dob,'nickname': nickname,'age': age,'gender': gender,
                       'hobbies/interest': interests_hobbies,'fix bordem': fix_bordem,'favourite song': F_song,
                       'favoute music genre': F_song_genre,'favourite book': F_book,'favourite film': F_film,
                       'favourite food': F_food,'disliked food': disliked_food,'disabilities': disabilities,
                       'number of pets': amount_of_pets,'name of pets': name_of_pets,'type of pets': type_of_pets,
                       'education': education,'work': work,'places visited': visited_places,'living location': living_location,
                       'news interest': news_interest,'news hate': news_hate,'city':city, 'country':country,
                       'location key':location_key}
        
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
        with open('data/responses.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)

            matching_rows = [row[1:] for row in reader if row[0] == tag]
            expected_context = matching_rows[0][:1]
            matching_rows = matching_rows[0][1:]
            if not matching_rows:
                print('An error as occured and an output cannont be produced.')
            
            random_output = random.choice(matching_rows)

            chatbot_tools.open_file(filename='data/expected context.txt', file='w', text=expected_context[0])
            
            return random_output

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
            #print(tree)
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
        text = "favourite food is " + text
        p = engine()#inflect
        
        singular_word = p.singular_noun(text)

        if singular_word == False:
            return text_tools.sent_parse(text).replace('-', '').replace("favoutie food is ", '')
        else:
            return text_tools.sent_parse(singular_word).replace('-', '').replace("favoutie food is ")
        
def check_internet():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return 0
    except requests.ConnectionError:
        return 1
    
def get_ip_address():
    '''
    Gets the user's device IP address
    '''
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response['ip']

def get_location_key():
    '''
    Gets the location key from accuweather api which uses the user's IP address
    '''
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
    internet = check_internet()
    if internet == 0:
        ip_address = get_ip_address()#get the device ip address
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')#get data from the ip
        
        if response.status_code == 200:
            response = response.json()
            city = response.get('city')#get the city
            country = response.get('country_name')#get the country

            chatbot_tools.write_user_data(city=city,country=country)#write city and country to user data

            location_key = get_location_key()#get the location key for the city
    
            chatbot_tools.write_user_data(location_key=location_key)
        elif response.status_code == 429:#this means that too many requests have been made in x time
            #free tier used for https://ipapi.co/ 1000 in 24 hours 30,000 in a month
            pass
    else:
        pass