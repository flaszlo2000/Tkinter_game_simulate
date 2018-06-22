from tkinter import *
from random import randrange

class App :
    # az akadályok koordinátái fogja tárolni x1, y1, x1+oldal hossz (= x2), y2+oldal hossz (= y2)
    #> a négy alap oldalt tartalmazza hogy ne lehessen kimenni a pályáról
    items = []
    def __init__(self) :
        "Konstrukrottal létrehozzuk a program vázát"
        self.run = False # progamfutás engedélyező változó
        self.root = Tk()
        self.root.bind("<Return>", self.res)
        # Játékvezérlő gombok inicializálása
        self.root.bind("<KeyPress-Left>", self.left_b_down)
        self.root.bind("<KeyRelease-Left>", self.left_b_up)
        self.root.bind("<KeyPress-Right>", self.right_b_down)
        self.root.bind("<KeyRelease-Right>", self.right_b_up)
        self.root.bind("<KeyPress-Up>", self.up_b_down)
        self.root.bind("<KeyRelease-Up>", self.up_b_up)
        self.root.bind("<KeyPress-Down>", self.down_b_down)
        self.root.bind("<KeyRelease-Down>", self.down_b_up)
        # Játéktér elkészítése
        self.can = Canvas(self.root, width=500, height=500, bg="light grey")
        self.can.pack()
        # betöltés indítása
        self.begin()
        # Eseményfogadó indítása
        self.root.mainloop()

    def res(self, event) :
        "Páéya újraindítása"
        if self.run == False :
            # ha a játék leállt
            self.begin()
            
    def begin(self) :
        "Játék betöltése"
        # teljesen újraindítunk mindent (a restartok miatt kell)
        self.can.delete(ALL)
        App.items = []
        # Játékvezérlő gombok tárolója
        self.button = []
        self.moving_speed = 15
        # Karakter adatai
        self.x1, self.y1 = 455, 5
        self.x2, self.y2 = 465, 15
        # Karakter elkészítése
        self.character = self.can.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red")
        # akadályok legenerálása
        thing = ObjectGenerator()
        thing.before_map(self.can, App.items)
        #thing.death_test(self.can, App.items)
        # programfutás engedélyezése
        self.run = True 
        # eseményfigyelő indítása
        self.start()
        
    def left_b_down(self, event) :
        "Bal nyíl lenyomva"

        if "left" not in self.button :
            self.button.append("left")
            
    def right_b_down(self, event) :
        "Job nyíl lenyomva"
        
        if "right" not in self.button :
            self.button.append("right")

    def up_b_down(self, event) :
        "Fel nyíl lenyomva"

        if "up" not in self.button :
            self.button.append("up")

    def down_b_down(self, event) :
        "Le nyíl lenyomva"

        if "down" not in self.button :
            self.button.append("down")
      
    def left_b_up(self, event) :
        "Nyíl felengedve"

        try :
            self.button.remove("left")
        except :
            pass

    def right_b_up(self, event) :    
        "Nyíl felengedve"

        try :
            self.button.remove("right")
        except :
            pass
        
    def up_b_up(self, event) :    
        "Nyíl felengedve"

        try :
            self.button.remove("up")
        except :
            pass
        
    def down_b_up(self, event) :        
        "Nyíl felengedve"

        try :
            self.button.remove("down")
        except :
            pass
        
    def start(self) :
        "Eseményfigyelő"
        if self.run == True :
            if len(self.button) != 0 :
                # ha van valamilyen gomb lenyomva
                if "up" in self.button :
                    # kipróbáljuk hogy az új koordináta szabad-e
                    if self.find(self.x1, self.y1-2, self.x2, self.y2-2, "up") :
                        # ha szabad akkor lépés engedélyezett
                        self.y1 -= 2
                        self.y2 -= 2
                    else :
                        # ütközés van, megnézzük hogy az ütközött elemnek van-e bármi speciális funkciója
                        self.specs_func()
                        
                if "down" in self.button :
                    if self.find(self.x1, self.y1+2, self.x2, self.y2+2, "down") :
                        self.y1 += 2
                        self.y2 += 2
                    else :
                        self.specs_func()
                        
                if "left" in self.button:
                    if self.find(self.x1-2, self.y1, self.x2-2, self.y2, "left") :
                        self.x1 -= 2
                        self.x2 -= 2
                    else :
                        self.specs_func()
                        
                if "right" in self.button :
                    if self.find(self.x1+2, self.y1, self.x2+2, self.y2, "right") :
                        self.x1 += 2
                        self.x2 += 2
                    else :
                        self.specs_func()

                # karakter áthelyezése
                self.can.coords(self.character, self.x1, self.y1, self.x2, self.y2)
            # rekurzivitás elérése a gombok figyelése érdekében
            self.root.after(self.moving_speed, self.start)
            
    def specs_func(self) :
        "A speciális funkciókat kezeli"
        if len(self.block) > 4 :
            # ha az elemnek amihez történt az ütközés van speciális tulajdonsága
            #> (mivel a szimpla "fal" elemeknek csak 4 paramétere van)
            if self.block[4] == "rekt" :
                # ha az 5. paraméter "rekt" akkor az ütköztető elem halált okoz
                # leállítjuk a játékot
                self.run = False
                # gameover állapot beállítása
                self.game_over()

    def game_over(self) :
        "Gameover állapot kezelője"
        self.can.create_text(self.can.winfo_width()/2, self.can.winfo_height()/3, text="Game over, press enter to restart")    

    def find(self, x1, y1, x2, y2, my_type) :
        "Ellenőrzi hogy a kapott pozíciók szabadak-e"
        for item in App.items :
            # végigmegyünk az adadályok listáján

            # az elmélet az hogy egy oldal csak egy bizonyos oldallal tud ütközni
            
            if my_type == "right" :
                # job oldalra megy a karakter, ütközik-e
                if y2 >= item[1] and y2 <= item[1]+item[3] and x2 >= item[0] and x2 <= item[0]+item[2] :
                    # menti azt az elemet amibe történt az ütközés, ez ahhoz kell hogy megnézzük hogy van-e
                    #> bármilyen speciális tulajdonsága az objektumnak (halál, teleport, stb..)
                    self.block = item 
                    return False
                elif y1 >= item[1] and y1 <= item[1]+item[3] and x2 >= item[0] and x2 <= item[0]+item[2]  :
                    self.block = item
                    return False

            elif my_type == "left" :
                # bal oldalra megy a karakter, ütközik-e
                if y1 <= item[1]+item[3] and y1 >= item[1] and x1 <= item[0]+item[2] and x1 >= item[0] :
                    self.block = item
                    return False
                elif y2 <= item[1]+item[3] and y2 >= item[1] and x1 <= item[0]+item[2] and x1 >= item[0] :
                    self.block = item
                    return False
                
            elif my_type == "up" :
                # felfele megy a karakter, ütközik-e
                if y1 <= item[1]+item[3] and y1 >= item[1] and x1 <= item[0]+item[2] and x1 >= item[0] :
                    self.block = item
                    return False
                elif y1 >= item[1] and y1 <= item[1]+item[3] and x2 >= item[0] and x2 <= item[0]+item[2] :
                    self.block = item
                    return False

            elif my_type == "down" :
                # lefele megy a karakter, ütközik-e
                if y2 >= item[1] and y2 <= item[1]+item[3] and x2 >= item[0] and x2 <= item[0]+item[2] :
                    self.block = item
                    return False
                elif y2 <= item[1]+item[3] and y2 >= item[1] and x1 <= item[0]+item[2] and x1 >= item[0] :
                    self.block = item
                    return False
        else :
            # nincs ütközés
            return True
        
    
class ObjectGenerator :
    "Az akadályokat generálja le"
    def random_map(self, master, holder) :
        x2_d = randrange(10, 56)
        y2_d = randrange(10, 56)
        x1 = randrange(500-x2_d) #randrange(master.winfo_width()-x2_d)
        y1 = randrange(500-y2_d) #randrange(master.winfo_height()-y2_d)

        # kirajzolja az akadályt
        master.create_rectangle(x1, y1, x1+x2_d, y1+y2_d, fill="blue")
        # menti az akadályt
        holder.append(tuple([x1, y1, x2_d, y2_d]))

    def before_map(self, master, holder) :
        "Alap pálya készítése"
        x = 3
        y = 3
        c = 0
        d = 12
        x_c = 1

        while True :
            if c % 37 != 0 and c % 38 != 0  :
                master.create_rectangle(x, y, x+10, y+10, fill="purple")

                if x_c % 4 != 0 and c % 36 != 0 : 
                    holder.append(tuple([x, y, 10, 10]))
                else :
                    holder.append(tuple([x, y, 10, 10, "rekt"]))

                #holder.append(tuple([x, y, 10, 10]))

            c += 1
            x += d

            if c % 40 == 0 :
                y -= 15
            
            if c % 41 == 0 :
                x -= d
                y += 30
                
            if c % 42 == 0 :
                x -= d
                y += 15
                d = -d
                c = 0
                x_c += 1
        
            if x_c % 18 == 0 :
                break

    def death_test(self, master, holder) :
        "Halál teszt"
        master.create_rectangle(250, 250, 300, 300, fill="dark green")
        master.create_line(150, 150, 200, 150, fill="orange")
        
        holder.append(tuple([150, 150, 50, 1, "rekt"]))
        holder.append(tuple([250, 250, 50, 50, "rekt"]))
        
                
            
if __name__ == "__main__" :
    App()
