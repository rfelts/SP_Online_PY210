import sys
from operator import itemgetter, attrgetter

donors_list = {
    "Jeff Bezos": {
        "donation_total": 877.33,
        "times_donated": 1,
        "average_donation": 877.33
    },
    "Paul Allen": {
        "donation_total": 708.42,
        "times_donated": 3,
        "average_donation": 236.14
    },
    "William Gates, III": {
        "donation_total": 653784.49,
        "times_donated": 2,
        "average_donation": 326892.24
    },
    "Bill Ackman": {
        "donation_total": 2354.05,
        "times_donated": 3,
        "average_donation": 784.68
    },
    "Mark Zuckerberg": {
        "donation_total": 16396.10,
        "times_donated": 3,
        "average_donation": 5465.37
    }
}

def menu_selection(prompt, dispatch_dict):
    # TODO Fix KeyError when user presses enter
    # causing an empty string to be sent as response
    while True:
        response = input(prompt)
        if dispatch_dict[response]() == "quit":
            sys.exit()

def quit_app():
    return "quit"

# Generate a list of donors from the database
def list_names():
    for i in sorted(donors_list.keys()):
        print(i)
    return

# sub menu for selecting donors
def find_donor():
    while True:
        fullname = input("type list to display names or quit to exit to main menu\n" \
                         "Enter full name of donor: ")
        if fullname == "list":
            return list_names()
        elif fullname:
            return send_thankyou(fullname)
        elif fullname == "quit":
            return menu_selection(main_menu, main_dispatch)
        else:
            return

# helper function to sort by total
def sort_donors(a_dict):
    return a_dict[1]["donation_total"]

# Generate report based on menu choice
# and return user to the menu prompt    
def generate_report(donors_list=donors_list):
    sorted_list = sorted(donors_list.items(), key=sort_donors, reverse=True)
    print("{:<20}|{:^15}|{:^15}|{:^15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gifts"))
    print("-" * 70)
    for donors in sorted_list:
        name = donors[0] 
        total = donors[1]["donation_total"] 
        times = donors[1]["times_donated"] 
        average = donors[1]["average_donation"]
        print(f"{name:<20}${total:>14.2f}{times:^18}${average:>12.2f}".format())

# This function sends the formatted email
# records donation amounts and adds new users 
# and their donaitons to the database
def send_thankyou(fullname):
    donation_amount = float(input("Donation amount: "))
    if fullname in donors_list.keys():
        print("Selecting Donor " + fullname)
        donors_list[fullname]["donation_total"] = donors_list[fullname]["donation_total"] + donation_amount
        donors_list[fullname]["times_donated"] += 1 
        donors_list[fullname]["average_donation"] = donors_list[fullname]["donation_total"] / donors_list[fullname]["times_donated"]
    else:
        donors_list.update({fullname: {"donation_total": donation_amount, "times_donated": 1, "average_donation": donation_amount}})

    email_template = "\n".join((f"Dear {fullname},\n\nThank you for your very kind donation of ${donation_amount:.2f}.\n",
                     "It will be put to very good use.\n",
                     "Sincerely,\n",
                     "-The Team"))

    with open(fullname + ".txt", "w") as file:
        file.write(email_template)

# Send email to all donors showing their total donations
def bulk_thankyou():
    for donors in donors_list.keys():
        donation_amount = donors_list[donors]["donation_total"]
        email_template = "\n".join((f"Dear {donors},\n\nThank you for your very kind donations this year totaling at ${donation_amount:.2f}.\n",
                     "It will be put to very good use.\n",
                     "Sincerely,",
                     "-The Team"))
        filename = donors.replace(" ","_") + ".txt"
        if "," in filename:
            filename = donors.replace(",","") + ".txt"
            with open(filename.replace(" ", "_"), "w") as file:
                file.write(email_template)
        else:
            with open(filename, "w") as file:
                file.write(email_template)
    
# main menu items    
main_menu = "Choose one of the following options. \n\n" \
            "1 - Send a Thank You to a single donor \n" \
            "2 - Create a Report \n" \
            "3 - Send letters to all donors \n" \
            "4 - Quit \n" \
            ">> "
# value returned from choice keys
main_dispatch = {
    "1": find_donor,
    "2": generate_report,
    "3": bulk_thankyou,
    "4": quit_app
}


if __name__ == '__main__':
    menu_selection(main_menu, main_dispatch)