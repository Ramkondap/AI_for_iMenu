import Restaurant

Restaurant.name = "Name Here"
Restaurant.delivery = False
Restaurant.website = "website.com"
Restaurant.schedule = {"weekday": "8 AM to 9 PM",
                       "weekend": "9 AM to 10 PM"}

no_set = {"no", "nope", "nah", "not right now", "no thanks", "not this time"}
yes_set = {"yes", "yup", "yeah", "yea", "ya", "yas", "yep", "totally", "sure"}
hours_set = {"open", "closed", "close", "time"}


def output_tts(reply):
    print(reply)

    '''
    # [START TTS]
    
    https://cloud.google.com/text-to-speech
    
        1. Enable Text-to-Speech API service.
        2. Create a Service Account.
        3. Download Service Account client file (JSON file).
        4. Install Text-To-Speech Python Client library.
        5. Create a Python program to convert texts to audio (MP4 file).
        6. Play back file. 

    
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=reply)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
          
    # [END TTS]
    
    # [PLAY AUDIO] 
    
    from playsound import playsound
    playsound('output.mp3')
'''


def greeting():
    output_tts("Thank you for calling " + Restaurant.name + "Would you like to place an order?")
    initial_response = input().lower()
    if initial_response in yes_set:
        carryout_or_delivery()
    else:
        for _ in initial_response:  # Might need to edit this
            if initial_response.__contains__(hours_set):
                output_tts("We are open from " + Restaurant.schedule.get("weekday") + "on the weekdays and "
                           + Restaurant.schedule.get("weekend") + "on the weekends.")
            else:
                get_human()


def carryout_or_delivery():
    output_tts("Carryout or delivery?")
    carryout_check = input().lower()
    if carryout_check == "delivery":
        if Restaurant.delivery is False:
            output_tts("Sorry, we don't support delivery over the phone at this point. For delivery options please "
                       "check our website " + Restaurant.website)
        carryout_instead = input("would you like to place a carry out order instead?")
        if carryout_instead in yes_set:
            take_order()
        else:
            other_help = input("Would you like help with anything else?")
            if other_help in no_set:
                output_tts("Thank you for calling, have a nice day.")
            else:
                get_human()
    take_order()


def take_order():
    pass


def get_human():
    output_tts("Please hold for one second.")
    pass


if __name__ == '__main__':
    greeting()
