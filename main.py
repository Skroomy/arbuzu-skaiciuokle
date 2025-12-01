import filesystem
import customtkinter as ctk
from PIL import Image

#Maisto prekiu klases
class kebabas:
    def __init__(self, info, papildas=[]):
        self.pavadinimas = info["pavadinimas"]
        self.kaina = info["kaina"]
        self.papildas = papildas
        for i in range(len(papildas)):
            self.kaina += papildas["kaina"]
        
class garnyras:
    def __init__(self, info):   
        self.pavadinimas = info["pavadinimas"]
        self.kainas = info["kaina"]

#sukurti menu_failo objekta
menu_file = filesystem.File("menu")

#ji nuskaityti
patiekalai = menu_file.read_json()





#Savadarbis prekes mygtukas:
class ImageButton(ctk.CTkFrame):
    def __init__(self, langas, image, name, price, command, **kwargs):
        # 1. Initialize the main container frame
        super().__init__(langas, fg_color="#444444", **kwargs)
        
        # Configure the grid rows for 2/3 (image) and 1/3 (text) split
        self.grid_rowconfigure(0, weight=2) 
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        if image:
            # 2. Image Label (Top 2/3)
            self.image_label = ctk.CTkLabel(self, text="", image=image)
            self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        # 3. Text Frame (Bottom 1/3)
        self.text_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.text_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        self.text_frame.grid_columnconfigure(0, weight=1)

        # Text Labels inside the text frame
        self.name_label = ctk.CTkLabel(self.text_frame, text=name, font=ctk.CTkFont(size=14, weight="bold"))
        self.name_label.pack(fill="x", padx=2, pady=(0, 0))

        self.price_label = ctk.CTkLabel(self.text_frame, text=price, font=ctk.CTkFont(size=12))
        self.price_label.pack(fill="x", padx=2, pady=(0, 2))
        
        # 4. Bind Click Event
        self.bind_click(command)

    def bind_click(self, command):
        # Create a list of all widgets to bind the command to
        all_widgets = [self, self.image_label, self.text_frame, self.name_label, self.price_label]
        for widget in all_widgets:
            # Bind the left mouse button click event
            widget.bind("<Button-1>", lambda event: command())

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        #nustatyti title ir dydi lango
        self.title("Užsakymo sąskaitos skaičiuoklė")
        self.geometry("1280x720")

        #sukurti langam kuris laikis visus kitus langus
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        #Nustatyti grid taip kad viduj esantis langai galetu issiplest
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #kintamieji kuriuos norim matyti per visus puslapius
        self.vardas = ctk.StringVar(value="")
        self.krepselis = []
        # Biblioteka kuri laikis visus puslapius
        self.frames = {}

        #Sukurti visus langus
        for PageClass in (Pradinis, Uzsakymas):
            page = PageClass(parent=container, controller=self)
            self.frames[PageClass] = page

            page.grid(row=0, column=0, sticky="nsew")

        #Rodyti pradini langa
        self.show_frame(Pradinis)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()#perkelti langa i virsu



class Pradinis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        content = ctk.CTkFrame(self)
        content.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(content, text="Naujas užsakymas", font=("Arial", 24))
        label.pack(padx=50, pady=25)

        description = ctk.CTkLabel(
            content,
            text="Įveskite savo vardą",
        )
        description.pack(pady=10)


         # Input field for the name
        self.name_entry = ctk.CTkEntry(content, placeholder_text="Vardenis")
        self.name_entry.pack(pady=10)

        # Button that tries to go to Settings
        continue_button = ctk.CTkButton(
            content,
            text="Pradėti užsakymą",
            command=self.on_continue_clicked
        )
        continue_button.pack(pady=10)
        # Label for warnings (e.g., if no name is entered)
        self.warning_label = ctk.CTkLabel(content, text="", text_color="red")
        self.warning_label.pack(pady=5)

    def on_continue_clicked(self):
        name = self.name_entry.get().strip()

        if not name:
            # No name → show warning and do NOT switch page
            self.warning_label.configure(text="Privalote įvesti savo vardą")
            return

        self.warning_label.configure(text="")
        self.controller.vardas.set(name)
        
        self.controller.show_frame(Uzsakymas)


# ---------- Page 2 ----------
class Uzsakymas(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #Sukurti grida
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)   # 75%
        self.grid_columnconfigure(1, weight=1)   # 25%

        #meniu langas
        meniu = ctk.CTkFrame(self, fg_color="#444444")
        meniu.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #uzsakymo langas
        desine = ctk.CTkFrame(self, fg_color="#444444")
        desine.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #krepsio frame
        self.krepsys = ctk.CTkScrollableFrame(desine,fg_color="#222222")
        self.krepsys.pack(padx=20, pady=20)

        tabs = ctk.CTkTabview(meniu)
        tabs.pack(fill="both", expand=True, padx=20, pady=20)

        # kebabo tabas
        tab_kebabai = tabs.add("Kebabai")
        scroll_kebabai = ctk.CTkScrollableFrame(tab_kebabai, width=400, height=300)
        scroll_kebabai.pack(fill="both", expand=True)
        #skelti i dvi puse
        scroll_kebabai.grid_columnconfigure(0, weight=1) 
        scroll_kebabai.grid_columnconfigure(1, weight=1)
        scroll_kebabai.grid_rowconfigure(0, weight=1)
        kairys = ctk.CTkFrame(scroll_kebabai,width=400, height=300).grid(row=0, column=0, sticky="nsew")
        desinis = ctk.CTkFrame(scroll_kebabai,width=400, height=300).grid(row=0, column=1, sticky="nsew")


        pil_image = Image.open(patiekalai["kebabai"][0]["img"])
        ctk_image = ctk.CTkImage(pil_image,pil_image,(100,100))
        for i in range(len(patiekalai["kebabai"])):
            #ImageButton(scroll_kebabai, ctk_image,patiekalai["kebabai"][i]["pavadinimas"],patiekalai["kebabai"][i]["kaina"],command=lambda idx=i: self.prideti_preke(kebabas(patiekalai["kebabai"][idx]))).pack(pady = 10)
            
            kairej = len(patiekalai["kebabai"]) // 2
            
            if i < kairej:
                stulpelis = kairys
            else:
                stulpelis = desinis

            mygtukas = ctk.CTkButton(
                stulpelis,
                text=patiekalai["kebabai"][i]["pavadinimas"] + "\n" + str(patiekalai["kebabai"][i]["kaina"]) + "€",
                command=lambda idx=i: self.prideti_preke(kebabas(patiekalai["kebabai"][idx])),
                image=ctk_image,
                width=275,
                height=50
                ).pack(pady=10)


                #uzkandziu tabas
        tab_uzkandziai = tabs.add("Užkandžiai")
        scroll_uzkandziai = ctk.CTkScrollableFrame(tab_uzkandziai, width=400, height=300)
        scroll_uzkandziai.pack(fill="both", expand=True)
        ctk.CTkLabel(scroll_uzkandziai, text="Settings options here").pack(pady=10)

        ctk.CTkLabel(desine, textvariable=controller.vardas).pack(pady=10)
        ctk.CTkButton(
           desine,
            text="Tuštinti krepšeli",
            command=self.valyti_krepsy
        ).pack(pady=10)


        button = ctk.CTkButton(
            desine,
            text="Back to Home",
            command=lambda: controller.show_frame(Pradinis)
        )
        button.pack(pady=10)


    def valyti_krepsy(self):
        self.controller.krepselis = []
        self.atnaujinti_krepsy()

    def atnaujinti_krepsy(self):
        for widget in self.krepsys.winfo_children():
            widget.destroy()

        for preke in self.controller.krepselis:
            ctk.CTkLabel(self.krepsys, text=preke.pavadinimas).pack(anchor="w")

    def prideti_preke(self, preke):
        self.controller.krepselis.append(preke)
        self.atnaujinti_krepsy()

# ---------- Run app ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")        # optional
    ctk.set_default_color_theme("green")    # optional

    app = App()
    app.mainloop()




