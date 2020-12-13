from PIL import Image, ImageTk
from tkinter import Tk


def read_dict(file):
    """Open the file given as parameter and returns a list made from its lines"""
    text = ""
    try:
        f = open(file)
        text = f.read().upper().split('\n')
        f.close()
    except IOError:
        print("File '{}' does not exist or has the wrong format.".format(file))
        exit(0)
    return text


def create_letter_images():
    """Opens the 'letters.png' file, computes a list of references for each letter image and returns it"""

    letter_img = Image.open("img/letters.png")
    letter_ref = []
    for x in range(26):
        img = letter_img.crop((x * 23, 0, (x + 1) * 23, 23)).resize((30, 30))
        img_pk = ImageTk.PhotoImage(img)

        letter_ref.append(img_pk)
    return letter_ref


def get_geometry(main):
    """Computes the screen geometry and returns it."""

    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.destroy()

    # Set main window on top
    main.attributes('-topmost', True)
    main.update()
    main.attributes('-topmost', False)

    return geometry
