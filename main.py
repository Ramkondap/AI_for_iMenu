!pip install scikit-multilearn 
import os
import Restaurant
import speech_recognition as sr
from google.cloud import speech
from google.cloud import texttospeech
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

#Load ML model and vectorizer
loadModel = joblib.load('label_powerset_file.pkl')
loadVector = joblib.load('tfidf_vectorizer.pkl')

#Create vectorizer object
tfidf = TfidfVectorizer()

# Text to speech stuff
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred.json"
STT_client = speech.SpeechClient()
TTS_client = texttospeech.TextToSpeechClient()

Restaurant.name = "Curry Craft Nordahl"
Restaurant.delivery = False
Restaurant.website = "currycraft S.D. .com"
Restaurant.schedule = {"weekday": "8 AM to 9 PM",
                       "weekend": "9 AM to 10 PM"}

# Load food data
food_data = pd.read_csv("Food.csv")
Restaurant.appetizers = food_data['A']
Restaurant.entree = food_data['E']
Restaurant.dessert = food_data['D']
Restaurant.drinks = food_data['Drinks']

# Distinguish between yes and no
no_set = {"no", "nope", "nah", "not right now", "no thanks", "not this time"}
yes_set = {"yes", "yup", "yeah", "yea", "ya", "yas", "yep", "totally", "sure", "okay", "yes yes", "correct"}

# Numbers
num_dict = pd.read_csv('numbers.csv', header=None, index_col=0, squeeze=True).to_dict()

# Audio in/out
listener = sr.Recognizer()


def output_tts(reply):
    str(reply)
    print(reply)

    # Text that will be converted to audio
    synth_input = texttospeech.SynthesisInput(text=reply)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(language_code='en-IN', name='en-IN-Wavenet-B',
                                              ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    # Select audio file that you want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, pitch=0)

    # Perform TTS request on the text input with the selected voice params
    response = TTS_client.synthesize_speech(input=synth_input, voice=voice, audio_config=audio_config)

    # The response is saved to mp3 file
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    # [PLAY AUDIO]
    print("[output]: playing audio")
    from playsound import playsound
    playsound('output.mp3')
    os.remove('output.mp3')


def input_stt():
    try:
        with sr.Microphone() as source:
            print("[output]: Listening....")
            caller_input = listener.listen(source)
            user_response = listener.recognize_google(caller_input)
            print(user_response)
    except:
        get_human()

    return user_response.lower()


# Phone operations
def greeting():
    output_tts("Thank you for calling " + Restaurant.name + ". How can I help you?")

    initial_response = input_stt()

    #vectorize initial response to classify which route to take
    initial_vector = loadVector.transform([initial_response])

    #make a prediction
    predict_vector = loadModel.predict(initial_vector).toarray()

    # This is to skip questions and test code: --------------------------------------------------
    if initial_response == "check code":
        print("\n\n[output]: Skipping steps, please say your order now:")
        take_order()
        pass
    # End of test. ------------------------------------------------------------------------------

    """if initial_response in yes_set:
        carryout_or_delivery()
    else:
        output_tts("Do you want to know the store hours?")
        second_greeting = input_stt()
        if second_greeting in yes_set:
            output_tts("We are open from " + Restaurant.schedule.get("weekday") + " on the weekdays and "
                       + Restaurant.schedule.get("weekend") + " on the weekends.")
        else:
            get_human()
        pass"""

    #
    class_check = False
    for idx, x in enumerate(np.nditer(predict_vector)):
        if x == 1.0:
            class_check = True
            if idx == 0:
                get_human()
            elif idx == 1:
                carryout_or_delivery()
            elif idx == 2:
                price_check()
            else:
                output_tts("We are open from " + Restaurant.schedule.get("weekday") + " on the weekdays and "
                       + Restaurant.schedule.get("weekend") + " on the weekends.")
        else:
            if idx == 3 and not check:
                get_human()


def carryout_or_delivery():
    output_tts("Carryout or delivery?")
    carryout_check = input_stt()
    if carryout_check == "delivery":
        if Restaurant.delivery is False:
            output_tts("Sorry, we don't support delivery over the phone at this point. For delivery options please "
                       "check our website " + Restaurant.website)
        carryout_instead_output = "Would you like to place a carry out order instead?"

        output_tts(carryout_instead_output)
        carryout_instead = input_stt()
        if carryout_instead in yes_set:
            output_tts("What would you like?")
            take_order()
        else:
            output_tts("Would you like help with anything else?")
            other_help = input_stt()
            if other_help in no_set:
                output_tts("Thank you for calling, have a nice day.")
                exit(0)
            else:
                get_human()
    elif carryout_check == "carryout":
        output_tts("Ok, what would you like for carryout?")
        take_order()
    else:
        get_human()


def take_order():
    print("[output]: Taking order now...")
    cont_check = True

    try:
        with sr.Microphone() as source:
            caller_input = listener.listen(source)
            order = listener.recognize_google(caller_input)
            confirm_order(order)
    except:
        get_human()


def confirm_order(order):
    output_tts("You said, " + order + ", is that correct?")
    order_check = input_stt()
    if order_check in yes_set:
        # Check user forgot to order appetizers, dessert or entree
        print("[TEST]: switching to 'you_forgot()' ")
        you_forgot(order)
        # Clean order to a dictionary form.

        # Take important user information for the order
        output_tts("Can I get a name for the order?")
        name = input_stt()
        output_tts("If you have any special instructions for the order, please say them now or say skip.")
        detail = input_stt()

        print("[output]: Saving file...")
        f = open("order.txt", "w+")
        f.write(order + "\nName: " + name + "\nOther order details: " + detail)
        f.close()
        output_tts("Your order will be ready soon, have a good day!")
    else:
        output_tts("Can you repeat your order please?")
        take_order()


def you_forgot(order):
    print("[TEST]: making order lowercase")
    order = order.lower()
    apps_check = False
    entree_check = False
    dessert_check = False
    # Break 'order' into single words
    you_forgot_check = order.split()
    print("[TEST]: split order")

    print("[TEST]: Checking if words from order are in the sets")
    # Check if words are in the 3 sets
    if Restaurant.appetizers.lower() in you_forgot_check:
        apps_check = True
    else:
        print("[output]: aaps test pass")

    if Restaurant.entree.lower() in you_forgot_check:
        entree_check = True
    else:
        print("[output]: entree test pass")

    if Restaurant.dessert.lower() in you_forgot_check:
        dessert_check = True
    else:
        print("[output]: dessert test pass")

    while not apps_check:
        output_tts("You haven' ordered any appetizers, would you like to add them?")
        app_check_input = input_stt()
        if app_check_input in yes_set:
            update_order(order)
            apps_check = True
        else:
            apps_check = True

    while not entree_check:
        output_tts("You haven' ordered any entrees, would you like to add them?")
        entree_check_input = input_stt()
        if entree_check_input in yes_set:
            update_order(order)
            entree_check = True
        else:
            entree_check = True

    while not dessert_check:
        output_tts("You haven' ordered any appetizers, would you like to add them?")
        dessert_check_input = input_stt()
        if dessert_check_input in yes_set:
            update_order(order)
            dessert_check = True
        else:
            dessert_check = True


def update_order(order):
    output_tts("ok what would you like to add?")
    updating_the_order = input_stt()
    order.append(updating_the_order)
    # return order

def price_check():
    print("check price")


def get_human():
    output_tts("Please hold for one second.")
    # break


if __name__ == '__main__':
    greeting()