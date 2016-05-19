import uitest
import tkinter as Tk

root = Tk.Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

ui = uitest.UI_NavMenu.Anzeigen(root, 1, 4, "12:39:40", "ok")
root.mainloop()