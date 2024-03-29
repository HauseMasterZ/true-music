import os

if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.lock")
):
    import sys

    sys.exit(0)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.lock"), "w"):
    pass
import json
import secrets
import threading
from tkinter import (
    CENTER,
    DISABLED,
    END,
    GROOVE,
    HORIZONTAL,
    NORMAL,
    RIDGE,
    SUNKEN,
    VERTICAL,
    Button,
    E,
    Entry,
    Label,
    PhotoImage,
    StringVar,
    Text,
    Tk,
    Toplevel,
    W,
    filedialog,
    messagebox,
    ttk,
)

import PIL.Image
import pyglet
import pystray
from pynput import keyboard
is_windows = os.name == "nt"

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text="widget info"):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def changeTheme() -> None:
    """
    Changes the theme of the application between light and dark mode.

    This function updates the background color, foreground color, and images of various widgets to match the selected theme.
    """
    global shuffle_flag
    root.focus()
    if theme_btn.cget("text") == "Theme: Dark":
        root.configure(background="White")
        arrow_lbl.configure(background="White", foreground="Black")
        title.configure(background="White", foreground="Black")
        theme_btn.configure(
            text="Theme: Light",
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="gray",
        )
        hotkey_btn.configure(
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="gray",
        )
        directory_box.configure(background="#F5F5F5", foreground="Black")
        volume_icon.configure(image=volume_image_inv, background="White")
        play_pause_btn.configure(
            image=pause_image_inv
        ) if player.playing else play_pause_btn.configure(image=play_image_inv)
        play_pause_btn.configure(background="White", activebackground="White")
        forward_btn.configure(image=forward_image_inv)
        previous_btn.configure(image=previous_image_inv)
        date_modified_btn.configure(
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="gray",
        )
        refresh_btn.configure(
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="gray",
        )
        previous_btn.configure(
            background="White", borderwidth=0, activebackground="#b3afaf"
        )
        forward_btn.configure(background="White", activebackground="#b3afaf")
        style.configure("myStyle.Horizontal.TScale", background="White")
        style.configure("myStyle.Vertical.TScale", background="White")
        remember_btn.configure(
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="#575655",
        )
        now_playing.configure(background="White", foreground="Black")
        seek_of_music.configure(background="White", foreground="Black")
        length_of_music.configure(background="White", foreground="Black")
        volume_val.configure(background="White", foreground="Black")
        clear_btn.configure(
            background="White",
            foreground="Black",
            activebackground="White",
            activeforeground="#575655",
        )
        autoplay_btn.configure(
            background="White", foreground="Black", activebackground="White"
        )
        always_on_top_btn.configure(
            background="White", foreground="Black", activebackground="White"
        )
        repeat_btn.configure(
            background="White", foreground="Black", activebackground="White"
        )
        if search_box.get() != "Press Enter To Search":
            search_box.configure(background="#F5F5F5", foreground="#16161d")
        else:
            search_box.configure(background="#F5F5F5")
        selectDirectory.configure(
            background="White", foreground="Black", activebackground="White"
        )
        trueShuffle_btn.configure(
            background="White",
            foreground="Black" if not shuffle_flag else "#2dd128",
            activebackground="White",
        )
    else:
        date_modified_btn.configure(
            background="#121212",
            foreground="White",
            activebackground="#121212",
            activeforeground="Grey",
        )
        refresh_btn.configure(
            background="#121212",
            foreground="White",
            activebackground="#121212",
            activeforeground="Grey",
        )
        root.configure(background="#121212")
        arrow_lbl.configure(background="#121212", foreground="White")
        if search_box.get() != "Press Enter To Search":
            search_box.configure(background="#3f3f40", foreground="White")
        else:
            search_box.configure(background="#3f3f40")
        title.configure(background="#121212", foreground="White")
        theme_btn.configure(
            text="Theme: Dark",
            background="#121212",
            foreground="white",
            activebackground="#121212",
            activeforeground="gray",
        )
        hotkey_btn.configure(
            background="#121212",
            foreground="white",
            activebackground="#121212",
            activeforeground="gray",
        )
        directory_box.configure(background="#0D0901", foreground="white")
        volume_icon.configure(image=volume_image)
        play_pause_btn.configure(
            image=pause_image
        ) if player.playing else play_pause_btn.configure(image=play_image)
        play_pause_btn.configure(background="#121212", activebackground="#121212")
        forward_btn.configure(image=forward_image)
        previous_btn.configure(image=previous_image)
        previous_btn.configure(
            background="#121212", activebackground="#121212", borderwidth=0
        )
        forward_btn.configure(
            background="#121212", activebackground="#121212", borderwidth=0
        )
        style.configure("myStyle.Horizontal.TScale", background="#121212")
        remember_btn.configure(
            background="#121212",
            foreground="White",
            activebackground="#121212",
            activeforeground="Grey",
        )
        clear_btn.configure(
            background="#121212",
            foreground="White",
            activebackground="#121212",
            activeforeground="Grey",
        )
        style.configure("myStyle.Vertical.TScale", background="#121212")
        now_playing.configure(background="#121212", foreground="White")
        seek_of_music.configure(background="#121212", foreground="White")
        length_of_music.configure(background="#121212", foreground="White")
        volume_val.configure(background="#121212", foreground="White")
        autoplay_btn.configure(
            background="#121212", foreground="White", activebackground="#121212"
        )
        always_on_top_btn.configure(
            background="#121212", foreground="White", activebackground="#121212"
        )
        repeat_btn.configure(
            background="#121212", foreground="White", activebackground="#121212"
        )
        selectDirectory.configure(
            background="#121212", foreground="White", activebackground="#121212"
        )
        trueShuffle_btn.configure(
            background="#121212",
            foreground="White" if not shuffle_flag else "#2dd128",
            activebackground="#121212",
        )


pyglet.options["audio"] = ("openal", "pulse", "xaudio2", "directsound", "silent")

# Audio Video
audio_set = (".m4a", ".mp3", ".aac", ".flac", ".wav", ".ogg", ".wma")
video_set = {"webm", "flv", "mp4", "mov", "wmv"}

# Variables
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
Directory = ""
dir_musics = []
number_of_files = 0
remember_flag = False
secretsGenerator = secrets.SystemRandom()
on_close = False
auto_play_flag = True
repeat_flag = False
always_on_top_flag = False
shuffle_flag = True
first_flag = True
date_modified_flag = False
clear_flag = False
hotkey_flag = False
notification_flag = False
file_name = ""
alphabetical_list = []
date_modified_list = []
player = pyglet.media.Player()
playing_index = 0
date_modified_cnt = 0
corrupt_flag = False
prev_corrupt_flag = False
played = set()

if is_windows:
    from win10toast import ToastNotifier

    toaster = ToastNotifier()
else:
    from plyer import notification

def secure_generator(prev_flag: bool = False, search_file: str = None) -> str:
    """
    Generates a secure random number to select a music file.

    This function generates a random number using the `secretsGenerator` object, which is used to select a music file to play.
    If the shuffle flag is set to True, the function ensures that the same file is not played twice in a row.
    If the search_file parameter is provided, the function loads the specified file instead of selecting a random file.
    If an error occurs while loading the file, the function sets the `corrupt_flag` variable to True and displays an error message.

    Args:
        prev_flag (bool, optional): A flag indicating whether to play the previous file. Defaults to False.
        search_file (str, optional): The path of the file to play. Defaults to None.

    Returns:
        str: The path of the selected music file.
    """
    global number_of_files, first_flag, playing_index, corrupt_flag, prev_corrupt_flag, shuffle_flag, played
    if search_file is None:
        if shuffle_flag:
            secure_choice = secretsGenerator.randint(0, number_of_files - 1)
            played = set() if len(played) >= number_of_files else played
            retries = 0
            while (
                secure_choice in played
                or secure_choice == playing_index
                and number_of_files > 1
                and retries < 10
            ):
                secure_choice = secretsGenerator.randint(0, number_of_files - 1)
                retries += 1
            played.add(secure_choice)
        else:
            secure_choice = (
                (max(playing_index - 1, 0) if prev_flag else playing_index + 1)
                if not first_flag
                else playing_index
            )
            played.clear()
    try:
        if search_file == None:
            media = pyglet.media.load(dir_musics[secure_choice], streaming=True)
        else:
            media = pyglet.media.load(search_file, streaming=True)
        corrupt_flag = False
    except Exception as e:
        print(e)
        messagebox.showerror(
            "Invalid Media Found", "Some if not all media files are corrupted"
        )
        clearDirectory()
        directory_box.config(state=NORMAL)
        directory_box.delete("1.0", END)
        directory_box.config(state=DISABLED)
        corrupt_flag = True
        prev_corrupt_flag = True
        player.next_source()
        return None
    player.delete()
    try:
        player.queue(media)
    except:
        return None
    if not prev_corrupt_flag and not first_flag:
        player.next_source()
    else:
        prev_corrupt_flag = False
    if search_file == None:
        playing_index = secure_choice
        return os.path.basename(dir_musics[secure_choice])
    else:
        playing_index = dir_musics.index(search_file)
        return os.path.basename(search_file)


def autoPlay() -> None:
    """
    Toggles the auto-play feature on and off. If auto-play is turned on, the function will also check if repeat is on and
    call the autoRepeat function. The function updates the tray icon menu and the autoplay button text accordingly.
    """
    global auto_play_flag, repeat_flag
    root.focus()
    autoplay_index = menu_items.index(
        next(item for item in menu_items if "Autoplay" in item.text)
    )
    if auto_play_flag:
        auto_play_flag = False
        menu_items[autoplay_index] = pystray.MenuItem("Autoplay: Off", on_click)
        autoplay_btn.config(text="Autoplay: Disabled", relief=RIDGE)
    else:
        auto_play_flag = True
        menu_items[autoplay_index] = pystray.MenuItem("Autoplay: On", on_click)
        autoplay_btn.config(text="Autoplay: Enabled", relief=SUNKEN)
        if repeat_flag:
            autoRepeat()
    tray_icon.menu = pystray.Menu(*menu_items)


def alwaysOnTop() -> None:
    """
    Toggles the "always on top" flag for the root window. If the flag is currently
    set, it will be unset, and vice versa. Updates the text and relief of the
    "always on top" button accordingly.
    """
    global always_on_top_flag
    root.focus()
    if always_on_top_flag:
        root.attributes("-topmost", False)
        always_on_top_flag = False
        always_on_top_btn.configure(text="Always On Top: Disabled", relief=RIDGE)
    else:
        root.attributes("-topmost", True)
        always_on_top_flag = True
        always_on_top_btn.configure(text="Always On Top: Enabled", relief=SUNKEN)


def trueShuffle() -> None:
    """
    Toggles the true shuffle feature on or off. If true shuffle is turned on, the menu item and button text will be updated
    to reflect this. If the date modified flag is set, the date modified button action will be called. The tray icon menu
    will also be updated to reflect the new state of the true shuffle feature.
    """
    global shuffle_flag, date_modified_flag
    root.focus()
    shuffle_index = menu_items.index(
        next(item for item in menu_items if "True Shuffle" in item.text)
    )
    if shuffle_flag:
        shuffle_flag = False
        menu_items[shuffle_index] = pystray.MenuItem("True Shuffle: Off", on_click)
        trueShuffle_btn.configure(
            text="True Shuffle: Off",
            relief=RIDGE,
            foreground="White" if theme_btn.cget("text") == "Theme: Dark" else "Black",
        )
    else:
        shuffle_flag = True
        menu_items[shuffle_index] = pystray.MenuItem("True Shuffle: On", on_click)
        trueShuffle_btn.configure(
            text="True Shuffle: On", relief=SUNKEN, foreground="#2dd128"
        )
        if date_modified_flag:
            date_modified_btn_action()
    tray_icon.menu = pystray.Menu(*menu_items)


def autoRepeat() -> None:
    """
    Toggles the repeat flag and updates the UI accordingly. If auto play is enabled, calls autoPlay().

    :return: None
    """
    global repeat_flag, auto_play_flag
    root.focus()
    repeat_index = menu_items.index(
        next(item for item in menu_items if "Repeat" in item.text)
    )
    if repeat_flag:
        repeat_flag = False
        menu_items[repeat_index] = pystray.MenuItem("Repeat: Off", on_click)
        repeat_btn.configure(text="Repeat: Disabled", relief=RIDGE)
    else:
        repeat_flag = True
        menu_items[repeat_index] = pystray.MenuItem("Repeat: On", on_click)
        repeat_btn.configure(text="Repeat: Enabled", relief=SUNKEN)
        if auto_play_flag:
            autoPlay()
    tray_icon.menu = pystray.Menu(*menu_items)


def get_all_files(folder_path: str) -> tuple:
    """
    Returns a tuple containing a list of all audio files in the given folder path and its subdirectories,
    and the total number of audio files found.

    Args:
    - folder_path (str): The path of the folder to search for audio files.

    Returns:
    - tuple: A tuple containing a list of all audio files in the given folder path and its subdirectories,
    and the total number of audio files found. If the function encounters a PermissionError while searching
    for files, it returns an empty list and -1 as the file count.
    """
    global on_close, clear_flag
    all_files = []
    file_count = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if clear_flag:
                    return [], 0
                if file.endswith(audio_set):
                    all_files.append(os.path.join(root, file))
                    file_count += 1
    except PermissionError:
        return [], -1
    return all_files, file_count


def openFilePicker() -> None:
    """
    Opens a file dialog to select a directory and loads music files from the selected directory.
    If the selected directory already exists, displays a warning message.
    """
    global dir_musics, Directory, clear_flag, first_flag
    if first_flag:
        now_playing.configure(text="Now Playing: Please Wait...")
    Directory = filedialog.askdirectory(title="Select Directory")
    Directory += "/"
    if Directory != "/" and Directory in directory_box.get("1.0", "end-1c"):
        messagebox.showwarning(
            "Existing Directory",
            "Directory Already Exists. Please Select Another Directory.",
        )
    elif Directory != "/":
        load_music_thread = threading.Thread(target=loadMusicThread)
        load_music_thread.daemon = True
        load_music_thread.start()
        clear_flag = False
        played.clear()
        return
    if first_flag:
        now_playing.configure(text="Now Playing: ")


def merge_sorted_lists(
    list1: list[str], list2: list[str], date: bool = False
) -> list[str]:
    """
    Merges two sorted lists of strings into a single sorted list.

    Args:
        list1 (list[str]): The first sorted list of strings.
        list2 (list[str]): The second sorted list of strings.
        date (bool, optional): If True, the function will sort the lists based on the creation time of the files
        that the strings represent. Defaults to False.

    Returns:
        list[str]: A single sorted list of strings that contains all the elements from list1 and list2.
    """
    merged_list = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if not date:
            if list1[i] < list2[j]:
                merged_list.append(list1[i])
                i += 1
            else:
                merged_list.append(list2[j])
                j += 1
        else:
            file_path1 = list1[i].split("#|#")[1]
            file_path2 = list2[j].split("#|#")[1]
            if os.stat(file_path1).st_ctime > os.stat(file_path2).st_ctime:
                merged_list.append(list1[i])
                i += 1
            else:
                merged_list.append(list2[j])
                j += 1
    merged_list.extend(list1[i:])
    merged_list.extend(list2[j:])
    return merged_list


def loadMusicThread() -> None:
    """
    Loads music files from the specified directory and updates the UI.

    If no music files are found in the directory, or if permission is denied to access the directory,
    an error message is displayed.

    If the music player is currently disabled, this function will start the player.

    This function also starts a separate thread to load the date modified information for the music files.

    Returns:
        None
    """
    global number_of_files, Directory, dir_musics
    Directory.replace("/", "//")
    tmp, tmp_num = get_all_files(Directory)
    if tmp_num == 0 or tmp_num == -1:
        messagebox.showerror(
            "Error", "No Music Files Found In Directory"
        ) if tmp_num == 0 else messagebox.showerror(
            "Error", "Permission Denied To Access Directory"
        )
        return
    dir_musics = merge_sorted_lists(dir_musics, tmp)
    number_of_files += tmp_num
    if music_bar.state() and music_bar.state()[0] == "disabled":
        threadAction()
    load_thread = threading.Thread(target=loadDateModified, args=(tmp,))
    load_thread.daemon = True
    load_thread.start()
    directory_box.config(state=NORMAL)
    directory_box.insert(END, Directory + ", ")
    directory_box.config(state=DISABLED)
    changeDirectoryBoxHeight()


def loadDateModified(all_paths: list[str]) -> None:
    global date_modified_list, on_close, date_modified_flag, alphabetical_list
    tmp = []
    date_file_names = sorted(all_paths, key=lambda x: os.path.getctime(x), reverse=True)
    for file_path in date_file_names:
        file_name = os.path.basename(file_path)
        tmp.append(f"{file_name}#|#{file_path}")
    date_modified_list = merge_sorted_lists(date_modified_list, tmp, date=True)
    tmp = []
    for file_path in all_paths:
        file_name = os.path.basename(file_path)
        tmp.append(f"{file_name}#|#{file_path}")
    alphabetical_list = merge_sorted_lists(alphabetical_list, tmp)
    if not on_close:
        drop_down["values"] = (
            tuple(alphabetical_list)
            if not date_modified_flag
            else tuple(date_modified_list)
        )


def clearDirectory() -> None:
    global clear_flag, number_of_files, Directory, alphabetical_list, date_modified_list
    search_box.delete(0, END)
    dir_musics.clear()
    search_box.insert(0, "Press Enter To Search")
    search_box.configure(foreground="Gray")
    drop_down.set("All Music Files appear here")
    drop_down.configure(foreground="Gray")
    played.clear()
    drop_down["values"] = ("",)
    alphabetical_list = []
    date_modified_list = []
    directory_box.config(state=NORMAL)
    directory_box.delete("1.0", END)
    directory_box.config(state=DISABLED)
    changeDirectoryBoxHeight()
    clear_flag = True
    number_of_files = 0
    tray_icon.title = "True Music"
    Directory = ""


def rememberPathBtnAction() -> None:
    global remember_flag
    if remember_flag:
        remember_btn.configure(text="Store Path: Disabled")
    else:
        remember_btn.configure(text="Store Path: Enabled")
    remember_flag = not remember_flag


def storePath() -> None:
    global number_of_files, data_file, Directory
    with open(data_file, "w", encoding="utf-8") as f:
        if remember_flag and not first_flag:
            data = {
                "number_of_files": number_of_files,
                "Directory": Directory,
                "full_paths": dir_musics,
                "date_modified_names": date_modified_list,
            }
            json.dump(data, f)
        else:
            writeEmptyData()


def updateSize(event: object) -> None:
    music_bar.configure(to=root.winfo_width() // 3)
    title.configure(font=("Corbel", (root.winfo_width() + root.winfo_height()) // 50))
    now_playing.configure(
        font=("Aerial", (root.winfo_width() + root.winfo_height()) // 100)
    )


def playBtnAction(event: object = None) -> None:
    global play_image, pause_image, clear_flag, file_name, first_flag
    if (
        clear_flag
        or (event and root.focus_get() == search_box)
        or player.time > player.source.duration
        or first_flag
    ):
        return
    play_index = menu_items.index(
        next(item for item in menu_items if "Play" in item.text)
    )
    if player.playing:
        player.pause()
        menu_items[play_index] = pystray.MenuItem("Play", on_click)
        music_bar.state(["disabled"])
        play_pause_btn.configure(image=play_image) if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else play_pause_btn.configure(image=play_image_inv)
    else:
        try:
            player.play()
        except:
            return
        if player.volume <= 0:
            player.volume = 1.0
            volume_bar.set(0)
            volume_val.configure(text="100")
        menu_items[play_index] = pystray.MenuItem("Pause", on_click)
        music_bar.state(["!disabled"])
        play_pause_btn.configure(image=pause_image) if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else play_pause_btn.configure(image=pause_image_inv)
    tray_icon.title = ("[Playing] " if player.playing else "[Paused] ") + file_name[:60]
    tray_icon.menu = pystray.Menu(*menu_items)


def forwardBtnAction() -> None:
    try:
        player.pause()
        player.delete()
    except:
        return
    threadAction()


def previousBtnAction() -> None:
    try:
        player.delete()
        player.pause()
    except:
        return
    threadAction(True)


def playerEnd() -> None:
    global repeat_flag, auto_play_flag
    if repeat_flag:
        player.delete()
        player.seek(0.0)
        player.play()
    elif auto_play_flag:
        threadAction()
    else:
        player.pause()
        play_pause_btn.configure(image=play_image) if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else play_pause_btn.configure(image=play_image_inv)


def threadAction(prev_flag: bool = False, search_file: str = None) -> None:
    global first_flag, file_name, clear_flag, corrupt_flag, date_modified_flag, date_modified_cnt, number_of_files, notification_flag, is_windows
    if clear_flag:
        music_bar.set(0)
        player.pause()
        play_pause_btn.configure(image=play_image) if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else play_pause_btn.configure(image=play_image_inv)
        music_bar.state(["disabled"])
        seek_of_music.configure(text="00:00")
        now_playing.configure(text="Now playing: ")
        length_of_music.configure(text="00:00")
        return
    clear_flag = False
    if first_flag:
        seekbar_thread = threading.Thread(target=update_seekbar)
        seekbar_thread.daemon = True
        seekbar_thread.start()
        file_name = secure_generator(prev_flag, search_file)
        first_flag = False
        if corrupt_flag or file_name is None:
            music_bar.state(["disabled"])
            return
    else:
        if date_modified_flag and search_file is None:
            date_modified_cnt = (
                max(0, date_modified_cnt - 2) if prev_flag else date_modified_cnt
            )
            search_file = date_modified_list[date_modified_cnt].split("#|#")[-1]
            date_modified_cnt = (date_modified_cnt + 1) % number_of_files
        file_name = secure_generator(prev_flag, search_file)
        if corrupt_flag or file_name is None:
            music_bar.state(["disabled"])
            return
    if notification_flag:
        try:
            if is_windows:
                toaster.show_toast(
                    title="Now Playing",
                    msg=file_name[:60],
                    duration=3,
                    threaded=True,
                    icon_path=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..",
                        "static",
                        "resurrection.ico",
                    ),
                )
            else:
                # For some dumb reason pyler's notify method is messing with system tray icon and creating ghost icons every time a new notifcation appears
                notification.notify(
                    title="Now Playing",
                    message=file_name[:60],
                    app_icon=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..",
                        "static",
                        "resurrection.ico",
                    ),
                )
        except Exception:
            print(Exception)
            return
    music_bar.state(["!disabled"])
    play_pause_btn.configure(image=pause_image) if theme_btn.cget(
        "text"
    ) == "Theme: Dark" else play_pause_btn.configure(image=pause_image_inv)
    track_length = int(player.source.duration)
    now_playing.configure(text=f"Now playing: {file_name[:60]}")
    try:
        player.seek(0.0)
        player.play()
        tray_icon.title = ("[Playing] " if player.playing else "[Paused] ") + file_name[
            :60
        ]
    except:
        pass
    mins = track_length // 60
    secs = track_length % 60
    length_of_music.configure(text=f"{mins}:{secs:02d}")


def notificationAction() -> None:
    global notification_flag
    notification_index = menu_items.index(
        next(item for item in menu_items if "Notify" in item.text)
    )
    if notification_flag:
        notification_flag = False
        menu_items[notification_index] = pystray.MenuItem("Notify: Off", on_click)
    else:
        notification_flag = True
        menu_items[notification_index] = pystray.MenuItem("Notify: On", on_click)
    tray_icon.menu = pystray.Menu(*menu_items)


def writeEmptyData() -> None:
    global data_file
    with open(data_file, "w", encoding="utf-8") as f:
        data = {
            "number_of_files": 0,
            "Directory": "",
            "full_paths": [],
            "date_modified_names": [],
        }
        json.dump(data, f)


def changeDirectoryBoxHeight() -> None:
    if float(len(directory_box.get("0.0", "end-1c"))) * 12.4181818182 > (
        root.winfo_width()
    ):
        directory_box.config(height=2)
        refresh_btn.place(rely=0.41)
    else:
        directory_box.config(height=1)
        refresh_btn.place(rely=0.43)


def readData() -> None:
    global Directory, drop_down, number_of_files, on_close, date_modified_list, dir_musics, alphabetical_list
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            number_of_files = loaded_data["number_of_files"]
            if number_of_files > 0:
                Directory = loaded_data["Directory"]
                dir_musics = loaded_data["full_paths"]
                play_thread = threading.Thread(target=threadAction)
                play_thread.daemon = True
                play_thread.start()
                if on_close:
                    return
                for path in dir_musics:
                    file_name = os.path.basename(path)
                    alphabetical_list.append(f"{file_name}#|#{path}")
                date_modified_list = loaded_data["date_modified_names"]
                rememberPathBtnAction()
                directory_box.config(state=NORMAL)
                directory_box.insert(END, Directory)
                directory_box.config(state=DISABLED)
                changeDirectoryBoxHeight()
                drop_down["values"] = tuple(alphabetical_list)
                refreshBtnAction(Directory)
            else:
                root.deiconify()
                root.lift()
                root.focus_force()
    except:
        writeEmptyData()
        root.deiconify()
        root.lift()
        root.focus_force()


def muteBtnAction(event: object = None) -> None:
    global play_image, play_image_inv
    player.pause()
    music_bar.state(["disabled"])
    play_pause_btn.configure(image=play_image) if theme_btn.cget(
        "text"
    ) == "Theme: Dark" else play_pause_btn.configure(image=play_image_inv)


def on_volume_change(event: object) -> None:
    player.volume = (100 - event.y) / 100
    volume_bar.set((event.y / volume_bar.winfo_height()) * 100)
    volume_val.configure(text=int(100 - volume_bar.get()))
    if player.volume == 0.0:
        muteBtnAction()


def seek_tap(event: object) -> None:
    if music_bar.state() and music_bar.state()[0] == "disabled":
        return
    seek_position = event.x / (root.winfo_width() / 3)
    total_time = player.source.duration
    player.delete()
    player.seek((seek_position * total_time))
    if not player.playing:
        play_pause_btn.configure(image=pause_image) if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else play_pause_btn.configure(image=pause_image_inv)
    player.play()


def on_key_press(event: object) -> None:
    if event.keysym == "XF86AudioPlay":
        playBtnAction()
    elif event.keysym == "XF86AudioPrev":
        previousBtnAction()
    elif event.keysym == "XF86AudioNext":
        forwardBtnAction()
    elif event.keysym == "XF86AudioMute":
        muteBtnAction()
    elif root.focus_get() != search_box:
        if event.keysym == "Right":
            try:
                if player.playing:
                    player.delete()
                    player.seek(player.time + 5)
                    player.play()
            except:
                return
        elif event.keysym == "Left":
            try:
                if player.playing or player.time >= player.source.duration:
                    player.delete()
                    player.seek(player.time - 5)
                    if not player.playing:
                        play_pause_btn.configure(image=pause_image) if theme_btn.cget(
                            "text"
                        ) == "Theme: Dark" else play_pause_btn.configure(
                            image=pause_image_inv
                        )
                    player.play()
            except:
                return
        elif event.keysym == "Down":
            drop_down.focus()
        elif event.state & 1 and event.keysym.lower() == "n":
            forwardBtnAction()


def update_seekbar() -> None:
    global on_close, file_name
    if on_close:
        return
    if player.playing and player.source:
        current_time = player.time
        total_time = player.source.duration
        if current_time >= total_time:
            on_eos = threading.Thread(target=playerEnd)
            on_eos.daemon = True
            on_eos.start()
            player.pause()
        mins, secs = divmod(int(current_time), 60)
        seek_of_music.configure(text=f"0{mins}:{secs:02d}")
        seek_position = (current_time / total_time) * music_bar.winfo_width()
        music_bar.set(seek_position)
    root.after(100, update_seekbar)


def date_modified_btn_action() -> None:
    global date_modified_flag, date_modified_cnt, shuffle_flag, alphabetical_list, date_modified_list
    date_modified_cnt = 0
    if date_modified_flag:
        drop_down["values"] = tuple(alphabetical_list)
        date_modified_btn.configure(text="Date Modified: Disabled")
    else:
        drop_down["values"] = tuple(date_modified_list)
        date_modified_btn.configure(text="Date Modified: Enabled")
        if shuffle_flag:
            trueShuffle()
    date_modified_flag = not date_modified_flag


def search_play_song(event: object = None) -> None:
    if (
        search_song.get().strip() == "No items match your search"
        or not search_song.get().strip()
    ):
        return  # If search box is empty, do nothing
    global date_modified_cnt, date_modified_flag
    if drop_down["values"] == tuple(date_modified_list):
        date_modified_cnt = event.widget.current() + 1
    else:
        date_modified_cnt = 0
    player.delete()
    player.pause()
    selected_value = search_song.get()
    selected_file_path = selected_value.split("#|#")[1]
    play_thread = threading.Thread(
        target=threadAction, args=(False, selected_file_path)
    )
    play_thread.daemon = True
    play_thread.start()


def search(event: object = None) -> None:
    global date_modified_list, alphabetical_list, date_modified_flag
    search_term = search_box.get().strip().lower()
    if search_term == "":
        drop_down["values"] = (
            tuple(date_modified_list)
            if date_modified_flag
            else tuple(alphabetical_list)
        )
        drop_down.selection_clear()
        drop_down.focus()
        drop_down.event_generate("<Down>")
    else:
        search_results = [
            f"{os.path.basename(item)}#|#{item}"
            for item in dir_musics
            if search_term in item.lower()
        ]
        if not search_results:
            search_results = ["No items match your search"]
        drop_down["values"] = tuple(search_results)
        drop_down.selection_clear()
        drop_down.focus()
        drop_down.event_generate("<Down>")


def on_entry_click(event: object = None) -> None:
    if search_box.get() == "Press Enter To Search":
        search_box.delete(0, "end")  # Remove the placeholder text
        search_box.configure(foreground="White") if theme_btn.cget(
            "text"
        ) == "Theme: Dark" else search_box.configure(
            foreground="#16161d"  # Dark gray
        )


def on_entry_leave(event=None):
    if search_box.get() == "":
        search_box.insert(0, "Press Enter To Search")
        search_box.configure(foreground="gray")


def directoryBoxThread() -> None:
    directory_thread = threading.Thread(target=openFilePicker)
    directory_thread.daemon = True
    directory_thread.start()


def refreshBtnAction(given_directory: str = None) -> None:
    global number_of_files, on_close, date_modified_list, date_modified_flag, alphabetical_list, dir_musics
    number_of_files = 0
    date_modified_list = []
    alphabetical_list = []
    dir_musics = []
    if not given_directory:
        directories = [
            d.strip() for d in directory_box.get("1.0", END).split(",") if d.strip()
        ]
    else:
        directories = [d.strip() for d in given_directory.split(",") if d.strip()]
    for Directory in directories:
        tmp, tmp_num = get_all_files(Directory)
        dir_musics = merge_sorted_lists(dir_musics, tmp)
        loadDateModified(tmp)
        number_of_files += tmp_num
    if not on_close:
        refresh_btn.configure(text="Refresh", state="normal")
    return


def refreshThreadAction() -> None:
    refresh_btn.configure(text="Refreshing...", state="disabled")
    refresh_thread = threading.Thread(target=refreshBtnAction)
    refresh_thread.daemon = True
    refresh_thread.start()


def set_focus(event: object = None) -> None:
    if event.widget == root:
        root.focus_set()


def hotkeys() -> None:
    global hotkey_flag
    root.focus()
    hotkey_index = menu_items.index(
        next(item for item in menu_items if "Hotkeys" in item.text)
    )
    if hotkey_flag:
        hotkey_flag = False
        menu_items[hotkey_index] = pystray.MenuItem("Hotkeys: Off", on_click)
        hotkey_btn.configure(text="Hotkeys: Off")
    else:
        hotkey_flag = True
        menu_items[hotkey_index] = pystray.MenuItem("Hotkeys: On", on_click)
        hotkey_btn.configure(text="Hotkeys: On")
        mediaKeysThread = threading.Thread(target=checkMediaKeys)
        mediaKeysThread.daemon = True
        mediaKeysThread.start()
    tray_icon.menu = pystray.Menu(*menu_items)


def on_click(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    global on_close
    if on_close:
        icon.stop()
        return
    if item.text == "Quit":
        icon.stop()
        onClosing()
    elif item.text == "Play" or item.text == "Pause":
        playBtnAction()
    elif item.text == "Next Track":
        forwardBtnAction()
    elif item.text == "Previous Track":
        previousBtnAction()
    elif item.text == "True Shuffle: On" or item.text == "True Shuffle: Off":
        trueShuffle()
    elif item.text == "Repeat: On" or item.text == "Repeat: Off":
        autoRepeat()
    elif item.text == "Autoplay: On" or item.text == "Autoplay: Off":
        autoPlay()
    elif item.text == "Hotkeys: On" or item.text == "Hotkeys: Off":
        hotkeys()
    elif item.text == "Notify: On" or item.text == "Notify: Off":
        notificationAction()


def showRoot(icon: pystray.Icon = None, item: pystray.MenuItem = None) -> None:
    if root.state() == "normal":
        root.withdraw()
    else:
        root.deiconify()
        root.lift()
        root.focus_force()


tray_icon = pystray.Icon(
    icon=PIL.Image.open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "resurrection.ico",
        )
    ),
    name="True Music",
    title="True Music",
)

menu_items = [
    pystray.MenuItem("Show/Hide", action=showRoot, default=True),
    pystray.MenuItem("True Shuffle: On", on_click),
    pystray.MenuItem("Repeat: Off", on_click),
    pystray.MenuItem("Notify: Off", on_click),
    pystray.MenuItem("Autoplay: On", on_click),
    pystray.MenuItem("Next Track", on_click),
    pystray.MenuItem("Pause", on_click),
    pystray.MenuItem("Previous Track", on_click),
    pystray.MenuItem("Hotkeys: Off", on_click),
    pystray.MenuItem("Quit", on_click),
]


def pystrayTray() -> None:
    global shuffle_flag
    tray_icon.menu = pystray.Menu(*menu_items)
    try:
        tray_icon.run()
        # tray_icon.run_detached()
    except:
        return
    onClosing()
    return


def checkMediaKeys() -> None:
    global on_close, hotkey_flag
    if on_close:
        return

    def on_press(key: object) -> None:
        try:
            if not hotkey_flag:
                listener.stop()
                return
            if key == keyboard.Key.media_play_pause:
                playBtnAction()
            elif key == keyboard.Key.media_previous:
                previousBtnAction()
            elif key == keyboard.Key.media_next:
                forwardBtnAction()
            elif key == keyboard.Key.media_volume_mute:
                muteBtnAction()
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    return


def onMinimize(event: object = None) -> None:
    root.withdraw()


store_path_thread = threading.Thread(target=storePath)


def onClosing() -> None:
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.lock"))
    global on_close, Directory, tray_icon
    store_path_thread.start()
    try:
        Directory = root.call(directory_box, "get", "1.0", "end-1c")
        on_close = True
        tray_icon.stop()
        played.clear()
        player.pause()
        pyglet.app.exit()
        root.destroy()
    except Exception as e:
        os.kill(os.getpid(), 9)


read_data_thread = threading.Thread(target=readData)
read_data_thread.daemon = True
read_data_thread.start()

if __name__ == "__main__":
    root = Tk()
    root.minsize(200, 50)
    root.geometry(f"{root.winfo_screenwidth()//2}x{root.winfo_screenheight()//2}")
    root.configure(background="#121212")
    root.title("True Music")
    root.withdraw()

    try:
        if is_windows:
            root.iconbitmap(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "..",
                    "static",
                    "resurrection.ico",
                )
            )
        else:
            root.iconbitmap(
                "@"
                + os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "..",
                    "static",
                    "trueShuffle.xbm",
                )
            )
    except:
        messagebox.showerror(
            "Iconbitmap icon not found", "Window Icon Cannot be loaded"
        )

    # Heading
    title = Label(root, text="True Music ~ HauseMaster", font=("Corbel", 13))
    title.place(relx=0.5, rely=0.1, anchor=CENTER)
    title.configure(background="#121212", foreground="#f0f0f0")

    # Style
    style = ttk.Style()
    style.configure("myStyle.Horizontal.TScale", background="#121212")
    style.configure("myStyle.Vertical.TScale", background="#121212")

    # Root
    clear_btn = Button(
        root, text="Clear All", command=clearDirectory, padx=6, font=("Corbel", 10)
    )

    clear_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="grey",
    )
    clear_btn.place(relx=0.83, rely=0.58, anchor=E)
    myTip4 = CreateToolTip(
        clear_btn,
        "Clear all the files in the directory " "and Search Box and Current Queue",
    )  # noqa

    remember_btn = Button(
        root,
        text="Store Path: Disabled",
        command=rememberPathBtnAction,
        padx=6,
        font=("Corbel", 10),
    )
    remember_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="grey",
    )
    remember_btn.place(relx=0.19, rely=0.58, anchor=W)

    myTip2 = CreateToolTip(
        remember_btn,
        "Store the path of the folder you selected and "
        "autoplay next time app is opened",
    )  # noqa

    date_modified_btn = Button(
        root,
        text="Date Modified: Disabled",
        command=date_modified_btn_action,
        padx=6,
        font=("Corbel", 10),
    )
    date_modified_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="grey",
    )
    date_modified_btn.place(relx=0.55, rely=0.58, anchor=CENTER)
    myTip1 = CreateToolTip(
        date_modified_btn, "Sorts the songs by date modified"
    )  # noqa

    now_playing = Label(root, text="Now playing: ", font=("Corbel", 10))
    now_playing.place(relx=0.5, rely=0.35, anchor=CENTER)
    now_playing.configure(background="#121212", foreground="#f0f0f0")

    seek_of_music = Label(root, text="00:00", font=("Verdana", 8))
    seek_of_music.place(relx=0.3, rely=0.25, anchor=CENTER)
    seek_of_music.configure(background="#121212", foreground="#f0f0f0")

    length_of_music = Label(root, text="0:00", font=("Verdana", 8))
    length_of_music.place(relx=0.7, rely=0.25, anchor=CENTER)
    length_of_music.configure(background="#121212", foreground="#f0f0f0")

    directory_box = Text(
        root,
        foreground="#121212",
        highlightthickness="1",
        background="#0D0901",
        state=DISABLED,
    )
    directory_box.configure(
        highlightcolor="lightblue",
        highlightthickness=1,
        highlightbackground="lightblue",
        foreground="white",
        height=1,
    )
    directory_box.place(relwidth=0.65, relx=0.51, rely=0.5, anchor=CENTER)

    Directory.replace("/", "//")

    search_box = Entry(
        root, foreground="gray", background="#3f3f40", bd=1, relief=GROOVE
    )
    search_box.configure(highlightthickness=0)
    search_box.place(anchor=W, relwidth=0.25, relx=0.05, rely=0.67)
    search_box.insert(0, "Press Enter To Search")  # Insert the placeholder text
    search_box.bind("<Return>", search)
    search_box.bind("<FocusIn>", on_entry_click)
    search_box.bind("<FocusOut>", on_entry_leave)

    try:
        arrow_lbl = Label(root, text="⇌", font=("Corbel", 14))
        arrow_lbl.configure(background="#121212", foreground="White")
        arrow_lbl.place(anchor=CENTER, relx=0.33, rely=0.67)
    except:
        pass

    search_song = StringVar()
    drop_down = ttk.Combobox(
        root,
        width=27,
        textvariable=search_song,
        state="readonly",
        takefocus=False,
        exportselection=False,
    )
    drop_down.place(anchor=E, relx=0.85, rely=0.67, relwidth=0.5)
    drop_down.configure(foreground="Gray")
    drop_down.set("All Music Files appear here")
    drop_down.bind("<<ComboboxSelected>>", search_play_song)
    drop_down["values"] = ("",)

    music_bar = ttk.Scale(
        root,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        style="myStyle.Horizontal.TScale",
        cursor="crosshair",
    )
    music_bar.bind("<Button-1>", seek_tap)
    # music_bar.bind('<ButtonRelease-1>', seek_tap)
    music_bar.place(relx=0.5, rely=0.2, anchor=CENTER, relwidth=0.33)
    music_bar.state(["disabled"])

    selectDirectory = Button(
        root,
        text="Select Music Folder",
        command=directoryBoxThread,
        width=root.winfo_width() // 50,
        padx=6,
        wraplength=root.winfo_width() // 6,
        font=("Corbel", 10),
    )
    selectDirectory.configure(
        background="#121212",
        foreground="White",
        relief="ridge",
        borderwidth=0,
        activeforeground="grey",
        activebackground="#121212",
    )

    def on_enter_direc(e: object) -> None:
        selectDirectory.configure(borderwidth=1)

    def on_leave_direc(e: object) -> None:
        selectDirectory.configure(borderwidth=0)

    selectDirectory.bind("<Enter>", on_enter_direc)
    selectDirectory.bind("<Leave>", on_leave_direc)

    selectDirectory.place(relx=0.01, rely=0.5, anchor=W, relwidth=0.17, relheight=0.15)

    refresh_btn = Button(
        root, text="Refresh", command=refreshThreadAction, padx=6, font=("Corbel", 10)
    )
    refresh_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="grey",
    )

    refresh_btn.place(relx=0.19, rely=0.43, anchor=W)
    myTip3 = CreateToolTip(
        refresh_btn, "Refresh All the files in the directory" " and "
    )

    volume_bar = ttk.Scale(
        root,
        from_=0,
        to=100,
        orient=VERTICAL,
        style="myStyle.Vertical.TScale",
        cursor="right_ptr",
    )
    volume_bar.set(0)
    # volume_bar.bind('<Button-1>', on_volume_change)
    volume_bar.bind("<ButtonRelease-1>", on_volume_change)
    volume_bar.place(relx=0.85, rely=0.19, anchor=W, relheight=0.25)

    volume_image = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static", "volume.png"
        )
    )
    volume_image_inv = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "volume_inverted.png",
        )
    )

    volume_icon = Label(root, image=volume_image)
    volume_icon.place(relx=0.91, rely=0.18, anchor=W)
    volume_icon.configure(borderwidth=0, background="#121212")
    volume_icon.bind("<Button-1>", muteBtnAction)

    volume_val = Label(root, text="100")
    volume_val.place(relx=0.95, rely=0.18, anchor=W)
    volume_val.configure(background="#121212", foreground="#f0f0f0", borderwidth=0)

    autoplay_btn = Button(
        root,
        text="Autoplay: Enabled",
        command=autoPlay,
        padx=6,
        pady=6,
        font=("Corbel", 10),
    )
    autoplay_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=1,
        activeforeground="grey",
    )
    autoplay_btn.place(relx=0.99, rely=0.85, anchor=E, relheight=0.15, width=140)

    repeat_btn = Button(
        root, text="Repeat: Disabled", command=autoRepeat, padx=6, font=("Corbel", 10)
    )
    repeat_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="ridge",
        borderwidth=1,
        activeforeground="grey",
    )
    repeat_btn.place(relx=0.5, rely=0.85, anchor=CENTER, relheight=0.15, width=120)

    always_on_top_btn = Button(
        root,
        text="Always On Top: Disabled",
        command=alwaysOnTop,
        padx=6,
        pady=6,
        font=("Corbel", 10),
    )
    always_on_top_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="ridge",
        borderwidth=1,
        activeforeground="grey",
    )
    always_on_top_btn.place(relx=0.01, rely=0.85, anchor=W, relheight=0.15, width=150)

    theme_btn = Button(
        root, text="Theme: Dark", command=changeTheme, font=("Corbel", 10)
    )
    theme_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="gray",
    )
    theme_btn.place(anchor=W, relx=0.01, rely=0.1, relheight=0.11, relwidth=0.11)

    hotkey_btn = Button(root, text="Hotkeys: Off", command=hotkeys, font=("Corbel", 10))
    hotkey_btn.configure(
        background="#121212",
        foreground="white",
        activebackground="#121212",
        relief="sunken",
        borderwidth=0,
        activeforeground="gray",
    )
    hotkey_btn.place(anchor=W, relx=0.15, rely=0.1, relheight=0.11, relwidth=0.11)

    play_image = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static", "play.png"
        )
    )

    play_image_inv = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "play_inverted.png",
        )
    )

    pause_image = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static", "pause.png"
        )
    )

    pause_image_inv = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "pause_inverted.png",
        )
    )

    play_pause_btn = Button(root, image=play_image, command=playBtnAction)
    play_pause_btn.configure(
        relief="sunken", borderwidth=0, background="#121212", activebackground="#121212"
    )
    play_pause_btn.place(relx=0.15, rely=0.2, anchor=CENTER)

    forward_image = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static", "forward.png"
        )
    )

    forward_image_inv = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "forward_inverted.png",
        )
    )

    forward_btn = Button(root, image=forward_image, command=forwardBtnAction)
    forward_btn.configure(
        relief="sunken", borderwidth=0, background="#121212", activebackground="#121212"
    )
    forward_btn.place(relx=0.25, rely=0.2, anchor=CENTER)

    previous_image = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static", "previous.png"
        )
    )

    previous_image_inv = PhotoImage(
        file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "static",
            "previous_inverted.png",
        )
    )

    previous_btn = Button(root, image=previous_image, command=previousBtnAction)
    previous_btn.configure(
        relief="sunken", borderwidth=0, background="#121212", activebackground="#121212"
    )
    previous_btn.place(relx=0.05, rely=0.2, anchor=CENTER)

    trueShuffle_btn = Button(
        root,
        text="True Shuffle: On",
        command=trueShuffle,
        padx=6,
        pady=6,
        font=("Corbel", 10),
    )
    trueShuffle_btn.configure(
        background="#121212",
        relief="groove",
        borderwidth=0,
        activeforeground="grey",
        activebackground="#121212",
        foreground="#2dd128",
    )

    def on_enter_shuffle(e: object) -> None:
        trueShuffle_btn.configure(borderwidth=1)

    def on_leave_shuffle(e: object) -> None:
        trueShuffle_btn.configure(borderwidth=0)

    trueShuffle_btn.bind("<Enter>", on_enter_shuffle)
    trueShuffle_btn.bind("<Leave>", on_leave_shuffle)

    trueShuffle_btn.place(relx=0.99, rely=0.5, anchor=E, relwidth=0.15, relheight=0.15)

    root.bind("<KeyPress>", on_key_press)
    root.bind("<space>", playBtnAction)
    root.bind("<Configure>", updateSize)
    root.protocol("WM_DELETE_WINDOW", root.iconify)
    root.bind("<Unmap>", onMinimize)
    root.bind("<Button-1>", set_focus)
    SystemTrayThread = threading.Thread(target=pystrayTray)
    SystemTrayThread.daemon = True
    SystemTrayThread.start()
    root.mainloop()
