'''
This is for usage and integration for pywikihow (aka, wikihow)
'''
import webbrowser
from pywikihow import WikiHow

#file imports
from handle_intent import handle_entity
from tools import *

class Wikihow():
    def __init__(self):
        pass
    
    def get_wiki_intent(self, user_input):
        if user_input.startswith('how to ') and len(user_input) > 7:
            self.search_how_to(user_input)
        else:
            return 0

    def search_how_to(self, user_input):
        search_results = list(WikiHow.search(user_input, max_results=1))

        if search_results:
            article = search_results[0]
            webbrowser.open(article.url)
        else:
            print("Sorry, I couldn't find any articles for that query.")