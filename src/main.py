"""The main file that runs the application."""

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

from segmentation import segmentation


def set_screen_shape(root: tk.Tk, width: int, height: int) -> None:
    """Set the screen size."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    total_width = (screen_width // 2) - (width // 2)
    total_height = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{total_width}+{total_height}')


def image_upload() -> None:
    """Load an image and display a segmented image on the screen."""
    path = filedialog.askopenfilename(
           filetypes=[('Image File', '.jpg .png .jpeg')]
    )

    if not len(path):
        return

    img = Image.open(path)
    upload_bttn.destroy()

    raw_img = ImageTk.PhotoImage(img)
    img_show = tk.Label(root, image=raw_img)
    img_show.image = raw_img

    set_screen_shape(root, img.width, img.height)
    img_show.pack(side='bottom', fill='both', expand='yes')

    segmented_img = segmentation(path)

    segmented_img = ImageTk.PhotoImage(segmented_img)
    segmented_img_show = tk.Label(root, image=segmented_img)
    segmented_img_show.image = segmented_img
    img_show.destroy()
    segmented_img_show.pack(side='bottom', fill='both', expand='yes')


if __name__ == '__main__':
    root = tk.Tk()

    root.title('Segmentation')

    set_screen_shape(root, 500, 300)

    upload_bttn = tk.Button(root, text='Choose image', command=image_upload)
    upload_bttn.pack(side='bottom', pady=50)

    root.mainloop()
