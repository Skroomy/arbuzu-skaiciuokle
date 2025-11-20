import filesystem
import customtkinter as ctk

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

#
uzsakovo_vardas = ""

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
        print(name)
        self.controller.show_frame(Uzsakymas)


# ---------- Page 2 ----------
class Uzsakymas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)


        # Configure the grid of the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)   # 66%
        self.grid_columnconfigure(1, weight=1)   # 33%

        # LEFT panel (0.66 width)
        left = ctk.CTkFrame(self, fg_color="#444444")
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # RIGHT panel (0.33 width)
        right = ctk.CTkScrollableFrame(self, fg_color="#444444")
        right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        tabs = ctk.CTkTabview(left)
        tabs.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        tab_kebabai = tabs.add("Kebabai")
        scroll_kebabai = ctk.CTkScrollableFrame(tab_kebabai, width=400, height=300)
        scroll_kebabai.pack(fill="both", expand=True)

        tab_uzkandziai = tabs.add("Užkandžiai")
        scroll_uzkandziai = ctk.CTkScrollableFrame(tab_uzkandziai, width=400, height=300)
        scroll_uzkandziai.pack(fill="both", expand=True)

        for i in range(len(patiekalai["kebabai"])):
            ctk.CTkButton(
                scroll_kebabai,
                text=patiekalai["kebabai"][i]["pavadinimas"],
                command=lambda: controller.krepselis.append(kebabas(patiekalai["kebabai"][i]))
                ).pack(pady = 10)


        ctk.CTkLabel(scroll_uzkandziai, text="Settings options here").pack(pady=10)

        ctk.CTkLabel(right, textvariable=controller.vardas).pack(pady=10)
        ctk.CTkButton(
            right,
            text="Krepšelis",
            command=lambda: print(controller.krepselis)
        ).pack(pady=10)
        button = ctk.CTkButton(
            right,
            text="Back to Home",
            command=lambda: controller.show_frame(Pradinis)
        )
        button.pack(pady=10)



# ---------- Run app ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")        # optional
    ctk.set_default_color_theme("green")    # optional

    app = App()
    app.mainloop()




