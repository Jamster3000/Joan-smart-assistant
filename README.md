(Still working on)

# Joan 🤖 - Your smart assistant

Welcome to **Joan**, a lightweight and resource-efficient smart assistant designed to run seamlessly on low-resource systems like Raspberry Pi. **Joan** leverages machine learning (scikit-learn) for speed and control, making it a user-friendly alternative to traditional chatbot frameworks. Unlike typical AI frameworks, **Joan** prioritizes transparency and simplicity for easy understanding.

## Features 🚀
- **Game Time:** Play blackjack, rock-paper-scissors, or a number guessing game.
- Ask it to open a specific video on `Youtube`
- **Entertainment:** **Joan** can tell jokes, riddles, trivia questions, and even gives facts and advice (Do not follow)
- **open Websites:** Open's random [XKCD](https://xkcd.com/) With a random image; akinator and the wiki game.
- **Wikihow:** Can search for wikihow articles and either read them to you or show you the webpage.
- **news:** Can give the latest news articles
- **Passcode:** A Passcode can be set up. This can be used to confirm you asked for certain commands, such as a factory reset (e.g. "factory reset [passcode]")
- **recipes:** Has built in dataset of recipes allowing you to ask for a specific one.
- **Factory rest:** This will remove any data that it has collected from the user, but it still remembers what it has learned from **wolfram Alpha**
- **weather:** Can ask for the current weather, what the weather will be like tomorrow or on a specific day.
- **Time/date:** Can tell the time, full date, the day, the month, and the year.
- **Security:** **Joan** can scan a website to determine whether it's safe, proceed with caution, or dangerous. you must have the website open or copy the URL of the website for this to work.

> [!NOTE]
> In addition to all these features, there are also ***Easter Eggs*** Because I am a fan of them in programs 🥚


## Memory 🧠
**Joan** possesses a memory feature designed not for conversation but for remembering crucial details on behalf of the user. This functionality is a work in progress, intricately crafted to address specific memory issues, including short-term memory loss.

### How Memory Works
**Command Keyword**: The memory feature requires commands to start with the keyword **remember**.

### Example Usage:
- To inform **Joan** about the location of your keys:
      `remember I have put my keys in the bowl`

- Inquiring about your keys later is as simple as asking,
      `Where are my keys?` and **Joan** will promptly retrieve the information.

- General reminders are also supported:
      `remember that I need to check my email`
  **Joan** sets a background timer, randomly ranging between 900 and 2400 seconds. Upon timer expiration, **Joan** reminds you during the next interaction.

- Reminders persist even if you plan to perform a task later. For example, if you state:
    `remember that I need to turn off the lights before leaving`
  **Joan** will remind you at an appropriate time, ensuring you don't forget.

### Quick Reference
Here's a summary of commands for easy reference:

- **To remember a location**: remember [details]
- **To set a general reminder***: remember that [reminder]
- **To ask about remembered details**: [question]
This functionality is part of **Joan's** commitment to providing a helpful and adaptive user experience.

> [!NOTE]
> This feature is continually evolving to better serve users with diverse memory-related needs.

## API's and Services 🌐
**Joan** integrates seamlessly with various APIs:

- **Wolfram  Alpha** - Used to respond to anything that **Joan** can't or doesn't have a response for. **Joan** saves the answer allowing it to do "Live Learning".
- **Accuweather** - Used to get weather data from a location (The user doesn't need to give **Joan** their location, It just knows).
- **omdbapi** - (Open Movie Database) API for getting data about movies, although Wolfram Alpha also knows information about movies.
- **spaceflightnewsapi** - Gets news about space flights and events in relation to it.
- **currentsapi** - Gets general news which also contains keywords to each article allowing the user to filter news sources.
- **genderize** - This is used to determine what gener the user is, this seems to work pretty well.
- **totalvirus** - this is used to scan a website, whether that be the website that is open or a link that was last copied.
- **ipapi** - This is used to get the user's IP data, which includes their current location.

> [!WARNING]
> While in the development phase the API keys are visible in the code and can be used easily. Many of these API's have limited usage every `week/month`.

## Prerequisites 🛠️

Ensure the following libraries are installed:

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
- ipinfo

> [!NOTE]
> Since this is being developed to run on devices such as a raspberry pi, the modules and libraries above should all install and work as expected, even on 32-bit system.


## How To Use 🚀
Run **Joan.py**, and within 3 to 5 seconds, you're ready to explore the capabilities.

## **Response** Tags 🏷️
<sub>Each tag is surrounded by "<" and ">"</sub>

- user-name - can include the user's name
- date - Includes the date whether that is current date or some other date
- emotion - a type of emotion
- F-food - The users favourite food
- game-name - Name of the game (used for user peference when game has multiple names).
- riddle-answe - the answer to the riddle
- correct-answer - The correct answer to a trivia question
- list-games - a list of games that can be played with **joan**
- unsafe-scans - the amount of scans that returned as a dangerous website
- food - food
- sure-name - the surename of the user


## Data Files 📂:
- datasets/ET.csv - Entity tag, this is the main file for recognizing what the user has inputted.
- datasets/ER.csv - Emotion recognition, used to detect the user's emotins based on their input.
- Expected content.txt - This includes what sort of input is expected next.
- last time used.txt - The last time **Joan** was used, which is used within the code.
- log.txt - Just logs basic background operations within **Joan**.
- responses.csv - A long list in each row containing different variations of outputs.
- user data.csv - all the user's data for **Joan** to remember.

![GitHub issues](https://img.shields.io/github/issues/jamster3000/Joan-smart-assistant)
![Last Commit](https://img.shields.io/github/last-commit/jamster3000/Joan-smart-assistant)
![GitHub Stars](https://img.shields.io/github/stars/jamster3000/Joan-smart-assistant?style=social)![Code Size](https://img.shields.io/github/languages/code-size/jamster3000/Joan-smart-assistant)
