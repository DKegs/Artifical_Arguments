This program simulates a debate between to characters.
The characters are created by the user in the CharacterOne and CharacterTwo txt files.
There is an example character in each file that is fully functional.
The program pits these two characters against each other on the debate topic presented by the user.
These characters come to life through OpenAI's AI.
The user can also jump into the argument, which the characters will respond to.
Hope you enjoy it, I had a lot of fun making it!
To use the program, run the Artifical_Arguments.py file.

Some important notes:

You will need the following to use this program:
    - An OPENAI api key with the proper funding (Make a .env file in this folder with the following format: OPENAI_API_KEY=sk-proj-*** (Your API Key in place of "***")).
    - The following packages installed with pip:
        - pygame (for automatic TTS)
        - openai (for connecting to OpenAI)
        - keyboard (for user inputs)