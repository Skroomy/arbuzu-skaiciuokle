import filesystem
import customtkinter as ctk

#Maisto prekiu klases
class kebabas:
    def __init__(self, info, papildas):
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

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        #nustatyti title ir dydi lango
        self.title("Užsakymo sąskaitos skaičiuoklė")
        self.geometry("1280x720")

        #sukurti langam kuris laikis visus kitus frameus
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        #Nustatyti grid taip kad viduj esantis langai galetu issiplest
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #kintamieji kuriuos norim matyti per visus puslapius
        self.user_name = ctk.StringVar(value="")

        # Biblioteka kuri laikis visus puslapius
        self.frames = {}

        # Create all pages and stack them in the same container
        for PageClass in (Pradinis, SettingsPage):
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
        self.controller.user_name.set(name)
        self.controller.show_frame(SettingsPage)


# ---------- Page 2 ----------
class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Settings Page", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(
            self,
            text="This is the settings page.\nClick the button to go back Home.",
        )
        description.pack(pady=10)

        button = ctk.CTkButton(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(Pradinis)
        )
        button.pack(pady=10)


# ---------- Run app ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")        # optional
    ctk.set_default_color_theme("blue")    # optional

    app = App()
    app.mainloop()




