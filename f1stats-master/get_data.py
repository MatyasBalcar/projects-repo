import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting
import time
import requests
import pandas as pd
import numpy as np
import json

plt.style.use('default')

#! ENV VRIABLES
tracks_configs_2024={
    8:[87, 167],#monaco
    9:[87, 167],#canada
    11:[70, 170]#rbring
}
#*QUALI
def get_pole(year,round_num,export=False):
    session=fastf1.get_session(year,round_num,'Q')
    session.load()
    pole=session.results
    pole_position_driver = pole[pole['Position'] == 1]
    if export:
        with open("pole.txt","w") as f:
            f.write(pole_position_driver["DriverNumber"][0])
            f.write("\n")
            f.write(str(pole_position_driver["Q3"][0]))
            #writes driver_number on one line and the laptime on the next one
    return pole_position_driver
    #returns a Pandas.DataFrame use ['param' to acces parameter]

#* RACE 
def get_fastest_lap(year,round_num,export=False):
    session=fastf1.get_session(year,round_num,'R')
    session.load()
    fastest_lap=session.laps.pick_fastest()
    print(fastest_lap)
    if export:
        with open("fastest_lap.txt", "w") as f:
            f.write(str(fastest_lap["Driver"]))
            f.write("\n")
            f.write(str(fastest_lap["LapTime"]))
    #returns the fastest race lap as a PDandas.DataFrame object
    return fastest_lap
def create_plot_for_changes(year,round_num):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    session = fastf1.get_session(year, round_num, 'R')
    session.load(telemetry=False, weather=False)

    fig, ax = plt.subplots(figsize=(8.0, 4.9))

    fig.set_facecolor('white')
    ax.set_facecolor('white')
    for drv in session.drivers:
        drv_laps = session.laps.pick_driver(drv)

        abb = drv_laps['Driver'].iloc[0]
        color = fastf1.plotting.driver_color(abb)

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                label=abb, color=color)
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()
    plt.title(session.session_info['Meeting']['OfficialName'])
    plt.show()
def create_plot_for_tire_strategies(year, round_num):


    session = fastf1.get_session(year,round_num, 'R')
    session.load()
    laps = session.laps
    drivers = session.drivers
    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})
    fig, ax = plt.subplots(figsize=(5, 10))
    fig.set_facecolor('white')
    ax.set_facecolor('white')
# Set the color of the ticks and the title to black
    ax.tick_params(colors='black')
    ax.title.set_color('black')

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            # each row contains the compound name and stint length
            # we can use these information to draw horizontal bars
            plt.barh(
                y=driver,
                width=row["StintLength"]*1.5,  # Increase the width of the bars by 50%
                left=previous_stint_end,
                color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]]  # Set the color of the bars to black
            )
            previous_stint_end += row["StintLength"]
    plt.title(session.session_info['Meeting']['OfficialName'],color="black")
    plt.show()
def pace_progression(year,round_num,drivers):
    session= fastf1.get_session(year,round_num,"R")
    session.load()
    data={

    }
    for d in drivers:
        laps=session.laps.pick_drivers(d)
        data[d]=laps
    extracted_data = {key: df[['LapTime', 'Compound']] for key, df in data.items()}
    # Convert 'LapTime' from timedelta to seconds
    for driver, df in extracted_data.items():
        df['LapTime'] = df['LapTime'].dt.total_seconds()

    # Plot lap times for each driver
    for driver, df in extracted_data.items():
        plt.plot(df['LapTime'].reset_index(drop=True), label=driver)


    plt.xlabel('Lap')
    plt.ylabel('LapTime (seconds)')
    plt.title('Pace of each driver')
    plt.legend()
    plt.show()
def plot_peak_teamamte_pace_diff(year,round_num):
    teams={
        "RBR":[1,11],
        "MER":[44,63],
        "FER":[16,55],
        "MCL":[4,81],
        "HAA":[27,20],
        "VRB":[3,22],
        "APN":[31,10],
        "AMR":[14,18],
        "SAU":[24,77],
        "WIL":[23,2]
    }

    session = fastf1.get_session(year,round_num,"R")
    session.load()
    laps=session.laps
    drivers=session.drivers
    driver_laps={

    }
    for d in drivers:
        driver_laps[d]=laps.pick_driver(d).pick_fastest()['LapTime']

    for team, drivers in teams.items():
        i = 0
        for driver in  drivers:
            if(i==2):
                teams[team].pop(0)
                teams[team].pop(0)
                continue

            teams[team].append(driver_laps[str(driver)])
            i+=1
    for team, times in teams.items():
        diff = max(times) - min(times)
        teams[team]=diff.total_seconds()
        #print(f"{team}: {diff.total_seconds()}")
        # Plotting
    teams_names = list(teams.keys())
    lap_time_diffs = list(teams.values())
    colors=["","","","","","","","","",""]
    i=0
    for t in teams_names:
        colors[i]=fastf1.plotting.TEAM_COLORS[fastf1.plotting.TEAM_TRANSLATE[t]]
        i+=1



    fig, ax = plt.subplots()
    fig.set_facecolor('white')
    ax.set_facecolor('white')

    plt.rcParams['text.color'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'black'
    plt.rcParams['xtick.color'] = 'black'
    plt.rcParams['ytick.color'] = 'black'

    plt.title(f"Teammate differences for {year} round {round_num}",color="black")

    plt.bar(teams_names,lap_time_diffs,color= colors)
    for index, value in enumerate(lap_time_diffs):
        plt.text(index, value, str(round(value, 2)), color='black', ha='center', va='bottom')
    plt.show()
    return teams
def plot_average_teammate_pace_diff(year,round_num):
    teams={
        "RBR":[1,11],
        "MER":[44,63],
        "FER":[16,55],
        "MCL":[4,81],
        "HAA":[27,20],
        "VRB":[3,22],
        "APN":[31,10],
        "AMR":[14,18],
        "SAU":[24,77],
        "WIL":[23,2]
    }

    session = fastf1.get_session(year,round_num,"R")
    session.load()
    laps=session.laps
    drivers=session.drivers
    driver_laps={

    }
    for d in drivers:
        d_laps = laps.pick_drivers(d)
        # Convert LapTime to seconds
        d_laps['LapTime'] = pd.to_timedelta(d_laps['LapTime']).dt.total_seconds()
        # Calculate average lap time
        average_lap_time = d_laps['LapTime'].mean()
        #print(f"Average lap time for driver {d}: {average_lap_time} seconds")
        driver_laps[d]=average_lap_time
    for team, drivers in teams.items():
        i = 0
        for driver in  drivers:
            if(i==2):
                teams[team].pop(0)
                teams[team].pop(0)
                continue

            teams[team].append(driver_laps[str(driver)])
            i+=1
    for team, times in teams.items():
        diff = max(times) - min(times)
        teams[team]=diff
        #print(f"{team}: {diff.total_seconds()}")
        # Plotting
    teams_names = list(teams.keys())
    lap_time_diffs = list(teams.values())
    colors=["","","","","","","","","",""]
    i=0
    for t in teams_names:
        colors[i]=fastf1.plotting.TEAM_COLORS[fastf1.plotting.TEAM_TRANSLATE[t]]
        i+=1



    fig, ax = plt.subplots()
    fig.set_facecolor('white')
    ax.set_facecolor('white')
    ax.tick_params(colors='black')
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'black'
    plt.rcParams['xtick.color'] = 'black'
    plt.rcParams['ytick.color'] = 'black'

    plt.title(f"Teammate differences for {year} round {round_num}")

    plt.bar(teams_names,lap_time_diffs,color= colors)
    for index, value in enumerate(lap_time_diffs):
        plt.text(index, value, str(round(value, 2)), color='black', ha='center', va='bottom')
    plt.show()
    return teams


#*CHAMPIONSHIP

def get_standings(year, last_num,export = False):
    data_dict={

        }
    url = f"https://ergast.com/api/f1/{year}/{last_num}/driverStandings.json"
    response = requests.get(url)
    data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    for driver in data:
        data_dict[f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"]=[]
    for i in range(1,last_num+1):
        url = f"https://ergast.com/api/f1/{year}/{i}/driverStandings.json"
        response = requests.get(url)
        data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        
        for driver in data:
            #print(f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}")
            
            data_dict[f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"].append(driver['points'])
    if export:
        with open('standings.json', 'w') as f:
            json.dump(data_dict, f)
    return data_dict
    #* returns a dict with driver_name:[points array]
def plot_championship(data):
    # Convert string values to integers
    for key in data:
        data[key] = list(map(int, data[key]))

    # Find the maximum length of the lists
    max_length = max(len(points) for points in data.values())

    # Pad shorter lists with their last value
    for key in data:
        last_value = data[key][-1]
        while len(data[key]) < max_length:
            data[key].append(last_value)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Generate a range for the x-axis (assuming these are race numbers or some sequential metric)
    x_values = range(1, max_length + 1)


    # Create the plot
    ax =plt.figure(figsize=(14, 10))

    # Plot each driver's points over the races
    for driver in df.columns:
        plt.plot(x_values, df[driver], label=driver)
        
    ax.set_facecolor("white")
    # Add titles and labels with light colors
    plt.title('Driver Points Over Time', color='black')
    plt.xlabel('Race Number', color='black')
    plt.ylabel('Points', color='black')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, color='gray')

    # Change tick colors to white
    plt.tick_params(colors='black', which='both')  # 'both' applies to both major and minor ticks

    # Show the plot
    plt.tight_layout()
    plt.show()


#*MISC
def get_sp_all(year, race, session, export=False):
    session = fastf1.get_session(year, race, session)
    session.load()
    laps = session.laps
    drivers = session.drivers
    results = {}

    for d in drivers:
        results[d] = 0
    for d in drivers:
        laps_for_driver = laps.pick_driver(d)
        print(laps_for_driver)
        max_speed_lap = laps_for_driver.loc[laps_for_driver['SpeedST'].idxmax()]
        results[d] = max_speed_lap["SpeedST"]
    # Convert the dictionary to a list of tuples, sort the list in descending order by the second element of each tuple, and convert it back to a dictionary
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    
    # Plotting
    drivers = list(results.keys())
    speeds = list(results.values())
    colors = plt.cm.RdYlGn(np.linspace(1, 0, len(drivers)))  # gradient from green to red
    plt.figure(figsize=(15, 6))
    plt.bar(drivers, speeds, color=colors, width=.8)
    plt.title('Speed in speed trap for each driver')
    plt.xlabel('Driver no.')
    plt.ylabel('Speed km/h')

    plt.xticks(rotation=90)  # rotate x-axis labels for better readability

    # Set minimum and maximum values for y-axis
    plt.ylim(min(speeds) - 5, max(speeds) + 5)  # Adjusting the min and max values by subtracting and adding 5 respectively for better visualization

    for index, value in enumerate(speeds):
        if(index == 0 or index == len(speeds) - 1):
            plt.text(index, value, str(round(value, 2)), color='black', ha='center', va='bottom')
    if export:
        with open('data.json', 'w') as f:
            json.dump(results, f)
    plt.show()
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)
def sector_breakdown(year,name,session):
  
    session = fastf1.get_session(year, name, session)
    session.load()
    lap = session.laps.pick_fastest()
    fastest_sector=[lap["Sector1Time"], lap["Sector2Time"], lap["Sector3Time"]]
    fastest_driver=[lap["Driver"], lap["Driver"], lap["Driver"]]
    fastest_color=[fastf1.plotting.DRIVER_COLORS[fastf1.plotting.DRIVER_TRANSLATE[fastest_driver[0]]],fastf1.plotting.DRIVER_COLORS[fastf1.plotting.DRIVER_TRANSLATE[fastest_driver[1]]],fastf1.plotting.DRIVER_COLORS[fastf1.plotting.DRIVER_TRANSLATE[fastest_driver[2]]]]

    laps=session.laps
    for _, l in laps.iterrows():
        s1 = l["Sector1Time"]
        s2 = l["Sector2Time"]
        s3 = l["Sector3Time"]
        if s1 < fastest_sector[0]:
            fastest_sector[0] = s1
            fastest_driver[0]=l["Driver"]
        if s2 < fastest_sector[1]:
            fastest_sector[1] = s2
            fastest_driver[1]=l["Driver"]
        if s3 < fastest_sector[2]:
            fastest_sector[2] = s3
            fastest_driver[2]=l["Driver"]


    i=0
    for d in fastest_driver:
        fastest_color[i]=fastf1.plotting.DRIVER_COLORS[fastf1.plotting.DRIVER_TRANSLATE[d]]
        i+=1

    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()

    track = pos.loc[:, ('X', 'Y')].to_numpy()
    track_angle = circuit_info.rotation / 180 * np.pi
    rotated_track = rotate(track, angle=track_angle)
    # Define indices that split the track into three parts
    indices =tracks_configs_2024[name]

    
    # Plot each part with a different color
    # Plot each part with a different color and add labels
    plt.plot(rotated_track[:indices[0], 0], rotated_track[:indices[0], 1], color=fastest_color[0], label=fastest_driver[0])
    plt.plot(rotated_track[indices[0]:indices[1], 0], rotated_track[indices[0]:indices[1], 1], color=fastest_color[1], label=fastest_driver[1])
    plt.plot(rotated_track[indices[1]:, 0], rotated_track[indices[1]:, 1], color=fastest_color[2], label=fastest_driver[2])

    # Add a legend
    plt.legend()

    offset_vector = [500, 0]



    plt.title(session.event['Location'])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')

    plt.show()

if __name__=="__main__" :
    test  = input("do you want to test? y/n")
    if test=='y':
        #testing
        print("testing...sleepeing after two print tasks")
        print(get_pole(2024,9))
        time.sleep(5)
        print(get_fastest_lap(2024,9))
        time.sleep(5)
        create_plot_for_changes(2024,9)
        create_plot_for_tire_strategies(2024,9)
        get_standings(2024,9)
        plot_championship(get_standings(2024,9))
        plot_peak_teamamte_pace_diff(2024,9)
        get_sp_all(2024,9,"Q")
        sector_breakdown(2024,9,"Q")
        pace_progression(2024,9,[1,4])
        plot_average_teammate_pace_diff(2024,9)
