

import tkinter as tk
import datetime
import time
import threading
import pygame
from tkinter import filedialog
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hunde-Spaziergangsprogramm")
        self.label_hour = tk.Label(self, text="Stunde:")
        self.label_hour.pack()
        self.entry_hour = tk.Entry(self)
        self.entry_hour.pack()
        self.label_minute = tk.Label(self, text="Minute:")
        self.label_minute.pack()
        self.entry_minute = tk.Entry(self)
        self.entry_minute.pack()
        self.label_duration = tk.Label(self, text="Dauer (in Minuten):")
        self.label_duration.pack()
        self.entry_duration = tk.Entry(self)
        self.entry_duration.pack()
        self.button_select_start_sound = tk.Button(self, text="Start-Ton wählen", command=self.select_start_sound)
        self.button_select_start_sound.pack()
        self.label_selected_start_sound = tk.Label(self, text="Ausgewählter Start-Ton:")
        self.label_selected_start_sound.pack()
        self.label_selected_start_sound_file = tk.Label(self, text="")
        self.label_selected_start_sound_file.pack()
        self.button_select_stop_sound = tk.Button(self, text="Stop-Ton wählen", command=self.select_stop_sound)
        self.button_select_stop_sound.pack()
        self.label_selected_stop_sound = tk.Label(self, text="Ausgewählter Stop-Ton:")
        self.label_selected_stop_sound.pack()
        self.label_selected_stop_sound_file = tk.Label(self, text="")
        self.label_selected_stop_sound_file.pack()
        
        self.button_start = tk.Button(self, text="Spaziergang starten", command=self.start_walk)
        self.button_start.pack()
        self.button_stop = tk.Button(self, text="Spaziergang abbrechen", command=self.stop_walk)
        self.button_stop.pack()

        self.button_select_image = tk.Button(self, text="Bild wählen", command=self.select_image)
        self.button_select_image.pack()
        self.image_label = tk.Label(self)
        self.image_label.pack()
        self.dog_images = [
            ImageTk.PhotoImage(Image.open("Hundebild1.jpg")),
            ImageTk.PhotoImage(Image.open("Hundebild2.jpg")),
            ImageTk.PhotoImage(Image.open("Hundebild3.jpg"))
        ]
        self.selected_image_index = 0

    def select_image(self):
        selected_index = self.selected_image_index
        selected_index += 1
        if selected_index >= len(self.dog_images):
            selected_index = 0
        self.selected_image_index = selected_index
        self.image_label.config(image=self.dog_images[selected_index])

    def select_start_sound(self):
        sound_file = filedialog.askopenfilename(title="Start-Ton auswählen", filetypes=(("Sounddateien", "*.wav;*.mp3"), ("Alle Dateien", "*.*")))
        self.selected_start_sound_file = sound_file
        self.label_selected_start_sound_file.config(text=sound_file)

    def select_stop_sound(self):
        sound_file = filedialog.askopenfilename(title="Stop-Ton auswählen", filetypes=(("Sounddateien", "*.wav;*.mp3"), ("Alle Dateien", "*.*")))
        self.selected_stop_sound_file = sound_file
        self.label_selected_stop_sound_file.config(text=sound_file)

    def start_walk(self):
        current_time = datetime.datetime.now().time()
        walk_time = datetime.time(int(self.entry_hour.get()), int(self.entry_minute.get()))
        walk_duration = int(self.entry_duration.get()) * 60
        if current_time >= walk_time:
            start_delay = datetime.datetime.combine(datetime.date.today(), walk_time) + datetime.timedelta(days=1) - datetime.datetime.now()
        else:
            start_delay = datetime.datetime.combine(datetime.date.today(), walk_time) - datetime.datetime.now()
        threading.Timer(start_delay.total_seconds(), self.walk_dogs, args=(walk_duration, self.selected_start_sound_file, self.selected_stop_sound_file)).start()

    def walk_dogs(self, duration, start_sound_file, stop_sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(start_sound_file)
        pygame.mixer.music.play()
        print("Starte den Spaziergang mit den Hunden...")
        time.sleep(duration)
        pygame.mixer.music.load(stop_sound_file)
        pygame.mixer.music.play()
        print("Spaziergang beendet!")

    def stop_walk(self):
        pygame.mixer.music.stop()
        print("Spaziergang abgebrochen")

if __name__ == "__main__":
    app = Application()
    app.mainloop()



