'''
Created on 2013-4-12

@author: Administrator
'''


from Tkinter import *
def on_click():
    label['text'] = text.get()
root = Tk(className = "lijianwei")
label = Label(root)
label['text'] = 'be on your own'
label.pack()
text = StringVar()
text.set("change to what ?")
entry = Entry(root)
entry['textvariable'] = text
entry.pack()
button = Button(root)
button['text'] = 'change it'
button['command'] = on_click
button.pack()
root.mainloop()