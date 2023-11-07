"""
[create a customContainer]
create a customizer file, convert mp3 to ogg, add custom cover and create a manifest
"""
# module buitl-in
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import (
    askokcancel,
    askretrycancel,
    showerror,
    showinfo,
    showwarning,
)
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter.constants import DISABLED, NORMAL
from io import BytesIO
import uuid

# third-party module
from PIL import Image
from pydub import AudioSegment
from mutagen import id3
from mutagen.mp3 import MP3

ALLOWED_FILE_TYPES = [("MP3 file", ".mp3")]
with open(os.getcwd() + "/Customizertemplate.txt", "r", encoding="UTF-8") as f:
    customizer_template = f.read()
CUSTOMIZER_TEMPLATE_END = """

//Don't modify anything past this point.

??""".replace(
    "?", "}"
)
class Main:
    """main class for the program"""

    def __init__(self) -> None:
        self.music_files = ""
        self.uuid_arg1 : str
        self.uuid_arg2 : str
        self.name_arg : str

    def music_file_selection(self):
        """
        Ask the user to select multiple music files (max: 100; type: MP3).
        """
        while True:
            self.music_files = askopenfilenames(
                title="choose your music files", filetypes=ALLOWED_FILE_TYPES
            )
            if self.music_files == "":
                showerror("error", "you didn't provide any music files ")
                process_button["state"] = DISABLED
                break
            if len(self.music_files) > 100:
                showerror(
                    "error",
                    "you provided too many music"+
                    f" files (max : 100, provided {len(self.music_files)}",
                )
                process_button["state"] = DISABLED
            else:
                process_button["state"] = NORMAL
                break


    @staticmethod
    def name_verif():
        """Verifies if the name is valid.

        The function checks if the name contains any of the following characters: 
        '{', '}', '\\', '?', '!'.
        If the name contains any of these characters, it is considered invalid.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if (
            "{" in PackNameField.get()
            or "}" in PackNameField.get()
            or "\\" in PackNameField.get()
            or "?" in PackNameField.get()
            or "!" in PackNameField.get()
        ):
            return False
        return True

    @staticmethod
    def dir_reate(save_directory):
        """
        Create all the necessary directories for the custom music container.

        Args:
        - save_directory (str): The path to the directory where 
        the custom music container will be saved.

        Returns:
        - str: The path to the created CustomMusicContainer directory.
        """
        try:
            os.mkdir(save_directory + "/CustomMusicContainer")
            os.mkdir(save_directory + "/CustomMusicContainer/custom_songs")
            os.mkdir(save_directory + "/CustomMusicContainer/custom_covers")
            return save_directory + "/CustomMusicContainer"
        except FileExistsError:
            n = 1
            while True:
                try:
                    os.mkdir(save_directory + f"/CustomMusicContainer({n})")
                    os.mkdir(save_directory + f"/CustomMusicContainer({n})/custom_songs")
                    os.mkdir(save_directory + f"/CustomMusicContainer({n})/custom_covers")
                    return save_directory + f"/CustomMusicContainer({n})"
                except FileExistsError:
                    n += 1


    def verif(self):
        """
        Verify if the pack argument are valid (pack name and files chosen).
        
        Returns:
        bool: True if the pack argument are valid, False otherwise.
        """
        if not self.name_verif:
            showerror("error", "the Pack Name is not a valide")
            return False
        if self.music_files == "":
            showwarning("no files chosen", "please choose your music files first")
            return False
        return True


    def get_args(self):
        """
        Get the arguments for creating a custom music container.
        If PackNameField is empty, the default name "Custom Music Container" is used.
        If DefaultUUID is selected, two default UUIDs are used.
        Otherwise, two random UUIDs are generated.
        """
        if PackNameField.get() == "":
            self.name_arg = "Custom Music Container"
        else:
            self.name_arg = PackNameField.get()
        if DefaultUUID.get():
            self.uuid_arg1 = "f087e50a-6508-11ec-90d6-0242ac120003"
            self.uuid_arg2 = "f087e6c2-6508-11ec-90d6-0242ac120003"
        else:
            self.uuid_arg1 = uuid.uuid4()
            self.uuid_arg2 = uuid.uuid4()


    def process(self):
        """Create a custom music container by processing the music files 
        and generating the necessary files and directories.
        
        Returns:
        -1 if verification fails, "NO DIR ERR" if no directory is chosen, 
        and a message box if the pack is created successfully.
        """
        self.get_args()
        prog1["value"] = 0
        if not self.verif:
            return -1
        save_directory = askdirectory(title="save directory", mustexist=True)
        while save_directory == "":
            if not askretrycancel("no directory chosen", "please choose a directory"):
                return "NO DIR ERR"
            save_directory = askdirectory(title="save directory", mustexist=True)
        container_path = self.dir_reate(save_directory)
        with Image.open(os.getcwd() + "/pack_icon.png") as i:
            i.save(container_path + "/pack_icon.png")
        with open(
            save_directory + "/CustomMusicContainer/manifest.json", "x", encoding="UTF-8"
        ) as man:
            man.write(
                f"""?
        "format_version": 2,
        "header": ?
        "description": "Provides custom song, cover, and property files for the music player. Apply this above the music player resource pack.",
        "name": "{self.name_arg}",
        "uuid": "{self.uuid_arg1}",
        "version": [1, 0, 1],
        "min_engine_version": [1, 13, 0]
    !,
    "modules": [
        ?
            "description": "Provides custom song, cover, and property files for the music player. Apply this above the music player resource pack.",
            "type": "resources",
            "uuid": "{self.uuid_arg2}",
            "version": [1, 0, 1]
        !
    ]
    !""".replace(
                    "?", "{"
                ).replace(
                    "!", "}"
                )
            )
        customizer = customizer_template
        n = 0
        top.deiconify()
        top.grab_set()
        top.update()
        app.update()
        prog1["maximum"] = len(self.music_files)
        for item in self.music_files:
            n += 1
            audio = MP3(item)
            try:
                title = audio["TIT2"][0]
            except KeyError:
                print(f"music n°{n} as no title")
                title = "unknow"
            try:
                artist = audio["TPE1"][0]
            except KeyError:
                print(f"music n°{n} named : {title} as no artist")
                artist = "unknow"
            customizer += f"""

    "$custom_song_{n}_title": "{title}",
    "$custom_song_{n}_duration": "{str(int(round(audio.info.length//60, None)))+"m" + str(int(round(audio.info.length%60, None)))+"s"}",
    "$custom_song_{n}_duration_in_seconds": {round(audio.info.length, None)},
    "$custom_song_{n}_artist": "{artist}","""
            try:
                with Image.open(BytesIO(id3.ID3(item).get("APIC:").data)) as cover:
                    cover.save(
                        container_path + f"/custom_covers/cover{n}.png", bitmap_format="png"
                    )
            except AttributeError:
                print(f"music n°{n} named : {title} as no cover")
            AudioSegment.from_mp3(item).export(
                container_path + f"/custom_songs/custom{n}.ogg", format="ogg"
            )
            prog1["value"] += 1
            top.update()
            app.update()
        if n != 100:
            for z in range(n + 1, 101):
                customizer += f"""

    "$custom_song_{z}_title": "",
    "$custom_song_{z}_duration": "",
    "$custom_song_{z}_duration_in_seconds": 0,
    "$custom_song_{z}_artist": "","""
                top.update()
                app.update()
        customizer = customizer[0:-1]
        customizer += CUSTOMIZER_TEMPLATE_END
        with open(container_path + "/Customizer.txt", "x", encoding="UTF-8") as cust:
            cust.write(customizer)
        top.grab_release()
        top.withdraw()
        return showinfo("pack created", "the pack has been created with sucess !")

    @staticmethod
    def menu_state(state):
        """
        Set the state of various GUI elements in the menu.

        Args:
            state (str): The state to set the GUI elements to. 
            Must be either "normal" or "disabled".

        Raises:
            ValueError: If the state argument is not "normal" or "disabled".
        """
        if state not in ("normal", "disabled"):
            raise ValueError
        SelectFileButton["state"] = state
        LabelText1["state"] = state
        PackNameField["state"] = state
        InterogationButton["state"] = state
        DefaultUUIDcheck["state"] = state
        process_button["state"] = state


def on_closing():
    """ask to the user if he want to quit"""
    if askokcancel("Quiter", "voulez-vous quitter ?"):
        app.destroy()
        exit()

def help_message():
    """show a info message"""
    showinfo(
        "advice",
        "you can't use ? ! { } \\ \nif you left the entry empty the default name will be used",
    )

main = Main()

app = tk.Tk()
top = tk.Tk("Procesing")
top.resizable(False, False)
top.geometry("250x50+500+100")
top.withdraw()
app.minsize(250, 250)
app.maxsize(500, 500)
app.geometry("500x500+500+100")
app.columnconfigure(0, weight=1)
app.columnconfigure(4, weight=1)


PackName = tk.StringVar()
DefaultUUID = tk.BooleanVar()
SelectFileButton = tk.Button(app, text="select music files", command=main.music_file_selection)
LabelText1 = tk.Label(app, text="name of the pack")
PackNameField = tk.Entry(app, textvariable=PackName)
InterogationButton = tk.Button(app, text="?", command=help_message)
DefaultUUIDcheck = tk.Checkbutton(
    app, text="use default UUID ?", variable=DefaultUUID, onvalue=True, offvalue=False
)
process_button = tk.Button(app, text="process", state=DISABLED, command=main.process)
tk.Label(top, text="your pack is in progress").grid()
prog1 = ttk.Progressbar(
    top, orient="horizontal", maximum=100, mode="determinate", length=100
)
prog1.grid()

SelectFileButton.grid(column=1, row=1, columnspan=2)
LabelText1.grid(column=1, row=2)
PackNameField.grid(column=2, row=2)
InterogationButton.grid(column=3, row=2)
DefaultUUIDcheck.grid(column=1, row=3, columnspan=2)
process_button.grid(column=1, row=4, columnspan=2)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
top.mainloop()
