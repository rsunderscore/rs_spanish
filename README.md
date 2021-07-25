# rs_spanish
## leaning spanish during COVID
I took up spanish(again) during COVID and I wanted a Q&A type game to practice vocabulary and conjugations.  
I also wanted to prevent data entry errors for accented letters so there is a module that will go to the internet and look up data from a web site.  
Translations are then cached locally.

MVP Objectives
1. user is prompted with a verb and tense in english and must enter a response with correct translation
1. user is prompted with a vocab word in spanish and must enter response in English
1. user is prompted with a vocab word in English and must enter response in Spanish

Nice-to-haves
1. a GUI for the user interaction
2. config file to retain user preferences
3. group vocab words by category
4. voice recognition

I used beautiful soup to parse a web site scanning for particular tags, classes, and text to identify the relevant tables, and then used pandas to extract them.
In most cases this required parsing several tables, reformatting, and combining them to get a complete conjugation data structure for use in the game portion.
The conjugation data structure is cached locally for offline used and increased speed for subsequent executions.  This method inherently tracks progress as the word 
list grows over time as they are added to the cache.  I did attempt to record the users voice and compare with a stored sample, but I was unable to get microphone interface
packages to work on Windows.  I suspect this is due to windows security features around microphone access but have not been able to find a workaround thus far.
