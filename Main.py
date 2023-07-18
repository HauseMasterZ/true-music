import os
from tkinter import messagebox
LOCK_FILE = os.path.join(os.path.dirname(__file__), 'lock_file')
if os.path.exists(LOCK_FILE):
    messagebox.showerror("Error", "True Music is already running!")
    import sys
    sys.exit(0)
else:
    with open(LOCK_FILE, 'w') as lock_file:
        pass
from pynput import keyboard
import threading
from tkinter import *
import secrets
from tkinter import filedialog
from tkinter import ttk
import pyglet
import pystray
import PIL.Image

root = Tk()
root.minsize(200, 50)
root.geometry(f"{root.winfo_screenwidth()//2}x{root.winfo_screenheight()//2}")
root.configure(background="#121212")
root.title("True Music")
root.withdraw()

# Heading
title = Label(root, text="True Music ~ HauseMaster", font=("Corbel", 13))
title.place(relx=0.5, rely=0.1, anchor=CENTER)
title.configure(background="#121212", foreground="#f0f0f0")



Directory = ""
dir_musics = []
number_of_files = 0
remember_flag = False
secretsGenerator = secrets.SystemRandom()



# Functions
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
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
        label = Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

# Theme Button Action
def changeTheme():
    global shuffle_flag
    if theme_btn.cget('text') == 'Theme: Dark':
        root.configure(background="White")
        arrow_lbl.configure(background='White', foreground='Black')
        title.configure(background="White", foreground="Black")
        theme_btn.configure(text="Theme: Light", background='White',
                            foreground='Black', activebackground='White', activeforeground='gray')
        hotkey_btn.configure(background='White', foreground='Black')
        directory_box.configure(background='#c2c1c1', foreground='Black')
        volume_icon.configure(image=volume_image_inv, background='White')
        play_pause_btn.configure(
            image=pause_image_inv) if player.playing else play_pause_btn.configure(image=play_image_inv)
        play_pause_btn.configure(background='White',
                                 activebackground='White')
        forward_btn.configure(image=forward_image_inv)
        previous_btn.configure(image=previous_image_inv)
        date_modified_btn.configure(background='White', foreground='Black')
        refresh_btn.configure(background='White', foreground='Black',)
        previous_btn.configure(background='White',
                               borderwidth=0, activebackground='#b3afaf')
        forward_btn.configure(background='White', activebackground='#b3afaf')
        style.configure("myStyle.Horizontal.TScale", background='White')
        style.configure("myStyle.Vertical.TScale", background='White')
        remember_btn.configure(background='White', foreground='Black',
                               activebackground='White', activeforeground='#575655')
        now_playing.configure(background='White', foreground='Black')
        seek_of_music.configure(background='White', foreground='Black')
        length_of_music.configure(background='White', foreground='Black')
        volume_val.configure(background='White', foreground='Black')
        clear_btn.configure(background='White', foreground='Black',
                            activebackground='White', activeforeground='#575655')
        autoplay_btn.configure(background='White', foreground='Black',activebackground='White')
        always_on_top_btn.configure(background='White', foreground='Black', activebackground='White')
        repeat_btn.configure(background='White', foreground='Black', activebackground='White')
        selectDirectory.configure(background='White', foreground='Black',activebackground='White')
        trueShuffle_btn.configure(background='White', foreground='Black' if not shuffle_flag else "#2dd128",activebackground='White')
    else:
        date_modified_btn.configure(background='#121212', foreground='White')
        refresh_btn.configure(background='#121212', foreground='White')
        root.configure(background='#121212')
        arrow_lbl.configure(background='#121212', foreground='White')
        title.configure(background="#121212", foreground="White")
        theme_btn.configure(text="Theme: Dark", background='#121212',
                            foreground='white', activebackground='#121212', activeforeground='gray')
        hotkey_btn.configure(background='#121212', foreground='white')
        directory_box.configure(background='#0D0901', foreground='white')
        volume_icon.configure(image=volume_image)
        play_pause_btn.configure(
            image=pause_image) if player.playing else play_pause_btn.configure(image=play_image)
        play_pause_btn.configure(background='#121212', activebackground='#121212')
        forward_btn.configure(image=forward_image)
        previous_btn.configure(image=previous_image)
        previous_btn.configure(
            background='#121212', activebackground='#121212', borderwidth=0)
        forward_btn.configure(background='#121212',
                              activebackground='#121212', borderwidth=0)
        style.configure("myStyle.Horizontal.TScale", background='#121212')
        remember_btn.configure(background='#121212', foreground='White',
                               activebackground='#121212', activeforeground='Grey')
        clear_btn.configure(background='#121212', foreground='White',
                            activebackground='#121212', activeforeground='Grey')
        style.configure("myStyle.Vertical.TScale", background='#121212')
        now_playing.configure(background='#121212', foreground='White')
        seek_of_music.configure(background='#121212', foreground='White')
        length_of_music.configure(background='#121212', foreground='White')
        volume_val.configure(background='#121212', foreground='White')
        autoplay_btn.configure(background='#121212', foreground='White', activebackground='#121212')
        always_on_top_btn.configure(background='#121212', foreground='White', activebackground='#121212')
        repeat_btn.configure(background='#121212', foreground='White', activebackground='#121212')
        selectDirectory.configure(background='#121212', foreground='White',activebackground='#121212')
        trueShuffle_btn.configure(background='#121212', foreground='White' if not shuffle_flag else "#2dd128", activebackground='#121212')

# Variables
on_close = False
auto_play_flag = True
repeat_flag = False
first_flag = True
pyglet.options['audio'] = ('openal', 'pulse', 'xaudio2', 'directsound', 'silent')

player = pyglet.media.Player()
pyglet.options['graphics'] = {'backend': 'gl'}
playing_index = 0
corrupt_flag = False
prev_corrupt_flag = False
played = set()

# Random Number Generator
def secure_generator(prev_flag=False, search_file=None):
    global number_of_files, first_flag, playing_index, corrupt_flag, prev_corrupt_flag, shuffle_flag
    if search_file is None:
        if shuffle_flag:
            secure_choice = secretsGenerator.randint(0, number_of_files-1)
        else:
            if not first_flag:
                if prev_flag:
                    secure_choice = max(playing_index - 1, 0)
                else:
                    secure_choice = playing_index + 1
            else:
                secure_choice = playing_index
        if secure_choice in played and shuffle_flag:
            if len(played) > number_of_files-1:
                played.clear()
            while secure_choice in played:
                secure_choice = secretsGenerator.randint(0, number_of_files-1)
        if shuffle_flag:
            played.add(secure_choice)
        else:
            played.clear()
    player.pause()
    player.seek(0)
    player.seek(0)
    try:
        player.delete()
        if search_file == None:
            media = pyglet.media.load(
                dir_musics[secure_choice], streaming=True)
        else:
            media = pyglet.media.load(search_file, streaming=True)
        corrupt_flag = False
    except:
        messagebox.showerror('Invalid Media Found',
                             'Some if not all media files are corrupted')
        clearDirectory()
        player.delete()
        directory_box.config(state=NORMAL)
        directory_box.delete("1.0", END)
        directory_box.config(state=DISABLED)
        corrupt_flag = True
        prev_corrupt_flag = True
        player.next_source()
        return None
    if not corrupt_flag:
        player.queue(media)
        if not prev_corrupt_flag and not first_flag:
            player.next_source()
        else:
            prev_corrupt_flag = False
        player.delete()
    media = None
    del media
    if search_file == None:
        playing_index = secure_choice
        return os.path.basename(dir_musics[secure_choice])
    else:
        return os.path.basename(search_file)

# Autoplay
def autoPlay():
    global auto_play_flag, repeat_flag
    if auto_play_flag:
        auto_play_flag = False
        menu_items[3] = pystray.MenuItem('Autoplay: Off', on_click)
        icon.menu = pystray.Menu(*menu_items)
        autoplay_btn.config(text="Autoplay: Disabled",
                            relief=RIDGE)
    else:
        auto_play_flag = True
        menu_items[3] = pystray.MenuItem('Autoplay: On', on_click)
        icon.menu = pystray.Menu(*menu_items)
        autoplay_btn.config(text="Autoplay: Enabled",
                            relief=SUNKEN)
        if repeat_flag:
            repeat_flag = False
            repeat_btn.configure(
                text='Repeat: Disabled', relief=RIDGE)
            menu_items[2] = pystray.MenuItem('Repeat: Off', on_click)
            icon.menu = pystray.Menu(*menu_items)



always_on_top_flag = False
shuffle_flag = True



# Always On Top
def alwaysOnTop():
    global always_on_top_flag
    if always_on_top_flag:
        root.attributes("-topmost", False)
        always_on_top_flag = False
        always_on_top_btn.configure(
            text="Always On Top: Disabled", relief=RIDGE)
    else:
        root.attributes("-topmost", True)
        always_on_top_flag = True
        always_on_top_btn.configure(
            text="Always On Top: Enabled", relief=SUNKEN)



# Shuffle Button
def trueShuffle():
    global shuffle_flag, date_modified_flag
    if date_modified_flag:
        date_modified_flag = False
        date_modified_btn.configure(
            text='Date Modified: Disabled')
        drop_down['values'] = file_names
    if shuffle_flag:
        shuffle_flag = False
        menu_items[1] = pystray.MenuItem('True Shuffle: Off', on_click)
        icon.menu = pystray.Menu(*menu_items)
        trueShuffle_btn.configure(
            text='True Shuffle: Off', relief=RIDGE, foreground='White' if theme_btn.cget('text') == 'Theme: Dark' else 'Black')
    else:
        shuffle_flag = True
        menu_items[1] = pystray.MenuItem('True Shuffle: On', on_click)
        icon.menu = pystray.Menu(*menu_items)
        trueShuffle_btn.configure(
            text='True Shuffle: On', relief=SUNKEN, foreground='#2dd128')

# Auto Repeat
def autoRepeat():
    global repeat_flag, auto_play_flag
    if repeat_flag:
        repeat_flag = False
        menu_items[2] = pystray.MenuItem('Repeat: Off', on_click)
        icon.menu = pystray.Menu(*menu_items)
        repeat_btn.configure(text='Repeat: Disabled',
                             relief=RIDGE)
    else:
        repeat_flag = True
        menu_items[2] = pystray.MenuItem('Repeat: On', on_click)
        icon.menu = pystray.Menu(*menu_items)
        repeat_btn.configure(text='Repeat: Enabled',
                             relief=SUNKEN)
        if auto_play_flag:
            auto_play_flag = False
            menu_items[3] = pystray.MenuItem('Autoplay: Off', on_click)
            icon.menu = pystray.Menu(*menu_items)
            autoplay_btn.config(text="Autoplay: Disabled",
                                relief=RIDGE)

# Audio Video
audio_set = ('.m4a', '.mp3', '.aac', '.flac', '.wav', '.ogg', '.wma')
# video_set = {"webm", "flv", "mp4", "mov", "wmv"}

# Function to get all the files in the directory including the subdirectories
def get_all_files(folder_path):
    global on_close, clear_flag
    if on_close:
        return [], [], 0
    all_files = []
    file_names = []
    file_count = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if on_close or clear_flag:
                    return [], [], 0
                if file.endswith(audio_set):
                    all_files.append(os.path.join(root, file))
                    file_names.append(file)
                    file_count += 1
    except PermissionError:
        return [], [], -1
    return all_files, file_names, file_count



file_names = ('', )
initial_drop_values = ('', )

# File Picker Open
def openFilePicker():
    global dir_musics, Directory, clear_flag, directory_box_flag, first_flag
    directory_box_flag = True
    if first_flag:
        now_playing.configure(text='Now Playing: Please Wait...')
    if clear_flag:
        dir_musics.clear()
    clear_flag = False
    Directory = filedialog.askdirectory(title="Select Directory")
    Directory += "/"
    if Directory != '/' and Directory in directory_box.get("1.0", "end-1c"):
        messagebox.showwarning('Existing Directory', 'Directory Already Exists. Please Select Another Directory.')
    elif Directory != '/':
        load_music_thread = threading.Thread(target=loadMusicThread)
        load_music_thread.daemon = True
        load_music_thread.start()
        directory_box_flag = False
        return
    directory_box_flag = False
    if first_flag:
        now_playing.configure(text='Now Playing: ')

# Search File In Directory
def loadMusicThread():
    global number_of_files, Directory
    tmp = directory_box.index("end-1c").split(".")
    if float(tmp[1])*12.4181818182 > (root.winfo_width()):
        directory_box.config(height=2)
        refresh_btn.place(rely=0.41)
    Directory.replace("/", "//")
    tmp, file_names, tmp_num = get_all_files(Directory)
    if file_names == [] or tmp_num == 0 or tmp_num == -1:
        messagebox.showerror("Error", "No Music Files Found In Directory") if tmp_num == 0 else messagebox.showerror('Error', 'Permission Denied To Access Directory')
        return
    directory_box.config(state=NORMAL)
    directory_box.insert(END, Directory + ', ')
    directory_box.config(state=DISABLED)
    load_thread = threading.Thread(target=loadDateModified, args=(tmp[::], file_names[::], number_of_files))
    load_thread.daemon = True
    load_thread.start()
    dir_musics.extend(tmp)
    number_of_files += tmp_num
    tmp.clear()
    file_names.clear()
    if music_bar.state()[0] == 'disabled':
        threadAction()


def merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    # Append remaining elements from list1, if any
    merged_list.extend(list1[i:])

    # Append remaining elements from list2, if any
    merged_list.extend(list2[j:])

    return merged_list

def get_unix_time_from_tuple(filename):
    return int(filename.split('unixStart')[-1].split('searchSelectIndex')[0])

def date_merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if get_unix_time_from_tuple(list1[i]) >= get_unix_time_from_tuple(list2[j]):
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1
    merged_list += list1[i:]
    merged_list += list2[j:]
    return merged_list

# date modified sort
def loadDateModified(tmp, date_file_names, number_of_files):
    global file_names, initial_drop_values, on_close, date_modified_flag
    res = ()
    for x, i in enumerate(date_file_names):
        if not on_close:
            res += (str(i) + '                                                                                                                          searchSelectIndex' + str(number_of_files+x),)
        else:
            return
    if file_names[0] == '':
        file_names = res
    else:
        file_names = merge_sorted_lists(file_names, res)
    res = ()

    date_file_names = sorted(enumerate(tmp), key = lambda x: os.path.getctime(x[1]), reverse=True)
    for ind, i in date_file_names:
        if not on_close:
                res += (str(os.path.basename(i)) + "                                                                                                                unixStart" + str(int(os.path.getctime(i))) + "searchSelectIndex" + str(number_of_files+ind),)
        else:
            return
    if on_close:
        return
    if initial_drop_values[0] == '':
        initial_drop_values = res[::]
    else:
        initial_drop_values = date_merge_sorted_lists(initial_drop_values, res)
    drop_down['values'] = file_names if not date_modified_flag else initial_drop_values

clear_flag = False

# Clear Directory
def clearDirectory():
    global clear_flag, number_of_files, Directory, file_names, initial_drop_values, date_modified_flag, remember_flag, first_flag
    search_box.delete(0, END)
    search_box.insert(0, 'Press Enter To Search')
    search_box.configure(foreground='Gray')
    directory_box.config(height=1)
    refresh_btn.place(rely=0.43)
    date_modified_btn.configure(text="Date Modified: Disabled")
    date_modified_flag = False
    remember_btn.configure(text='Store Path: Disabled')
    remember_flag = False
    drop_down.set('All Music Files appear here')
    drop_down.configure(foreground='Gray')
    played.clear()
    drop_down['values'] = ('',)
    file_names = ('', )
    initial_drop_values = ('',)
    root.focus_set()
    if first_flag:
        return
    directory_box.config(state=NORMAL)
    directory_box.delete("1.0", END)
    directory_box.config(state=DISABLED)
    clear_flag = True
    number_of_files = 0
    Directory = "\n"

# Remember Path
def rememberPathBtnAction():
    global remember_flag
    if remember_flag:
        remember_btn.configure(text='Store Path: Disabled')
    else:
        remember_btn.configure(text='Store Path: Enabled')
    remember_flag = not remember_flag

# data file path modify here
data_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data.txt')

# Store Path
def storePath():
    global number_of_files, Directory, data_file, clear_flag
    with open(data_file, 'w', encoding='utf-8') as f:
        if remember_flag and not first_flag:
            f.write(f'{number_of_files} \n')
            f.write(Directory)
            f.writelines('\n'.join(dir_musics)
                         ) if not clear_flag else f.writelines('\n')
            if initial_drop_values:
                f.writelines('\nDateModifiedStart\n')
                f.writelines('\n'.join(initial_drop_values))
        else:
            f.write('0')

# Size Update Function
def updateSize(event):
    music_bar.configure(to=root.winfo_width()//3)
    title.configure(
        font=("Corbel", (root.winfo_width() + root.winfo_height()) // 50))
    now_playing.configure(font=("Aerial", (root.winfo_width() +
                                           root.winfo_height()) // 100)) 


store_path_thread = threading.Thread(target=storePath)

file_name = ''

# Play button action
def playBtnAction(event=None):
    global play_image, pause_image, clear_flag
    if clear_flag or first_flag or root.focus_get() == search_box :
        return
    if player.playing:
        player.pause()
        music_bar.state(['disabled'])
        play_pause_btn.configure(image=play_image) if theme_btn.cget(
            'text') == 'Theme: Dark' else play_pause_btn.configure(image=play_image_inv)
    else:
        if player.volume <= 0:
            player.volume = 1.0
            volume_bar.set(100)
            volume_val.configure(text='50')
        music_bar.state(['!disabled'])
        player.play()
        play_pause_btn.configure(image=pause_image) if theme_btn.cget(
            'text') == 'Theme: Dark' else play_pause_btn.configure(image=pause_image_inv)

# forward button action
def forwardBtnAction():
    player.seek(0)
    threadAction()

# backward button action
def previousBtnAction():
    player.pause()
    player.seek(0)
    threadAction(True)

# on play end
def playerEnd():
    global repeat_flag, auto_play_flag
    if repeat_flag:
        player.pause()
        player.seek(0)
        player.seek(0)
        update_seekbar()
        play_pause_btn.configure(image=pause_image) if theme_btn.cget(
            'text') == 'Theme: Dark' else play_pause_btn.configure(image=pause_image_inv)
        player.play()
    elif auto_play_flag:
        player.pause()
        player.seek(0)
        player.seek(0)
        threadAction()


date_modified_cnt = 0


# Play Music
def threadAction(prev_flag=False, search_file=None):
    global first_flag, length_of_music, file_name, clear_flag, corrupt_flag, date_modified_flag, playing_index, date_modified_cnt, number_of_files
    player.delete()
    if clear_flag:
        music_bar.set(0)
        player.pause()
        play_pause_btn.configure(image=play_image) if theme_btn.cget(
            'text') == 'Theme: Dark' else play_pause_btn.configure(image=play_image_inv)
        music_bar.state(['disabled'])
        seek_of_music.configure(text='00:00')
        now_playing.configure(text='Now playing: ')
        length_of_music.configure(text='00:00')
        dir_musics.clear()
        return
    clear_flag = False
    if first_flag:
        music_bar.state(['!disabled'])
        if date_modified_flag and search_file is None:
            date_modified_cnt = date_modified_cnt % number_of_files
            if not prev_flag:
                index = int(initial_drop_values[date_modified_cnt].rsplit('searchSelectIndex')[-1])
                file_name = secure_generator(prev_flag, dir_musics[index])
            else:
                index = int(initial_drop_values[max(0, date_modified_cnt-2)].rsplit('searchSelectIndex')[-1])
                file_name = secure_generator(False, dir_musics[index])
                date_modified_cnt -= 2
            playing_index = index
            date_modified_cnt += 1
        else:
            file_name = secure_generator(prev_flag, search_file)
        first_flag = False
        if corrupt_flag:
            music_bar.state(['disabled'])
            return
    else:
        player.pause()
        if date_modified_flag and search_file is None:
            date_modified_cnt = date_modified_cnt % number_of_files
            if not prev_flag:
                index = int(initial_drop_values[date_modified_cnt].rsplit('searchSelectIndex')[-1])
                file_name = secure_generator(prev_flag, dir_musics[index])
            else:
                index = int(initial_drop_values[max(0, date_modified_cnt-2)].rsplit('searchSelectIndex')[-1])
                file_name = secure_generator(False, dir_musics[index])
                date_modified_cnt -= 2
            playing_index = index
            date_modified_cnt += 1
        else:
            file_name = secure_generator(prev_flag, search_file)
        if corrupt_flag:
            music_bar.state(['disabled'])
            return
    playBtnAction()
    track_length = int(player.source.duration) + 2
    now_playing.configure(text=f'Now playing: {file_name[:75]}')
    mins = track_length//60
    secs = (track_length % 60)
    length_of_music.configure(text=f'{mins}:{secs:02d}')
    update_seekbar()

def muteBtnAction(event=None):
    global play_image, play_image_inv
    player.volume = 0.0
    volume_val.configure(text='0')
    volume_bar.set(100)
    player.pause()
    music_bar.state(['disabled'])
    play_pause_btn.configure(image=play_image) if theme_btn.cget(
        'text') == 'Theme: Dark' else play_pause_btn.configure(image=play_image_inv)

# Volume button action
def on_volume_change(event):
    player.volume = (100 - event.y) / 100
    volume_bar.set((event.y/volume_bar.winfo_height()) * 100)
    volume_val.configure(text=int(100 - volume_bar.get()))
    if player.volume == 0.0:
        muteBtnAction()

# Seekbar update
def seek_tap(event):
    if player.playing:
        seek_position = event.x / (root.winfo_width()/3)
        total_time = player.source.duration
        player.seek((seek_position * total_time))
        def seekAgain():
            player.seek((seek_position * total_time))
            return
        root.after(100, seekAgain)
        return


# key press
def on_key_press(event):
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
            player.seek(player.time)
            def seekAgain():
                player.seek(player.time + 5)
            root.after(100, seekAgain)
        elif event.keysym == "Left":
            player.seek(player.time)
            def seekAgain():
                player.seek(player.time - 5)
            root.after(100, seekAgain)
        elif event.keysym == "Down":
            drop_down.focus()
        elif event.state & 1 and event.keysym.lower() == "n":
            forwardBtnAction()



# Update seekbar
def update_seekbar():
    global on_close, is_windows, file_name
    if on_close:
        return
    if player.playing and player.source:
        icon.title = file_name[:65]
        current_time = player.time
        total_time = player.source.duration + 2
        if current_time > total_time:
            playBtnAction()
            on_eos = threading.Thread(target=playerEnd)
            on_eos.daemon = True
            on_eos.start()
            return
        mins, secs = divmod(int(current_time), 60)
        seek_of_music.configure(
            text=f'0{mins}:{secs:02d}')
        seek_position = (current_time / total_time) * music_bar.winfo_width()
        music_bar.set(seek_position)
    else:
        icon.title = "True Music"

    root.after(1000, update_seekbar)

def date_modified_btn_action():
    global date_modified_flag, date_modified_cnt, shuffle_flag, file_names , initial_drop_values
    date_modified_cnt = 0
    if shuffle_flag:
        shuffle_flag = False
        trueShuffle_btn.configure(
            text='True Shuffle: Off', foreground='white' if theme_btn.cget('text') == 'Theme: Dark' else 'black')
        menu_items[1] = pystray.MenuItem('True Shuffle: Off', on_click)
        icon.menu = pystray.Menu(*menu_items)        
    if date_modified_flag:
        drop_down['values'] = file_names[::]
        date_modified_btn.configure(text="Date Modified: Disabled")
    else:
        drop_down['values'] = initial_drop_values[::]
        date_modified_btn.configure(text="Date Modified: Enabled")
    date_modified_flag = not date_modified_flag


def search_play_song(event=None):
    if search_song.get().strip() == 'No items match your search':
        return # If search box is empty, do nothing
    global date_modified_cnt, date_modified_flag, initial_drop_values
    if date_modified_flag:
        date_modified_cnt = event.widget.current() + 1
    player.pause()
    index = int(search_song.get().rsplit('searchSelectIndex', 1)[-1])
    root.focus_set()
    threadAction(False, dir_musics[index])


def search(event=None):
    global previous_search_term, initial_drop_values, file_names, date_modified_flag
    search_term = search_box.get().strip().lower()
    if search_term == '':
        drop_down['values'] = initial_drop_values if date_modified_flag else file_names
        drop_down.selection_clear()
        drop_down.focus()
        drop_down.event_generate("<Down>")
    elif search_term != previous_search_term:
        found = False
        search_results = []
        for ind, item in enumerate(dir_musics):
            if search_term in item.lower():
                found = True
                search_results.append(os.path.basename(item) + "                                                                                                                          searchSelectIndex" + str(ind))
        if not found:
            search_results.append("No items match your search")
        drop_down['values'] = tuple(search_results)
        drop_down.selection_clear()
        drop_down.focus()
        drop_down.event_generate("<Down>")
    previous_search_term = search_term


def on_entry_click(event=None):
    if search_box.get() == 'Press Enter To Search':
        search_box.delete(0, "end")  # Remove the placeholder text
        search_box.configure(foreground='White')  # Change text color to #121212


def on_entry_leave(event=None):
    if search_box.get() == '':
        search_box.insert(0, 'Press Enter To Search')
        search_box.configure(foreground='gray')

def directoryBoxThread():
    global directory_box_flag
    if not directory_box_flag:
        directory_thread = threading.Thread(target=openFilePicker)
        directory_thread.daemon = True
        directory_thread.start()


def refreshBtnAction():
    global directory_box_flag, number_of_files, on_close, initial_drop_values, file_names, date_modified_flag
    number_of_files = 0
    if not directory_box_flag:
        refresh_btn.configure(text="Refreshing...", state="disabled")
        directory_box_flag = True
        drop_down['values'] = ('', )
        initial_drop_values = ('', )
        file_names = ('', )
        dir_musics.clear()
        directories = [d.strip() for d in directory_box.get("1.0", END).split(",") if d.strip()]
        if not directories:
            messagebox.showerror("Error", "Please select a directory to refresh.")
            refresh_btn.configure(text="Refresh", state="normal")
            directory_box_flag = False
            return
        for Directory in directories:
            Directory = Directory.replace("/", "//")
            tmp, date_file_names, tmp_num = get_all_files(Directory)
            if not tmp_num or date_file_names == []:
                messagebox.showerror("Error", "Permission Denied To Access Directory")
                refresh_btn.configure(text="Refresh", state="normal")
                directory_box_flag = False
                return
            res = ('', )
            for x, i in enumerate(date_file_names):
                if not on_close:
                    res += tuple([str(i) + '                                                                                                                          searchSelectIndex' + str(x)])
                else:
                    return
            file_names += res[1::]
            dir_musics.extend(tmp)
            res = ('', )
            number_of_files += tmp_num
            date_file_names = sorted(enumerate(zip(tmp, date_file_names)), key = lambda x: os.path.getmtime(x[1][0]), reverse=True)
            for ind, i in date_file_names:
                if not on_close:
                    initial_drop_values += tuple([str(i[1]) + '                                                                                                                          searchSelectIndex' + str(ind)])
                else:
                    return
        if on_close:
            return
        file_names = file_names[1::]   
        drop_down['values'] = file_names
        refresh_btn.configure(text="Refresh", state="normal")
        directory_box_flag = False

def refreshThreadAction():
    global directory_box_flag
    if not directory_box_flag:
        refresh_thread = threading.Thread(target=refreshBtnAction)
        refresh_thread.daemon = True
        refresh_thread.start()

def set_focus(event):
    if event.widget == root:
        root.focus_set()

def readData():
    global Directory, dir_musics, drop_down, initial_drop_values, number_of_files, file_names, on_close
    with open(data_file, 'r', encoding='utf-8') as f:
        number_of_files = f.readline().strip()
        if number_of_files != '':
            number_of_files = int(number_of_files)
            if number_of_files > 0:
                rememberPathBtnAction()
                directory_box.config(state=NORMAL)
                directory_box.insert(END, f.readline().strip())
                directory_box.config(state=DISABLED)
                tmp = directory_box.index("end-1c").split(".")
                if float(tmp[1])*12.4181818182 > (root.winfo_width()):
                    directory_box.config(height=2)
                    refresh_btn.place(rely=0.41)
                Directory = '\n'
                current_index = 0
                for line in f:
                    line = line.strip()
                    if line == 'DateModifiedStart' or on_close or line == '':
                        break
                    if line:
                        dir_musics.append(line)
                        file_names += (os.path.basename(line)+ "                                                                                                                          searchSelectIndex" + str(current_index),)
                        current_index += 1
                if on_close:
                    return
                play_thread = threading.Thread(target=threadAction)
                play_thread.daemon = True
                play_thread.start() 
                file_names = file_names[1::]   
                drop_down['values'] = file_names
                for line in f:
                    line = line.strip()
                    if line and not on_close:
                        initial_drop_values += (line,)
                    else:
                        break
            else:
                root.deiconify()
                root.lift()
                root.focus_force()
        else:
            root.deiconify()
            root.lift()
            root.focus_force()

read_data_thread = threading.Thread(target=readData)
read_data_thread.daemon = True

# Style
style = ttk.Style()
style.configure("myStyle.Horizontal.TScale", background='#121212')
style.configure("myStyle.Vertical.TScale", background='#121212')


# Root
clear_btn = Button(root, text="Clear All",
                   command=clearDirectory, padx=6, font=("Corbel", 10))

clear_btn.configure(background='#121212', foreground='white',
                    activebackground='#121212', relief="sunken", borderwidth=0, activeforeground='grey')
clear_btn.place(relx=0.83, rely=0.58,  anchor=E)
myTip4 = CreateToolTip(clear_btn, "Clear all the files in the directory "
                       "and Search Box and Current Queue")  # noqa



remember_btn = Button(root, text="Store Path: Disabled",
                      command=rememberPathBtnAction, padx=6, font=("Corbel", 10))

remember_btn.configure(background='#121212', foreground='white',
                       activebackground='#121212', relief="sunken", borderwidth=0, activeforeground='grey')
remember_btn.place(relx=0.19, rely=0.58,  anchor=W)
myTip2 = CreateToolTip(remember_btn, "Store the path of the folder you selected and"
                       "it will be autoplay next time you open the app")  # noqa



date_modified_flag = False



date_modified_btn = Button(root, text="Date Modified: Disabled",
                      command=date_modified_btn_action, padx=6, font=("Corbel", 10))

date_modified_btn.configure(background='#121212', foreground='white',
                       activebackground='#121212', relief="sunken", borderwidth=0, activeforeground='grey')
date_modified_btn.place(relx=0.55, rely=0.58,  anchor=CENTER)
myTip1 = CreateToolTip(date_modified_btn, "Sorts the songs by date modified")  # noqa

now_playing = Label(root, text="Now playing: ", font=("Corbel", 10))
now_playing.place(relx=0.5, rely=0.33, anchor=CENTER)
now_playing.configure(background="#121212", foreground="#f0f0f0")


seek_of_music = Label(root, text="00:00", font=("Verdana", 8))
seek_of_music.place(relx=0.3, rely=0.25, anchor=CENTER)
seek_of_music.configure(background="#121212", foreground="#f0f0f0")

length_of_music = Label(root, text="0:00", font=("Verdana", 8))
length_of_music.place(relx=0.7, rely=0.25, anchor=CENTER)
length_of_music.configure(background="#121212", foreground="#f0f0f0")


directory_box = Text(root, foreground="#121212", highlightthickness="1",
                     background="#0D0901", state=DISABLED)
directory_box.configure(highlightcolor='lightblue', highlightthickness=1,
                        highlightbackground='lightblue', foreground='white', height=1)
directory_box.place(relwidth=0.65, relx=0.51, rely=0.5, anchor=CENTER)



Directory.replace("/", "//")

previous_search_term = ''

search_box = Entry(root, foreground='gray',
                   background='#3f3f40', bd=1, relief=GROOVE)
search_box.configure(highlightthickness=0)
search_box.place(anchor=W, relwidth=0.25, relx=0.05, rely=0.67)
search_box.insert(0, 'Press Enter To Search')  # Insert the placeholder text
search_box.configure(foreground='gray')
search_box.bind("<Return>", search)
search_box.bind("<FocusIn>", on_entry_click)
search_box.bind("<FocusOut>", on_entry_leave)



try:
    arrow_lbl = Label(root, text='⇌', font=('Corbel', 14))
    arrow_lbl.configure(background='#121212', foreground='White')
    arrow_lbl.place(anchor=CENTER, relx=0.33, rely=0.67)
except:
    pass



search_song = StringVar()
drop_down = ttk.Combobox(root, width=27, textvariable=search_song, state='readonly')
drop_down.place(anchor=E, relx=0.85, rely=0.67, relwidth=0.5)
drop_down.configure(foreground='Gray')
drop_down.set('All Music Files appear here')
drop_down.bind('<<ComboboxSelected>>', search_play_song)
drop_down['values'] = ('', )

music_bar = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL,
                      style='myStyle.Horizontal.TScale', cursor='crosshair')
# music_bar.bind('<Button-1>', seek_tap)
music_bar.bind('<ButtonRelease-1>', seek_tap)
music_bar.place(relx=0.5, rely=0.2, anchor=CENTER, relwidth=0.33)
music_bar.state(['disabled'])


directory_box_flag = False




selectDirectory = Button(root, text="Select Music Folder", command=directoryBoxThread,
                         width=root.winfo_width()//50, padx=6, wraplength=root.winfo_width()//6, font=("Corbel", 10))


selectDirectory.configure(background='#121212', foreground='White',relief="ridge", borderwidth=0, activeforeground='grey', activebackground='#121212')

def on_enter_direc(e):
    selectDirectory.configure(borderwidth=1)
def on_leave_direc(e):
    selectDirectory.configure(borderwidth=0)
selectDirectory.bind("<Enter>", on_enter_direc)
selectDirectory.bind("<Leave>", on_leave_direc)

selectDirectory.place(relx=0.01, rely=0.5, anchor=W,
                      relwidth=0.17, relheight=0.15)



refresh_btn = Button(root, text="Refresh",
                      command=refreshThreadAction, padx=6, font=("Corbel", 10))
refresh_btn.configure(background='#121212', foreground='white',
                       activebackground='#121212', relief="sunken", borderwidth=0, activeforeground='grey')

refresh_btn.place(relx=0.19, rely=0.43,  anchor=W)
myTip3 = CreateToolTip(refresh_btn, "Refresh Music List"
                       "and Search Box")

volume_bar = ttk.Scale(root, from_=0, to=100, orient=VERTICAL,
                       style='myStyle.Vertical.TScale', cursor='right_ptr')
volume_bar.set(0)
volume_bar.bind('<Button-1>', on_volume_change)
volume_bar.bind('<ButtonRelease-1>', on_volume_change)
volume_bar.place(relx=0.85, rely=0.19, anchor=W, relheight=0.25)


volume_image = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'volume.png'))
volume_image_inv = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'volume_inverted.png'))


volume_icon = Label(root, image=volume_image)
volume_icon.place(relx=0.91, rely=0.18, anchor=W)
volume_icon.configure(borderwidth=0, background="#121212")
volume_icon.bind('<Button-1>', muteBtnAction)

volume_val = Label(root, text='100')
volume_val.place(relx=0.95, rely=0.18, anchor=W)
volume_val.configure(background="#121212", foreground="#f0f0f0", borderwidth=0)


autoplay_btn = Button(root, text="Autoplay: Enabled",
                      command=autoPlay, padx=6, pady=6, font=("Corbel", 10))

autoplay_btn.configure(background='#121212', foreground='white',
                       activebackground='#121212', relief="sunken", borderwidth=1, activeforeground='grey')


autoplay_btn.place(relx=0.99, rely=0.85, anchor=E, relheight=0.15, width=140)

repeat_btn = Button(root, text="Repeat: Disabled",
                    command=autoRepeat, padx=6, font=("Corbel", 10))
repeat_btn.configure(background='#121212', foreground='white',
                     activebackground='#121212', relief="ridge", borderwidth=1, activeforeground='grey')


repeat_btn.place(relx=0.5, rely=0.85, anchor=CENTER, relheight=0.15, width=120)

always_on_top_btn = Button(root, text="Always On Top: Disabled",
                           command=alwaysOnTop, padx=6, pady=6, font=("Corbel", 10))

always_on_top_btn.configure(background='#121212', foreground='white',
                            activebackground='#121212', relief="ridge", borderwidth=1, activeforeground='grey')


always_on_top_btn.place(relx=0.01, rely=0.85, anchor=W, relheight=0.15, width=150)



theme_btn = Button(root, text="Theme: Dark",
                   command=changeTheme, font=("Corbel", 10))
theme_btn.configure(background='#121212', foreground='white', activebackground='#121212',
                    relief="sunken", borderwidth=0, activeforeground='gray')
theme_btn.place(anchor=W, relx=0.01, rely=0.1, relheight=0.11, relwidth=0.11)



def hotkeys():
    global hotkey_flag
    if hotkey_flag:
        hotkey_flag = False
        menu_items[7] = pystray.MenuItem('Hotkeys: Off', on_click)
        icon.menu = pystray.Menu(*menu_items)
        hotkey_btn.configure(text="Hotkeys: Off")
    else:
        hotkey_flag = True
        menu_items[7] = pystray.MenuItem('Hotkeys: On', on_click)
        icon.menu = pystray.Menu(*menu_items)
        hotkey_btn.configure(text="Hotkeys: On")
        mediaKeysThread = threading.Thread(target=checkMediaKeys)
        mediaKeysThread.daemon = True
        mediaKeysThread.start()

hotkey_btn = Button(root, text="Hotkeys: Off",
                   command=hotkeys, font=("Corbel", 10))
hotkey_btn.configure(background='#121212', foreground='white', activebackground='#121212',
                    relief="sunken", borderwidth=0, activeforeground='gray')
hotkey_btn.place(anchor=W, relx=0.15, rely=0.1, relheight=0.11, relwidth=0.11)


play_image = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'play.png'))

play_image_inv = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'play_inverted.png'))

pause_image = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'pause.png'))

pause_image_inv = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'pause_inverted.png'))

play_pause_btn = Button(root, image=play_image, command=playBtnAction)
play_pause_btn.configure(relief="sunken", borderwidth=0,
                         background='#121212', activebackground='#121212')
play_pause_btn.place(relx=0.15, rely=0.2, anchor=CENTER)

forward_image = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'forward.png'))

forward_image_inv = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'forward_inverted.png'))

forward_btn = Button(root, image=forward_image, command=forwardBtnAction)
forward_btn.configure(relief="sunken", borderwidth=0,
                      background='#121212', activebackground='#121212')
forward_btn.place(relx=0.25, rely=0.2, anchor=CENTER)


previous_image = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'previous.png'))

previous_image_inv = PhotoImage(file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'previous_inverted.png'))

previous_btn = Button(root, image=previous_image, command=previousBtnAction)
previous_btn.configure(relief="sunken", borderwidth=0,
                       background='#121212', activebackground='#121212')
previous_btn.place(relx=0.05, rely=0.2, anchor=CENTER)



trueShuffle_btn = Button(root, text="True Shuffle: On",
                         command=trueShuffle, padx=6, pady=6, font=("Corbel", 10))
trueShuffle_btn.configure(background='#121212',relief="groove", borderwidth=0, activeforeground='grey', activebackground='#121212', foreground='#2dd128')
def on_enter_shuffle(e):
    trueShuffle_btn.configure(borderwidth=1)
def on_leave_shuffle(e):
    trueShuffle_btn.configure(borderwidth=0)
trueShuffle_btn.bind("<Enter>", on_enter_shuffle)
trueShuffle_btn.bind("<Leave>", on_leave_shuffle)

trueShuffle_btn.place(relx=0.99, rely=0.5, anchor=E,
                      relwidth=0.15, relheight=0.15)


def on_click(icon, item):
    global on_close
    if on_close:
        icon.stop()
        return
    if item.text == 'Quit':
        on_close = True
        icon.stop()
        return
    elif item.text == 'Play/Pause':
        playBtnAction()
    elif item.text == 'Next Track':
        forwardBtnAction()
    elif item.text == 'Previous Track':
        previousBtnAction()
    elif item.text == 'True Shuffle: On' or item.text == 'True Shuffle: Off':
        trueShuffle()
    elif item.text == 'Repeat: On' or item.text == 'Repeat: Off':
        autoRepeat()
    elif item.text == 'Autoplay: On' or item.text == 'Autoplay: Off':
        autoPlay()
    elif item.text == 'Hotkeys: On' or item.text == 'Hotkeys: Off':
        hotkeys()

def showRoot(icon=None, item=None):
    if root.state() == 'normal':
        root.withdraw()
    else:
        root.deiconify()
        root.lift()
        root.focus_force()


icon = pystray.Icon(icon=PIL.Image.open(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'resurrection.ico')), name = 'True Music', title="True Music")

menu_items = [
    pystray.MenuItem('Show/Hide', action=showRoot, default=True),
    pystray.MenuItem('True Shuffle: On', on_click),
    pystray.MenuItem('Repeat: Off', on_click),
    pystray.MenuItem('Autoplay: On', on_click),
    pystray.MenuItem('Next Track', on_click),
    pystray.MenuItem('Play/Pause', on_click),
    pystray.MenuItem('Previous Track', on_click),
    pystray.MenuItem('Hotkeys: Off', on_click),
    pystray.MenuItem('Quit', on_click),
]

def pystrayTray():
    global icon, shuffle_flag
    icon.menu = pystray.Menu(*menu_items)
    icon.run()
    onClosing()
    return

is_windows = os.name == 'nt'

try:
    if is_windows:
        root.iconbitmap(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'resurrection.ico'))
    else:
        root.iconbitmap('@'+os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'trueShuffle.xbm'))
except:
    messagebox.showerror('Iconbitmap icon not found',
                         'Window Icon Cannot be loaded')

hotkey_flag = False

def checkMediaKeys():
    global on_close, hotkey_flag
    if on_close:
        return
    def on_press(key):
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


def onMinimize(event):
    root.withdraw()

def onClosing():
    global on_close, Directory, icon
    os.remove(LOCK_FILE)
    on_close = True
    try:
        Directory = directory_box.get("1.0", END)
        store_path_thread.start()
        icon.stop()
        played.clear()
        player.pause()
        pyglet.app.exit()
        root.destroy()
    except RuntimeError:
        os.kill(os.getpid(), 9)


SystemTrayThread = threading.Thread(target=pystrayTray)
SystemTrayThread.daemon = True
SystemTrayThread.start()



root.bind("<KeyPress>", on_key_press)
root.bind("<space>", playBtnAction)
root.bind("<Configure>", updateSize)
root.protocol("WM_DELETE_WINDOW", onClosing)
root.bind("<Unmap>", onMinimize)
root.bind("<Button-1>", set_focus)
read_data_thread.start()
root.mainloop()
