import tkinter as tk


fields = 'Observatory 1', 'Observatory 2', 'Observation start', 'Observation end'

def fetch(entries): # - fetching entries from the fields list 
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text)) 

def makeform(root, fields): # - making a form from those entries 
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__': # -- executing root 
    root = tk.Tk()
    ents = makeform(root, fields)

    # --- dropdown menu 
    master = tk()
    variable = StringVar(master)
    variable.set("one") # default value

    w = OptionMenu(master, variable, "one", "two", "three")
    w.pack()

    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Display',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()