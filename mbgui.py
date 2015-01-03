#!/usr/bin/python3

# mbgui: a GUI front-end to a subset of MB-System functionality.

# Copyright 2014, The Federation of Earth Science Information Partners.
# Written and designed by Jason Ninneman and Kelly Monteleone.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

mbs_bin_dir = "/home/ninneman/Documents/freelance/mbsystem-5.4.2209/src/utilities"

import tkinter as tk
import tkinter.filedialog as tkfd
import os
import subprocess
import tempfile
import platform
import sys

class App(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.infile = tk.Entry(self)
        self.outdir = tk.Entry(self)
        self.input_selectors = None
        self.txttype = tk.StringVar()
        self.txttype.set("txt")
        self.pack(fill = tk.X, expand = True)
        self.showWidgets()
        self.cmd_env = {"PATH": "{0}:{1}".format(mbs_bin_dir, os.environ["PATH"])}

    def get_type_states(self):
        """Return the output type list as a dictionary of booleans."""
        result = {}
        for k, v in self.outtypes.items():
            number = v.get()
            if number == 1:
                result[k] = True
            else:
                result[k] = False
        return result

    def quote(self, string):
        """Wrap a string in double quotes."""
        return "\"" + string + "\""

    def convert(self):
        """Convert the input file to the output type(s)."""

        for selector in self.input_selectors:
            outfile_base, _ = os.path.splitext(os.path.basename(selector))
            outfile_full_base = os.path.join(self.outdir.get(), outfile_base)
            datalist = outfile_full_base + ".datalist"
            final_output = outfile_full_base + "." + self.txttype.get()
            print("converting {0} to {1}".format(selector, final_output))
            #logfile = open("log", "w")
            if platform.system() == "Windows":
                suffix = ".exe"
            else:
                suffix = ""
            with open(datalist, "w") as dlf:
                subprocess.call(
                    ["mbdatalist" + suffix, "-F", "0", "-I", selector],
                    stdout = dlf,
                    stderr = None,
                    env = self.cmd_env
                )
            subprocess.call(
                ["mbdatalist" + suffix, "-F", "-1", "-I", datalist, "-N"],
                stdout = None,
                stderr = None,
                env = self.cmd_env
            )
            subprocess.call(
                ["mblist" + suffix, "-F", "-1", "-I", datalist, "-D2", "-X", final_output],
                stdout = None,
                stderr = None,
                env = self.cmd_env
            )
            #logfile.close()
            
        return None

    def get_input_files(self):
        """Pop up the 'open file' dialog, assign whatever's picked to the input file entry box, and set an attribute with an iterable of the file selectors."""
        options = {
            "title": "Select file",
        }
        selectors = tkfd.askopenfilenames(**options)
        self.input_selectors = selectors
        self.infile.delete(0, tk.END)
        self.infile.insert(0, selectors)
        return None

    def get_output_dir(self):
        """Pop up the 'open directory' dialog, and assign whatever's picked to the output directory entry box."""
        options = {
            "title": "Select directory",
        }
        selector = tkfd.askdirectory(**options)
        self.outdir.delete(0, tk.END)
        self.outdir.insert(0, selector)
        return None

    def showWidgets(self):
        """Lay out the various widgets."""
        
        tk.Label(self, text = "Input file:").grid(row = 0, column = 0, sticky = tk.E)
        self.infile.grid(row = 0, column = 1, sticky = tk.W + tk.E)
        tk.Button(self, text = "Browse...", command = self.get_input_files).grid(row = 0, column = 2)
        
        tk.Label(self, text = "Output directory:").grid(row = 1, column = 0, sticky = tk.E)
        self.outdir.grid(row = 1, column = 1, sticky = tk.W + tk.E)
        tk.Button(self, text = "Browse...", command = self.get_output_dir).grid(row = 1, column = 2)
        
        tk.Label(self, text = "Output type:").grid(row = 2, column = 0, sticky = tk.E)
        tk.Radiobutton(self, text = "ascii", variable = self.txttype, value = "ascii").grid(row = 2, column = 1)
        tk.Radiobutton(self, text = "txt", variable = self.txttype, value = "txt").grid(row = 2, column = 2)
        tk.Radiobutton(self, text = "xyz", variable = self.txttype, value = "xyz").grid(row = 2, column = 3)
        
        tk.Button(self, text = "Quit", command = self.quit).grid(row = 3, column = 0)
        tk.Button(self, text = "Convert", command = self.convert).grid(row = 3, column = 1)
        self.grid_columnconfigure(1, weight = 1)

root = tk.Tk()
app = App(master = root)
app.master.title("MB-System file converter")
app.mainloop()
