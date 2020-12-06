from PIL import Image, ImageTk


def read_dict(file):
    with open(file) as f:
        text = f.read().upper().split('\n')
        f.close()
        return text


def create_letter_images():
    letter_img = Image.open("img/letters.png")
    letter_ref = []
    for x in range(26):
        img = letter_img.crop((x * 23, 0, (x + 1) * 23, 23)).resize((30, 30))
        img_pk = ImageTk.PhotoImage(img)

        letter_ref.append(img_pk)
    return letter_ref
