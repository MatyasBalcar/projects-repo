#imports
import time,pickle,os

#ELEMENTAL VARIABLES
#stores users in an array, no user can exist outside of it
users=[]
users_dict={}

run = True
#template for a user
class User:
    def __init__(self, name):
        self.name =  name
        self.debt =0#negative is good
        self.debts_list= {}
        users_dict[self.name]=self
    #changes debt amount based on amount given
    def changeDebt(self, amount):
        self.debt+=amount
    #adds the amount and payer to the dict
    def newDebt(self, amount, debtor):
        self.debts_list[debtor]=(amount)
    def save(self):
        #debts_list
        with open(str(self.name)+'.pkl','wb') as pkl:
            pickle.dump(self.debts_list,pkl)
        with open(str(self.name)+'-debt.txt','w')as file:
            if self.debt !=0:
                file.write(str(self.debt))
            else:
                file.write(str(0))
            print("Succesfully saved debt file")

#*Saves the information from users
def saveAppInfo(people):

    names = set()  # Use a set to store unique names

    for person in people:
        person.save()
        names.add(person.name)  # Add the name to the set

    # Open names.txt and read the current data
    with open('names.txt', 'r') as file:
        content = file.read()
        items = content.splitlines()

    # Iterate over the items and add them to the set
    for i in items:
        names.add(i)

    # Write the unique names back to names.txt
    with open("names.txt", "w") as f:
        for i in names:
            f.write(i + '\n')

    f.close()
#*Load apps info
def loadAppInfo():
    file = open('names.txt', 'r')
    content = file.read()
    items = content.splitlines()
    file.close()
    for name in items:
        addUser(name,users)
        with open(name+'.pkl','rb') as pkl:
            person=pickle.load(pkl)
        users_dict[name].debts_list=person  
        try:
            with open(name+'-debt.txt','r') as file:
                debt = file.read()
                if debt !='':
                    debt=float(debt)
                else:
                    debt = 0
        except:
            with open(name+'-debt.txt','w') as file:
                debt = 0
                file.write(debt)
        users_dict[name].changeDebt(debt)
    
#*deletes user
def deleteUser(user):
    #deletes the user from users array
    to_delete=[]
    for u in users:
        if u.name == user.name:
            to_delete.append(u)
    for u in to_delete:
        users.remove(u)
    print(f"to delete and users: {to_delete}")
    print(users)
    #deletes user from users dict
    del users_dict[user.name]

    #removes user.name from names.txt
    names = set()  # Use a set to store unique names

    for person in users:
        person.save()
        names.add(person.name)  # Add the name to the set

    # Open names.txt and read the current data
    with open('names.txt', 'r') as file:
        content = file.read()
        items = content.splitlines()

    # Iterate over the items and add them to the set
    for i in items:
        names.add(i)

    # Write the unique names back to names.txt
    names.discard(user.name)
    with open("names.txt", "w") as f:
        for i in names:
            f.write(i + '\n')

    f.close()
    #deletes the pkl file
    user_pkl_file = user.name + '.pkl'
    if os.path.exists(user_pkl_file):
        os.remove(user_pkl_file)
#*adds a user based on name
def addUser(name,people):
    people.append(User(name))
def showUsers(people):
    print("USERS:")
    for user in people:
        print(user.name)
#*add an expense
def addExpense(payer, people, amount):
    all_people=people
    #Exclude people
    exclude = input("Do you want to exclude someone [y/n]: ").capitalize()
    people_to_exclude=[]
    if exclude=="Y":
        people_to_exclude = input("who do you want to exclude (separate by , if multiple) : ")
        people_to_exclude = people_to_exclude.split(",")


    #debt for the debtors
    debt =  amount / (len(all_people)-len(people_to_exclude))
    #what the guy payed for the other people aka all - his share
    payed= (amount - debt)*-1   
    payer.changeDebt(payed)

    print(f"added expense to {payer.name} of {payed}")
    #adding debt to all people but the payer
    for user in all_people:
        if user!=payer and user.name not in people_to_exclude:
            user.changeDebt(debt)
            user.newDebt(debt, payer.name)

#*shows expenses with users (totals)
def showExpenses(people):
    for user in people:
        if user.debt >0:
            print(f"User {user.name} owes {user.debt}. ")
        elif user.debt<0:
            print(f"User {user.name} is owed {user.debt *-1}")
        else:
            print(f"User doesnt owe anything.")
#*shows individuals debts for users
def showDebts(people):
    for user in people:
        if user.debts_list!={}:
            print(f"{user.name}'s debts")
            print(user.debts_list)
        else:
            print(f"{user.name} is up to date.")
#*Settles debts
def setleDebts(debtor, payer):
    total=0
    for x in debtor.debts_list:
        if x == payer.name:
            total+=debtor.debts_list[x]
    print(f"{debtor.name} owes {payer.name}:{total} in total")
    ready=input("Do you want to settle? [y/n]")
    if ready=="y":
        to_delete=[]
        for x in debtor.debts_list:
            if x == payer.name:
                to_delete.append(x)
        for y in to_delete:
            del debtor.debts_list[y]
        debtor.changeDebt(-total)
        print(f"Debts between {debtor.name} and {payer.name} have been settled.")
    else:
        print('Debts have NOT been settled')
#*Creates debt based on amount
def calculateDebtOnAmount(people,payer):
    total=0
    debts_dict={}
    for i in people:
        if i.name!=payer.name:
            amount=int(input(f"How much does {i.name} owe: "))
            total+=amount
            debts_dict[i.name]=amount
            i.changeDebt(amount)
            i.newDebt(amount,payer.name)
    payer.changeDebt(-total)
    print(f"Succesfully assigned debts and {payer.name} is now owed {total}")
    for i in debts_dict:
        print(i)
    

#*-->MAIN LOOP<--

loadAppInfo()
print("User's info loaded succesfully!")
print(users)
while run:

    action=input("""Select an action to do: \n
                 [1] - USER ACTIONS \n
                 [2] - DEBT ACTIONS \n
                 [3] - SETTLE A DEBT\n
                 [4] - SHOW DEBTS\n
                 anything else - QUIT\n
                 """)
    if action=='1':
        user_action = input("""
                            [A] - ADD USER
                            [B] - DELETE USER
                            [C] - SHOW USERS\n
                            """).capitalize()
        if user_action=="A":
            name=input("What is the name of the user : ")
            addUser(name,users)
        elif user_action=="B":
            showUsers(users)
            name=input("Which user do you want to delete : ")
            deleteUser(name)
        elif user_action=="C":
            showUsers(users)
    elif action=="2":
                debt_action = input("""
                            [A] - ADD EQUAL DEBT
                            [B] - ADD DEBT BY AMOUNT\n
                            """).capitalize()
                if debt_action=="A":
                    payer=users_dict[input("Who paid for this: ")]
                    amount= int(input("How much did this cost: "))
                    addExpense(payer,users,amount)
                elif debt_action=="B":
                    payer=users_dict[input("Who paid for this: ")]
                    calculateDebtOnAmount(users,payer)
    elif action=="3":
        payer=users_dict[input("Who is the payer: ")]
        debtor=users_dict[input("Who is the debtor: ")]
        setleDebts(debtor, payer)
    elif action=="4":
        showDebts(users)

    else:
        print("Goodbye!")
        saveAppInfo(users)
        print("App info saved sucessfully!")
        time.sleep(5)
        run = False
