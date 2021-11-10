import os
import subprocess
import tkinter as tk
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

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconbitmap('./img/icon.ico')
        self.winfo_toplevel().title("EZ Flash SD Runner v0.1")

        if not os.path.exists("./rom"):
            os.makedirs("rom")

        rootdir = filedialog.askdirectory()

        if not os.path.exists("./visualboyadvance.exe"):
            messagebox.showinfo("You Fool",
                                "Could not find VisualBoyAdvance.exe!\n" \
                                "Ensure the file is present alongside this " \
                                "script, otherwise it won't work.")
            self.CloseApp()

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

        gamelist.bind('<Double-Button-1>', lambda event, arg1=games, arg2=rootdir: self.OnSelect(event, arg1, arg2))

        for frame in [topframe, middleframe, bottomframe]:
            frame.pack(expand=True, fill='both')

        toplabel.pack()
        bottomlabel.pack()
        gamelist.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    def CheckForSaveData(self, filename, root):
        if os.path.exists(os.path.join(root, "SYSTEM", "SAVER")):
            possible_sav_path = os.path.join(root, "SYSTEM", "SAVER", f"{filename}.sav")
        else:
            possible_sav_path = os.path.join(root, "SAVER", f"{filename}.sav")
        if os.path.exists(possible_sav_path):
            return possible_sav_path
        else:
            return None

    def OnSelect(self, event, games, rootdir):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        savedata = self.CheckForSaveData(value, rootdir)
        try:
            path = games[value]
            self.RunGame(value, path, savedata)
        except KeyError:
            self.CloseApp()

    def RunGame(self, game, gamepath, savepath):
        print(f"Booting {game}...")
        if os.name == "nt":
            execname = "visualboyadvance.exe"
        else:
            execname = "visualboyadvance-m"

        copy(gamepath, "./rom")
        copy(savepath, "./rom")

        path = f"./rom/{game}.gba"

        try:
            process = subprocess.call([execname, path])
        except:
            print("Error")

        print("Game closed, copying savedata back...")
        copy(f"./rom/{game}.sav", savepath)

        answer = messagebox.askyesno(title="Exiting",
                          message="Would you like to clear the copied ROM " \
                          "and save data?\n\n" \
                          "This will not delete your data from the SD card, " \
                          "only the temporary copy for use in the emulator.")
        if answer:
            for subdir, dirs, files in os.walk("./rom"):
                for file in files:
                    os.remove(os.path.join("./rom", file))
        messagebox.showinfo("Thank You", "Done. Have a nice day!")
        self.quit()

if __name__ == "__main__":
    app = EZF_Runner()
    app.mainloop()
