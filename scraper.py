import json

import requests, selenium, lxml, schedule, pyautogui
from bs4 import BeautifulSoup

from datetime import datetime


#Get today's date --> Format in D/M/Y --> Convert to string --> Get string slice starting at the -4 index to get current year --> Convert year to int --> Add one for range end
this_year = int((str(datetime.today().strftime("%d/%m/%Y")))[-4:])

class standingsApp():
    def collect_wdc_standings(self):
        all_wdc_standings = {}
        driver_stats = {}
        for year in range(1950, this_year+1):
            all_wdc_standings[year] = {}

            #html in bytes
            response = requests.get(f"https://www.formula1.com/en/results/{year}/drivers")

            #bytes to html
            parsed_html = BeautifulSoup(response.content, 'html.parser')

            #get all table rows with each driver's details
            tr_all_drivers = parsed_html.find_all("tr", "hover:bg-[rgb(from_var(--f1rd-colour-surface-neutral-surface-neutral-11)_r_g_b_/_0.03)]")
         
            #check if new year but before season has started
            if year == this_year and len(tr_all_drivers) == 0:
                print("Check back when the season has started for this years standings!")
                break

            #iterate for individual driver's details
            for ranking, tr_each_driver in enumerate(tr_all_drivers):
                p_driver_data = tr_each_driver.find_all("p", class_="typography-module_body-s-semibold__O2lOH")

                #iterate through a driver's details
                for index, p_element in enumerate(p_driver_data):

                    if index == 0:
                        position = p_element.text

                    #get driver's name and abbreviated name --> Abbr name gets stuck on to end of full name when using p_element.text, hence the slicing
                    elif index == 1:
                        driver_name = str(p_element.text[:-3]).replace("\xa0", " ")
                        driver_abbr = p_element.text[-3:]

                    elif index == 2:
                        nationality = p_element.text

                    #get the driver's team, set default if driver didn't have a team
                    elif index == 3:
                        constructor = p_element.text or "No Team"

                    elif index == 4:
                        points = p_element.text

                    #idk, i have silly brain :P
                    else:
                        print(":3")

                #create dictionary of driver's stats/info, copy appended so dicts in list are not overridden and become uniform
                driver_stats.update({"POSITION":position , "NAME": driver_name , "ABBREVIATION":driver_abbr , 
                                        "NATIONALITY":nationality , "CONSTRUCTOR":constructor , "POINTS":points})
                all_wdc_standings[year][ranking+1] = driver_stats.copy()

        with open("wdc.json", "w") as outFile:
            json.dump(all_wdc_standings, outFile ,indent=4)
            outFile.close()



    def collect_wcc_standings(self):
        all_wcc_standings = {}
        team_stats = {}
        for year in range(1958, this_year+1):
            all_wcc_standings[year] = {}

            #html in bytes
            response = requests.get(f"https://www.formula1.com/en/results/{year}/team")

            #bytes to html
            parsed_html = BeautifulSoup(response.content, 'html.parser')

            #get all table rows with each team's details
            tr_all_teams = parsed_html.find_all("tr", "hover:bg-[rgb(from_var(--f1rd-colour-surface-neutral-surface-neutral-11)_r_g_b_/_0.03)]")
         
            #check if new year but before season has started
            if year == this_year and len(tr_all_teams) == 0:
                print("Check back when the season has started for this years standings!")
                break

            #iterate for individual team's details
            for ranking, tr_each_driver in enumerate(tr_all_teams):
                p_team_data = tr_each_driver.find_all("p", class_="typography-module_body-s-semibold__O2lOH")

                #iterate through a teams's details
                for index, p_element in enumerate(p_team_data):

                    if index == 0:
                        position = p_element.text

                    elif index == 1:
                        team_name = p_element.text

                    elif index == 2:
                        points = p_element.text

                    #brain == mush --> True :3
                    else:
                        print(":3")

                #create dictionary of team's stats/info, copy appended so dicts in list are not overridden and become uniform
                team_stats.update({"POSITION":position , "CONSTRUCTOR": team_name , "POINTS":points})
                all_wcc_standings[year][ranking+1] = team_stats.copy()

        with open("wcc.json", "w") as outFile:
            json.dump(all_wcc_standings, outFile ,indent=4)
            outFile.close()


    
    def view_wdc_standings(self):
        with open("wdc.json", "r") as inFile:
            wdc_standings = json.load(inFile)

            while True:
                wdc_year = input(f"Get data from which year?(1950-{this_year}): ")
                try:
                    int(wdc_year)
                except:
                    print("Enter year as a whole number!")
                    continue

                if (1950 > int(wdc_year)) or (int(wdc_year) > this_year):
                    print("Year must be in the valid range!")
                    continue
                break
                
            print(f"\nWorld Driver's Championship Standings {wdc_year}\n------------------------------------------")
            for driver_rank in wdc_standings[wdc_year]:
                print(wdc_standings[wdc_year][driver_rank])
            inFile.close()



    def view_wcc_standings(self):
        with open("wcc.json", "r") as inFile:
            wcc_standings = json.load(inFile)

            while True:
                wcc_year = input(f"Get data from which year?(1958-{this_year}): ")
                try:
                    int(wcc_year)
                except:
                    print("Enter year as a whole number!")
                    continue

                if (1958 > int(wcc_year)) or (int(wcc_year) > this_year):
                    print("Year must be in the valid range!")
                    continue
                break

            print(f"\nWorld Constructor's Championship Standings {wcc_year}\n-----------------------------------------------")
            for team_rank in wcc_standings[wcc_year]:
                print(wcc_standings[wcc_year][team_rank])
            inFile.close()



    def function_choice(self):
        while True:
            print("\n=====Choose Function===== \n 1. Collect WDC Standings \n 2. Collect WCC Standings \n 3. View WDC Standings \n 4. View WCC Standings \n 0. Exit")

            try:
                choice = int(input("Enter choice --> "))
            except:
                print("\nEnter a number!")
                continue
            print()

            match choice:
                case 1:
                    self.collect_wdc_standings()
                case 2:
                    self.collect_wcc_standings()
                case 3:
                    self.view_wdc_standings()
                case 4:
                    self.view_wcc_standings()
                case 0:
                    print("Goodbye!")
                    exit()
                case _:
                    print("Enter valid choice!")



app = standingsApp()

print("\nWelcome to the F1 Standings Navigator!")
print("--------------------------------------")

while True:
    match input("Run Program?(y/n): "):
        case "y"|"yes"|"Y"|"Yes"|"YES":
            app.function_choice()
        case "n"|"no"|"N"|"No"|"NO":
            print("Goodbye!")
            exit()
        case _:
            print("Input valid option!")