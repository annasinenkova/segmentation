from tkinter import *


if __name__ == '__main__':
    root = Tk()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    total_width = (screen_width // 2) - (500 // 2)
    total_height = (screen_height // 2) - (300 // 2)
    
    root.title('Segmentation')
    root.geometry(f'{500}x{300}+{total_width}+{total_height}')
    
    root.mainloop()

