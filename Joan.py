import time, datetime, warnings

warnings.filterwarnings("ignore")

start_time = time.time()

import csv, random, threading
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from fuzzywuzzy import process
from tools import *
from conversations import *
from interactions import *

#writes the date and times of when the program starts
with open('data/last time used.txt', 'w') as f:
    f.write(str(datetime.datetime.now().day) + '/' + str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().year))

#empties expected context file
chatbot_tools.open_file('data/expected context.txt', file='w', text='')

current_time = datetime.datetime.now()

def write_to_log(text):
    with open('data/log.txt', 'a') as a:
        a.write(str(current_time) + ': ' + str(text) + '\n')
        
end_time = time.time()
write_to_log('All libraries imported. Time taken... ' + str(end_time-start_time))

get_ip_data()

class models():       
    def process_input(user_input, vectorizer, classifier, er_vectorizer, er_classifier):
        #imports
        import string
        import webbrowser
        from pywikihow import RandomHowTo, HowTo, search_wikihow
        
        with open('data/expected context.txt', 'r') as f:
            context = f.read()
        
        user_data = chatbot_tools.get_user_data()
        user_input = user_input.lower().translate(str.maketrans("","",string.punctuation))
        
        if context == 'how are you':
            query_er_vectorizer = er_vectorizer.transform([user_input])
            user_emotion = er_classifier.predict(query_er_vectorizer)[0]
            print('Emotion', user_emotion)#***
            for emotion in positive_emotions:
                if user_emotion == emotion:
                    print(chatbot_tools.random_output('positive emotion').replace('<emotion>', emotion))
                    return None
            for emotion in neutral_emotions:
                how_are_you_response.neutral_response(user_emotion, emotion)
                break      
            for emotion in negative_emotions:
                if user_emotion == emotion:
                    print(chatbot_tools.random_output('negative emotion').replace('<emotion>', emotion))
                    return None
        elif context == 'learn favourite food':
            ud = chatbot_tools.get_user_data()
            user_data = pd.read_csv('data/user data.csv')
            user_favourite_food_extract = text_tools.find_food(str(user_input))
            user_data['F-food'] = user_favourite_food_extract
            user_data.to_csv('data/user data.csv', index=False)
            print(chatbot_tools.random_output('favourite food response').replace('<F-food>', user_favourite_food_extract).replace('<name>', ud['first name']).replace('-', 'and'))
        elif context == 'bordem play game':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                print(chatbot_tools.random_output('play which game'))
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'bordem watch video':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                bordem_entertainment.play_video()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'tell joke':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                tell_joke()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'tell riddle':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                tell_riddle()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'trivia':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                with open('data/amountOfQuestions.txt', 'r+') as f:
                    read = f.read()

                    if read == '0':
                        print(chatbot_tools.random_output('No more questions').replace('<user-name>', user_data['first name']))
                        with open('data/amountOfQuestions.txt', 'w') as f:
                            f.write('')
                    else:
                        num = int(read) - 1 
                        f.write(str(num))
                        user_question_amount = chatbot_tools.process_input_to_numbers(input(chatbot_tools.random_output('amount of questions')))
                        if user_question_amount == 'unknown':
                            trivia_quiz('100000000')
                        else:
                            trivia_quiz(user_question_amount)
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'fun fact':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                facts()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'wiki game':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.open_wiki_game()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'phone person':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                print(chatbot_tools.random_output('phone person'))
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'xkcd':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.xkcd()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'read wikihow':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                wikihow()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'read wiki': #TODO: Need to use the wikipedia library to search and process articles to read articles.
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                pass
            else:
                pass
        elif context == 'play akinator':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.akinator()
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'play blackjack again':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.blackjack('')
            else:
                print(chatbot_tools.random_output('no worries game').replace('<user-name>', user_data['first name']))
        elif context == 'play number guess again':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.numberGuess()
            else:
                print(chatbot_tools.random_output('no worries game').replace('<user-name>', user_data['first name']))
        elif context == 'play rps again':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                games.rps()
            else:
                print(chatbot_tools.random_output('no worries').replace('<user-name>', user_data['first name']))
        elif 'waiting trivia answer' in context:
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]

            correct_answer = context.splitlines()[1]

            text_vectorized = vectorizer.transform([user_input])
            user_entity = classifier.predict(text_vectorized)[0]
            print(user_entity)
            if user_entity == 'quit':
                with open('data/amountOfQuestions.txt', 'w') as f:
                    f.write('')
                with open('data/expected context.txt', 'w') as f:
                    f.write('')
                print(chatbot_tools.random_output('quit trivia').replace('<user-name>', user_data['first name']))
            else:
                if user_input.lower() in context.splitlines()[1].lower():
                    print(chatbot_tools.random_output('correct answer').replace('<user-name>', user_data['first name']).replace('<correct-answer>', correct_answer))
                elif sentiment == 'negative' and user_input.lower() not in context:
                   print(chatbot_tools.random_output('unsure trivia answer').replace('<correct-answer>', correct_answer))
                else:
                    print(chatbot_tools.random_output('incorrect answer').replace('<user-name>', user_data['first name']).replace('<correct-answer>', correct_answer))
            
                with open('data/amountOfQuestions.txt', 'r') as f:
                    read = f.read()
                    read = int(read) - 1
                    if int(read) == 0:
                        print(chatbot_tools.random_output('no more questions').replace('<user-name>', user_data['first name']))
                        with open('data/amountOfQuestions.txt', 'w') as f:
                                f.write('')
                    else:
                        with open('data/amountOfQuestions.txt', 'w') as f:
                            f.write(str(read))
                        print(chatbot_tools.random_output('continue quiz'))
                        trivia_quiz(read)
        elif context == 'wikihow detail':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                with open('data/wikihow links.txt', 'r') as f:
                    article = HowTo(f.read())
                    
                    first_step = article.steps[0]
                    first_step.print()
                    data = first_step.as_dict()
                    article.print(extended=True)
            else:
                print(chatbot_tools.randomt_output('no worries general'))
        
        elif context == 'read space article':
            latest_news = requests.get('https://api.spaceflightnewsapi.net/v4/articles/?format=json')
            if latest_news.status_code == 200:
                latest_news = latest_news.json()
                print(chatbot_tools.random_output('newest space articles'))

                read_articals = True
                article_iteration = 0
                while read_articals is True:
                    try:
                        user_data = chatbot_tools.get_user_data()
                        article = latest_news['results'][article_iteration]
                        source = article["news_site"]
                   
                        print(f"{article['title']} - {source}")
 
                        news_user_input = input('... ')
                    
                        #if user input is postive or negative
                        sr_vectorizer = vectorizer.transform([news_user_input])
                        sentiment = classifier.predict(sr_vectorizer)[0]
                        print(sentiment)

                        if sentiment == 'positive' and 'continue' in news_user_input or 'description' in news_user_input:
                            #read the summary of title
                            print(article['summary'])
                        
                            news_user_input = input('Let me know if you want me to open the article or continue to the next article:')
                            #if user input is postive or negative
                            sr_vectorizer = vectorizer.transform([news_user_input])
                            sentiment = classifier.predict(sr_vectorizer)[0]

                            if sentiment == 'positive' and 'next' in news_user_input:#moves to next article
                                article_iteration += 1 
                            
                            elif sentiment == 'positive' and 'url' in news_user_input or 'open' in news_user_input:#opens the url to the article to find out more
                                 webbrowser.open(article['url'])
                                 article_iteration += 1
                            
                            elif sentiment == 'negative':#stops reading or taking inout for the news
                                with open('data/expected context.txt', 'w') as w:
                                    w.write('')
                                read_articals = False
                                break
                            
                        elif 'next' in news_user_input:#moves onto the next article
                            article_iteration += 1
                            
                        elif sentiment == 'negative':
                            print('test')
                            with open('data/expected context.txt', 'w') as w:
                                w.write('')
                            read_articles = False
                            break
                    except IndexError:
                        print(chatbot_tools.random_output('no more latest news'))
                        with open('data/expected context.txt', 'w') as w:
                            w.write('')
                        read_articals = False

        elif context == 'read article':
            latest_news = requests.get('https://api.currentsapi.services/v1/latest-news?page_size=200&language=en&apiKey=iChF0rDovQfg2Kf787UiAGKB4QHOBLK2aSrSp6mA8PSGhzVe')
            if latest_news.status_code == 200:
                latest_news = latest_news.json()
                print(chatbot_tools.random_output('newest articles'))

                read_articals = True
                article_iteration = 0
                while read_articals is True:
                    try:
                        user_data = chatbot_tools.get_user_data()
                        article = latest_news['news'][article_iteration]
                        source = chatbot_tools.extract_website_name(article['url'])
                    
                        category_result = [t in article['category'] for t in user_data['news hate'].rstrip().lstrip().split(', ')]
                        site_result = [t in article['url'] for t in list(filter(None, user_data['band news site'].rstrip().lstrip().split(', ')))]

                        if True in category_result:#if the user doesn't want to know about news taged with specific categories
                            article_iteration += 1
                        else:
                            if True in site_result and user_data['band news site'] != '':
                                article_iteration += 1
                            else:
                                print(f"{article['title']} - {source} - category: {', '.join(article['category'])}")
 
                                news_user_input = input('... ')
                    
                                #if user input is postive or negative
                                sr_vectorizer = vectorizer.transform([news_user_input])
                                sentiment = classifier.predict(sr_vectorizer)[0]

                                if sentiment == 'positive' and 'continue' in news_user_input or 'description' in news_user_input:
                                    #read the description of title
                                    print(article['description'])
                        
                                    news_user_input = input('Let me know if you want me to open the article or continue to the next article:')
                                    #if user input is postive or negative
                                    sr_vectorizer = vectorizer.transform([news_user_input])
                                    sentiment = classifier.predict(sr_vectorizer)[0]

                                    if sentiment == 'positive' and 'next' in news_user_input:#moves to next article
                                        article_iteration += 1 
                            
                                    elif sentiment == 'positive' and 'url' in news_user_input:#opens the url to the article to find out more
                                         webbrowser.open(article['url'])
                            
                                    elif sentiment == 'negative':#stops reading or taking inout for the news
                                        with open('data/expected context.txt', 'w') as w:
                                            w.write('')
                                        read_articals = False
                                        break
                            
                                elif 'next' in news_user_input:#moves onto the next article
                                    article_iteration += 1
                        
                                elif sentiment == 'negative' and "not interested" in news_user_input:#removes a specific category stopping it from suggesting news from category
                                    categories = ["technology","lifestyle","business","general","programming","science","entertainment","world","sports","finance","academia","politics","health","opinion","food","game","fashion","academic","crap","travel","culture","economy","environment","art","music","notsure","CS","education","redundant","television","commodity","movie","entrepreneur","review","auto","energy","celebrity","medical","gadgets","design","EE","security","mobile","estate","funny"]
                                    find_category = [i for i in categories if news_user_input == categories]

                                    if find_category == []:#meaning that the category wasn't specified
                                        chatbot_tools.write_user_data(news_hate=', '.join(article['category']))
                                        article_iteration += 1
                                    else:
                                        chatbot_tools.write_user_data(news_hate=find_category)
                                        article_iteration += 1
                        
                                elif sentiment == 'negative' and "don't show" in news_user_input or "dont show" in news_user_input:
                                    chatbot_tools.write_user_data(band_news_site=article['url'])
                                    article_iteration += 1
                            
                                elif sentiment == 'negative':
                                    with open('data/expected context.txt', 'w') as w:
                                        w.write('')
                                    read_articles = False
                                    break
                    except IndexError:
                        print(chatbot_tools.random_output('no more latest news'))
                        with open('data/expected context.txt', 'w') as w:
                            w.write('')
                        read_articals = False

        elif context == 'wikihow search':
            with open('data/wiki links.txt', 'w') as f:
                f.write(user_input)
            print(chatbot_tools.random_output('wikihow search read or open'))
        elif context == 'wikihow search read or open':
            with open('data/wiki links.txt', 'r') as f:
                read = f.read()
            how_tos = search_wikihow(read, 1)

            if 'open' in user_input.lower():
                if how_tos:
                    for how_to in how_tos:
                        webbrowser.open(how_to.url)
            elif 'read' in user_input.lower():
                with open('data/wiki links.txt', 'r') as f:
                    article = HowTo(f.read())
                    
                    first_step = article.steps[0]
                    first_step.print()
                    data = first_step.as_dict()
                    article.print(extended=True)
            with open('data/expected context.txt', 'w') as f:
                f.write('')
        elif context == 'wikihow random':
            text_vectorized = vectorizer.transform([user_input])
            user_entity = classifier.predict(text_vectorized)[0]
            
            if user_entity == 'random wikihow article':
                print(chatbot_tools.random_output('open or read'))
            elif user_entity == 'search wikihow':
                print(chatbot_tools.random_output('wikihow search'))        
        elif context == 'open or read':
            if 'open' in user_input.lower():
                random_article = RandomHowTo()
                webbrowser.open(random_article.url)
            elif 'read' in user_input.lower():
                random_article = RandomHowTo()
                random_article.print()
                with open('data/wikihow links.txt', 'w') as f:
                    f.write(random_article.url)
                print(chatbot_tools.random_output('more wikihow detail'))    
        elif context == 'speak passcode':
            with open('data/user passcode.txt', 'w') as f:
                f.write(user_input)
            print(chatbot_tools.random_output('speak passcode again'))
        elif context == 'repeat passcode':
            with open('data/user passcode.txt', 'r') as f:
                passcode = f.read()
            
            if user_input == passcode:
                print(chatbot_tools.random_output('passcode accepted'))
            else:
                with open('data/user passcode.txt', 'w') as f:
                    f.write('')
                print(chatbot_tools.random_output('passcode denied'))
        elif context == 'welcome user':
            #get the user's name from their input
            user_name = chatbot_tools.get_user_name(user_input)
            user_name = user_name[0].split(' ')
            if len(user_name) > 1:
                if len(user_name) >= 3:
                    chatbot_tools.write_user_data(first_name=user_name[0],middle_name=user_name[1],surname=user_name[2])
                else:
                    chatbot_tools.write_user_data(first_name=user_name[0],surname=user_name[1])
            else:
                chatbot_tools.write_user_data(first_name=user_name[0])
            user_data = chatbot_tools.get_user_data()
            print(chatbot_tools.random_output('welcome users name').replace('<user-name>', user_data['first name']))
            
            #get the user's gender based on their name using an api
            gender_call = requests.get(f"https://api.genderize.io?name={user_data['first name']}")
            
            if gender_call.status_code == 200:
                gender_call = gender_call.json()
                gender = gender_call['gender']
                chatbot_tools.write_user_data(gender=gender)

        elif context == 'change passcode':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            if sentiment == 'positive':
                print(chatbot_tools.random_output('passcode before change'))
            else:
                print(chatbot_tools.random_output('no worries general'))
                
        elif context == 'random activity':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]

            if sentiment == 'positive':
                print(chatbot_tools.random_output('bored activity attempt'))
            else:
                print(chatbot_tools.random_output('no worries general'))
        elif context == 'info food':
            sr_vectorizer = vectorizer.transform([user_input])
            sentiment = classifier.predict(sr_vectorizer)[0]
            
            if sentiment == 'positive':
                with open('data/tempFile.txt', 'r') as f:
                    read = f.read()
                    
                search_food_ingriedents(read)
        elif context == 'passcode before change':
            with open('data/user passcode.txt', 'r') as f:
                passcode = f.read()
            
            if passcode == user_input:
                print(chatbot_tools.random_output('blank passcode accept'))
                print(chatbot_tools.random_output('speak replace passcode'))
                with open('data/expected context.txt', 'w') as f:
                    f.write('speak passcode')
            else:
                print(chatbot_tools.random_output('blank passcode denied'))
        elif context == 'choose video':
            from youtubesearchpython import VideosSearch
            videoResults = VideosSearch(user_input, limit=1)
            webbrowser.open(videoResults.result()['result'][0]['link'])
            chatbot_tools.open_file('data/expected context.txt', file='w', text='')
        else:
            matched_keywords = models.find_matched_keywords(user_input, vectorizer, threshold=0.6)
        
            text = process_text_tools.preprocess_text(user_input)
            text_vectorized = vectorizer.transform([text])
            entity = classifier.predict(text_vectorized)[0]
                
            intent = models.find_intent(user_input, ET_data)
                
            ###The main if, elif, else statements for the ET data

            try:
                ET_data.set_index('name', inplace=True)
            except KeyError:
                pass
            
            print(entity)#***
            if entity == 'greeting':
                remember_data = pd.read_csv('data/userRemember.csv')
                
                for index, row in remember_data.iterrows():
                    if row['when'] == 'hi':
                        if 'water' in row['remember']:
                            print('Remember', row['remember'])
                            break
                        else:
                            remember_data = remember_data.drop(index, axis=0)
                            remember_data.to_csv('data/userRemember.csv')
                            print('Remember', row['remember'])
                            break
                    
                greeting_response(user_input)
            elif entity == 'been while':
                been_while()
            elif entity == 'how are you':
                how_are_you()
            elif entity == 'play blackjack':
                games.blackjack(user_input)
            elif entity == 'play guessing game':
                games.numberGuess()
            elif entity == 'play rps':
                games.rps()
            elif entity == 'tell joke':
                tell_joke()
            elif entity == 'tell riddle':
                tell_riddle()
            elif entity == 'fact':
                facts()
            elif entity == 'wiki game':
                games.open_wiki_game()
            elif entity == 'xkcd':
                games.xkcd()
            elif entity == 'random wikihow article':
                wikihow()
            elif entity == 'factory reset':
                with open('data/user passcode.txt', 'r') as f:
                    passcode = f.read()
                    
                if passcode == '' or passcode not in user_input:
                    print(chatbot_tools.random_output('factory reset unrecognized passcode'))
                else:
                    print(chatbot_tools.random_output('factory reset passcode accecpted'))
                    factory_reset()
            elif entity == 'how to':
                with open('data/wiki links.txt', 'w') as f:
                    f.write(user_input)
                print(chatbot_tools.random_output('wikihow search read or open'))
            elif entity == 'search wikihow':
                print(chatbot_tools.random_output('wikihow search'))
            elif entity == 'akinator':
                games.akinator()
            elif entity == 'list games':
                games.game_list()
            elif entity == 'describe akinator':
                print(chatbot_tools.random_output('explain akinator'))
            elif entity == 'descrive wiki game':
                print(chatbot_tools.random_output('explain wiki game'))
            elif entity == 'bye':
                remember_data = pd.read_csv('data/userRemember.csv')
                
                for index, row in remember_data.iterrows():
                    if row['when'] == 'bye':
                        if 'water' in row['remember']:
                            print('Remember', row['remember'])
                            break
                        else:
                            remember_data = remember_data.drop(index, axis=0)
                            remember_data.to_csv('data/userRemember.csv')
                            print('Remember', row['remember'])
                            break
                
                print(chatbot_tools.random_output('bye').replace('<user-name>', user_data['first name']))
            elif entity == 'thank':
                print(chatbot_tools.random_output('thank').replace('<user-name>', user_data['first name']))
            elif entity == 'set passcode':
                with open('data/user passcode.txt', 'r') as f:
                    passcode = f.read()
                    
                if passcode == '':
                    print(chatbot_tools.random_output('speak passcode'))
                else:
                    print(chatbot_tools.random_output('current passcode'))
            elif entity == 'play trivia':
                print(chatbot_tools.random_output('accepct trivia request'))
                with open('data/amountOfQuestions.txt', 'r+') as f:
                    read = f.read()
                    if read == '':
                        user_difficulty = input("What difficulty would you like the questions. Your choices are either easy, medium, hard, or you can just have any questions.")
                        if 'easy' in user_difficulty.lower():
                            difficulty = 'easy'
                        elif 'medium' in user_difficulty.lower():
                            difficulty = 'medium'
                        elif 'hard' in user_difficulty.lower():
                            difficulty = 'hard'
                        else:
                            difficulty = 'none'
                                
                        with open('data/quiz difficulty.txt', 'w') as f:
                            f.write(difficulty)
                        #ask user how many questions they would like
                        user_question_amount = chatbot_tools.process_input_to_numbers(input(chatbot_tools.random_output('amount of questions') + '\n'))
                        if user_question_amount == 'unknown':
                            trivia_quiz('100000000')
                        else:
                            trivia_quiz(user_question_amount)
                    elif int(read) == 0:
                        print(chatbot_tools.random_output('no more questions').replace('<user-name>', user_data['first name']))
                    else:
                        num = int(read) - 1 
                        f.write(str(num))
                        trivia_quiz(read)
            elif entity == 'play game':
                print(chatbot_tools.random_output('suggest play game'))
            elif entity == 'what is passcode':
                print(chatbot_tools.random_output('explain passcode'))
            elif entity == 'current weather':
                current_weather()
            elif entity == 'weather tomorrow':
                weather_tomorrow()
            elif entity == 'weather day':
                days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                for day in days_of_week:
                    if day in user_input:   
                        weather_day(day)
                        break
            elif entity == 'choose youtube video':
                internet = check_internet()
                if internet == 0:
                    print(chatbot_tools.random_output('choose video'))
                else:
                    print(chatbot_tools.random_output('no internet'))
            elif entity == 'users name':
                user_data = chatbot_tools.get_user_data()
                print(chatbot_tools.random_output('tell user name').replace('<user-name>',user_data['first name']))
            elif entity == 'advice':
                with open('data/datasets/advice.txt', 'r') as f:
                    advice = f.readlines()
                    
                print(random.choice(advice))
            elif entity == 'question amount':
                print(chatbot_tools.random_output('amount of questions data'))
            elif entity == 'chewie':
                print(chatbot_tools.random_output('chewie'))
            elif entity == 'wax on':
                print(chatbot_tools.random_output('wax of'))
            elif entity == 'wizard of oz':
                print(chatbot_tools.random_output('dog too'))
            elif entity == 'mama says':
                print(chatbot_tools.random_output('stupid'))
            elif entity == 'roads':
                print(chatbot_tools.random_output('roads'))
            elif entity == 'father':
                print(chatbot_tools.random_output('father'))
            elif entity == 'rd1':
                print(chatbot_tools.random_output('red dwarf one').replace('<user-name>', user_data['first name']))
            elif entity == 'rd2':
                print(chatbot_tools.random_output('red dwarf two').replace('<user-name>', user_data['first name']))
            elif entity == 'rd3':
                print(chatbot_tools.random_output('red dwarf three').replace('<user-name>', user_data['first name']))
            elif entity == 'rd4':
                print(chatbot_tools.random_output('red dwarf four').replace('<user-name>', user_data['first name']))
            elif entity == 'rd5':
                print(chatbot_tools.random_output('red dwarf five').replace('<user-name>', user_data['first name']))
            elif entity == 'rd6':
                print(chatbot_tools.random_output('red dwarf six').replace('<user-name>', user_data['first name']))
            elif entity == 'rd7':
                print(chatbot_tools.random_output('red dwarf seven').replace('<user-name>', user_data['first name']))
            elif entity == 'rd8':
                print(chatbot_tools.random_output('red dwarf eight').replace('<user-name>', user_data['first name']))
            elif entity == 'rd9':
                print(chatbot_tools.random_output('red dwarf nine').replace('<user-name>', user_data['first name']))
            elif entity == 'who are you':
                print(chatbot_tools.random_output('who are you'))
            elif entity == 'call bot':
                print(chatbot_tools.random_output('call bot'))
            elif entity == 'why named':
                print(chatbot_tools.random_output('why named'))
            elif entity == 'love user':
                print(chatbot_tools.random_output('love user').replace('<user-name>', user_data['first name']))
            elif entity == 'robot':
                print(chatbot_tools.random_output('not robot'))
            elif entity == 'human':
                print(chatbot_tools.random_output('not human'))
            elif entity == 'change bot name':
                print(chatbot_tools.random_output('change bot name'))
            elif entity == 'real or not':
                print(chatbot_tools.random_output('real or not'))
            elif entity == 'last night':
                print(chatbot_tools.random_output('last night'))
            elif entity == 'what doing':
                print(chatbot_tools.random_output('what doing'))
            elif entity == 'what next':
                print(chatbot_tools.random_output('what next').replace('<user-name>', user_data['first name']))
            elif entity == 'collection':
                print(chatbot_tools.random_output('bot collection'))
            elif entity == 'bot hobby':
                print(chatbot_tools.random_output('bot hobby'))
            elif entity == 'talk request':
                print(chatbot_tools.random_output('talk request').replace('<user-name>', user_data['first name']))
            elif entity == 'question bot':
                print(chatbot_tools.random_output('question').replace('<user-name>', user_data['first name']))
            elif entity == 'something':
                print(chatbot_tools.random_output('something'))
            elif entity == 'not talking bot':
                print(chatbot_tools.random_output('not talking bot').replace('<user-name>', user_data['first name']))
            elif entity == 'bot live forever':
                print(chatbot_tools.random_output('bot live forever'))
            elif entity == 'bot favourite':
                print(chatbot_tools.random_output('bot favourite'))
            elif entity == 'created':
                print(chatbot_tools.random_output('created'))
            elif entity == 'gender':
                print(chatbot_tools.random_output('gender'))
            elif entity == 'bot version':
                with open('data/version.txt', 'r') as f:
                    version = f.read()
                print(chatbot_tools.random_output('version'))
            elif entity == 'user thinking':
                print(chatbot_tools.random_output('user thinking'))
            elif entity == 'knowledge about user':
                print('Here are the things that I know about you')
                if user_data['first name'] != '':
                    print(f"Your first name is {user_data['first name']}")
                if user_data['middle name'] != '':
                    print(f"Your middle name is {user_data['middle name']}")
                if user_data['surename'] != '':
                    print(f"Your surname is {user_data['surename']}")
                if user_data['dob'] != '':
                    print(f"Your date of birth is {user_data['dob']}")
                if user_data['nickname'] != '':
                    print(f"Your nickname is {user_data['nickname']}")
                if user_data['hobbies/interest'] != '':
                    print(f"These are your hobbies and interests {user_data['hobbies/interests']}")
                if user_data['favourite song'] != '':
                    print(f"Your favourite song is {user_data['favourite song']}")
                if user_data['favourite music genre'] != '':
                    print(f"Your favourite music genre is {user_data['favourite music genre']}")
                if user_data['favourite film'] != '':
                    print(f"Your favourite film is {user_data['favourite film']}")
                if user_data['favourite food'] != '':
                    print(f"Your favourite food is {user_data['favourite food']}")
                if user_data['favourite book'] != '':
                    print(f"Your favourite book is {user_data['favourite book']}")
                if user_data['disliked food'] != '':
                    print(f"You dislike {user_data['disliked food']}")
                if user_data['disabilities'] != '':
                    print(f"You have {user_data['disability']}")
                if user_data['number of pets'] != '':
                    print(f"You have {user_data}")
                if user_data['name of pets'] != '':
                    print(f"The name of your pets are {user_data['name of pets']}")
                if user_data['places visited'] != '':
                    print(f"The places you have visited are {user_data['places visited']}")
            elif entity == 'time':
                tell_time()
            elif entity == 'date':
                tell_date()
            elif entity == 'day':
                tell_day()
            elif entity == 'month':
                tell_month()
            elif entity == 'year':
                tell_year()
            elif entity == 'movie release':
                user_input = user_input.lower().lstrip().replace('when', '').replace('did', '').replace('release', '').replace('released', '').replace('was', '')
                movie.collect_data(user_input, movie.release)
            elif entity == 'weather monday':
                weather_day('monday')
            elif entity == 'weather tuesday':
                weather_day('tuesday')
            elif entity == 'weather wednesday':
                weather_day('wednesday')
            elif entity == 'weather thrusday':
                weather_day('thrusday')
            elif entity == 'weather friday':
                weather_day('friday')
            elif entity == 'weather saturday':
                weather_day('saturday')
            elif entity == 'weather sunday':
                weather_day('sunday')      
            elif entity == 'weather hour':
                weather_hour_advanced()
            elif entity == 'movie rate':
                user_input = user_input.replace('what', '').replace('is', '').replace('rating' , '').replace('of', '').replace('for', '').replace('the', '').lstrip().rstrip().title()
                movie.collect_data("The " + user_input, movie.rate)
            elif entity == 'movie runtime':
                user_input = user_input.replace('what', '').replace('is', '').replace('the', '').replace('run', '').replace('time', '').replace('of', '').replace('for', '').lstrip().strip().title()
                movie.collect_data("The " + user_input, movie.runtime)
            elif entity == 'movie genre':
                user_input = user_input.replace('what', '').replace('is', '').replace('the', '').replace('genre', '').replace('of', '').lstrip().rstrip().title()
                movie.collect_data("The " + user_input, movie.genre)
            elif entity == 'movie director':
                user_input = user_input.replace('who', '').replace('is', '').replace('director', '').replace('directed', '').replace('for', '').replace('of', '').replace('was', '').lstrip().rstrip().title()
                movie.collect_data(user_input, movie.director)
            elif entity == 'movie writer':
                user_input = user_input.replace('who', '').replace('wrote', '').replace('is', '').replace('writer', '').replace('for', '')
                movie.collect_data(user_input, movie.writer)
            elif entity == 'movie actor':
                user_input = user_input.replace('actors', '').replace('acted', '').replace('for', '').replace('who', '').replace('in', '').replace('actor', '').replace('is', '').replace('the', '')
                movie.collect_data(user_input, movie.actor)
            elif entity == 'movie plot':
                user_input = user_input.replace('what', '').replace('is', '').replace('the', '').replace('plot', '').replace('of', '').rstrip().lstrip().title()
                movie.collect_data(user_input, movie.plot)
            elif entity == 'languages':
                user_input = user_input.replace('what', '').replace('languages', '').replace('language', '').replace('in', '').repalce('are', '').rstrip().lstrip().title()
                movie.collect_data(user_input, movie.languages)
            elif entity == 'awards':
                user_input = user_input.replace('what', '').replace('award', '').replace('awards', '').replace('did', '').replace('win', '').rstrip().lstrip().title()
                movie.collect_data(user_input, movie.awards)
            elif entity == 'specific weather location':
                user_input = user_input.split('for ')
                weather_for_area(user_input[1])
            elif entity == 'latest news':
                read_latest_news()
            elif entity == 'scan open website':
                website_url = copy_website_url()
                scan_url(website_url)
            elif entity == 'scan copied website':
                website_url = get_copied_text()
                scan_url(get_copied_text)
            elif entity == 'space news':
                read_space_news()
            elif entity == 'remember':
                memory.remember(user_input)
                return 'reload data'
            elif entity == 'search':
                search_food(user_input.replace('show', '').replace('recipies', '').replace('search', '').replace('for', '').replace('how', '').replace('to', '').replace('bake', '').replace('cook', '').rstrip().lstrip())
            elif entity == 'ingredients':
                search_food_ingriedents(user_input.replace('ingredients', '').replace('ingredients', '').replace('for', ''))
            elif entity == 'meal suggestion':
                suggest_meal()
            elif entity == 'where object':
                remember = pd.read_csv('data/userRemember.csv')

                for index, row in remember.iterrows():
                    keyword = row['output'].split('***')
                    if keyword[0] in user_input:
                        print(keyword[1])#this is the sentence rather than the keyword
                
                        #remove from the userRemember.csv
                        remember = remember.drop(index, axis=0)
                        remember.to_csv('data/userRemember.csv')
                        
                        ET = pd.read_csv('data/datasets/ET.csv')
                        ET = ET[~ET['name'].str.contains(user_input.split()[-1], case=False)]
                        ET.to_csv('data/datasets/ET.csv', index=False)
                return 'reload data'
            else:
                if entity == 'positive' or entity == 'negative':
                    if user_input.startswith('remember'):# if input starts with remember then user must be asking to remember something
                        memory.remember(user_input)
                        return 'reload data'
                    else:
                        chatbot_tools.big_guns(user_input)
                        return 'reload data'
                else:
                    if user_input.startswith('remember'):
                        memory.remember(user_input)
                        return 'reload data'
                    else:
                        print(entity)
            
            #checks if the timer is still running
            if not timer.is_alive():
                remember_data = pd.read_csv('data/userRemember.csv')
                
                for index, row in remember_data.iterrows():
                    if row['when'] == 'timer' or row['when'] == 'hi':
                        print('Also remember', row['remember'])
                
                        user_response_to_reminder = input('Input >>> ')
                
                        user_response_to_reminder = user_response_to_reminder.lower().translate(str.maketrans("","",string.punctuation))

                        matched_keywords = models.find_matched_keywords(user_response_to_reminder, vectorizer, threshold=0.6)
        
                        text = process_text_tools.preprocess_text(user_response_to_reminder)
                        text_vectorized = vectorizer.transform([text])
                        entity = classifier.predict(text_vectorized)[0]
                        print(entity)
                        if entity == 'later' or entity == 'negative':
                            print(chatbot_tools.random_output('remind later').replace('<user-name>', user_data['first name']))
                        elif entity == 'thank':
                            if 'water' not in row['remember']:
                                remember_data = remember_data.drop(index, axis=0)
                                remember_data.to_csv('data/userRemember.csv')#assume user is going to do it, remove
                            break
                        elif entity == 'forget':
                            if 'water' not in row['remember']:
                                remember_data = remember_data.drop(index, axis=0)
                                remember_data.to_csv('data/userRemember.csv')
                            print(chatbot_tools.random_output('forget').replace('<user-name>', user_data['first name']))
                            break
                        else:
                            if 'water' not in row['remember']:
                                remember_data = remember_data.drop(index, axis=0)
                                remember_data.to_csv('data/userRemember.csv')
                                process = models.process_input(user_response_to_reminder, vectorizer, classifier, er_vectorizer, er_classifier)
                            break

    def find_intent(user_input, ET_data):
        try:
            user_inpuit = user_input.lower()
            ET_data = ET_data.iloc[ET_data['name'].str.len().argsort()]
            ET_data.set_index('name', inplace=True)
        
            matches = process.extractOne(user_input, ET_data)
        
            if matches[1] > 80:
                return matches[0]
            else:
                return ''
        except KeyError:
            pass
            
    def preprocess_data():
        start = time.time()
    
        vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b')
        classifier = LinearSVC()
    
        df = pd.read_csv('data/datasets/ET.csv')
        pos_neg_data = pd.read_csv('data/datasets/SR.csv')
    
        combined_data1 = pd.concat([df['name'], pos_neg_data['text']], axis=0, ignore_index=True)
        combined_data2 = pd.concat([df['ET'], pos_neg_data['sentiment']], axis=0, ignore_index=True)
    
        x_train = combined_data1.tolist()
        y_train = combined_data2.tolist()

        X_train = [process_text_tools.preprocess_text(text) for text in x_train]
    
        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
        x_train_vectorized = vectorizer.fit_transform(X_train)
        x_test_vectorized = vectorizer.transform(X_test)
    
        classifier.fit(x_train_vectorized, y_train)
    
        #emotion recognizer
        emotion_data = pd.read_csv('data/datasets/ER.csv')
    
        er_x_train = emotion_data['text']
        er_y_train = emotion_data['emotion']
    
        er_vectorizer = TfidfVectorizer()
        x_train_er_vectorized = er_vectorizer.fit_transform(er_x_train)
    
        er_classifier = SVC(kernel='linear')
        er_classifier.fit(x_train_er_vectorized, er_y_train)
    
        end = time.time()
        write_to_log('Time taken to preprocess data: ' + str(end-start))
    
        return vectorizer, classifier, er_vectorizer, er_classifier
    
    def find_matched_keywords(user_input, vectorizer, threshold=0.5):
        try:
            keywords = ET_data.iloc[:, 0].tolist()
            preprocess_input = [process_text_tools.preprocess_text(user_input)]
            input_vectorized = vectorizer.transform(preprocess_input)
            similarity_scores = cosine_similarity(input_vectorized, vectorizer.transform(keywords))[0]
            matched_keywords = [keywords[i] for i, score in enumerate(similarity_scores) if score >= threshold]
            return matched_keywords
        except Exception as e:
            return user_input

class memory:   
    def remember(user_input):
        vectorizer, classifier = memory.load_data()
        intent = memory.process_input(vectorizer, classifier, user_input)
        
        user_input = text_tools.first_to_third(user_input)

        memory.determine_intent(intent, user_input)
        
    def load_data():
        data = pd.read_csv('data/datasets/rememberTrainingData.csv')

        x_train = data['memory']

        y_train = data['keyword']

        vectorizer = TfidfVectorizer()
        x_train_vectorized = vectorizer.fit_transform(x_train)

        classifier = SVC(kernel='linear')
        classifier.fit(x_train_vectorized, y_train)
    
        return vectorizer, classifier
    
    def process_input(vectorizer, classifier, query):
        query_vectorized = vectorizer.transform([query])

        intent = classifier.predict(query_vectorized)[0]
    
        return intent
    
    def determine_intent(intent, user_input):
        '''
        Determines what the intent of the user's remember input was
        '''
        
        #list of all keywords in relation to what the user could say
        intent_list = ['item location', 'completed acheivement', 'respond',
                       'check email', 'pay bills', 'rubbish out',
                       'set', 'charge phone', 'water',
                       'precsription', 'return item', 'attend to pets']
    
        #list of keywords that are most likley to need reminding of before the user leaves
        before_going_out = ['call', 'lock before leaving', 'turn off', 'charge phone',  
                            'bags shopping', 'close windows', 'check keys', 'check wallet', 'attend to pets',
                            'buy item', 'return item']
        
        after_coming_home = ['check email', 'respond', 'charge phone', 'attend to pets', 'call']

        #running the functions in threads because they use ntlk for NLP which can be slow, so it can be done in the background instead
        continue_loops = True
        for i in before_going_out:
            if intent == i:
                continue_loops = False
                going_out = threading.Thread(target=memory.going_out_thread, args=(user_input,))
                going_out.start()

                print('Of course, I will remember', user_input)
                break
            
        for i in after_coming_home:
            if intent == i:
                continue_loops = False
                coming_home = threading.Thread(target=memory.coming_home, args=(user_input,))
                coming_home.start()
                
                print('Of course, I will remember', user_input)
                break
        
        if continue_loops == True:
            for i in intent_list:
                if intent == i and i == 'item location':
                    item_location_memory = threading.Thread(target=memory.item_location, args=(user_input,))
                    item_location_memory.start()#runs in background
                    
                    #informs user of comfirmation
                    print('Of course, I will remember', user_input)

                    #stops for loop.
                    break
                    
                elif intent == i and i in ['respond', 'call', 'check email', 'pay bills', 'rubbish out', 'set', 'charge phone', 'precsription', 'return item', 'attend to pets', 'water']:
                    respond_memory = threading.Thread(target=memory.respond, args=(user_input,))
                    respond_memory.start()#runs in background
                    
                    #informs user of confirmation
                    print('Of course, I will remember', user_input)
                    
                    try:
                        timer.start()
                    except RuntimeError:pass
                    #stops for loop
                    break

    def coming_home(user_input):
        remember_data = pd.read_csv('data/userRemember.csv')#load data file
        new_row = {'remember': user_input, 'when': 'hi', 'output': 'None'}#prepare the new row
        remember_data.loc[len(remember_data)] = new_row#create a new row for the data
        remember_data.to_csv('data/userRemember.csv', index=False)#append to the csv file
    
    def respond(user_input):
        '''
        remind the user to respond to a specific contact type (e.g., email, whatsapp, message, etc.)
        '''
        remember = pd.read_csv('data/userRemember.csv')
        
        contact_type, person = memory.contact_pos_tag(user_input)

        if person == '':
            new_row = {'remember': user_input, 'when': 'timer', 'output': 'Reminder that you need to ' + contact_type + ' someone.'}
        else:
            new_row = {'remember': user_input, 'when': 'timer', 'output': 'Reminder that you need to ' + contact_type + person}
        
        remember.loc[len(remember)] = new_row
        remember.to_csv('data/userRemember.csv', index=False)
    
    def going_out_thread(user_input):
        remember_data = pd.read_csv('data/userRemember.csv')#load data file
        new_row = {'remember': user_input, 'when': 'bye', 'output': 'None'}#prepare the new row
        remember_data.loc[len(remember_data)] = new_row#create a new row for the data
        remember_data.to_csv('data/userRemember.csv', index=False)#append to the csv file
    
    def item_location(user_input):
        remember_data = pd.read_csv('data/userRemember.csv')
        ET_data = pd.read_csv('data/datasets/ET.csv')

        pos_tag = memory.pos_tagging(user_input)
        if pos_tag != "error":
            new_row = {'remember': user_input, 'when': 'None', 'output': pos_tag}#prepare the new row
            remember_data.loc[len(remember_data)] = new_row#create a new row for the data
            remember_data.to_csv('data/userRemember.csv', index=False)#append to the csv file
            
            new_ET_row = {'name': 'where is ' + pos_tag.split('***')[0], 'ET': 'where object'}
            ET_data.loc[len(ET_data)] = new_ET_row
            ET_data.to_csv('data/datasets/ET.csv', index=False)
            
            return 'reload data'
    
    def contact_pos_tag(user_input):
        from nltk import pos_tag, ne_chunk, word_tokenize, Tree
        
        words = word_tokenize(user_input)
        tags = pos_tag(words)
        tree = ne_chunk(tags)

        contact_type = []
        
        for subtree in tree:
            if isinstance(subtree, tuple):
                word, pos = subtree
                if pos == 'VB':
                    contact_type.append(word)
        
        name = user_input.split(contact_type[0])[1]
        return ''.join(contact_type), name
    
    def pos_tagging(user_input):
        from nltk import pos_tag, ne_chunk, word_tokenize
        
        words = word_tokenize(user_input)
        tags =  ne_chunk(pos_tag(words))
        
        item_and_location = []
        NNS = False

        for i in range(len(tags)):
            if tags[i][1] == 'NN' or tags[i][1] == 'NNS':
                if tags[i][1] == 'NNS':
                    NNS = True
                if tags[i-2][1] == 'IN':
                    item_and_location.append(tags[i-2][0])
            
                if tags[i-1][1] == 'DT':
                    item_and_location.append(tags[i-1][0])
            
                item_and_location.append(tags[i][0])
                
        try:
            if NNS is True:
                return f"{item_and_location[0]}***Your {item_and_location[0]} are {item_and_location[1]} {item_and_location[2]} {item_and_location[3]}"
            else:
                return f"{item_and_location[0]}***Your {item_and_location[0]} is {item_and_location[1]} {item_and_location[2]} {item_and_location[3]}"
        except IndexError:
            print(chatbot_tools.random_output('cannot find pos tag'))
            return 'error'

def blank_function():
    '''
    This is the only way of getting a background timer that seems to work as I want it throughout the entire program
    because threading.Timer requires a function (which is not desired) then this blank function that doesn't do anything 
    works as a decoy
    '''
    pass

#timer = threading.Timer(random.randint(900, 2400), blank_function)
timer = threading.Timer(12.00, blank_function)

#entity tag data
ET_data = pd.read_csv('data/datasets/ET.csv')#datasets/datatsets

#emotion based on positive, netrual, and negative emotions
positive_emotions = ['happy', 'love']
neutral_emotions = ['surprise', 'pain', 'hungry', 'bored']
negative_emotions = ['sad', 'anger', 'fear', 'unhappy']

vectorizer, classifier, er_vectorizer, er_classifier = models.preprocess_data()

#outputs different depending on whether the user is new or not to the program
with open('data/new user.txt', 'r') as f:
    read = f.read()
    if read == 'true':
        with open('data/new user.txt', 'w') as f:
            f.write('false')
        print(chatbot_tools.random_output('welcome user'))

run_loop = True

while run_loop is True:
    user_input = input('Input >>> ')
    process = models.process_input(user_input, vectorizer, classifier, er_vectorizer, er_classifier)  

    if process == 'reload data': #if the bot learns from wolfram alpha then it returns 'reload data' for it load the data model in again (takes around 1.5 seconds)
        vectorizer, classifier, er_vectorizer, er_classifier = models.preprocess_data()

###for any code that is temp search for ***
#TODO: Need to add bot birthday output once completed version, including it's age
#TODO: Need to be able to ask the user questions about themselves - (only once speech recognition in place)
#TODO: be able to allow the user to create a rountine to be reminded of
#TODO: Add built in calendar which can be used to remind the user of things on specific dates.

###list of things to add for it to remember
#take tablets (morning, afternoon, evening, night)