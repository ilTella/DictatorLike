import random
import pandas as pd
import numpy as np

# functions

def print_factions_stats():
    print()
    print("!!! POLICE REPORT !!!")
    print("POPULARITY -- GROUPS -- STRENGTH")
    i = 1
    for x in factions:
        plot_code = factions[x][2]
        if (plot_code == -1):
            plot = 'A'
        else:
            if (plot_code == 0):
                plot = ' '
            else:
                plot = str(plot_code)
            
        str1 = ' ' * (9 - factions[x][0]) + '*' * (factions[x][0])
        str2 = ' ' * 3 + str(i) + ' ' + x + ' ' * (12 - len(x))
        str3 = plot + ' ' + '*' * factions[x][1]
        print(str1 + str2 + str3)
        i += 1
    print("Your strenght is ", bodyguard)
    print("Strength for revolution is ", strength_for_revolution)
    print()

def simple_question(question):
    answer = 0
    while (answer != 'y' and answer != 'n'):
        answer = input(question)
        if (answer == 'Y' or answer == 'Yes' or answer == 'YES'):
            answer = 'y'
        if (answer == 'N' or answer == 'No' or answer == 'NO' or answer == ''):
            answer = 'n'
    return answer

def police_report() -> int:
    if (factions["SPolice"][0] <= 4):
        print("Your reputation with the Secret Police is too low, no report for you...")
    else:
        answer = simple_question("Pay $1000 for police report?")
        if (answer == 'y'):
            if (budget >= 1000):
                print_factions_stats()
                return -1000
            else:
                print("There is not enough money for this...")
    print()
    return 0

def budget_report():
    print()
    print("$$$ BUDGET REPORT $$$")
    if (budget >= 0):
        print("The treasury holds", budget)
    else:
        print("The treasury owes", budget)
    print("Monthly costs are", monthly_costs)
    print()

def print_request_stats(request_popularity, request_strength):
    print()
    request_popularity = str(request_popularity)
    request_strength = str(request_strength)
    pop_changes = request_popularity.split(" | ")
    str_changes = request_strength.split(" | ")
    first_flag = True
    if len(request_popularity) > 1:
        print("POPULARITY CHANGES:")
        for x in pop_changes:
            y = x.split(", ")
            arrows = " "
            if (first_flag):
                num_arrows = int(y[1])
                if (num_arrows > 3):
                    num_arrows = 3
                arrows = "<"*num_arrows
                first_flag = False
            print(y[0] + " " + y[1] + " " + arrows)
    if len(request_strength) > 1:
        print("STRENGTH CHANGES:")
        for x in str_changes:
            y = x.split(",")
            print(y[0] + " " + y[1])

    print()

def apply_audience_accept(request_popularity, request_strength):
    request_popularity = str(request_popularity)
    request_strength = str(request_strength)
    pop_changes = request_popularity.split(" | ")
    str_changes = request_strength.split(" | ")
    if len(request_popularity) > 1:
        for x in pop_changes:
            y = x.split(", ")
            factions[y[0]][0] += int(y[1])
            if factions[y[0]][0] < 0:
                factions[y[0]][0] = 0
            if factions[y[0]][0] > 9:
                factions[y[0]][0] = 9
    if len(request_strength) > 1:
        for x in str_changes:
            y = x.split(",")
            factions[y[0]][1] += int(y[1])
            if factions[y[0]][1] < 0:
                factions[y[0]][1] = 0
            if factions[y[0]][1] > 9:
                factions[y[0]][1] = 9

def apply_audience_negate(request_popularity):
    request_popularity = str(request_popularity)
    pop_changes = request_popularity.split(" | ")
    if len(request_popularity) > 1:
        y = pop_changes[0].split(", ")
        change = -(int(y[1]))
        if change < -3:
            change = -3
        factions[y[0]][0] += change
        if factions[y[0]][0] < 0:
            factions[y[0]][0] = 0
        if factions[y[0]][0] > 9:
            factions[y[0]][0] = 9

def audience() -> list[int]:
    print()
    print("=== AN AUDIENCE ===")
    faction = random.choice(["Army", "Peasants", "Landowners"])

    if (faction == "Army"):
        request_id = random.choice(army_requests_ind)
        request = army_requests.loc[request_id]
        army_requests.drop(index=request_id, inplace=True)
        army_requests_ind.remove(request_id)
    else:
        if (faction == "Peasants"):
            request_id = random.choice(peasants_requests_ind)
            request = peasants_requests.loc[request_id]
            peasants_requests.drop(index=request_id, inplace=True)
            peasants_requests_ind.remove(request_id)
        else:
            request_id = random.choice(landowners_requests_ind)
            request = landowners_requests.loc[request_id]
            landowners_requests.drop(index=request_id, inplace=True)
            landowners_requests_ind.remove(request_id)

    request_text = request['text']
    request_popularity = request['popularity_change']
    request_strength = request['strength_change']
    request_cost = request['cost']
    request_mcost = request['monthly_cost']

    print("A request from the " + faction)
    print("Will your excellency agree to")
    print(request_text + "?")

    answer = simple_question("Advice?")
    if (answer == 'y'):
        print_request_stats(request_popularity, request_strength)

    if (request_cost != 0 or request_mcost != 0):
        if (request_cost > budget):
            print("No enough money for this...")
            print()
            apply_audience_negate(request_popularity)
            return [0, 0]
        else:
            if request_cost > 0:
                print("Profit: " + str(request_cost))
            else:
                if request_cost < 0:
                    print("Cost: " + str(request_cost))
            if request_mcost > 0:
                print("Monthly cost increase: " + str(request_mcost))
            else:
                if request_mcost < 0:
                    print("Monthly cost decrease: " + str(request_mcost))
    else:
        print("No money involved.")

    answer = simple_question("Grant request?")
    if (answer == 'y'):
        print()
        apply_audience_accept(request_popularity, request_strength)
        return [request_cost, request_mcost]
    else:
        apply_audience_negate(request_popularity)
        print()
        return [0, 0]
    
###############
###############

# Highscores loading

with open('Saves/hiscores.txt', 'r') as f:
    hiscores = []
    for item in f:
        hiscores.append(item)

for i in range(len(hiscores)):
    split = hiscores[i].split(sep=", ")
    el = [split[0], int(split[1])]
    hiscores[i] = el

hiscores.sort(key=lambda n: n[1], reverse=True)

# GAME START

while (1):

    if len(hiscores) > 0:
        hiscore = hiscores[0][1]
        name = hiscores[0][0]
    else:
        hiscore = 0

    if hiscore > 0:
        print("Best president is", name)
        print("With an hiscore of", hiscore)
    else:
        print("You're the first president!")
    _ = input("Press ENTER to become Dictator of the Ritimban Republic")

    # Setting variables

    army_requests = pd.read_csv('Data/army_requests.csv', index_col=0)
    peasants_requests = pd.read_csv('Data/peasants_requests.csv', index_col=0)
    landowners_requests = pd.read_csv('Data/landowners_requests.csv', index_col=0)
    army_requests_ind = army_requests.index.tolist()
    peasants_requests_ind = peasants_requests.index.tolist()
    landowners_requests_ind = landowners_requests.index.tolist()

    factions = {
        "Army" : [7, 6, 0],
        "Peasants" : [7, 6, 0],
        "Landowners" : [7, 6, 0],
        "Guerillas" : [0, 6, 0],
        "Leftotans" : [7, 6, 0],
        "SPolice" : [7, 6, 0],
        "Russians" : [7, 0, 0],
        "Americans" : [7, 0, 0]
    }

    bodyguard = 4
    strength_for_revolution = 10
    month = 1

    budget = 1_000_000
    monthly_costs = 60_000

    presidential_decisions = pd.read_csv('Data/presidential_decisions.csv', index_col=0)

    please_group = presidential_decisions[presidential_decisions["type"] == "please_group"]
    please_everyone = presidential_decisions[presidential_decisions["type"] == "please_everyone"]
    improve_chances = presidential_decisions[presidential_decisions["type"] == "improve_chances"]
    raise_cash = presidential_decisions[presidential_decisions["type"] == "raise_cash"]
    strengthen_group = presidential_decisions[presidential_decisions["type"] == "strengthen_group"]

    newsflash = pd.read_csv('Data/newsflash.csv', index_col=0)

    # GAME CYCLE

    while(1):

        budget_report() # treasury report

        print("MONTH ", month) # print current month, starting with 1

        if (month == 1): # ask for police report
            print("Your first police report is FREE:")
            print_factions_stats()
        else:
            budget += police_report()

        res = audience() # faction audience
        budget += res[0]
        monthly_costs += res[1]

        budget += police_report() # ask for police report, again

    # presidential decision
        # police report
    # check for revolution or assassination
        # resolve revolution or assassination
            # eventual gameover
        
        if budget >= 0: # budget update
            budget -= monthly_costs
        else:
            factions["Army"][0] -= 1 # if broken unpaid army and bodyguard angry
            if factions["Army"][0] < 0:
                factions["Army"][0] = 0
            bodyguard -= 1
            if bodyguard < 0:
                bodyguard = 0
        month += 1 # month update

    


