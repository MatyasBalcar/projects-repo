from get_data import (
    get_pole
    ,get_fastest_lap
    ,create_plot_for_changes
    ,create_plot_for_tire_strategies
    ,get_standings
    ,plot_championship
    ,plot_peak_teamamte_pace_diff
    ,get_sp_all
    ,plot_average_teammate_pace_diff
    ,sector_breakdown
    ,pace_progression)
import tkinter as tk

year=2024
lr=11
session_type="FP1"
export = False
drivers=[]
def add_driver():
    global drivers
    driver_name = drivers_input.get()
    drivers.append(driver_name)
    drivers_text.set(f"Drivers to be used: {drivers}")
def clear_drivers():
    global drivers
    drivers=[]
    drivers_text.set(f"Drivers to be used: {drivers}")
def save_input():
    global year
    year = int(year_input.get())
    print(f"Year: {year}")
    label_text.set(f"Values: year:{year} | round:{lr} | export:{export} | seesion type: {session_type}")
def save_input2():
    global lr
    lr = int(lr_input.get())
    print(f"Lr : {lr}")
    label_text.set(f"Values: year:{year} | round:{lr} | export:{export} | seesion type: {session_type}")
def change_export():
    global export
    export = not export
    print("export switched to "+str(export))
    label_text.set(f"Values: year:{year} | round:{lr} | export:{export} | seesion type: {session_type}")
def change_session_type():
    global session_type
    session_type=session_input.get()
    label_text.set(f"Values: year:{year} | round:{lr} | export:{export} | seesion type: {session_type}")
def call_all():

    pole_driver=get_pole(year,lr,export)
    print(f"Name:{pole_driver['BroadcastName']}")
    print(pole_driver['Q3'])
    fastest_lap=get_fastest_lap(year,lr,export)
    print(fastest_lap['Driver'])
    print(fastest_lap['Team'])
    print(fastest_lap['LapTime'])
    create_plot_for_changes(year,lr)
    create_plot_for_tire_strategies(year,lr)
    plot_peak_teamamte_pace_diff(year,lr)
    data=get_standings(year,lr,export)
    plot_championship(data)
    get_sp_all(year,lr,session_type,export)
    get_sp_all(year,lr,session_type,export)
    sector_breakdown(year,lr,session_type)
    pace_progression(year,lr,[1,4])
    plot_average_teammate_pace_diff(year,lr)

root = tk.Tk()
root.geometry("600x400")
root.configure(bg="grey")


label_text = tk.StringVar()
label_text.set(f"Values: year:{year} | round:{lr} | export:{export} | seesion type: {session_type}")

drivers_text = tk.StringVar()
drivers_text.set(f"Drivers to be used: {drivers}")

label = tk.Label(root, text="Enter your information:", fg='white', bg='black')
label.grid(row=1,column=1)

year_input = tk.Entry(root)
year_input.grid(row=2,column=1)

year_number = tk.Button(root, text="Save year", command=save_input, width=15, fg='white', bg='grey')
year_number.grid(row=2,column=2)

lr_input = tk.Entry(root)
lr_input.grid(row=3,column=1)

round_number = tk.Button(root, text="Save round number", command=save_input2,  width=15, fg='white', bg='grey')
round_number.grid(row=3,column=2)

session_input = tk.Entry(root)
session_input.grid(row=4,column=1)

session_type_button = tk.Button(root, text="Change session type", command=change_session_type,  width=15, fg='white', bg='grey')
session_type_button.grid(row=4,column=2) 

drivers_input = tk.Entry(root)
drivers_input.grid(row=5,column=1)

drivers_button = tk.Button(root, text="Add a driver", command=add_driver,  width=15, fg='white', bg='grey')
drivers_button.grid(row=5,column=2) 

drivers_clear_button = tk.Button(root, text="Clear drivers", command=clear_drivers,  width=15, fg='red', bg='grey')
drivers_clear_button.grid(row=5,column=3) 

export_checkbutton = tk.Checkbutton(root, text="Export", command=change_export)
export_checkbutton.grid(row=6,column=1)

call_all_button = tk.Button(root, text="Call all functions", command=call_all, width=15, fg='green', bg='grey')
call_all_button.grid(row=6,column=2)

label = tk.Label(root, text="Call separate functions:", fg='white', bg='black')
label.grid(row=7,column=1)

label = tk.Label(root, textvariable=label_text, fg='white', bg='black')
label.grid(row=8,column=1)

labedrivers_lable = tk.Label(root, textvariable=drivers_text, fg='white', bg='black')
labedrivers_lable.grid(row=9,column=1)

pc = tk.Button(root, text="Generate plot changes", command=lambda: create_plot_for_changes(year, lr), width=25, fg='white', bg='grey')
pc.grid(row=10, column=1)

ts = tk.Button(root, text="Generate tire strategies", command=lambda: create_plot_for_tire_strategies(year,lr), width=25, fg='white', bg='grey')
ts.grid(row=10, column=2)

wdc = tk.Button(root, text="Generate WDC graph", command=lambda: plot_championship(get_standings(year,lr,export)), width=25, fg='white', bg='grey')
wdc.grid(row=11, column=1)

pd = tk.Button(root, text="Generate |PEAK| pace diff graph", command=lambda: plot_peak_teamamte_pace_diff(year,lr), width=25, fg='white', bg='grey')
pd.grid(row=11, column=2)

sp = tk.Button(root, text="Generate speed trap graph", command=lambda: get_sp_all(year,lr,session_type,export), width=25, fg='white', bg='grey')
sp.grid(row=12, column=1)

sbd = tk.Button(root, text="Generate sector breakdown", command=lambda:sector_breakdown(year,lr,session_type), width=25, fg='white', bg='grey')
sbd.grid(row=12, column=2)

pp = tk.Button(root, text="Generate pace progression ", command=lambda:pace_progression(year,lr,drivers), width=25, fg='white', bg='grey')
pp.grid(row=13, column=1)

apd = tk.Button(root, text="Generate |AVG| pace diff", command=lambda:plot_average_teammate_pace_diff(year,lr), width=25, fg='white', bg='grey')
apd.grid(row=13, column=2)
root.mainloop()