import Restaurant
import speech_recognition as sr

Restaurant.name = "Name Here"
Restaurant.delivery = False
Restaurant.website = "website.com"
Restaurant.schedule = {"weekday": "8 AM to 9 PM",
                       "weekend": "9 AM to 10 PM"}

no_set = {"no", "nope", "nah", "not right now", "no thanks", "not this time"}
yes_set = {"yes", "yup", "yeah", "yea", "ya", "yas", "yep", "totally", "sure"}

listener = sr.Recognizer()


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


def input_stt():
    try:
        with sr.Microphone() as source:
            print("Listening....")
            caller_input = listener.listen(source)
            user_response = listener.recognize_google(caller_input)
            print(user_response)
    except:
        get_human()

    return user_response.lower()


def greeting():
    output_tts("Thank you for calling " + Restaurant.name + ". Would you like to place an order?")
    initial_response = input_stt()

    if initial_response in yes_set:
        carryout_or_delivery()
    else:
        output_tts("Do you want to know the store hours?")
        second_greeting = input_stt()
        if second_greeting in yes_set:
            output_tts("We are open from " + Restaurant.schedule.get("weekday") + " on the weekdays and "
                       + Restaurant.schedule.get("weekend") + " on the weekends.")
        else:
            get_human()
        pass


def carryout_or_delivery():
    output_tts("Carryout or delivery?")
    carryout_check = input_stt()
    if carryout_check == "delivery":
        if Restaurant.delivery is False:
            output_tts("Sorry, we don't support delivery over the phone at this point. For delivery options please "
                       "check our website " + Restaurant.website)
        carryout_instead_output = "Would you like to place a carry out order instead?"
        print(carryout_instead_output)
        carryout_instead = input_stt()
        if carryout_instead in yes_set:
            print("mark as delivery")  # need to do this.
            take_order()
        else:
            print("Would you like help with anything else?")
            other_help = input_stt()
            if other_help in no_set:
                output_tts("Thank you for calling, have a nice day.")
                return
            else:
                get_human()
    print("Ok, what would you like for carryout?")
    take_order()


def take_order():
    cont_check = True

    try:
        while cont_check:
            with sr.Microphone() as source:
                caller_input = listener.listen(source)
                order = listener.recognize_google(caller_input)
                print(order)

                if order == "thats it":
                    cont_check = False
    except:
        get_human()

    confirm_order()


def confirm_order():
    print("This will repete back the order.")
    pass


def get_human():
    output_tts("Please hold for one second.")
    # break


if __name__ == '__main__':
    greeting()
