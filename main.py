import os, subprocess, configparser, tempfile
import tkinter as tk
from datetime import datetime
from shutil import copy2 as copy
from tkinter import filedialog, messagebox

class EZF_Runner(tk.Tk):
    def CloseApp(self):
        print("Exiting...")
        self.destroy()
        self.quit()

    def FindGames(self, rootdir):
        allowed_extensions = ("gba")
        games = {}

        print("Finding games...")
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.lower().endswith(allowed_extensions):
                    games[file[:-4]] = os.path.join(subdir, file)
        return games

    def BackupFiles(self, type, dir):
        time = datetime.now().strftime('%b-%d-%Y')
        savedir = filedialog.askdirectory()

        timedir = os.path.join(savedir, time)
        if not os.path.exists(timedir):
            os.makedirs(timedir)
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                file = os.path.join(dir, file)
                copy(file, timedir)
        messagebox.showinfo("Done", f"{type.upper()} backup complete")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconbitmap('./img/icon.ico')
        self.winfo_toplevel().title("EZ Flash SD Runner v0.1")

        config = configparser.ConfigParser()
        config.read("settings.ini")
        emulator = config["settings"]["emulator_path"]

        if not os.path.exists(emulator):
            messagebox.showinfo("You Fool",
                                "Could not find emulator!\n" \
                                "Ensure the path to the executable is " \
                                "defined in settings.ini, otherwise " \
                                "it won't work.")
            self.CloseApp()

        rootdir = filedialog.askdirectory()
        games = self.FindGames(rootdir)

        topframe = tk.Frame(self, width=60, relief="raised", borderwidth=2)
        middleframe = tk.Frame(self)
        bottomframe = tk.Frame(self)

        toplabel = tk.Label(topframe, text="Double-click a game:")
        gamelist = tk.Listbox(middleframe, width=60, height=35)
        bottomlabel = tk.Label(bottomframe, text="EZ Flash SD Runner v0.1 - by dj505")
        scrollbar = tk.Scrollbar(middleframe)

        for game in sorted(games):
            gamelist.insert(tk.END, game)
        if len(games) < 1:
            gamelist.insert(tk.END, "No games found. Double click me to exit.")

        gamelist.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = gamelist.yview)

        gamelist.bind('<Double-Button-1>', lambda event, arg1=games,
                      arg2=rootdir, arg3=emulator: self.OnSelect(event, arg1,
                                                                 arg2, arg3))

        for frame in [topframe, middleframe, bottomframe]:
            frame.pack(expand=True, fill="both")

        svbackupbtn = tk.Button(bottomframe, text="Backup Saves", width=40,
                      command=lambda : self.BackupFiles("save", self.GetSaveDir(rootdir)))

        toplabel.pack()
        svbackupbtn.pack(expand=True)

        bottomlabel.pack()
        gamelist.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        gamelist.select_set(0)
        gamelist.focus_set()

    def CheckForSaveData(self, filename, root):
        possible_sav_path = os.path.join(root, self.GetSaveDir(root), f"{filename}.sav")
        if os.path.exists(possible_sav_path):
            return possible_sav_path
        else:
            return None

    def GetSaveDir(self, root):
        if os.path.exists(os.path.join(root, "SYSTEM", "SAVER")):
            print("Save location is SYSTEM/SAVER")
            return os.path.join(root, "SYSTEM", "SAVER")
        else:
            print("Save location is SAVER")
            return os.path.join(root, "SAVER")

    def OnSelect(self, event, games, rootdir, emulatorpath):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        savedata = self.CheckForSaveData(value, rootdir)
        try:
            path = games[value]
            self.RunGame(value, path, savedata, emulatorpath)
        except KeyError:
            self.CloseApp()

    def RunGame(self, game, gamepath, savepath, emulator):
        print(f"Booting {game}...")

        tempdir = tempfile.TemporaryDirectory()
        temp = tempdir.name
        print(f"Using temporary directory {temp}")

        if os.name == "nt":
            if not emulator.endswith(".exe"):
                emulator = emulator + ".exe" # probably unnecessary,
            execname = emulator              # just to be safe, idk
        else:
            execname = emulator

        copy(gamepath, temp)
        if savepath != None:
            copy(savepath, temp)

        path = os.path.join(temp, f"{game}.gba")

        try:
            process = subprocess.call([execname, path])
        except:
            print("Error")

        print("Game closed, copying savedata back...")
        copy(os.path.join(temp, f"{game}.sav"), savepath)

        messagebox.showinfo("Thank You", "Done. Have a nice day!")
        self.quit()

if __name__ == "__main__":
    app = EZF_Runner()
    app.mainloop()
