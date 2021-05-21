restaurant_name = "Name"
website = "website.com"


def greeting():
    print("Thank you for calling", restaurant_name)
    initial_response = input("Would you like to place an order?")
    if initial_response == "No":
        # need to do a check to see if they want to know about restaurant hours.
        # this part is not finished
        time_check = input("What do you need help with?")
        if time_check == "yes":
            pass
    else:
        is_carryout()


def is_carryout():
    carryout_check = input("Carryout or Delivery?")
    if carryout_check == "delivery":
        print("Sorry, we don't support delivery over the phone at this point."
              "For delivery options please check our website ", website)
        no_delivery = input("would you like to place a carry out order instead?")
        if no_delivery == "yes":
            return True
        else:
            other_help = input("Would you like help with anything else?")
            if other_help == "no":
                print("Thank you for calling, have a nice day.")
            else:
                # Get human
                # this part is not finished
                pass


greeting()
