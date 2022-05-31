import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import tkinter.messagebox as tm
import fahrzeugnummer_ocr
from PIL import ImageTk, Image
from tkinter.filedialog import *
import threading
import time as t
from playsound import playsound
import dmcr
import ocr
import backend
import os
import login
import keys
import customtkinter
import sys

# globale Variablen für Tank-/Leitung-Kennziffern aus dem Modul 'keys' laden
tank_keys = keys.get_tank_keys()
leitung_keys = keys.get_leitung_keys()
mode =["Dark","Light"]


customtkinter.set_appearance_mode(mode[0])


# ----------------------------------------------------------------------------------------------------------
# START der Klasse ProvaPiApp
# ----------------------------------------------------------------------------------------------------------

class ProvaPiApp(tk.Tk):
    """Hauptklasse und Stage für alle ProvaPi-Frames"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set standard properties
        self.title("ProvaPi")
        self.iconbitmap("mediaFiles/provapi_logo.ico")
        self.standard_font = tkfont.Font(family='Microsoft JhengHei UI', size=18, weight="bold")
        self.geometry('1600x900')
        self.resizable(False, False)

        # Container
        container = tk.Frame(self, takefocus=0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create frames and add them to the list
        self.frames = {}
        for F in (StartPage, LoginFrame, ConfigFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            if page_name == "StartPage":
                self.start_page = frame

            elif page_name == "LoginFrame":
                self.login_frame = frame

            elif page_name == "ConfigFrame":
                self.config_frame = frame

            # Frames platzieren
            frame.grid(row=0, column=0, sticky="nsew")

        # Startseite anzeigen
        self.show_frame("StartPage")

    # ----------------------------------------------------------------------------------------------------------
    # Funktionen
    # ----------------------------------------------------------------------------------------------------------

    def show_frame(self, page_name):
        """zeigt das gewählte Frame"""
        frame = self.frames[page_name]
        # gewähltes Frame über die anderen platzieren
        frame.tkraise()
        # verhindert, dass Widgets eines vorherigen Frames ausgewählt bleiben
        self.focus_set()

# ----------------------------------------------------------------------------------------------------------
# ENDE der Klasse ProvaPiApp
# START der Klasse StartPage
# ----------------------------------------------------------------------------------------------------------

class StartPage(tk.Frame):
    """Startseite"""
    bs_tank = ""
    bs_leitung = ""
    dmc_tank = ""
    dmc_leitung = ""
    ergebnis = ""
    count = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="grey10", takefocus=0)

        self.running = True
        self.done = False

        # pattern_list laden
        self.pattern_list = tank_keys + leitung_keys

        # Innerer Frame
        self.frame_inner = customtkinter.CTkFrame(master=self, width=1500, height=780, corner_radius=8,
                                                  fg_color=("gray80","gray15"), takefocus=0)
        self.frame_inner.place(relx=0.5, rely=0.53, anchor=CENTER)


        # Frame unten
        self.frame_south = customtkinter.CTkFrame(master=self.frame_inner, width=1450, height=280, corner_radius=8,
                                                  fg_color=("white","gray20"), takefocus=0)
        self.frame_south.place(relx=0.5, rely=0.79, anchor=CENTER)

        # counter für Animation-Frames
        self.counter = 1
        self.main_animation_running = False
        self.bauschein_animation_running = False
        self.tank_animation_running = False
        self.leitung_animation_running = False

        # ----------------------------------------------------------------------------------------------------------
        # Feedback Images
        # ----------------------------------------------------------------------------------------------------------

        # Images für Feedback laden
        self.img_falsch = Image.open("mediaFiles/falsch.png")
        self.img_richtig = Image.open("mediaFiles/richtig.png")
        self.img_fehler = Image.open("mediaFiles/fehlersuche.png")
        self.img_neutral = Image.open("mediaFiles/neutral.png")
        self.text_neutral = Image.open("mediaFiles/textneutral.png")

        # Images für Feedback resizen
        self.img_falsch = self.img_falsch.resize((700, 400), Image.ANTIALIAS)
        self.img_richtig = self.img_richtig.resize((700, 400), Image.ANTIALIAS)
        self.img_fehler = self.img_fehler.resize((700, 400), Image.ANTIALIAS)
        self.img_neutral = self.img_neutral.resize((700, 400), Image.ANTIALIAS)
        self.text_neutral = self.text_neutral.resize((700, 50), Image.ANTIALIAS)

        # Images für Feedback in Tk.PhotoImage umwandeln
        self.img_falsch = ImageTk.PhotoImage(self.img_falsch)
        self.img_richtig = ImageTk.PhotoImage(self.img_richtig)
        self.img_fehler = ImageTk.PhotoImage(self.img_fehler)
        self.img_neutral = ImageTk.PhotoImage(self.img_neutral)
        self.text_neutral = ImageTk.PhotoImage(self.text_neutral)

        # Canvas für Images erstellen und platzieren
        self.feedback_container = tk.Label(self, image=self.img_neutral, takefocus=0)
        self.feedback_container.pack()
        self.feedback_container.place(rely=0.35, relx=0.5, anchor=CENTER)
        self.feedback_img = tk.Label(self, image=self.img_neutral, takefocus=0, bg='#181818')
        self.feedback_img.pack()
        self.feedback_img.place(rely=0.35, relx=0.5, anchor=CENTER)

        self.textfeedback = tk.Label(self, image=self.text_neutral, takefocus=0)
        self.textfeedback.pack()
        self.textfeedback.place(rely=0.57, relx=0.5, anchor=CENTER)

        # Symbole welche neben den Kennziffern angezeigt werden öffnen
        self.symbol_falsch = Image.open("mediaFiles/falsch_symbol.png")
        self.symbol_falsch = self.symbol_falsch.resize((40, 40), Image.ANTIALIAS)
        self.symbol_falsch = ImageTk.PhotoImage(self.symbol_falsch)

        self.symbol_korrekt = Image.open("mediaFiles/korrekt_symbol.png")
        self.symbol_korrekt = self.symbol_korrekt.resize((40, 40), Image.ANTIALIAS)
        self.symbol_korrekt = ImageTk.PhotoImage(self.symbol_korrekt)

        self.symbol_untersuchen = Image.open("mediaFiles/untersuchen_symbol.png")
        self.symbol_untersuchen = self.symbol_untersuchen.resize((40, 40), Image.ANTIALIAS)
        self.symbol_untersuchen = ImageTk.PhotoImage(self.symbol_untersuchen)

        # Labels für Symbole erstellen und platzieren
        self.symbol_bs_tank = tk.Label(self.frame_south, text="", takefocus=0, bg="grey20", width=52, highlightthicknes=0, bd=0, height=52)
        self.symbol_bs_leitung = tk.Label(self.frame_south, text="", takefocus=0, bg="grey20", width=52, highlightthicknes=0, bd=0, height=52)
        self.symbol_tank = tk.Label(self.frame_south, text="", takefocus=0, bg="grey20", width=52, highlightthicknes=0, bd=0, height=52)
        self.symbol_leitung = tk.Label(self.frame_south, text="", takefocus=0, bg="grey20", width=52, highlightthicknes=0, bd=0, height=52)

        self.symbol_bs_tank.place(rely=0.31, relx=0.275, anchor=SW)
        self.symbol_bs_leitung.place(rely=0.76, relx=0.275, anchor=SW)
        self.symbol_tank.place(rely=0.31, relx=0.95, anchor=SE)
        self.symbol_leitung.place(rely=0.76, relx=0.95, anchor=SE)

        # ----------------------------------------------------------------------------------------------------------
        #   Schwarze Leiste für Buttons
        # ----------------------------------------------------------------------------------------------------------

        self.canvas = Canvas(self, width=1600, height=100, background="grey5", highlightthickness=0, takefocus=0)
        self.canvas.place(rely=0.01, relx=0.5, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # Configs-Button
        # ----------------------------------------------------------------------------------------------------------

        # Image für Configs-Button
        self.img_configs = Image.open("mediaFiles/button_configs.png")
        self.img_configs = self.img_configs.resize((40, 40), Image.ANTIALIAS)
        self.img_configs = ImageTk.PhotoImage(self.img_configs)

        self.img_configs_light = Image.open("mediaFiles/configs_light.png")
        self.img_configs_light = self.img_configs_light.resize((40, 40), Image.ANTIALIAS)
        self.img_configs_light = ImageTk.PhotoImage(self.img_configs_light)


        # configs_button erstellen, platzieren und Funktion zuweisen
        self.configs_button = customtkinter.CTkButton(master=self, image=self.img_configs, fg_color=("grey45","grey5"),
                                                      command=lambda: [controller.show_frame("LoginFrame"),
                                                                       hiddentext()],
                                                      border_width=0, text="", hover_color=("grey70","grey30"), takefocus=0,
                                                      width=48, corner_radius=0)

        self.configs_button.pack()
        self.configs_button.place(rely=0.01, relx=0.925)

        # Image für Day/Nightmode-Button
        '''Hier kommen die Pfade für die Bilder hin'''
        self.img_mode = Image.open("mediaFiles/darkmode_on.png")
        self.img_mode = self.img_mode.resize((60, 40), Image.ANTIALIAS)
        self.img_mode = ImageTk.PhotoImage(self.img_mode)

        self.img_mode_light = Image.open("mediaFiles/darkmode_off.png")
        self.img_mode_light = self.img_mode_light.resize((60, 40), Image.ANTIALIAS)
        self.img_mode_light = ImageTk.PhotoImage(self.img_mode_light)

        # configs_button erstellen, platzieren und Funktion zuweisen
        self.mode_button = customtkinter.CTkButton(master=self, image=self.img_mode, fg_color=("grey45","grey5"),
                                                      command=lambda: self.swap_mode(), hover=False,
                                                      border_width=0, text="", takefocus=0,
                                                      width=80, corner_radius=0)

        self.mode_button.pack()
        self.mode_button.place(rely=0.01, relx=0.06)

        # ----------------------------------------------------------------------------------------------------------
        # Help-Button
        # ----------------------------------------------------------------------------------------------------------

        # Erstelle verschiedene Labels und generiere Text:

        self.label6 = customtkinter.CTkLabel(text="Rechts erscheint das \nErgebnis des Vergleichs.",
                                             text_font=('Segoe UI', 14),
                                             bg_color="white", text_color="black", takefocus=0, width=202, height=55)

        self.label7 = customtkinter.CTkLabel(text="Oben gelangen Sie \nin den Admin-Bereich.",
                                             text_font=('Segoe UI', 14),
                                             bg_color="white", text_color="black", takefocus=0, width=190, height=50)

        self.label8 = customtkinter.CTkLabel(text="Laden Sie hier Ihre DMC Codes\nund Bauscheine hoch.",
                                             text_font=('Segoe UI', 12),
                                             bg_color="white", text_color="black", takefocus=0, width=215, height=37)

        self.label10 = customtkinter.CTkLabel(text="Wechseln Sie hier oben \nzwischen Dark und Light Mode.",
                                             text_font=('Segoe UI', 12),
                                             bg_color="white", text_color="black", takefocus=0, width=225, height=42)

        # Erstelle verschiedene Sprechblasen und lege Größe fest

        self.speechbubble = Image.open("mediaFiles/speechbubble.png")
        self.speechbubble = self.speechbubble.resize((240, 160), Image.ANTIALIAS)
        self.speechbubble = ImageTk.PhotoImage(self.speechbubble)

        self.speechbubble = customtkinter.CTkButton(master=self, image=self.speechbubble, fg_color=("grey80","grey15"),
                                                    border_width=0, text="", hover=False, takefocus=0,
                                                    width=48, corner_radius=0)

        self.speechbubble2 = Image.open("mediaFiles/speechbubble.png")
        self.speechbubble2 = self.speechbubble2.resize((300, 100), Image.ANTIALIAS)
        self.speechbubble2 = ImageTk.PhotoImage(self.speechbubble2)

        self.speechbubble2 = customtkinter.CTkButton(master=self, image=self.speechbubble2, fg_color=("white","grey20"),
                                                     border_width=0, text="", hover=False, takefocus=0,
                                                     width=48, corner_radius=0)

        self.speechbubble3 = Image.open("mediaFiles/speechbubble2.png")
        self.speechbubble3 = self.speechbubble3.resize((300, 100), Image.ANTIALIAS)
        self.speechbubble3 = ImageTk.PhotoImage(self.speechbubble3)

        self.speechbubble3 = customtkinter.CTkButton(master=self, image=self.speechbubble3, fg_color=("grey80","grey15"),
                                                     border_width=0, text="", hover=False, takefocus=0,
                                                     width=48, corner_radius=0)

        self.speechbubble4 = Image.open("mediaFiles/speechbubble3.png")
        self.speechbubble4 = self.speechbubble4.resize((300, 100), Image.ANTIALIAS)
        self.speechbubble4 = ImageTk.PhotoImage(self.speechbubble4)

        self.speechbubble4 = customtkinter.CTkButton(master=self, image=self.speechbubble4,
                                                     fg_color=("grey80", "grey15"),
                                                     border_width=0, text="", hover=False, takefocus=0,
                                                     width=48, corner_radius=0)

        # Hilfe-Funktion
        def help():
            self.label6.place(rely=0.35, relx=0.133, anchor=SW)
            self.label7.place(rely=0.20, relx=0.785, anchor=SW)
            self.label8.place(rely=0.69, relx=0.42, anchor=SW)
            self.label10.place(rely=0.203, relx=0.105, anchor=SW)

            self.speechbubble.pack()
            self.speechbubble.place(rely=0.25, relx=0.12)

            self.speechbubble2.pack()
            self.speechbubble2.place(rely=0.625, relx=0.39)

            self.speechbubble3.pack()
            self.speechbubble3.place(rely=0.1, relx=0.75)

            self.speechbubble4.pack()
            self.speechbubble4.place(rely=0.11, relx=0.08)

            self._stop_event = threading.Event()
            time.sleep(10)
            self.label6.place_forget()
            self.label7.place_forget()
            self.label8.place_forget()
            self.label10.place_forget()
            self.speechbubble.place_forget()
            self.speechbubble2.place_forget()
            self.speechbubble3.place_forget()
            self.speechbubble4.place_forget()

        # Hilfe-Thread
        def start_help(self):
            help_thread = threading.Thread(target=help, args=())
            help_thread.start()

        # Verstecke Text bei Szenenwechsel
        def hiddentext():
            self.label6.place_forget()
            self.label7.place_forget()
            self.label8.place_forget()
            self.label10.place_forget()
            self.speechbubble.place_forget()
            self.speechbubble2.place_forget()
            self.speechbubble3.place_forget()
            self.speechbubble4.place_forget()

        # Image für Help-Button


        self.img_help = Image.open("mediaFiles/help.png")
        self.img_help = self.img_help.resize((40, 40), Image.ANTIALIAS)
        self.img_help = ImageTk.PhotoImage(self.img_help)

        self.img_help_light = Image.open("mediaFiles/help_light.png")
        self.img_help_light = self.img_help_light.resize((40, 40), Image.ANTIALIAS)
        self.img_help_light = ImageTk.PhotoImage(self.img_help_light)

        # help_button erstellen, platzieren und Funktion zuweisen
        self.button_help = customtkinter.CTkButton(master=self, image=self.img_help, fg_color=("grey45","grey5"),
                                                   command=lambda: start_help(self),width=48,
                                                border_width=0, text="", hover_color=("grey70","grey30"), takefocus=0,corner_radius=0)

        self.button_help.pack()
        self.button_help.place(rely=0.01, relx=0.96)

        # Image für ProvaPi Logo
        self.img_logo = Image.open("mediaFiles/provapi_logo.png")
        self.img_logo = self.img_logo.resize((52, 52), Image.ANTIALIAS)
        self.img_logo = ImageTk.PhotoImage(self.img_logo)

        self.img_logo_light = Image.open("mediaFiles/logo_light.png")
        self.img_logo_light = self.img_logo_light.resize((52, 52), Image.ANTIALIAS)
        self.img_logo_light = ImageTk.PhotoImage(self.img_logo_light)

        self.label_logo = customtkinter.CTkButton(master=self, image=self.img_logo, hover=False, border_width=0, text="", takefocus=0, fg_color=("grey45","grey5"), width=5, corner_radius=0, height=5)
        self.label_logo.place(rely=0.003, relx=0.02)

        # ----------------------------------------------------------------------------------------------------------
        # Labels und Entries
        # ----------------------------------------------------------------------------------------------------------

        # Labels für Input Entries erstellen
        self.label1 = customtkinter.CTkLabel(master=self.frame_south, text="Leitung Bauschein:",
                                             text_font=('Segoe UI', 28),
                                             bg_color=None, text_color=("black","white"), takefocus=0, width=300, height=55)
        self.label2 = customtkinter.CTkLabel(master=self.frame_south, text="Leitung DMC:", text_font=('Segoe UI', 28),
                                             bg_color=None, text_color=("black","white"), takefocus=0, width=300, height=55)
        self.label3 = customtkinter.CTkLabel(master=self.frame_south, text="Tank Bauschein:",
                                             text_font=('Segoe UI', 28),
                                             bg_color=None, text_color=("black","white"), takefocus=0, width=300, height=55)
        self.label4 = customtkinter.CTkLabel(master=self.frame_south, text="Tank DMC:", text_font=('Segoe UI', 28),
                                             bg_color=None, text_color=("black","white"), takefocus=0, width=300, height=55)

        # Labels für Input Entries platzieren
        self.label1.place(rely=0.75, relx=0.02, anchor=SW)
        self.label2.place(rely=0.75, relx=0.9, anchor=SE)
        self.label3.place(rely=0.3, relx=0.035, anchor=SW)
        self.label4.place(rely=0.3, relx=0.915, anchor=SE)

        # Labels für ausgelesene Kennziffern
        self.label_bs_tank = customtkinter.CTkLabel(master=self.frame_south, text=self.bs_tank,
                                                    text_font=('Segoe UI Semibold', 30),
                                                    bg_color=None, text_color=("black","white"), takefocus=0, width=40, height=55)
        self.label_bs_leitung = customtkinter.CTkLabel(master=self.frame_south, text=self.bs_leitung,
                                                    text_font=('Segoe UI Semibold', 30),
                                                    bg_color=None, text_color=("black","white"), takefocus=0, width=40, height=55)
        self.label_dmc_tank = customtkinter.CTkLabel(master=self.frame_south, text=self.dmc_tank,
                                                    text_font=('Segoe UI Semibold', 30),
                                                    bg_color=None, text_color=("black","white"), takefocus=0, width=40, height=55)
        self.label_dmc_leitung = customtkinter.CTkLabel(master=self.frame_south, text=self.dmc_leitung,
                                                       text_font=('Segoe UI Semibold', 30),
                                                       bg_color=None, text_color=("black","white"), takefocus=0, width=40,
                                                       height=55)

        self.label_bs_tank.place(rely=0.3, relx=0.24, anchor=SW)
        self.label_bs_leitung.place(rely=0.75, relx=0.24, anchor=SW)
        self.label_dmc_tank.place(rely=0.3, relx=0.91, anchor=SE)
        self.label_dmc_leitung.place(rely=0.75, relx=0.91, anchor=SE)

        # Label für Fahrzeugnummer
        self.label_num = customtkinter.CTkLabel(master=self.frame_south, text=self.bs_tank,
                         text_font=('Segoe UI Semibold', 22),
                         bg_color=None, text_color=("black","white"), takefocus=0, width=400, height=80)
        self.label_num.place(rely=0.28, relx=0.5, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------------------------------------------------------

        # Buttons erstellen und Funktionen zuweisen
        self.abgleich_button = customtkinter.CTkButton(master=self.frame_south, width=350, text='Scan Bauschein',
                                                       command=lambda: self.kickstart(),
                                                       text_font=('Segoe UI Semibold', 28), takefocus=0, height=70,
                                                       border_color="#5EA880",
                                                       fg_color=("grey50","grey15"), border_width=3, hover_color="#458577")

        # Buttons platzieren
        self.abgleich_button.place(rely=0.5, relx=0.5, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # 'Loading' Images
        # ----------------------------------------------------------------------------------------------------------
        self.trans = Image.open("mediaFiles/animation/trans.png")
        self.trans = self.trans.resize((1, 1), Image.ANTIALIAS)
        self.trans = ImageTk.PhotoImage(self.trans)

        self.f1 = Image.open("mediaFiles/animation/loading1.png")
        self.f1 = self.f1.resize((256, 256), Image.ANTIALIAS)
        self.f1 = ImageTk.PhotoImage(self.f1)
        self.f2 = Image.open("mediaFiles/animation/loading2.png")
        self.f2 = self.f2.resize((256, 256), Image.ANTIALIAS)
        self.f2 = ImageTk.PhotoImage(self.f2)
        self.f3 = Image.open("mediaFiles/animation/loading3.png")
        self.f3 = self.f3.resize((256, 256), Image.ANTIALIAS)
        self.f3 = ImageTk.PhotoImage(self.f3)
        self.f4 = Image.open("mediaFiles/animation/loading4.png")
        self.f4 = self.f4.resize((256, 256), Image.ANTIALIAS)
        self.f4 = ImageTk.PhotoImage(self.f4)
        self.f5 = Image.open("mediaFiles/animation/loading5.png")
        self.f5 = self.f5.resize((256, 256), Image.ANTIALIAS)
        self.f5 = ImageTk.PhotoImage(self.f5)
        self.f6 = Image.open("mediaFiles/animation/loading6.png")
        self.f6 = self.f6.resize((256, 256), Image.ANTIALIAS)
        self.f6 = ImageTk.PhotoImage(self.f6)
        self.f7 = Image.open("mediaFiles/animation/loading7.png")
        self.f7 = self.f7.resize((256, 256), Image.ANTIALIAS)
        self.f7 = ImageTk.PhotoImage(self.f7)
        self.f8 = Image.open("mediaFiles/animation/loading8.png")
        self.f8 = self.f8.resize((256, 256), Image.ANTIALIAS)
        self.f8 = ImageTk.PhotoImage(self.f8)

        self.f1_small = Image.open("mediaFiles/animation/loading1.png")
        self.f1_small = self.f1_small.resize((40, 40), Image.ANTIALIAS)
        self.f1_small = ImageTk.PhotoImage(self.f1_small)
        self.f2_small = Image.open("mediaFiles/animation/loading2.png")
        self.f2_small = self.f2_small.resize((40, 40), Image.ANTIALIAS)
        self.f2_small = ImageTk.PhotoImage(self.f2_small)
        self.f3_small = Image.open("mediaFiles/animation/loading3.png")
        self.f3_small = self.f3_small.resize((40, 40), Image.ANTIALIAS)
        self.f3_small = ImageTk.PhotoImage(self.f3_small)
        self.f4_small = Image.open("mediaFiles/animation/loading4.png")
        self.f4_small = self.f4_small.resize((40, 40), Image.ANTIALIAS)
        self.f4_small = ImageTk.PhotoImage(self.f4_small)
        self.f5_small = Image.open("mediaFiles/animation/loading5.png")
        self.f5_small = self.f5_small.resize((40, 40), Image.ANTIALIAS)
        self.f5_small = ImageTk.PhotoImage(self.f5_small)
        self.f6_small = Image.open("mediaFiles/animation/loading6.png")
        self.f6_small = self.f6_small.resize((40, 40), Image.ANTIALIAS)
        self.f6_small = ImageTk.PhotoImage(self.f6_small)
        self.f7_small = Image.open("mediaFiles/animation/loading7.png")
        self.f7_small = self.f7_small.resize((40, 40), Image.ANTIALIAS)
        self.f7_small = ImageTk.PhotoImage(self.f7_small)
        self.f8_small = Image.open("mediaFiles/animation/loading8.png")
        self.f8_small = self.f8_small.resize((40, 40), Image.ANTIALIAS)
        self.f8_small = ImageTk.PhotoImage(self.f8_small)

        # Animation-Clock starten
        thread = threading.Thread(target=self.animation_clock, args=())
        thread.start()

    # ----------------------------------------------------------------------------------------------------------
    # Funktionen
    # ----------------------------------------------------------------------------------------------------------

    def swap_mode(self):
        if customtkinter.get_appearance_mode() =="Dark":
            self.symbol_bs_tank.configure(bg="white")
            self.symbol_bs_leitung.configure(bg="white")
            self.symbol_tank.configure(bg="white")
            self.symbol_leitung.configure(bg="white")
            self.canvas.configure(bg="grey45")

            self.configs_button.configure(image=self.img_configs_light)
            self.label_logo.configure(image=self.img_logo_light)
            self.button_help.configure(image=self.img_help_light)
            self.mode_button.configure(image=self.img_mode_light)

            ##self.feedback_img = tk.Label(self, image=self.img_neutral, takefocus=0, bg='#181818')
            self.configure(bg="grey50")
            provapi.config_frame.configs_button.configure(image=self.img_configs_light)
            provapi.login_frame.configs_button.configure(image=self.img_configs_light)
            provapi.config_frame.button_help.configure(image=self.img_help_light)
            provapi.login_frame.button_help.configure(image=self.img_help_light)
            provapi.config_frame.label_logo.configure(image=self.img_logo_light)
            provapi.login_frame.label_logo.configure(image=self.img_logo_light)
            provapi.config_frame.configure(bg="grey50")
            provapi.login_frame.configure(bg="grey50")


            #LoginFrame.swap_mode(LoginFrame)

            customtkinter.set_appearance_mode(mode[1])
        else:
            self.symbol_bs_tank.configure(bg="grey20")
            self.symbol_bs_leitung.configure(bg="grey20")
            self.symbol_tank.configure(bg="grey20")
            self.symbol_leitung.configure(bg="grey20")
            self.canvas.configure(bg="grey5")

            self.configs_button.configure(image=self.img_configs)
            self.label_logo.configure(image=self.img_logo)
            self.button_help.configure(image=self.img_help)
            self.mode_button.configure(image=self.img_mode)

            provapi.config_frame.configs_button.configure(image=self.img_configs)
            provapi.login_frame.configs_button.configure(image=self.img_configs)
            provapi.config_frame.button_help.configure(image=self.img_help)
            provapi.login_frame.button_help.configure(image=self.img_help)
            provapi.config_frame.label_logo.configure(image=self.img_logo)
            provapi.login_frame.label_logo.configure(image=self.img_logo)
            provapi.config_frame.configure(bg="grey10")
            provapi.login_frame.configure(bg="grey10")

            self.configure(bg="grey10")
            customtkinter.set_appearance_mode(mode[0])

    def kickstart(self):
        thread = threading.Thread(target=self.start_comparison, args=())
        thread.start()

    def start_comparison(self):
        self.done = False
        if self.count == 0:
            #key = ocr.get_bauschein_from_file(askopenfilename(title="Select a File"))
            self.main_animation_running = True
            self.bauschein_animation_running = True
            path = askopenfilename(title="Select a File")
            # self.label_num.config(text="Fahrzeugnummer: " + fahrzeugnummer_ocr.readImage(path))
            key = ocr.readImage(path)
            self.bs_tank = key[0]
            self.bs_leitung = key[1]
            self.label_bs_tank.config(text=self.bs_tank)
            self.label_bs_leitung.config(text=self.bs_leitung)
            self.abgleich_button.config(text="Scan Tank")
            self.count += 1
            self.bauschein_animation_running = False
        elif self.count == 1:
            self.tank_animation_running = True
            key = dmcr.get_dmc_from_file(askopenfilename(title="Select a File"), "tank")
            self.dmc_tank = key
            self.label_dmc_tank.config(text=self.dmc_tank)
            self.abgleich_button.config(text="Scan Leitung")
            self.count += 1
            self.tank_animation_running = False
        elif self.count == 2:
            self.leitung_animation_running = True
            key = dmcr.get_dmc_from_file(askopenfilename(title="Select a File"), "bauschein")
            self.dmc_leitung = key
            self.label_dmc_leitung.config(text=self.dmc_leitung)
            self.abgleich_button.config(text="Starte Abgleich")
            self.count += 1
            self.leitung_animation_running = False

            print("DMC Tank: " + self.dmc_tank)
            print("DMC Leitung: " + self.dmc_leitung)
            print("Bauschein Tank: " + self.bs_tank)
            print("Bauschein Leitung: " + self.bs_leitung)

            self.ergebnis = backend.start_comparison(self.bs_tank, self.bs_leitung,
                                                 self.dmc_tank, self.dmc_leitung)

            self.main_animation_running = False
            self.done = True

            # ergebnis ist ein Integer {1, 2, 3}, wobei gilt:
            # 1: korrekt
            # 2, 3 und 4: falsch
            # 5: fehlerhaft
            if self.ergebnis == 1:
                thread = threading.Thread(target=self.vergleich_optisch_korrekt, args=())
                thread.start()
            elif self.ergebnis == 2 or self.ergebnis == 3 or self.ergebnis == 4:
                thread = threading.Thread(target=self.vergleich_optisch_falsch, args=())
                thread.start()
            elif self.ergebnis == 5:
                thread = threading.Thread(target=self.vergleich_optisch_fehler, args=())
                thread.start()
            else:
                raise Exception

            self.count = 0

    def animation_clock(self):
        while self.running:
            if self.main_animation_running:
                self.main_animation()
            if self.bauschein_animation_running:
                self.bauschein_animation()
            elif not self.done:
                self.symbol_bs_tank.config(image=self.trans)
                self.symbol_bs_leitung.config(image=self.trans)
            if self.leitung_animation_running:
                self.leitung_animation()
            elif not self.done:
                self.symbol_leitung.config(image=self.trans)
            if self.tank_animation_running:
                self.tank_animation()
            elif not self.done:
                self.symbol_tank.config(image=self.trans)
            if self.counter == 8:
                self.counter = 1
            else:
                self.counter += 1
            t.sleep(0.05)

    def main_animation(self):
        if self.counter == 1:
            self.feedback_img.configure(image=self.f1)
        elif self.counter == 2:
            self.feedback_img.configure(image=self.f2)
        elif self.counter == 3:
            self.feedback_img.configure(image=self.f3)
        elif self.counter == 4:
            self.feedback_img.configure(image=self.f4)
        elif self.counter == 5:
            self.feedback_img.configure(image=self.f5)
        elif self.counter == 6:
            self.feedback_img.configure(image=self.f6)
        elif self.counter == 7:
            self.feedback_img.configure(image=self.f7)
        elif self.counter == 8:
            self.feedback_img.configure(image=self.f8)

    def bauschein_animation(self):
        if self.counter == 1:
            self.symbol_bs_tank.config(image=self.f1_small)
            self.symbol_bs_leitung.config(image=self.f1_small)
        elif self.counter == 2:
            self.symbol_bs_tank.config(image=self.f2_small)
            self.symbol_bs_leitung.config(image=self.f2_small)
        elif self.counter == 3:
            self.symbol_bs_tank.config(image=self.f3_small)
            self.symbol_bs_leitung.config(image=self.f3_small)
        elif self.counter == 4:
            self.symbol_bs_tank.config(image=self.f4_small)
            self.symbol_bs_leitung.config(image=self.f4_small)
        elif self.counter == 5:
            self.symbol_bs_tank.config(image=self.f5_small)
            self.symbol_bs_leitung.config(image=self.f5_small)
        elif self.counter == 6:
            self.symbol_bs_tank.config(image=self.f6_small)
            self.symbol_bs_leitung.config(image=self.f6_small)
        elif self.counter == 7:
            self.symbol_bs_tank.config(image=self.f7_small)
            self.symbol_bs_leitung.config(image=self.f7_small)
        elif self.counter == 8:
            self.symbol_bs_tank.config(image=self.f8_small)
            self.symbol_bs_leitung.config(image=self.f8_small)

    def leitung_animation(self):
        if self.counter == 1:
            self.symbol_leitung.config(image=self.f1_small)
        elif self.counter == 2:
            self.symbol_leitung.config(image=self.f2_small)
        elif self.counter == 3:
            self.symbol_leitung.config(image=self.f3_small)
        elif self.counter == 4:
            self.symbol_leitung.config(image=self.f4_small)
        elif self.counter == 5:
            self.symbol_leitung.config(image=self.f5_small)
        elif self.counter == 6:
            self.symbol_leitung.config(image=self.f6_small)
        elif self.counter == 7:
            self.symbol_leitung.config(image=self.f7_small)
        elif self.counter == 8:
            self.symbol_leitung.config(image=self.f8_small)

    def tank_animation(self):
        if self.counter == 1:
            self.symbol_tank.config(image=self.f1_small)
        elif self.counter == 2:
            self.symbol_tank.config(image=self.f2_small)
        elif self.counter == 3:
            self.symbol_tank.config(image=self.f3_small)
        elif self.counter == 4:
            self.symbol_tank.config(image=self.f4_small)
        elif self.counter == 5:
            self.symbol_tank.config(image=self.f5_small)
        elif self.counter == 6:
            self.symbol_tank.config(image=self.f6_small)
        elif self.counter == 7:
            self.symbol_tank.config(image=self.f7_small)
        elif self.counter == 8:
            self.symbol_tank.config(image=self.f8_small)

    def vergleich_optisch_korrekt(self):
        """visuelles und akkustisches Signal für 'korrekt'"""
        # Symbole in den Labels einfügen
        self.symbol_bs_tank.config(image=self.symbol_korrekt)
        self.symbol_bs_leitung.config(image=self.symbol_korrekt)
        self.symbol_tank.config(image=self.symbol_korrekt)
        self.symbol_leitung.config(image=self.symbol_korrekt)
        self.feedback_img.configure(image=self.img_richtig)
        #Label erstellen mit Infotext und platzieren
        self.label9 = customtkinter.CTkLabel(text="Abgleich erfolgreich",
                                             text_font=('Segoe UI', 20),
                                             bg_color="grey10", text_color="white", takefocus=0, width=690, height=40)
        self.label9.place(rely=0.588, relx=0.285, anchor=SW)
        # Ergebnis auf Button anzeigen
        self.abgleich_button.config(text="Korrekt!")
        # Sound laden und abspielen
        path = os.path.abspath("mediaFiles/glocke.mp3")
        path = path.replace("\\", "/")
        playsound(path)
        # warte 10 Sekunden
        t.sleep(10)
        # Label mit 'neutral' überschreiben
        self.feedback_img.configure(image=self.img_neutral)
        # Kennziffern verschwinden lassen
        self.label_dmc_tank.config(text="")
        self.label_dmc_leitung.config(text="")
        self.label_bs_tank.config(text="")
        self.label_bs_leitung.config(text="")
        self.abgleich_button.config(text="Scan Bauschein")
        self.label_num.config(text="")
        # Symbole verschwinden lassen
        self.symbol_bs_tank.config(image="")
        self.symbol_bs_leitung.config(image="")
        self.symbol_tank.config(image="")
        self.symbol_leitung.config(image="")
        #Label verschwinden lassen
        self.label9.place_forget()

    def vergleich_optisch_falsch(self):
        """visuelles und akkustisches Signal für 'falsch'"""
        # Symbole in den Labels einfügen
        if self.ergebnis == 2:
            self.symbol_bs_tank.config(image=self.symbol_korrekt)
            self.symbol_bs_leitung.config(image=self.symbol_falsch)
            self.symbol_tank.config(image=self.symbol_korrekt)
            self.symbol_leitung.config(image=self.symbol_falsch)
        elif self.ergebnis == 3:
            self.symbol_bs_tank.config(image=self.symbol_falsch)
            self.symbol_bs_leitung.config(image=self.symbol_korrekt)
            self.symbol_tank.config(image=self.symbol_falsch)
            self.symbol_leitung.config(image=self.symbol_korrekt)
        else:
            self.symbol_bs_tank.config(image=self.symbol_falsch)
            self.symbol_bs_leitung.config(image=self.symbol_falsch)
            self.symbol_tank.config(image=self.symbol_falsch)
            self.symbol_leitung.config(image=self.symbol_falsch)
        self.feedback_img.configure(image=self.img_falsch)
        # Label erstellen mit Infotext und platzieren
        self.label9 = customtkinter.CTkLabel(text="Abgleich fehlgeschlagen",
                                             text_font=('Segoe UI', 20),
                                             bg_color="grey10", text_color="white", takefocus=0, width=690, height=40)
        self.label9.place(rely=0.588, relx=0.285, anchor=SW)
        # Ergebnis auf Button anzeigen
        self.abgleich_button.config(text="Falsch!")
        # Sound laden und abspielen
        path = os.path.abspath("mediaFiles/alarm.mp3")
        path = path.replace("\\", "/")
        playsound(path)
        # warte 10 Sekunden
        t.sleep(10)
        # Label mit 'neutral' überschreiben
        self.feedback_img.configure(image=self.img_neutral)
        # Kennziffern verschwinden lassen
        self.label_dmc_tank.config(text="")
        self.label_dmc_leitung.config(text="")
        self.label_bs_tank.config(text="")
        self.label_bs_leitung.config(text="")
        self.abgleich_button.config(text="Scan Bauschein")
        self.label_num.config(text="")
        # Symbole verschwinden lassen
        self.symbol_bs_tank.config(image="")
        self.symbol_bs_leitung.config(image="")
        self.symbol_tank.config(image="")
        self.symbol_leitung.config(image="")
        # Label verschwinden lassen
        self.label9.place_forget()

    def vergleich_optisch_fehler(self):
        """visuelles und akkustisches Signal für 'fehlerhaft'"""
        # Symbole anzeigen
        if (self.label_dmc_tank.text == "?" or self.label_bs_tank.text == "?") and (self.label_dmc_leitung.text == "?" or self.label_bs_leitung.text == "?"):
            self.symbol_bs_tank.config(image=self.symbol_untersuchen)
            self.symbol_bs_leitung.config(image=self.symbol_untersuchen)
            self.symbol_tank.config(image=self.symbol_untersuchen)
            self.symbol_leitung.config(image=self.symbol_untersuchen)
        elif self.label_dmc_tank.text == "?" or self.label_bs_tank.text == "?":
            self.symbol_bs_tank.config(image=self.symbol_untersuchen)
            self.symbol_tank.config(image=self.symbol_untersuchen)
            if self.label_dmc_leitung.text == self.label_bs_leitung.text:
                self.symbol_bs_leitung.config(image=self.symbol_korrekt)
                self.symbol_leitung.config(image=self.symbol_korrekt)
            else:
                self.symbol_bs_leitung.config(image=self.symbol_falsch)
                self.symbol_leitung.config(image=self.symbol_falsch)
        else:
            self.symbol_bs_leitung.config(image=self.symbol_untersuchen)
            self.symbol_leitung.config(image=self.symbol_untersuchen)
            if self.label_dmc_tank.text == self.label_bs_tank.text:
                self.symbol_bs_tank.config(image=self.symbol_korrekt)
                self.symbol_tank.config(image=self.symbol_korrekt)
            else:
                self.symbol_bs_tank.config(image=self.symbol_falsch)
                self.symbol_tank.config(image=self.symbol_falsch)
        self.feedback_img.configure(image=self.img_fehler)
        # Label erstellen mit Infotext und platzieren
        self.label9 = customtkinter.CTkLabel(text="Eingabe ungültig. Bitte überprüfen Sie Ihre Eingabe!",
                                             text_font=('Segoe UI', 20),
                                             bg_color="grey10", text_color="white", takefocus=0, width=690, height=40)
        self.label9.place(rely=0.588, relx=0.285, anchor=SW)
        # Ergebnis auf Button anzeigen
        self.abgleich_button.config(text="Unzulässig!")
        # sound
        path = os.path.abspath("mediaFiles/alarm.mp3")
        path = path.replace("\\", "/")
        playsound(path)
        # warte 10 Sekunden
        t.sleep(10)
        # Label mit 'neutral' überschreiben
        self.feedback_img.configure(image=self.img_neutral)
        # Kennziffern verschwinden lassen
        self.label_dmc_tank.config(text="")
        self.label_dmc_leitung.config(text="")
        self.label_bs_tank.config(text="")
        self.label_bs_leitung.config(text="")
        self.abgleich_button.config(text="Scan Bauschein")
        self.label_num.config(text="")
        # Symbole entfernen
        self.symbol_bs_tank.config(image="")
        self.symbol_bs_leitung.config(image="")
        self.symbol_tank.config(image="")
        self.symbol_leitung.config(image="")
        # Label verschwinden lassen
        self.label9.place_forget()


# ----------------------------------------------------------------------------------------------------------
# ENDE der Klasse StartPage
# START der Klasse LoginFrame
# ----------------------------------------------------------------------------------------------------------

class LoginFrame(tk.Frame):
    """Loginseite"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(takefocus=0)

        if "win" in sys.platform:
            if customtkinter.get_appearance_mode() == "Dark":
                self.configure(bg="gray10")  # set window background to dark color
            ##else: self.configure(bg="white")

        # login mit ENTER-Taste
        self.controller.bind('<Return>', lambda x: self.login())

        self.frame_outer = customtkinter.CTkFrame(master=self, width=1600,height=900,corner_radius=0,
                                                  fg_color=("grey50","gray10"), takefocus=0)
        self.frame_inner = customtkinter.CTkFrame(master=self, width=1500, height=780, corner_radius=8,
                                                  fg_color=("grey80", "gray15"), takefocus=0)
        self.frame_south = customtkinter.CTkFrame(master=self.frame_inner, width=900, height=420, corner_radius=8,
                                                  fg_color=("grey70", "grey20"), takefocus=0)
        self.frame_outer.place(relx=0, rely=0)
        self.frame_inner.place(relx=0.5, rely=0.53, anchor=CENTER)
        self.frame_south.place(relx=0.5, rely=0.85, anchor=S)

        self.label_info = customtkinter.CTkLabel(master=self.frame_inner,
                                                 text="Bitte loggen Sie sich als Administrator ein,\n" +
                                                      "  um in die Konfigurationen zu gelangen:",
                                                 width=900,
                                                 height=120,
                                                 corner_radius=8,
                                                 fg_color=("grey70", "gray20"),
                                                 justify=LEFT,
                                                 text_font=('Segoe UI', 25), takefocus=0)
        self.label_info.place(relx=0.5, rely=0.1, anchor=N)

        # ----------------------------------------------------------------------------------------------------------
        #   Schwarze Leiste für Buttons
        # ----------------------------------------------------------------------------------------------------------
        self.frame_canvas = customtkinter.CTkFrame(master=self, width=1600, height=100, corner_radius=0,
                                                 fg_color=("grey45", "grey5"), takefocus=0)
        self.frame_canvas.place(relx=0.5, rely=0.01, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # Configs-Button
        # ----------------------------------------------------------------------------------------------------------

        self.img_configs = Image.open("mediaFiles/button_configs.png")
        self.img_configs = self.img_configs.resize((40, 40), Image.ANTIALIAS)
        self.img_configs = ImageTk.PhotoImage(self.img_configs)

        self.img_configs_light = Image.open("mediaFiles/configs_light.png")
        self.img_configs_light = self.img_configs_light.resize((40, 40), Image.ANTIALIAS)
        self.img_configs_light = ImageTk.PhotoImage(self.img_configs_light)

        # configs_button erstellen, platzieren und Funktion zuweisen
        self.configs_button = customtkinter.CTkButton(master=self, image=self.img_configs, fg_color=("grey45","grey5"),
                                                      border_width=0, text="", takefocus=0, hover=False,
                                                      width=48, corner_radius=0)
        self.configs_button.pack()
        self.configs_button.place(rely=0.01, relx=0.925)

        # ----------------------------------------------------------------------------------------------------------
        # Help-Button
        # ----------------------------------------------------------------------------------------------------------

        self.img_help = Image.open("mediaFiles/help.png")
        self.img_help = self.img_help.resize((40, 40), Image.ANTIALIAS)
        self.img_help = ImageTk.PhotoImage(self.img_help)

        # help_button erstellen, platzieren und Funktion zuweisen
        self.button_help = customtkinter.CTkButton(master=self, image=self.img_help, fg_color=("grey45","grey5"),
                                                border_width=0, text="",takefocus=0,hover=False,
                                                width=48, corner_radius=0)

        self.button_help.pack()
        self.button_help.place(rely=0.01, relx=0.96)

        # Image für ProvaPi Logo
        self.img_logo = Image.open("mediaFiles/provapi_logo.png")
        self.img_logo = self.img_logo.resize((52, 52), Image.ANTIALIAS)
        self.img_logo = ImageTk.PhotoImage(self.img_logo)
        self.label_logo = customtkinter.CTkButton(master=self, image=self.img_logo, hover=False, border_width=0,
                                                  text="", takefocus=0, fg_color=("grey45", "grey5"), width=5,
                                                  corner_radius=0, height=5)
        self.label_logo.place(rely=0.003, relx=0.02)

        # ----------------------------------------------------------------------------------------------------------
        # Labels und Entries
        # ----------------------------------------------------------------------------------------------------------

        self.label_username = customtkinter.CTkLabel(master=self.frame_south, text="Nutzername:", corner_radius=8,
                                                     fg_color=("grey70", "gray20"), text_font=('Segoe UI', 25),
                                                     width=200, height=60, takefocus=0)
        self.label_username.place(relx=0.3, rely=0.25, anchor=CENTER)

        self.entry_username = customtkinter.CTkEntry(master=self.frame_south, corner_radius=8,
                                                     font=('Segoe UI Semilight', 25), fg_color="white",
                                                     text_color="grey10", width=300, height=48, takefocus=0)
        self.entry_username.place(relx=0.6, rely=0.25, anchor=CENTER)

        self.label_password = customtkinter.CTkLabel(master=self.frame_south, text="Passwort:", corner_radius=8,
                                                     fg_color=("grey70", "gray20"), text_font=('Segoe UI', 25),
                                                     width=150, height=60, takefocus=0)
        self.label_password.place(relx=0.328, rely=0.45, anchor=CENTER)

        self.entry_password = customtkinter.CTkEntry(master=self.frame_south, corner_radius=8,
                                                     font=('Segoe UI Semilight', 25), fg_color="white",
                                                     text_color="grey10", show="*", width=300, height=48, takefocus=0)
        self.entry_password.place(relx=0.6, rely=0.45, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------------------------------------------------------

        # Login-Button erstellen
        self.button_login = customtkinter.CTkButton(master=self.frame_south, text="Login", command=self.login,
                                                    text_font=('Segoe UI Semibold', 23), border_color="#5EA880",
                                                    fg_color=("grey45", "grey15"), border_width=3, hover_color="#458577",
                                                    height=40, takefocus=0)
        self.button_login.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Reset-Button erstellen
        self.button_reset = customtkinter.CTkButton(master=self.frame_south, text="Reset", command=self.reset,
                                                    text_font=('Segoe UI Semibold', 23), border_color="#5EA880",
                                                    fg_color=("grey45", "grey15"), border_width=3, hover_color="#458577",
                                                    height=40, takefocus=0)
        self.button_reset.place(relx=0.67, rely=0.65, anchor=CENTER)

        # Image für Back-Button
        self.img_back = Image.open("mediaFiles/back_button.png")
        self.img_back = self.img_back.resize((72, 72), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(self.img_back)

        # Zurück-Button erstellen
        # Funktion 'self.back()': aktuelle Eingaben löschen und Startseite anzeigen
        self.button_back = customtkinter.CTkButton(master=self.frame_inner, image=self.img_back, fg_color=None,
                                                   command=lambda: self.back(), takefocus=0, border_width=0, text="",
                                                   width=50, hover_color=("grey90","grey10"))
        self.button_back.place(rely=0.94, relx=0.04, relwidth=0.06, relheight=0.075, anchor=CENTER)

    # ----------------------------------------------------------------------------------------------------------

    def back(self):
        """löscht die aktuellen Eingaben und zeigt die Startseite an"""
        self.reset()
        self.controller.show_frame("StartPage")

    def login(self):
        """überprüft, ob username und password valide sind und handelt entsprechend"""
        if len(self.entry_username.get()) > 0 and len(self.entry_password.get()) > 0:
            username = self.entry_username.get()
            password = self.entry_password.get()

            if login.check_userinfo(username, password):
                # löscht Eingaben und leitet zur Konfigurationsseite weiter
                self.reset()
                self.controller.show_frame("ConfigFrame")
            else:
                # zeigt Error-Message
                tm.showerror("Attempt Failed", "Incorrect Username or Password!")

    def reset(self):
        """löscht die aktuellen Eingaben"""
        self.entry_username.delete(0, END)
        self.entry_username.insert(0, "")
        self.entry_password.delete(0, END)
        self.entry_password.insert(0, "")
        self.entry_username.focus()


# ----------------------------------------------------------------------------------------------------------
# ENDE der Klasse LoginFrame
# START der Klasse ConfigFrame
# ----------------------------------------------------------------------------------------------------------

class ConfigFrame(tk.Frame):
    """Konfigurationsseite"""

    def __init__(self, parent, controller):
        # setzt 'tank_keys' und 'leitung_keys' als globale variablen
        global tank_keys, leitung_keys

        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(takefocus=0)

        if "win" in sys.platform:
            if customtkinter.get_appearance_mode() == "Dark":
                self.configure(bg="gray10")  # set window background to dark color

        # erstellt eine Scrollbar für die Listboxen der Tank-Kennziffern, sowie Leitung-Kennziffern
        scrollbar = tk.Scrollbar(self, orient="vertical", takefocus=0)
        # Frame Outer, workaround ersatz für configure
        self.frame_outer = customtkinter.CTkFrame(master=self, width=1600, height=900, corner_radius=0,
                                                  fg_color=("grey50", "gray10"), takefocus=0)
        self.frame_outer.place(relx=0, rely=0)
        # Frame INNER
        self.frame_inner = customtkinter.CTkFrame(master=self, width=1500, height=780, corner_radius=8,
                                                  fg_color=("grey70","gray15"), takefocus=0)
        self.frame_inner.place(relx=0.5, rely=0.53, anchor=CENTER)

        # Frame SOUTH
        self.frame_south = customtkinter.CTkFrame(master=self.frame_inner, width=1300, height=550, corner_radius=8,
                                                  fg_color=("grey80","gray20"), takefocus=0)
        self.frame_south.place(relx=0.5, rely=0.9, anchor=S)

        # HEADER
        self.label_info = customtkinter.CTkLabel(master=self.frame_inner,
                                                 text="Kennziffer Konfiguration",
                                                 width=1300,
                                                 height=80,
                                                 corner_radius=8,
                                                 fg_color=("white", "gray20"),
                                                 justify=LEFT,
                                                 text_font=('Segoe UI Semibold', 25), takefocus=0)
        self.label_info.place(relx=0.5, rely=0.05, anchor=N)

        # ----------------------------------------------------------------------------------------------------------
        #   Schwarze Leiste für Buttons
        # ----------------------------------------------------------------------------------------------------------


        #self.canvas = Canvas(self, width=1600, height=100, background="grey5", highlightthickness=0, takefocus=0)
        #self.canvas.place(rely=0.01, relx=0.5, anchor=CENTER)

        self.frame_canvas = customtkinter.CTkFrame(master=self, width=1600, height=100, corner_radius=0,
                                                   fg_color=("grey45", "grey5"), takefocus=0)
        self.frame_canvas.place(relx=0.5, rely=0.01, anchor=CENTER)

        # ----------------------------------------------------------------------------------------------------------
        # Configs-Button
        # ----------------------------------------------------------------------------------------------------------

        # Image für Configs-Button
        self.img_configs = Image.open("mediaFiles/button_configs.png")
        self.img_configs = self.img_configs.resize((40, 40), Image.ANTIALIAS)
        self.img_configs = ImageTk.PhotoImage(self.img_configs)

        # configs_button erstellen, platzieren und Funktion zuweisen
        self.configs_button = customtkinter.CTkButton(master=self, image=self.img_configs, fg_color=("grey45","grey5"),
                                                      border_width=0, text="", takefocus=0, hover=False,
                                                      width=48, corner_radius=0)

        self.configs_button.pack()
        self.configs_button.place(rely=0.01, relx=0.925)

        # ----------------------------------------------------------------------------------------------------------
        # Help-Button
        # ----------------------------------------------------------------------------------------------------------

        # Image für Help-Button
        self.img_help = Image.open("mediaFiles/help.png")
        self.img_help = self.img_help.resize((40, 40), Image.ANTIALIAS)
        self.img_help = ImageTk.PhotoImage(self.img_help)

        # help_button erstellen, platzieren und Funktion zuweisen
        self.button_help = customtkinter.CTkButton(master=self, image=self.img_help, fg_color=("grey45","grey5"),
                                                border_width=0, text="", takefocus=0,hover=False,
                                                width=48, corner_radius=0)

        self.button_help.pack()
        self.button_help.place(rely=0.01, relx=0.96)

        # Image für ProvaPi Logo
        self.img_logo = Image.open("mediaFiles/provapi_logo.png")
        self.img_logo = self.img_logo.resize((52, 52), Image.ANTIALIAS)
        self.img_logo = ImageTk.PhotoImage(self.img_logo)
        self.label_logo = customtkinter.CTkButton(master=self, image=self.img_logo, hover=False, border_width=0,
                                                  text="", takefocus=0, fg_color=("grey45", "grey5"), width=5,
                                                  corner_radius=0, height=5)
        self.label_logo.place(rely=0.003, relx=0.02)

        # ----------------------------------------------------------------------------------------------------------
        # Bilder für Delete und Add
        # ----------------------------------------------------------------------------------------------------------

        # Image für Add-Button
        self.img_add = Image.open("mediaFiles/add.png")
        self.img_add = self.img_add.resize((56, 56), Image.ANTIALIAS)
        self.img_add = ImageTk.PhotoImage(self.img_add)

        # Image für Delete-Button
        self.img_delete = Image.open("mediaFiles/delete.png")
        self.img_delete = self.img_delete.resize((56, 56), Image.ANTIALIAS)
        self.img_delete = ImageTk.PhotoImage(self.img_delete)

        # ----------------------------------------------------------------------------------------------------------
        # Tank-Liste
        # ----------------------------------------------------------------------------------------------------------

        # erstellt und platziert das Header-Label für Tank-Kennziffern
        label_tanklist = customtkinter.CTkLabel(master=self.frame_south, text='Kennziffern für Tanks:',
                                                text_font=('Segoe UI', 25),
                                                fg_color=None, bg_color=None, takefocus=0, width=350, height=60)
        label_tanklist.place(rely=0.08, relx=0.104, anchor=NW)

        # erstellt eine Listbox für die Tank-Kennziffern
        self.listbox_tank = tk.Listbox(self.frame_south, font=('Segoe UI Semilight', 20), takefocus=0)
        self.listbox_tank.config(yscrollcommand=scrollbar.set)
        self.listbox_tank.place(rely=0.2, relx=0.12, width=320, height=200, anchor=NW)

        # erstellt Entry für das Hinzufügen der Tank-Kennziffern
        lb_entry_tank = customtkinter.CTkEntry(master=self.frame_south, width=320, height=45,
                                               font=('Segoe UI Semilight', 20), corner_radius=8,
                                               fg_color=("grey70","white"), text_color=("white","grey10"), takefocus=0)
        lb_entry_tank.place(rely=0.61, relx=0.12, anchor=NW)

        # Add-Tank-Button erstellen und platzieren
        # Funktion 'self.insert()': Kennziffer der globalen 'tank_keys'-Liste, sowie der Listbox hinzufügen
        addbtn_tank = customtkinter.CTkButton(master=self.frame_south, image=self.img_add, fg_color=None,
                                              command=lambda: self.insert(self.listbox_tank, lb_entry_tank, tank_keys),
                                              takefocus=0, text="",
                                              width=50, hover_color=("grey90","grey10"), corner_radius=5)
        addbtn_tank.place(rely=0.5955, relx=0.375, width=64, height=64, anchor=NW)

        # Delete-Tank-Button erstellen und platzieren
        # Funktion 'self._delete_item()': Kennziffer aus der globalen 'tank_keys'-Liste, sowie der Listbox entfernen
        delbtn_tank = customtkinter.CTkButton(master=self.frame_south, image=self.img_delete, fg_color=None,
                                              command=lambda: self.delete_item(self.listbox_tank, tank_keys),
                                              takefocus=0, text="", hover_color=("grey90","grey10"), corner_radius=5)

        delbtn_tank.place(rely=0.2, relx=0.375, width=64, height=64, anchor=NW)

        # ----------------------------------------------------------------------------------------------------------
        # Leitung-Liste
        # ----------------------------------------------------------------------------------------------------------

        # erstellt und platziert das Header-Label für Leitung-Kennziffern
        label_leitunglist = customtkinter.CTkLabel(master=self.frame_south, text='Kennziffern für Leitungen:',
                                                   text_font=('Segoe UI', 25),
                                                   fg_color=None, bg_color=None, takefocus=0, width=380, height=60)
        label_leitunglist.place(rely=0.08, relx=0.545, anchor=NW)

        # erstellt eine Listbox für die Tank-Kennziffern
        self.listbox_leitung = tk.Listbox(self.frame_south, font=('Segoe UI Semilight', 20), takefocus=0)
        self.listbox_leitung.config(yscrollcommand=scrollbar.set)
        self.listbox_leitung.place(rely=0.2, relx=0.55, width=320, height=200, anchor=NW)

        # erstellt Entry für das Hinzufügen der Tank-Kennziffern
        lb_entry_leitung = customtkinter.CTkEntry(master=self.frame_south, width=320, height=45,
                                                  font=('Segoe UI Semilight', 20), corner_radius=8,
                                                  fg_color=("grey70","white"), text_color=("white","grey10"), takefocus=0)
        lb_entry_leitung.place(rely=0.61, relx=0.55, anchor=NW)

        # Add-leitung-Button erstellen und platzieren
        # Funktion 'self.insert()': Kennziffer der globalen 'leitung_keys'-Liste, sowie der Listbox hinzufügen
        addbtn_leitung = customtkinter.CTkButton(master=self.frame_south, image=self.img_add, fg_color=None,
                                                 command=lambda: self.insert(self.listbox_leitung, lb_entry_leitung,
                                                                             leitung_keys), takefocus=0,
                                                 border_width=0, text="",
                                                 hover_color=("grey90","grey10"), corner_radius=5)
        addbtn_leitung.place(rely=0.5955, relx=0.805, width=64, height=64, anchor=NW)

        # Delete-Leutung-Button erstellen und platzieren
        # Funktion 'self._delete_item()': Kennziffer aus der globalen 'leitung_keys'-Liste, sowie der Listbox entfernen
        delbtn_leitung = customtkinter.CTkButton(master=self.frame_south, image=self.img_delete, fg_color=None,
                                                 command=lambda: self.delete_item(self.listbox_leitung, leitung_keys),
                                                 takefocus=0,
                                                 border_width=0, text="", hover_color=("grey90","grey10"))
        delbtn_leitung.place(rely=0.2, relx=0.805, width=64, height=64, anchor=NW)

        # ----------------------------------------------------------------------------------------------------------
        # Allgemein und Funktionen
        # ----------------------------------------------------------------------------------------------------------

        # füllt beide Listboxen
        self.fill_list(self.listbox_tank, tank_keys)
        self.fill_list(self.listbox_leitung, leitung_keys)

        # Image für Back-Button
        self.img_back = Image.open("mediaFiles/back_button.png")
        self.img_back = self.img_back.resize((72, 72), Image.ANTIALIAS)
        self.img_back = ImageTk.PhotoImage(self.img_back)

        # Zurück-Button erstellen
        # Funktion 'self.back()': aktuelle Eingaben löschen und Startseite anzeigen
        self.button_back = customtkinter.CTkButton(master=self.frame_inner, image=self.img_back, fg_color=None,
                                                   command=lambda: self.back(lb_entry_tank, lb_entry_leitung),
                                                   takefocus=0, border_width=0, text="",
                                                   width=50, hover_color=("grey90","grey10"))

        self.button_back.place(rely=0.94, relx=0.04, relwidth=0.06, relheight=0.075, anchor=CENTER)

    def back(self, entrybox1, entrybox2):
        """leert Entries und zeigt Startseite an"""
        entrybox1.delete(0, END)
        entrybox1.insert(0, "")
        entrybox2.delete(0, END)
        entrybox2.insert(0, "")
        self.controller.show_frame("StartPage")

    def insert(self, listbox, entrybox, key_list):
        """Kennziffer der globalen '###_keys'-Liste, sowie der Listbox hinzufügen"""
        if listbox == self.listbox_tank:
            keys.add_tank_key(entrybox.get())
        elif listbox == self.listbox_leitung:
            keys.add_leitung_key(entrybox.get())
        entrybox.delete(0, END)
        entrybox.insert(0, "")
        self.fill_list(listbox, key_list)

    def delete_item(self, listbox, key_list):
        """Kennziffer aus der globalen '###_keys'-Liste, sowie der Listbox entfernen"""
        index = listbox.curselection()
        item_listbox = listbox.get(index)
        listbox.delete(index)
        for item in key_list:
            if item == item_listbox:
                if listbox == self.listbox_tank:
                    keys.remove_tank_key(item)
                elif listbox == self.listbox_leitung:
                    keys.remove_leitung_key(item)
                self.fill_list(listbox, key_list)

    def fill_list(self, listbox, key_list):
        """erstmaliges Befüllen der Listbox mit den keys aus den globalen Variablen"""
        global tank_keys, leitung_keys
        tank_keys = keys.get_tank_keys()
        leitung_keys = keys.get_leitung_keys()
        listbox.delete(0, 'end')
        i = 0
        for key in key_list:
            listbox.insert(i, key)
            i += 1


# ----------------------------------------------------------------------------------------------------------
# ENDE der Klasse ConfigFrame
# ----------------------------------------------------------------------------------------------------------

def stop_thread():
    provapi.start_page.running = False
    provapi.start_page.main_animation_running = False
    provapi.start_page.tank_animation_running = False
    provapi.start_page.leitung_animation_running = False
    provapi.start_page.done = True
    provapi.destroy()
    os._exit(0)

if __name__ == "__main__":
    provapi = ProvaPiApp()
    provapi.protocol("WM_DELETE_WINDOW", stop_thread)
    provapi.mainloop()