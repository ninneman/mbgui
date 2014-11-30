#!/usr/bin/python3

# MB-System file converter
# A GUI front-end to a subset of MB-System functionality.
# Copyright 2014, Jason S. Ninneman and Kelly Monteleone
# <license info here>

import tkinter as tk
import tkinter.filedialog as tkfd

class App(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.infile = tk.Entry(self)
        self.outdir = tk.Entry(self)
        self.outtypes = {
            "xyz": tk.IntVar(),
            "ascii": tk.IntVar(),
            "geotiff": tk.IntVar(),
        }
        self.grid()
        self.showWidgets()

    def get_type_states(self):
        result = {}
        for k, v in self.outtypes.items():
            number = v.get()
            if number == 1:
                result[k] = True
            else:
                result[k] = False
        return result

    def convert(self):
        print("converting: {0}".format(self.infile.get()))
        print("destination: {0}".format(self.outdir.get()))
        print("output types: {0}".format(self.get_type_states()))
        return None

    def get_input_file(self):
        options = {
            "title": "Select file",
        }
        selector = tkfd.askopenfilename(**options)
        self.infile.delete(0, tk.END)
        self.infile.insert(0, selector)
        return None

    def get_output_dir(self):
        options = {
            "title": "Select directory",
        }
        selector = tkfd.askdirectory(**options)
        self.outdir.delete(0, tk.END)
        self.outdir.insert(0, selector)
        return None

    def showWidgets(self):
        tk.Label(self, text = "Input file:").grid(row = 0)
        self.infile.grid(row = 1, column = 0)
        tk.Button(self, text = "Browse...", command = self.get_input_file).grid(row = 1, column = 1)
        tk.Label(self, text = "Output directory:").grid(row = 2)
        self.outdir.grid(row = 3, column = 0)
        tk.Button(self, text = "Browse...", command = self.get_output_dir).grid(row = 3, column = 1)
        tk.Label(self, text = "Output types:").grid(row = 4)
        tk.Checkbutton(self, text = "xyz", variable = self.outtypes["xyz"]).grid(row = 5, column = 0)
        tk.Checkbutton(self, text = "ascii", variable = self.outtypes["ascii"]).grid(row = 5, column = 1)
        tk.Checkbutton(self, text = "GeoTIFF", variable = self.outtypes["geotiff"]).grid(row = 5, column = 2)
        tk.Button(self, text = "Quit", command = self.quit).grid(row = 6, column = 0)
        tk.Button(self, text = "Convert", command = self.convert).grid(row = 6, column = 1)

root = tk.Tk()
app = App(master = root)
app.master.title("MB-System file converter")
app.mainloop()
