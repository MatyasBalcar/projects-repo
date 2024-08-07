import json
import tkinter as tk



def submit():
    print(entry.get())
    


    
file = open('data.json')
data = json.load(file)
    
    
window = tk.Tk()
greeting = tk.Label(text="F1 quiz")
greeting.pack()
    
    

body=0
    
for i in data["q_a"]:
    #i je otazka
    j=1



    otazka = tk.Label(text=i)
    otazka.pack()
    entry = tk.Entry( width=50)
    entry.pack()
    




    button = tk.Button(
        master=window,
        text="Click me!",
        command=submit
    )
    button.pack()
        

    if odpoved==data["q_a"][i]:
        body+=1

    body_ = tk.Label(text=f"Body {body}")
    body_.pack()

    j+=1



    window.mainloop()




    




