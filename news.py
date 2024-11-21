'''
This is for giving the user news
'''

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
import re
import webbrowser

from tools import *

class News():
    def get_news_intent(self, entity, vectorizer, classifier):
        if entity == "latest news": self.get_latest_news(vectorizer, classifier)
        elif entity == "space news": self.get_latest_space_news()
        else: return 0

    def get_latest_news(self, vectorizer, classifier):
        latest_news = requests.get('https://api.currentsapi.services/v1/latest-news?page_size=200&language=en&apiKey=iChF0rDovQfg2Kf787UiAGKB4QHOBLK2aSrSp6mA8PSGhzVe')
        if latest_news.status_code == 200:
            latest_news = latest_news.json()
            for news in latest_news['news']:
                source = chatbot_tools.extract_website_name(news['url']).replace("www.", "")

                print(f"{news['title']}... {''.join(news['category'])} from {source}") #outputs the minimal of the news to see if the user is interested
                
                user_input = input("") #make it feel more natual by keeping input blank so the user can say what they want

                sr_vectorizer = vectorizer.transform([user_input])
                sentiment = classifier.predict(sr_vectorizer)[0]#uses sentiment analysis to determine if the user is interested in the news or wants to continue

                if sentiment == 'positive' and 'next' not in user_input:
                    if 'open' in user_input or 'look' in user_input or 'full' in user_input: #if any of these words are included in the user's input then they likekly want the news article opening up in a web browser
                        webbrowser.open(news['url'])
                        
                        check = self.latest_news_continue_check(vectorizer, classifier)#checks if the user wants to continue reading news
                        
                        if check == "break": break
                        else : continue
                    else:
                        print("Sure, here's more information:")
                        description = re.sub(r'(\.\.\.\s*|,\s*|\band\s+)[^.]*$', '', news['description'])
                        print(description)

                        check = self.latest_news_continue_check(vectorizer, classifier)#checks if the user wants to continue reading news
                        
                        if check == "break": break
                        else : continue

                elif sentiment == 'negative':
                    continue #continue to the next news article

    def latest_news_continue_check(self, vectorizer, classifier):
        continue_input = input()
        sr_vectorizer = vectorizer.transform([continue_input])
        sentiment = classifier.predict(sr_vectorizer)[0]

        if sentiment == 'positive':
            return None #let it continue to a new article
        else:
            print("Stopping the news...")
            return "break"