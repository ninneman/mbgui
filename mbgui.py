#!/usr/bin/python3

# mbgui: a GUI front-end to a subset of MB-System functionality.

# <copyright info here>

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

class App(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.infile = tk.Entry(self)
        self.outdir = tk.Entry(self)
        self.input_selectors = None
        self.outtypes = {
            "xyz": tk.IntVar(),
            "ascii": tk.IntVar(),
            "geotiff": tk.IntVar(),
        }
        self.grid()
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
            final_output = outfile_full_base + ".txt"
            print("converting {0} to {1}".format(selector, final_output))
            #logfile = open("log", "w")
            with open(datalist, "w") as dlf:
                subprocess.call(
                    ["mbdatalist", "-F", "0", "-I", selector],
                    stdout = dlf,
                    stderr = None,
                    env = self.cmd_env
                )
            subprocess.call(
                ["mbdatalist", "-F", "-1", "-I", datalist, "-N"],
                stdout = None,
                stderr = None,
                env = self.cmd_env
            )
            subprocess.call(
                ["mblist", "-F", "-1", "-I", datalist, "-D2", "-X", final_output],
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
        tk.Label(self, text = "Input file:").grid(row = 0)
        self.infile.grid(row = 1, column = 0)
        tk.Button(self, text = "Browse...", command = self.get_input_files).grid(row = 1, column = 1)
        tk.Label(self, text = "Output directory:").grid(row = 2)
        self.outdir.grid(row = 3, column = 0)
        tk.Button(self, text = "Browse...", command = self.get_output_dir).grid(row = 3, column = 1)
        tk.Label(self, text = "Output types:").grid(row = 4)
        #tk.Checkbutton(self, text = "xyz", variable = self.outtypes["xyz"]).grid(row = 5, column = 0)
        #tk.Checkbutton(self, text = "ascii", variable = self.outtypes["ascii"]).grid(row = 5, column = 1)
        #tk.Checkbutton(self, text = "GeoTIFF", variable = self.outtypes["geotiff"]).grid(row = 5, column = 2)
        tk.Button(self, text = "Quit", command = self.quit).grid(row = 6, column = 0)
        tk.Button(self, text = "Convert", command = self.convert).grid(row = 6, column = 1)

root = tk.Tk()
app = App(master = root)
app.master.title("MB-System file converter")
app.mainloop()
