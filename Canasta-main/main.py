
main_bull = True
hraci_body = []
micha_hrac = 1
preklada_hrac = micha_hrac + 1
pocet_hracu = int(input("Zadej pocet hracu: "))
print("\n")
for i in range(0,pocet_hracu):
    hraci_body.append(0)

while main_bull:
    #kteri hraci provadi akce
    print(f"Micha hrac {micha_hrac} ")
    print(f"Preklada hrac{preklada_hrac} ")
    k = 0
    #kolik hraci vykjladaji
    for hrac in hraci_body:
        if hraci_body[k] < 0:
            print(f"Hrac {k+1} vyklada 15")
        if hraci_body[k] < 1500:
            print(f"Hrac {k+1} vyklada 50")
        elif hraci_body[k] < 2500:
            print(f"Hrac {k+1} vyklada 90")
        elif hraci_body[k] < 5000:
            print(f"Hrac {k+1} vyklada 120")
        else:
            print(f"Hrac {k+1} vyklada 150")


    i= 1
    #TODO pridej body hracum
    body_pro_hrace = []
    print("Body:\n")
    #ziskavani bodu
    for hrac in hraci_body:
        hraci_body[i-1] = int(input(f"Zadej body pro hrace {i} : "))
        i +=1
    j=1
    #zobrazovani bodu
    for hrac in hraci_body:
        print(f"Hrac {j}: ma {hrac} bodu")
        j+=1

    if micha_hrac < pocet_hracu:
        micha_hrac += 1
    else:
        micha_hrac = 1
    if preklada_hrac <pocet_hracu:
        preklada_hrac +=1 
    else:
        preklada_hrac = 1
