import filesystem
import customtkinter as ctk
from PIL import Image
import math

#Maisto prekiu klases
class kebabas:
    def __init__(self, info, papildai=None):
        self.pavadinimas = info["pavadinimas"]
        self.kaina = info["kaina"]
        self.papildai = papildai if papildai is not None else []
        for papildas in self.papildai:
            self.kaina += papildas["kaina"]
        
class uzkandziai:
    def __init__(self, info):   
        self.pavadinimas = info["pavadinimas"]
        self.kaina = info["kaina"]

#sukurti menu_failo objekta
menu_file = filesystem.File("menu")

#ji nuskaityti
patiekalai = menu_file.read_json()

#Nuotrauku nuskaitymas, grazina ctk image
def open_img(name,  size):
    try:
        pil_image = Image.open(filesystem.get_base_path() + "data\\assets\\" + name)
        return ctk.CTkImage(pil_image,pil_image,size=size)
    except:
        print("Nepavyko atidaryti nuotraukos " + name)


class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        #nustatyti title ir dydi lango
        self.title("Užsakymo sąskaitos skaičiuoklė")
        self.geometry("1280x720")
        self.iconbitmap(filesystem.get_base_path() + "data\\assets\\arbuzas.ico")

        #sukurti langam kuris laikis visus kitus langus
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        #Nustatyti grid taip kad viduj esantis langai galetu issiplest
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #kintamieji kuriuos norim matyti per visus puslapius
        self.vardas = ""
        self.krepselis = []
        # Biblioteka kuri laikis visus puslapius
        self.frames = {}

        #Sukurti visus langus
        for PageClass in (Pradinis, Uzsakymas, Ivadinis):
            page = PageClass(parent=container, controller=self)
            self.frames[PageClass] = page

            page.grid(row=0, column=0, sticky="nsew")

        #Rodyti pradini langa
        self.show_frame(Ivadinis)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()#perkelti langa i virsu

class Ivadinis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        langas = ctk.CTkFrame(self, corner_radius=25)
        langas.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(langas, text="Komanda \"Arbūz\" ", font=("Arial", 24)).pack(padx=50, pady=10)
        ctk.CTkLabel(
            langas,
            text="Jokūbas Kriaučiūnas EEI-5/3 | "
            ).pack(pady=10)
        ctk.CTkLabel(
            langas,
            text="Timur Valužis EEI-5/3 | "
            ).pack(pady=10)
        ctk.CTkLabel(
            langas,
            text="Arnas Makutėnas EEI-5/4 | "
            ).pack(pady=10)

        mygtukas = ctk.CTkButton(
            langas,
            text="Testi",
            command=lambda: self.controller.show_frame(Pradinis)
        )
        mygtukas.pack(pady=10)

class Pradinis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        langas = ctk.CTkFrame(self, corner_radius=25)
        langas.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            master=langas, 
            text="",
            image=open_img("logo.png",(250,250)),
            fg_color="transparent").pack()
        ctk.CTkLabel(langas, text="Naujas užsakymas", font=("Arial", 24)).pack(padx=50, pady=10)
        ctk.CTkLabel(langas,text="Įveskite savo vardą").pack(pady=10)


        self.name_entry = ctk.CTkEntry(langas, placeholder_text="Vardenis")
        self.name_entry.pack(pady=10)

        mygtukas = ctk.CTkButton(
            langas,
            text="Pradėti užsakymą",
            command=self.pradeti
        )
        mygtukas.pack(pady=10)
        self.warning_label = ctk.CTkLabel(langas, text="", text_color="red")
        self.warning_label.pack(pady=5)

    def pradeti(self):
        name = self.name_entry.get().strip()

        if not name:
            self.warning_label.configure(text="Privalote įvesti savo vardą")
            return

        self.warning_label.configure(text="")
        self.controller.vardas = name
        self.controller.show_frame(Uzsakymas)


class Uzsakymas(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #Sukurti grida
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)   # 75%
        self.grid_columnconfigure(1, weight=1)   # 25%

        #meniu langas
        meniu = ctk.CTkFrame(self, fg_color="#ebd3a7")
        meniu.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #uzsakymo langas
        desine = ctk.CTkFrame(self, fg_color="#ebd3a7")
        desine.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(meniu,text="Meniu", font=("Arial", 24)).pack(pady=(15,0))

        tabs = ctk.CTkTabview(meniu)
        tabs.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # kebabo tabas
        tab_kebabai = tabs.add("Kebabai")
        scroll_kebabai = ctk.CTkScrollableFrame(tab_kebabai, width=400, height=300)
        scroll_kebabai.pack(fill="both", expand=True)
        #skelti i dvi puses
        scroll_kebabai.grid_columnconfigure(0, weight=1) 
        scroll_kebabai.grid_columnconfigure(1, weight=1)
        
        
        self.kurti_meniu(scroll_kebabai, "kebabai", kebabas)


        #uzkandziu tabas
        tab_uzkandziai = tabs.add("Užkandžiai ir gėrimai")
        scroll_uzkandziai = ctk.CTkScrollableFrame(tab_uzkandziai, width=400, height=300)
        scroll_uzkandziai.pack(fill="both", expand=True)
        #skelti i dvi puses
        scroll_uzkandziai.grid_columnconfigure(0, weight=1) 
        scroll_uzkandziai.grid_columnconfigure(1, weight=1)

        self.kurti_meniu(scroll_uzkandziai, "uzkandziai", uzkandziai)



        #krepsio frame
        ctk.CTkLabel(desine,text="Krepšelis", font=("Arial", 16), fg_color="#f0ad32", corner_radius=5).pack(pady=(15,0), fill="x", padx=10)
        
        self.krepsys = ctk.CTkScrollableFrame(desine,fg_color="#ebd3a7")
        self.krepsys.pack(fill="both", expand=True, padx=10, pady=(10,0))

        self.sumos_mygtukas = ctk.CTkButton(
            desine,
            text="Mokėti 0.00€",
            command=self.moketi
        )
        self.sumos_mygtukas.pack(fill="x", padx=10, pady=10)
        self.sumos_mygtukas._text = "gejus"



    def kurti_meniu(self, langas, skiltis, klase):
        for i in range(len(patiekalai[skiltis])):
            kairej = math.ceil(len(patiekalai[skiltis]) / 2)
            eile = i
            if i < kairej:
                stulpelis = 0
            else:
                stulpelis = 1
                eile = i - kairej

            command = lambda idx=i: self.prideti_preke(klase(patiekalai[skiltis][idx]))
            if klase is kebabas:
                command = lambda idx=i: self.pasirinkti_priedus(patiekalai[skiltis][idx])

            ctk.CTkButton(
                langas,
                text=patiekalai[skiltis][i]["pavadinimas"] + "\n" + f"{patiekalai[skiltis][i]['kaina']:.2f}€",
                command=command,
                image=open_img(patiekalai[skiltis][i]["img"], (100 + ( 50 if klase is kebabas else 0 ),150)),
                width=275,
                height=50,
                fg_color="#ebd3a7",
                font=("Arial", 14)
                ).grid(row=eile, column=stulpelis, sticky="nsew", padx=10, pady=10)


    def pasirinkti_priedus(self, kebabo_info):
        popup = ctk.CTkToplevel(self)
        popup.title("Pasirinkite priedus")
        popup.transient(self)
        popup.grab_set()
        popup.overrideredirect(True)
        # Lango centravimas
        popup_width = 300
        popup_height = 350
        main_x = self.controller.winfo_x()
        main_y = self.controller.winfo_y()
        main_width = self.controller.winfo_width()
        main_height = self.controller.winfo_height()
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        ctk.CTkLabel(popup, text="Pasirinkite priedus", font=("Arial", 16)).pack(pady=10)
        popup.configure(fg_color="#fce5bb")

        papild_sarasas = patiekalai["papildai"]
        checkboxes = []
        for papild in papild_sarasas:
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(popup, text=f"{papild['pavadinimas']} (+{papild['kaina']:.2f}€)", variable=var, onvalue="on", offvalue="off")
            cb.pack(anchor="w", padx=20, pady=5)
            checkboxes.append((var, papild))

        def patvirtinti():
            pasirinkti_priedai = []
            for var, papild_info in checkboxes:
                if var.get() == "on":
                    pasirinkti_priedai.append(papild_info)
            
            naujas_kebabas = kebabas(kebabo_info, pasirinkti_priedai)
            self.prideti_preke(naujas_kebabas)
            popup.destroy()

        def atsaukti():
            naujas_kebabas = kebabas(kebabo_info)
            self.prideti_preke(naujas_kebabas)
            popup.destroy()

        ctk.CTkButton(popup, text="Patvirtinti", command=patvirtinti).pack(pady=10)
        ctk.CTkButton(popup, text="Pridėti be priedų", command=atsaukti).pack(pady=5)

    def valyti_krepsy(self):
        self.controller.krepselis = []
        self.atnaujinti_krepsy()

    def krepselio_suma(self):
        suma = 0.00
        for i in self.controller.krepselis:
            suma += i.kaina
        return round(suma,2)

    def krepselio_elemento_logika(self, idx):
        self.controller.krepselis.pop(idx)
        self.atnaujinti_krepsy()


    def atnaujinti_krepsy(self):
        for widget in self.krepsys.winfo_children():
            widget.destroy()

        for preke in self.controller.krepselis:
            ctk.CTkButton(
                self.krepsys,
                text=preke.pavadinimas + f"   {preke.kaina:.2f}€",
                font=("Arial", 14),
                anchor="w",
                fg_color="transparent",
                command=lambda idx=self.controller.krepselis.index(preke): self.krepselio_elemento_logika(idx)
            ).pack(anchor="w", fill="x", padx=10)
            if isinstance(preke, kebabas):
                for papildas in preke.papildai:
                    ctk.CTkLabel(self.krepsys, text=f"  + {papildas['pavadinimas']} (+{papildas['kaina']:.2f}€)", font=("Arial", 12)).pack(anchor="w", padx=(10,0))

        self.sumos_mygtukas.configure(text=f"Mokėti {self.krepselio_suma():.2f}€")

    def prideti_preke(self, preke):
        self.controller.krepselis.append(preke)
        self.atnaujinti_krepsy()

    def moketi(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Mokėjimas")
        popup.transient(self)
        popup.grab_set()

        popup.overrideredirect(True)
        # Lango centravimas
        popup_width = 350
        popup_height = 125
        main_x = self.controller.winfo_x()
        main_y = self.controller.winfo_y()
        main_width = self.controller.winfo_width()
        main_height = self.controller.winfo_height()
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.configure(fg_color="#fce5bb")

        ctk.CTkLabel(popup, text="Užsakymas vardu: " + self.controller.vardas.capitalize(), font=("Arial", 16)).pack(pady=5)
        if self.krepselio_suma() == 0:
            ctk.CTkLabel(popup, text=f"Užsakymas tuščias").pack(fill="x", padx=10, pady=5)
        else:
            ctk.CTkLabel(popup, text=f"Mokėti: {self.krepselio_suma():.2f}€").pack(fill="x", padx=10, pady=5)
        def sumoketa():
            popup.destroy()
            self.valyti_krepsy()
            self.controller.show_frame(Pradinis)



        ctk.CTkButton(popup, text="Baigti", command=sumoketa).pack(pady=5)


if __name__ == "__main__":
    ctk.set_default_color_theme(filesystem.get_base_path() + "data\\spalvos.json")
    ctk.set_appearance_mode("light")        # optional

    app = App()
    app.mainloop()
