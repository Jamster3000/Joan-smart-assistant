(Still working on)

# Joan

🤖 This is a smart assistant called `"Joan"`. Being developed purposly for running on low resource systems, such as a raspberry pi. It uses machine learning (scikit-learn) rather than chatbot frameworks (such as tensorflow, chatterbot, etc.), which is much faster and allows for more control over how the assistant works. In addition to this, A.I. isn't used for this because it's easier to understand and know what's going on with machine learning than it is A.I. frameworks.

## API's used:
In addition to the machine leaning it also uses several different APIs and more to come. None of these used API's have been paied for as they are free or use a free tier. A list of API's that are used:
- Wolfram  Alpha - Used to respond to anything that `"Joan`" can't or doesn't have a response for. Joan saves the answer allowing it to do "Live Learning".
- Accuweather - Used to get weather data from a location (The user doesn't need to give `"Joan"` their location, It just knows).
- omdbapi - (Open Movie Database) API for getting data about movies, although Wolfram Alpha also knows information about movies.
- spaceflightnewsapi - Gets news about space flights and events in relation to it.
- currentsapi - Gets general news which also contains keywords to each article allowing the user to filter news sources.
- genderize - This is used to determine what gener the user is, this seems to work pretty well.
- totalvirus - this is used to scan a website, whether that be the website that is open or a link that was last copied.
- api64.ipify - Get's the user's IP address.
- ipapi - This is used to get the user's IP data, which includes their current location.

> [!WARNING]
> While in the development phase the API keys are visible in the code and can be used easily. Many of these API's have limited usage every `week/month`.

## Modules/libraries that are required to be installed:
- Pandas
- Scikit-learn
- pywikihow
- youtube-search-python
- nltk
- inflect
- fuzzywuzzy
- requests
- pyperclip
- pyautogui
- word2number

> [!NOTE]
> Since this is being developed to run on devices such as a raspberry pi, the modules and libraries above should all install and work as expected, even on 32-bit system.

## How To Use:
To run this code open up `"Joan.py"` and run it, depending on your machine specs it should take anywhere from 3 (ish) to 5 seconds to import all the libraries and load and train the model.


## List Of Things Currently Possible With `Joan`:
- 

## "Responses.csv" Tags:
<sub>Each tag is surrounded by "<" and ">"</sub>

- user-name - can include the user's name
- date - Includes the date whether that is current date or some other date
- emotion - a type of emotion
- F-food - The users favourite food
- game-name - Name of the game (used for user peference when game has multiple names).
- riddle-answe - the answer to the riddle
- correct-answer - The correct answer to a trivia question
- list-games - a list of games that can be played with `Joan`
- unsafe-scans - the amount of scans that returned as a dangerous website
- food - food
- sure-name - the surename of the user


## Data Files included:
- datasets/ET.csv - Entity tag, this is the main file for recognizing what the user has inputted.
- datasets/ER.csv - Emotion recognition, used to detect the user's emotins based on their input.
- Expected content.txt - This includes what sort of input is expected next.
- last time used.txt - The last time `"Joan"` was used, which is used within the code.
- log.txt - Just logs basic background operations within Joan.
- responses.csv - A long list in each row containing different variations of outputs.
- user data.csv - all the user's data for `Joan` to remember.

![GitHub issues](https://img.shields.io/github/issues/jamster3000/ImageSearch)
![Last Commit](https://img.shields.io/github/last-commit/jamster3000/ImageSearch)
![GitHub Stars](https://img.shields.io/github/stars/jamster3000/ImageSearch?style=social)![Code Size](https://img.shields.io/github/languages/code-size/jamster3000/ImageSearch)
