# GOAL: Two characters debate,
# The debate starts randomly with one of the two characters,
# The program has the first one generate a response to the debate prompt
# The first response is then read using tts.
# Once the message is fully read, the other character is given his description and the past conversation and prompted to respond to it
# The reponse is then put through tts as well
# The debate continues back and forth until paused or closed
# Each response is only made after the user clicks the spacebar
# If the user presses "t" instead, they can enter the debate and have the other two respond to their message.
# If the user presses "e", the program closes

from openai import OpenAI
from pathlib import Path
from pygame import mixer
import random
import keyboard
import os

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

one = open('characterOne.txt', 'r')
two = open('characterTwo.txt', 'r')
char_a_desc = one.read()
char_b_desc = two.read()
one.close()
two.close()

client = OpenAI()
mixer.init()


# Class that runs all events within the AI characters' debate
class DebateSimulator:
    

    # Define each character's description, 
    # Create a history variable to keep track of all debate messages, 
    # And add a token counter (For personal knowledge)
    def __init__(self, char_a_desc, char_b_desc, char_a_voiceID, char_b_voiceID, user_voiceID):
        self.char_a_desc = char_a_desc
        self.char_b_desc = char_b_desc
        self.char_a_voiceID = char_a_voiceID
        self.char_b_voiceID = char_b_voiceID
        self.user_voiceID = user_voiceID
        self.history = []



    # This method is for getting a character's response through the OpenAI API call
    def get_response(self, character_description, prompt):
        # OpenAI API call
        messages = [
            {"role": "system", "content": character_description},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        response_text = response.choices[0].message.content
        
        return response_text
        

    # This method is for turning any text inputs either from characters or from the user into speech
    def text_to_speech(self, text, voice_id, speech_file_location):
        # Check if there is already a mp3 file in the desired location, and if so, delete the file
        if os.path.exists(speech_file_location):
            os.remove(speech_file_location)
        
        # Convert the text response into speech using OpenAI's speech module
        speech_file_path = Path(__file__).parent / speech_file_location  #"speech.mp3"
        audio = client.audio.speech.create(
            model = "tts-1",
            voice = voice_id,
            input = text
        )
        
        audio.stream_to_file(speech_file_path)
        mixer.music.load(speech_file_location)
        mixer.music.play()
        

    # This is the main method of the program, all other functions are called within this function
    # This function also loops until the program is ended by the user
    def debate(self, debate_prompt):
        debate_opening = "Today's debate will be on the following topic: " + debate_prompt
        self.text_to_speech(debate_opening, self.user_voiceID, user_file_location) # Read the inital prompt out in the user's voice
        turn = random.choice(['A', 'B'])   # Turn variable used to keep track of which character is up next
        self.history.append({"role": "user", "content": debate_prompt})
        
        if turn == 'A':
            response_a = self.get_response(self.char_a_desc, debate_prompt)
            print(f"Character A: {response_a}")
            self.text_to_speech(response_a, character_a_voiceID, character_a_file_location)
            self.history.append({"role": "assistant", "content": response_a})
            turn = 'B'
        
        else:
            response_b = self.get_response(self.char_b_desc, debate_prompt)
            print(f"Character B: {response_b}")
            self.text_to_speech(response_b, character_b_voiceID, character_b_file_location)
            self.history.append({"role": "assistant", "content": response_b})
            turn = 'A'
        
        # Begin debate loop after initial response
        while True:
            
            # Wait for user input (spacebar, t, or e)
            # "Spacebar" continues the debate nominally, 
            # "t" allows user to input an argument, 
            # "e" ends the debate
            print("-----------------------------------------------------------------------------------------------------------------------")
            print("Press spacebar to continue, 't' to input your argument, or 'e' to end the debate...")
            event = keyboard.read_event()

            # If "spacebar" is the user input
            if event.event_type == keyboard.KEY_DOWN and event.name == 'space': 
                pass
            
            # If "t" is the user input
            elif event.event_type == keyboard.KEY_DOWN and event.name == 't':
                user_argument = input("Enter your argument: ").strip()
                print(f"You: {user_argument}")
                self.text_to_speech(user_argument, user_voiceID, user_file_location)
                self.history.append({"role": "user", "content": user_argument})
                
                if turn == 'B':
                    response_b = self.get_response(self.char_b_desc, user_argument)
                    print(f"Character B: {response_b}")
                    self.text_to_speech(response_b, character_b_voiceID, character_b_file_location)
                    self.history.append({"role": "assistant", "content": response_b})
                    turn = 'A'

                else:
                    response_a = self.get_response(self.char_a_desc, user_argument)
                    print(f"Character A: {response_a}")
                    self.text_to_speech(response_a, character_a_voiceID, character_a_file_location)
                    self.history.append({"role": "assistant", "content": response_a})
                    turn = 'B'
                
                continue
            
            # If "e" is the user input
            elif event.event_type == keyboard.KEY_DOWN and event.name == 'e':
                print("The Debate has concluded.")
                self.text_to_speech("Today's debate has concluded!", self.user_voiceID, user_file_location)
                break
            
            # Continuing the debate normally after spacebar is pressed
            if turn == 'B':
                response_b = self.get_response(self.char_b_desc, self.history[-1]["content"])
                print(f"Character B: {response_b}")
                self.text_to_speech(response_b, character_b_voiceID, character_b_file_location)
                self.history.append({"role": "assistant", "content": response_b})
                turn = 'A'
            else:
                response_a = self.get_response(self.char_a_desc, self.history[-1]["content"])
                print(f"Character A: {response_a}")
                self.text_to_speech(response_a, character_a_voiceID, character_a_file_location)
                self.history.append({"role": "assistant", "content": response_a})
                turn = 'B'
            


if __name__ == '__main__':

  # Define character descriptions
  character_a_description = char_a_desc
  character_a_voiceID = "fable"
  character_a_file_location = "characterOne.mp3"

  character_b_description = char_b_desc
  character_b_voiceID = "onyx"
  character_b_file_location = "characterTwo.mp3"

  user_voiceID = "echo"
  user_file_location = "user.mp3"

  # Get debate prompt from user
  debate_prompt = input("Enter the debate prompt: ").strip()

  # Initialize the DebateSimulator and start the debate
  simulator = DebateSimulator(character_a_description, character_b_description, character_a_voiceID, character_b_voiceID, user_voiceID)
  simulator.debate(debate_prompt)
