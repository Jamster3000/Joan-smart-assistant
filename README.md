(Still working on)

A smart assistant called "Joan". Being developed purposly for running on low resource systems, such as a raspberry pi. Uses machine learning (scikit-learn) rather than chatbot frameworks (such as tensorflow, chatterbot, etc.), which is much faster and allows for more control over how the assistant works.

In addition to the machine leaning it also uses several different APIs and more to come. A major API used is wolfram alpha which is used to respond to the users input when "Joan" doesn't have a response for it (which is slowly becoming less likely).
It also uses accuweather api to get weather data from five days in advanced.

###Tags used in the responses.csv file###
#tag bewteen left and right arrow symbol

user-name - can include the user's name

date - Includes the date whether that is current date or some other date

emotion - a type of emotion

F-food - The users favourite food

game-name - Name of the game (used for user peference when game has multiple names).

riddle-answe - the answer to the riddle

correct-answer - The correct answer to a trivia question

list-games - a list of games that can be played with Joan

unsafe-scans - the amount of scans that returned as a dangerous website

food - food
______________________________________________________________________________________________________________

###data files###

The csv data files are named based on their letters

datasets/ET.csv - Entity tag

datasets/ER.csv - Emotion recognition

conversations.csv - For remembing past conversations

Expected content.txt - Includes what sort of user input is expected next

last time used.txt - The last time "Joan" was used

log.txt                   Just logs basic background operations within Joan

responses.csv             Joan's outputs

user data.csv             all the user's data for Joan to remember.


______________________________________________________________________________________________________________
  
