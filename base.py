# Import module
from tkinter import *
from tkcalendar import Calendar

# Create object
root = Tk()

# Adjust size
root.geometry( "600x400" )

# Change the label text
def show():
    label.config(text = 'Observatories Selected')
	# label.config(text = clicked.get())    
    # # label2.config(obs2 = clicked2.get())

# Dropdown menu options
options = [
	"I-LOFAR",
    "LOFAR-SE"
]

# datatype of menu text
clicked = StringVar()
clicked2 = StringVar()

# initial menu text
clicked.set("Observatory 1")
clicked2.set("Observatory 2")

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()
drop2 = OptionMenu( root , clicked2 , *options )
drop2.pack()

# Create button, it will change label text
button = Button( root , text = "Select" , command = show ).pack()

# Create Label
label = Label( root , text = " " )
label.pack()
label2 = Label( root , text = " " )
label2.pack()

# # Add Calendar
# cal = Calendar(root, selectmode = 'day',
#                year = 2022, month = 5,
#                day = 22)
 
# cal.pack(pady = 20)
 
# def grad_date():
#     date.config(text = "Selected Date is: " + cal.get_date())
 
# # Add Button and Label
# Button(root, text = "Get Date",
#        command = grad_date).pack(pady = 20)
 
# date = Label(root, text = "")
# date.pack(pady = 20)

# Execute tkinter
root.mainloop()
