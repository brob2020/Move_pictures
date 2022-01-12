from tkinter import *
from PIL import Image,ImageTk

window = Tk() 
window.title('first app ')


my_img = ImageTk.PhotoImage(Image.open("20201219_151029.jpg"))
my_label = Label(image=my_img)
my_label.pack()


window.mainloop()
