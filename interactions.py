import random, webbrowser, html, requests, json, datetime
from nltk.corpus.reader import udhr
import pandas as pd
from youtubesearchpython import VideosSearch
from tools import *

weather_api_key = 'F7DxhfQx1EoPuopgN59Tq0OkGRJwVkWQ'

class bordem_entertainment():
    def play_game():
        print(chatbot_tools.random_output('play which game'))
    
    def play_video():
        user_video = input(chatbot_tools.random_output('which video') + '\n>>> ')
        videoResults = VideosSearch(user_video, limit=1)
        webbrowser.open(videoResults.result()['result'][0]['link'])
        
class games():      
    def rps():
        user_data = chatbot_tools.get_user_data()
        bot_answer = random.choice(['Rock', 'Paper', 'Scissors'])
        user_answer = input('You can just say R for rock, P for paper, and S for scissors. Ready... Rock... Paper... Scissors... Shoot.')
    
        while user_answer.lower() not in ['rock', 'paper', 'scissors', 'r', 'p', 's']:
            pass #invalid input
        if user_answer.lower() == bot_answer:
            print(chatbot_tools.random_output('rps tie'))
        elif (
            (user_answer.lower() == 'rock' and bot_answer == 'scissors' or user_answer.lower() == 'r' and bot_answer == 'scissors') or
            (user_answer.lower() == 'paper' and bot_answer == 'rock'  or user_answer.lower() == 'p' and bot_answer == 'rock') or
            (user_answer.lower() == 'scissors' and bot_answer == 'paper'  or user_answer.lower() == 's' and bot_answer == 'paper')
        ):
            print('I chose ' + bot_answer)
            print(chatbot_tools.random_output('rps win').replace('<user-name>', user_data['first name']))
        else:
            print('I chose ' + bot_answer)
            print(chatbot_tools.random_output('rps lose').replace('<user-name>',user_data['first name']))
            
    def numberGuess():
        user_data = chatbot_tools.get_user_data()
        random_number = random.randint(1, 100)
        print('Okay I have my number.')
        
        run_game = True
        while run_game is True:
            user_guess = int(input('Now take a guess. Any number between 1 and 100.'))
            
            if user_guess > random_number and user_guess < 100:
                print('Too high. Try again.')
            elif user_guess < random_number and user_guess > 0:
                print('Too low. Try again.')
            elif user_guess < 0:
                print(chatbot_tools.random_output('number too low'))
            elif user_guess > 100:
                print(chatbot_tools.random_output('number to high'))
            elif user_guess == random_number:
                print(chatbot_tools.random_output('guess number win').replace('<user-name>', user_data['first name']))
                run_game = False
            else:
                print(chatbot_tools.random_output('incorrect number guess'))
                
    def blackjack(user_input):
        def create_deck():
            deck = []
            for suit in suits:
                for rank in ranks:
                    deck.append((rank, suit))
            return deck
        
        def deal_card(deck, hand):
            card = deck.pop()
            hand.append(card)
        
        def calculate_hand_value(hand):
            value = 0
            num_aces = 0
            for card in hand:
                rank = card[0]
                value += values[rank]
                if rank == 'Ace':
                    num_aces += 1
            while value > 21 and num_aces:
                value -= 10
                num_aces -= 1
            return value
        
        user_data = chatbot_tools.get_user_data()
        
        user_game_name = 'blackjack'
        if 'blackjack' in user_input.lower():
            user_game_name = 'blackjack'
        elif 'twenty one' in user_input.lower() or '21' in user_input.lower():
            user_game_name = 'twenty one'
        elif 'pontoon' in user_input.lower():
            user_game_name = 'pontoon'
        
        print(chatbot_tools.random_output('welcome blackjack game').replace('<game-name>', user_game_name))
        
        # Define card ranks, suits, and values
        suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
        ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
        values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
                  'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

        deck = create_deck()
        random.shuffle(deck)

        player_hand = []
        dealer_hand = []

        for _ in range(2):
            deal_card(deck, player_hand)
            deal_card(deck, dealer_hand)

        while True:
            print("\nYour Hand:")
            for card in player_hand:
                print(f"{card[0]} of {card[1]}")
            player_value = calculate_hand_value(player_hand)
            print(f"Total Value: {player_value}")

            if player_value == 21:
                print("Blackjack!")
                print(chatbot_tools.random_output('user win blackjack').replace('<user-name>', user_data['first name']))
                break
            elif player_value > 21:
                print("Bust!")
                print(chatbot_tools.random_output('dealer win blackjack').replace('<user-name>', user_data['first name']))
                break

            action = input("Do you want to 'hit' or 'stand'? ").lower()
            if 'hit' in action or action == 'h':
                deal_card(deck, player_hand)
            elif 'stand' in action or action == 's':
                while calculate_hand_value(dealer_hand) < 17:
                    deal_card(deck, dealer_hand)
                print("\nDealer's Hand:")
                for card in dealer_hand:
                    print(f"{card[0]} of {card[1]}")
                dealer_value = calculate_hand_value(dealer_hand)
                print(f"Total Value: {dealer_value}")
                if dealer_value > 21:
                    print("Dealer busts!")
                    print(chatbot_tools.random_output('user win blackjack').replace('<user-name>', user_data['first name']))
                elif dealer_value >= player_value:
                    print(chatbot_tools.random_output('dealer win blackjack').replace('<user-name>', user_data['first name']))
                else:
                    print(chatbot_tools.random_output('user win blackjack').replace('<user-name>', user_data['first name']))
                break
        
        print(chatbot_tools.random_output('play blackjack again'))
        
    def open_wiki_game():
        webbrowser.open('https://www.thewikigame.com/group')
    
    def xkcd():
        number = random.randint(0, 2801)
        webbrowser.open(f"https://xkcd.com/{number}/")
    
    def akinator():
        webbrowser.open('https://en.akinator.com/theme-selection')
    
    def game_list():
        games = '\n'.join(['blackjack','number guess','wiki game','akinator'])
        print(chatbot_tools.random_output('list playable games').replace('<list-games>', games))

def tell_joke():
    jokes_data = pd.read_csv('data/jokes.csv')
    
    random_joke = jokes_data.iloc[random.randint(0, len(jokes_data))]
    
    setup_joke = random_joke['setup']
    punchline = random_joke['punchline']
    
    for column, value in random_joke.items():
        if not pd.isna(punchline):
            print(setup_joke)
            print(punchline)
            break
        else:
            print(setup_joke)
            break
    
def tell_riddle():
    user_data = chatbot_tools.get_user_data()
    riddles_data = pd.read_csv('data/riddles.csv')

    random_riddle = riddles_data.iloc[random.randint(0, len(riddles_data))]
    riddle_question = random_riddle['question']
    riddle_answer = random_riddle['answer']
    
    user_answer = input(riddle_question + '\n>>> ').lower()
    if riddle_answer in user_answer:
        print(chatbot_tools.random_output('correct riddle').replace('<user-name>', user_data['first name']).replace('<riddle-answer>', riddle_answer))
    else:
        print(chatbot_tools.random_output('incorrect riddle').replace('<user-name>', user_data['first name']).replace('<riddle-answer>', riddle_answer))

def trivia_quiz(number_of_questions):
    #create a dictionary of all the questions ranking from easy to hard
    questions_by_difficulty = {'easy': [], 'medium': [], 'hard': []}
    
    #write the number of questions to a file
    with open('data/amountOfQuestions.txt', 'w') as f:
        f.write(str(number_of_questions))
    
    #open the json file of questions and answers
    with open('data/trivia.json', 'r') as f:
        trivia_questions = json.load(f)
    
    for q in trivia_questions:
        questions_by_difficulty[q['difficulty']].append(q)
        
    #what difficulty the user wants the questions to be.
    with open('data/quiz difficulty.txt', 'r') as f:
        read = f.read()
    
    if read == 'none':
        amount_of_questions = len(trivia_questions)
        random_number = random.randint(0, amount_of_questions)

        question = html.unescape(trivia_questions[random_number]['question'])
        correct_answer = html.unescape(trivia_questions[random_number]['correct_answer'])
        incorrect_answers = html.unescape(trivia_questions[random_number]['incorrect_answers']) #this is used to get a list of either one or three incorrect answers.
        answers = incorrect_answers + [correct_answer]


        with open('data/expected context.txt', 'w') as f:
            f.write('waiting trivia answer\n' + correct_answer)
    
        print(question)
        random.shuffle(answers)
        i = 1
        for a in answers:
            print(f"{i}) {answers[i-1]}")
            i += 1
    else:
        #random question
        question_data = random.choice(questions_by_difficulty[read])
        #question info
        question = html.unescape(question_data['question'])
        correct_answer = html.unescape(question_data['correct_answer'])
        incorrect_answers = html.unescape(question_data['incorrect_answers'])
        answers = incorrect_answers + [correct_answer]
        with open('data/expected context.txt', 'w') as f:
            f.write('waiting trivia answer\n' + correct_answer)
        #output question and possible answers.
        print(question)        
        random.shuffle(answers)
        i = 1
        for a in answers:
            print(f"{i}) {answers[i-1]}")
            i += 1
    
def facts():
    with open('data/facts.txt', 'r') as f:
        read = f.read().splitlines()
        
        print(chatbot_tools.random_output('give fact'))
        print(random.choice(read))
        
def wikihow():
    print(chatbot_tools.random_output('wikihow random'))
    
def factory_reset():
    files_to_empty = ['expected context.txt', 'last time used.txt', 'log.txt', 'quiz difficulty.txt', 'user passcode.txt', 'wiki links.txt']
    csv_to_empty = ['conversation.csv']    

    #make sure all txt data files are emptied
    for file in files_to_empty:
        with open('data/' + file, 'w') as f:
            f.write('')
    
    #forgetting all conversations made
    header = None
    data = []
    with open('data/conversation.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            data.append(row)

    with open('data/' + file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
       
    #forgetting user data
    with open('data/user data.csv', 'r', newline='') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)

    # Clear the data in the 2nd row (except the first column)
    if len(data) > 1:
        data[1][1:] = [''] * (len(data[1]) - 1)

    # Write the modified content back to the same CSV file
    with open('data/user data.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)
    
    #reset Joan, it should think that the user is new 
    with open('data/new user.txt', 'w') as f:
        f.write('true')
    
    #restarts the python script
    chatbot_tools.restart_program()

def current_weather():
    user_data = chatbot_tools.get_user_data()
    internet = check_internet()
    if internet == 0:
        location_key = user_data['location key']
    
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={weather_api_key}&details=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        
            current_weather = data[0]['WeatherText']
            current_temperature = str(data[0]['Temperature']['Metric']['Value'])

            print(f"The current weather in {user_data['city']} is {current_weather} and the temperature is {current_temperature} celsius")
        else:
            print(chatbot_tools.random_output('unaccessable weather').replace('<user-name>', user_data['first name']))
    else:
        print(chatbot_tools.random_output('no internet').replace('<user-name>', user_data['first name']))
    
def weather_tomorrow():
    internet = check_internet()
    if internet == 0:
        user_data = chatbot_tools.get_user_data()
        location_key = user_data['location key']
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
    
        params = {
            'apikey': weather_api_key,
            'metric': True,  # Use metric units for temperature
            'details': True   # Request additional details in the forecast
        }
    
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            tomorrow_weather = data['DailyForecasts'][0]['Day']['LongPhrase']
            percentageOfRain = data['DailyForecasts'][0]['Day']['PrecipitationProbability']
            precentageOfThunder = data['DailyForecasts'][0]['Day']['ThunderstormProbability']
            percentageOfSnow = data['DailyForecasts'][0]['Day']['SnowProbability']
            hoursOfRain = data['DailyForecasts'][0]['Day']['HoursOfRain']
            grassPollon = data['DailyForecasts'][0]['AirAndPollen'][1]['Category']
            moldPollon = data['DailyForecasts'][0]['AirAndPollen'][2]['Category']
            treePollon = data['DailyForecasts'][0]['AirAndPollen'][3]['Category']
            minimum_temperature = data['DailyForecasts'][0]['Temperature']['Minimum']['Value']
            maximum_temperature = data['DailyForecasts'][0]['Temperature']['Maximum']['Value']

            print(f"For {user_data['city']}, {tomorrow_weather}. Chance to rain: {str(percentageOfRain)}%. This rain should last about {str(hoursOfRain)} hours. The chance for a thunder storm is {str(precentageOfThunder)}% and the chance for snow is {str(percentageOfSnow)}%")
            print(f"Grass pollon is {grassPollon}. Mold pollon is {moldPollon}, and tree pollon is {treePollon}")
            print(f"The minimum temperature for tomorrow is {str(minimum_temperature)} celsius, and the maximum temperature for tomorrow is {str(maximum_temperature)} celsius")
        else:
            print(chatbot_tools.random_output('unaccessable weather').replace('<user-name>', user_data['first name']))
    else:
        print(chatbot_tools.random_output('no internet').replace('<user-name>', user_data['first name']))

def weather_for_area(place):
    user_data = chatbot_tools.get_user_data()
    internet = check_internet()
    location_key = ''
    
    if internet == 0:
        weather_api_key = 'F7DxhfQx1EoPuopgN59Tq0OkGRJwVkWQ'

        # AccuWeather API endpoint for location search
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search"

        # Parameters for the API request
        params = {
            'apikey': weather_api_key,
            'q': place,
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
    
            # Assuming you want the first result
            if data:
                location_key = data[0]['Key']    
       
        # Get the weather from the location specified
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={weather_api_key}&details=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        
            current_weather = data[0]['WeatherText']
            current_temperature = str(data[0]['Temperature']['Metric']['Value'])

            print(f"The current weather in {place} is {current_weather} and the temperature is {current_temperature} celsius")
        else:
            print(chatbot_tools.random_output('unaccessable weather').replace('<user-name>', user_data['first name']))
    else:
        print(chatbot_tools.random_output('no internet').replace('<user-name>', user_data['first name']))

def weather_day(day):
    user_data = chatbot_tools.get_user_data()
    internet = check_internet()
    if internet == 0:
        date = chatbot_tools.day_to_date(day.title())
    
        url = f"https://dataservice.accuweather.com/forecasts/v1/daily/1day/{user_data['location key']}?apikey={weather_api_key}&details=true&date={date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tomorrow_weather = data['DailyForecasts'][0]['Day']['LongPhrase']
            percentageOfRain = data['DailyForecasts'][0]['Day']['PrecipitationProbability']
            precentageOfThunder = data['DailyForecasts'][0]['Day']['ThunderstormProbability']
            percentageOfSnow = data['DailyForecasts'][0]['Day']['SnowProbability']
            hoursOfRain = data['DailyForecasts'][0]['Day']['HoursOfRain']
            grassPollon = data['DailyForecasts'][0]['AirAndPollen'][1]['Category']
            moldPollon = data['DailyForecasts'][0]['AirAndPollen'][2]['Category']
            treePollon = data['DailyForecasts'][0]['AirAndPollen'][3]['Category']
            minimum_temperature = data['DailyForecasts'][0]['Temperature']['Minimum']['Value']
            maximum_temperature = data['DailyForecasts'][0]['Temperature']['Maximum']['Value']

            print(f"For {user_data['city']}, {tomorrow_weather}. Chance to rain: {str(percentageOfRain)}%. This rain should last about {str(hoursOfRain)} hours. The chance for a thunder storm is {str(precentageOfThunder)}% and the chance for snow is {str(percentageOfSnow)}%")
            print(f"Grass pollon is {grassPollon}. Mold pollon is {moldPollon}, and tree pollon is {treePollon}")
            print(f"The minimum temperature for tomorrow is {str(minimum_temperature)} celsius, and the maximum temperature for tomorrow is {str(maximum_temperature)} celsius")
        else:
            print(chatbot_tools.random_output('unaccessable weather').replace('<user-name>', user_data['first name']))
    else:
        print(chatbot_tools.random_output('no internet').replace('<user-name>', user_data['first name']))
        
def weather_hour_advanced():
    user_data = chatbot_tools.get_user_data()
    current_time = datetime.datetime.now()
    rounded_time = (current_time + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    format_time = rounded_time.strftime("%Y-%m-%dT%H:%m:%S")

    url = f"https://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{user_data['location key']}"

    params = {
        "apikey": weather_api_key,
        "details": True, 
        "metric": True,
        "startdate": format_time
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        get_time = data[0]['DateTime'].split('T')[1].split('+')[0].split(':')
        phrase = f"It will be {data[0]['PrecipitationIntensity']} {data[0]['PrecipitationType'].lower().replace('rain', 'raining')} at {get_time[0] + ':' + get_time[1]} in {user_data['city']}"
        temperature = str(data[0]['Temperature']['Value']) + ' Celcius'
        rain_prob = str(data[0]['RainProbability']) + '%'
        snow_prob = str(data[0]['SnowProbability']) + '%'
        thunder_prob = str(data[0]['ThunderstormProbability']) + '%'

        print(phrase)
        print(f"The temperature will be {temperature}. The chance for rain is {rain_prob}, the chance for thunder is {thunder_prob} and the chance for snow is {snow_prob}.")

def tell_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    
    print(f"The current time is {formatted_time}")
    
def tell_date():
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%d/%m/%Y')
    
    print(f"Today's date it {formatted_date}")
    
def tell_day():
    current_date = datetime.datetime.today()
    current_day = current_date.weekday()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    print("It is", days_of_week[current_day], "today.")
    
def tell_month():
    current_date = datetime.datetime.now()
    current_month = current_date.strftime('%B')
    print(f"The month is {current_month}")
    
def tell_year():
    print(f"The year is {datetime.datetime.now().year}")

class movie():
    def read_movie_data():
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(e)
            
    def collect_data(user_input, function):
        movie_data = {}
        user_input = (user_input.lstrip().rstrip().title())

        fun = function(user_input)
        if fun != '':
            pass
        else:
            internet = check_internet()
            if internet == 0:
                response = requests.get(f"https://www.omdbapi.com/?apikey=32486892&s={user_input.replace(' ','%20')}")
                if response.status_code == 200:
                    data = response.json()
                
                    #usful data elements
                    try:
                        title = data['Search'][0]['Title'].title()#TODO: This returns an error, need to deal with it
                        year = data['Search'][0]['Year']
                        ID = data['Search'][0]['imdbID']
                        file_type = data['Search'][0]['Type']
                        image_url = data['Search'][0]['Poster']
        
                        #call for addional detail using the id
                        url = f"https://www.omdbapi.com/?apikey=32486892&i={ID}"
                        detailed_response = requests.get(url)
        
                        if detailed_response.status_code == 200:
                            data = detailed_response.json()

                            rated = data['Rated']
                            released = data['Released']
                            runtime = data['Runtime']
                            genre = data['Genre']
                            director = data['Director']
                            writer = data['Writer']
                            actors = data['Actors']
                            plot = data['Plot']
                            languages = data['Language']
                            awards = data['Awards']

                            for rating in data['Ratings']:
                                if rating['Source'] == 'Rotten Tomatoes':
                                    rate = rating['Value']
            
                            try:
                                #reads currently collected data
                                with open('data/movie data.json', 'r') as f:
                                    movie_data = json.load(f)
                            except:
                                pass
            
                            #writes data to a dictionary
                            collected_data = {
                                "Year": released,
                                "rated": rated,
                                "runTime": runtime,
                                "genre": genre,
                                "director": director,
                                "writer": writer,
                                "actors": actors,
                                "plot": plot,
                                "languages": languages,
                                "awards": awards,
                                "rate": rate}
            
                            movie_data[title] = collected_data
            
                            #writes all previous and new data to file
                            with open('data/movie data.json', 'w') as f:
                                json.dump(movie_data, f, indent=4)
                        else:
                            print(response.status_code)
                        print(function(user_input))
                    except KeyError:
                        pass                  
            else:
                print(chatbot_tools.random_output('no internet'))

    def release(user_input):
        user_input = user_input.title().lstrip().rstrip().replace(' D', '')
    
        try:
            movie_data = movie.read_movie_data()    
            movie_data = movie_data[user_input]
            return (f"{user_input} was released in {movie_data['Year']}")
        except KeyError:
            movie_data = movie.read_movie_data()    
            movie_data = movie_data["The " + user_input]
            print(f"The {user_input} was released in {movie_data['Year']}")

    def rate(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
            
                movie_data = data[user_input]
                return(f"{user_input} is rated {movie_data['rated']}")
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
            
                movie_data = data["The " + user_input]
                print(f"The {user_input} is rated {movie_data['rated']}")
        
    def runtime(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
            
                movie_data = data[user_input]
                return f"{user_input} runs for {movie_data['runTime'].replace('min', 'minutes')}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
            
                movie_data = data["The " + user_input]
                print(f"The {user_input} runs for {movie_data['runTime'].replace('min', 'minutes')}")
    
    def genre(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                return f"The genre for {user_input} is {movie_data['genre']}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                print(f"The genre for The {user_input} is {movie_data['genre']}")
     
    def director(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                list_of_directors = movie_data['director'].split(', ')
                directors = ", ".join(list_of_directors[:-1]) + " and " + list_of_directors[-1]
                return f"The directors for {user_input} are {directors}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                list_of_directors = movie_data['director'].split(', ')
                directors = ", ".join(list_of_directors[:-1]) + " and " + list_of_directors[-1]
                print(f"The directors for The {user_input} are {directors}")
        
    def writer(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                list_of_writer = movie_data['writer'].split(', ')
                writers = ", ".join(list_of_writer[:-1]) + " and " + list_of_writer[-1]
                return f"The directors for {user_input} are {writers}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                list_of_writer = movie_data['writer'].split(', ')
                writers = ", ".join(list_of_writer[:-1]) + " and " + list_of_writer[-1]
                print(f"The directors for The {user_input} are {writers}")
                                      
    def actor(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                list_of_actors = movie_data['actors'].split(', ')
                actors = ", ".join(list_of_actors[:-1]) + " and " + list_of_actors[-1]
                return f"The actors for {user_input} are {actors}"
        except Exception as e:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                list_of_actors = movie_data['actors'].split(', ')
                actors = ", ".join(list_of_actors[:-1]) + " and " + list_of_actors[-1]
                print(f"The actors for The {user_input} are {actors}")
            
    def plot(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                plot = movie_data['plot']
                return f"The plot of {user_input} is: {plot}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                plot = movie_data['plot']
                return f"The plot of The {user_input} is: {plot}"
    
    def languages(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                list_of_languages = movie_data['languages'].split(', ')
                languages = ", ".join(list_of_languages[:-1]) + " and " + list_of_languages[-1]
                return f"The languages for {user_input} are {languages}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                list_of_languages = movie_data['languages'].split(', ')
                languages = ", ".join(list_of_languages[:-1]) + " and " + list_of_languages[-1]
                print(f"The languages for The {user_input} are {languages}")
    
    def awards(user_input):
        try:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data[user_input]
                awards = movie_data['awards']
                return f"The awards for {user_input} is: {awards}"
        except KeyError:
            with open('data/movie data.json', 'r') as f:
                data = json.load(f)
                
                movie_data = data["The " + user_input]
                awards = movie_data['awards']
                print(f"The awards for The {user_input} is: {awards}")
                
def read_latest_news():
    internet = check_internet()
    
    if internet == 0:
        print(chatbot_tools.random_output('read article'))
    else:
        print(chatbot_tools.random_output('no internet'))
