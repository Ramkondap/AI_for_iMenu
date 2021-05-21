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
    print(reply)  # need to change this to TTS.
    
    
def greeting():
    output_tts("Thank you for calling " + Restaurant.name + "Would you like to place an order?")
    initial_response = input().lower()
    if initial_response in yes_set:
        carryout_or_delivery()
    else:
        for i in initial_response:
            if initial_response[i] in hours_set:
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
    pass


if __name__ == '__main__':
    greeting()
