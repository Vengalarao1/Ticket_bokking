import random
import pickle
import sys

logged_in = False  # global variable
uid = 0
pwd = ''

class Train:
    def __init__(self, name='', num=0, arr_time='', dep_time='', src='', des='', day_of_travel='', seat_available_in_1AC=0, seat_available_in_2AC=0, seat_available_in_SL=0, fare_1ac=0, fare_2ac=0, fare_sl=0):
        self.name = name
        self.num = num
        self.arr_time = arr_time
        self.dep_time = dep_time
        self.src = src
        self.des = des
        self.day_of_travel = day_of_travel
        self.seats = {'1AC': seat_available_in_1AC, '2AC': seat_available_in_2AC, 'SL': seat_available_in_SL}
        self.fare = {'1AC': fare_1ac, '2AC': fare_2ac, 'SL': fare_sl}

    def print_seat_availability(self):
        print("No. of seats available in 1AC: " + str(self.seats['1AC']))
        print("No. of seats available in 2AC: " + str(self.seats['2AC']))
        print("No. of seats available in SL: " + str(self.seats['SL']))

    def check_availability(self, coach='', ticket_num=0):
        coach = coach.upper()
        if coach not in ('SL', '1AC', '2AC'):
            self.print_seat_availability()
            coach = input("Enter the coach (1AC/2AC/SL): ")
        if self.seats[coach] == 0:
            return False
        elif self.seats[coach] >= ticket_num:
            return True
        else:
            return False

    def book_ticket(self, coach='', no_of_tickets=0):
        self.seats[coach] -= no_of_tickets
        return True

class Ticket:
    def __init__(self, train, user, ticket_num, coach):
        self.pnr = str(train.num) + str(user.uid) + str(random.randint(100, 999))
        self.train_num = train.num
        self.coach = coach
        self.uid = user.uid
        self.train_name = train.name
        self.user_name = user.name
        self.ticket_num = ticket_num
        user.history.update({self.pnr: self})
        ticket_dict.update({self.pnr: self})

class User:
    def __init__(self, uid=0, name='', hometown='', cell_num='', pwd=''):
        self.uid = uid
        self.name = name
        self.hometown = hometown
        self.cell_num = cell_num
        self.pwd = pwd
        self.history = {}

class Acceptors:
    ''' Class containing functions for accepting and 
    validating values properly'''

    @staticmethod
    def accept_uid():
        try:
            uid = int(input("Enter the User ID: "))
        except ValueError:
            print("Please enter user ID properly.")
            return Acceptors.accept_uid()
        else:
            return uid

    @staticmethod
    def accept_pwd():
        pwd = input("Enter your password: ")
        return pwd

    @staticmethod
    def accept_train_number():
        try:
            train_num = int(input("Enter the train number: "))
        except ValueError:
            print("Please enter train number properly.")
            return Acceptors.accept_train_number()
        else:
            if train_num not in trains:
                print("Please enter a valid train number.")
                return Acceptors.accept_train_number()
            else:
                return train_num

    @staticmethod
    def accept_menu_option():
        option = input("Enter your option: ")
        if option not in ('1', '2', '3', '4', '5', '6', '7', '8'):
            print("Please enter a valid option!")
            return Acceptors.accept_menu_option()
        else:
            return int(option)

    @staticmethod
    def accept_coach():
        coach = input("Enter the coach: ").upper()
        if coach not in ('SL', '1AC', '2AC'):
            print("Please enter coach properly.")
            return Acceptors.accept_coach()
        else:
            return coach

    @staticmethod
    def accept_prompt():
        prompt = input("Confirm? (y/n): ")
        if prompt not in ('y', 'n'):
            print("Please enter proper choice.")
            return Acceptors.accept_prompt()
        return prompt

    @staticmethod
    def accept_ticket_num():
        try:
            ticket_num = int(input("Enter the number of tickets: "))
            if ticket_num < 0:
                raise ValueError
        except ValueError:
            print("Enter proper ticket number.")
            return Acceptors.accept_ticket_num()
        else:
            return ticket_num

    @staticmethod
    def accept_pnr():
        pnr = input("Enter your PNR number: ")
        if pnr not in ticket_dict:
            print("Please enter proper PNR number.")
            return Acceptors.accept_pnr()
        else:
            return pnr

def book_ticket():
    if not logged_in:
        login('p')
    check_seat_availability('p')
    choice = Acceptors.accept_train_number()
    trains[choice].print_seat_availability()
    coach = Acceptors.accept_coach()
    ticket_num = Acceptors.accept_ticket_num()
    if trains[choice].check_availability(coach, ticket_num):
        print("You have to pay: ", trains[choice].fare[coach] * ticket_num)
        prompt = Acceptors.accept_prompt()
        if prompt == 'y':
            trains[choice].book_ticket(coach, ticket_num)
            print("Booking Successful!")
            tick = Ticket(trains[choice], users[uid], ticket_num, coach)
            print("Please note PNR number: ", tick.pnr)
            menu()
        else:
            print("Exiting...")
            menu()
    else:
        print(ticket_num, " tickets not available")
        menu()

def cancel_ticket():
    pnr = Acceptors.accept_pnr()
    if pnr in ticket_dict:
        check_pnr(pnr)
        print("Cancel the tickets?")
        prompt = Acceptors.accept_prompt()
        if prompt == 'y':
            if logged_in:
                print("Ticket Cancelled.")
                trains[ticket_dict[pnr].train_num].seats[ticket_dict[pnr].coach] += ticket_dict[pnr].ticket_num
                del users[ticket_dict[pnr].uid].history[pnr]
                del ticket_dict[pnr]
            else:
                login('p')
                print("Ticket Cancelled.")
                trains[ticket_dict[pnr].train_num].seats[ticket_dict[pnr].coach] += ticket_dict[pnr].ticket_num
                del users[ticket_dict[pnr].uid].history[pnr]
                del ticket_dict[pnr]
        else:
            print("Ticket not cancelled")
    menu()

def check_seat_availability(flag=''):
    src = input("Enter the source station: ")
    des = input("Enter the destination station: ")
    flag_2 = 0
    for i in trains:
        if trains[i].src == src and trains[i].des == des:
            print("Train Name: ", trains[i].name, "Number: ", trains[i].num, "Day of Travel: ", trains[i].day_of_travel)
            flag_2 += 1
    if flag_2 == 0:
        print("No trains found between the stations you entered.")
        menu()
    if flag == '':
        train_num = Acceptors.accept_train_number()
        trains[train_num].print_seat_availability()
        menu()
    else:
        pass

def check_pnr(pnr=''):
    if pnr == '':
        pnr = Acceptors.accept_pnr()
    print("User name: ", ticket_dict[pnr].user_name)
    print("Train name: ", ticket_dict[pnr].train_name)
    print("Train number: ", ticket_dict[pnr].train_num, "Source: ", trains[ticket_dict[pnr].train_num].src, "Destination: ", trains[ticket_dict[pnr].train_num].des)
    print("No. of Tickets Booked: ", ticket_dict[pnr].ticket_num)
    print()

def create_new_acc():
    user_name = input("Enter your user name: ")
    pwd = input("Enter your password: ")
    uid = random.randint(1000, 9999)
    hometown = input("Enter your hometown: ")
    cell_num = input("Enter your phone number: ")
    u = User(uid, user_name, hometown, cell_num, pwd)
    print("Your user ID is: ", uid)
    users.update({u.uid: u})
    menu()

def login(flag=''):
    global uid
    global pwd
    uid = Acceptors.accept_uid()
    pwd = Acceptors.accept_pwd()
    if uid in users and users[uid].pwd == pwd:
        print("Welcome ", users[uid].name, "!")
        global logged_in
        logged_in = True
    else:
        print("No such user ID / Wrong Password!")
        return login()
    if flag == '':
        menu()

def check_prev_bookings():
    if not logged_in:
        login('p')
    for i in users[uid].history:
        print("PNR number: ", i)
        check_pnr(i)
    menu()

def end():
    save_data()
    print("Thank You!")
    sys.exit()

def load_data():
    global trains, users
