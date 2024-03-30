#!/usr/bin/env python3
### Author: Ahmed Tijani Akinfalabi
### Date: 2024-02-02
### Name: UniProt-Parser 

"""Uniprot-Parser by Ahmed Tijani Akinfalabi, 2024
Extract information from Uniprot data files.
-------------------------------------------
Optional arguments are:
    --help - display this help page
    --go   - show a protein id to GO id mapping
    --doi  - show a protein id to DOI mapping (not used today)

Mandatory arguments are:
    FILE - one or more compressed or uncompressed Uniprot data files \n
"""

import sys, os, gzip, re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mbox

from guibaseclass import GuiBaseClass
import parser_1 as txt

class UniProtGui(GuiBaseClass):

    def __init__(self,root):
        super().__init__(root)

        self.lastdir = None
        self.folder_path = tk.StringVar()
        self.filetypes = [('UniProt Files', '*.dat'), ('zipped UniProt Files', '*.gz'), ('Text Files', '*.txt'), ('All Files', '*.*')]
        
        fmenu = self.getMenu('File')
        fmenu.insert_command(0,label = "Open File ...", underline = 0,command = self.fileOpen)
        
        frame = self.getFrame()
        self.addStatusBar()
        self.progress(50)

        # Create and add paned window
        self.paned = tk.PanedWindow(frame, orient = tk.HORIZONTAL, sashrelief = tk.RAISED)
        self.paned.pack(fill = tk.BOTH, expand = True)

        # Create, configure and add the first listbox
        self.listbox_1 = tk.Listbox(self.paned, exportselection=False)  # selectmode=tk.SINGLE :allows single selection
        self.paned.add(self.listbox_1)

        # Create, configure and add the second listbox
        self.listbox_2 = tk.Listbox(self.paned, selectmode=tk.SINGLE, exportselection=False)  # selectmode=tk.SINGLE
        self.paned.add(self.listbox_2)

        self.listbox_2.insert(tk.END, "GO")
        self.listbox_2.insert(tk.END, "KEGG")
        self.listbox_2.insert(tk.END, "DOI")

        # Bind events to listboxes
        self.listbox_1.bind("<<ListboxSelect>>", self.selections)       # Filename display
        self.listbox_2.bind("<<ListboxSelect>>", self.selections)       # lisbox selection

        # Text widget with scrollbar on the left side
        self.text = tk.Text(self.paned)
        self.paned.add(self.text)


        # create a frame and place both the text and scrol bar and then put it on the paned window.

        # If i use your scrolled module, then i put the frame, and then text widget into the frame. and then i called scrolled to the text widget.
        # The outer frame must be added to the paned window
        
        # scrollbar_text = tk.Scrollbar(frame, command = self.text.yview)
        # scrollbar_text.pack(side = "left", fill = "y")
        # self.text.config(yscrollcommand = scrollbar_text.set)
             
        # Adjust column and row weights
        for i in range(3):
            root.columnconfigure(i, weight=1)
        root.rowconfigure(1, weight=1)

    def folder_open(self):
        if self.folder_path is not None:
            selected_folder = fd.askdirectory()
            if selected_folder:
                self.folder_path.set(selected_folder)
                # self.message(selected_folder)
        return selected_folder

    def load_files(self, folder):
        folder_path = folder        #.get()
        self.listbox_1.delete(0, tk.END)
        self.message(folder_path)
        for filenames in os.listdir(folder_path):
            if filenames.endswith(('.dat', '.gz', '.txt')):
                self.listbox_1.insert(tk.END, os.path.join(folder_path, filenames))
                
    def fileOpen(self):
        if self.lastdir is not None:
            initialdir = self.lastdir
        else:
            initialdir = os.getcwd()
        self.file = fd.askopenfilename(initialdir = initialdir, title = "Select a UniProt file", filetypes=self.filetypes)
        if self.file:
            self.message(self.file)
            # self.listbox_1.delete(0, tk.END)      # I don't want to delete the initially selected files.
            self.listbox_1.insert(tk.END, self.file)

    def selections(self, event):
        # if self.file:
        selected_index_1 = self.listbox_1.curselection()
        if selected_index_1:
            selected_file = self.listbox_1.get(selected_index_1[0])
        open_function = gzip.open if selected_file.endswith('.gz') else open

        with open_function(selected_file, "r") as file:
            content = file.read()
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', content)

        # The second listbox selection
        selected_index_2 = self.listbox_2.curselection()
            
        if selected_index_1 and selected_index_2:
            selected_option = self.listbox_2.get(selected_index_2[0])

            class_instance = txt.UniProtParse()
            self.text.delete("1.0", tk.END)

            # Process based on the selected options
            if selected_option == "GO":
                entries = class_instance.get_go_ids(selected_file)
            elif selected_option == "KEGG":
                entries = class_instance.get_kegg_ids(selected_file)
            
            for entry in entries:
                id_value = entry['ID']
                values = entry[selected_option] if entry[selected_option] else ['NA']

                for value in values:
                    self.text.insert(tk.END, f'{id_value} \t {value}\n')


    def main(self, argv):
        class_instance = txt.UniProtParse()
        class_instance.main(argv)

if __name__ == "__main__":
    root   = tk.Tk()
    uniprot_class = UniProtGui(root)
    # root.geometry('1000x630')
    root.title("UniProt Parser App by Ahmed")

    if len(sys.argv) > 1:
        folder_path = sys.argv[-1]  # The last element is the folder path
        if os.path.isdir(folder_path):
            uniprot_class.folder_path.set(folder_path)
            uniprot_class.load_files(folder_path)
    else:
        folder_path = uniprot_class.folder_open()
        uniprot_class.load_files(folder_path)
        
    uniprot_class.mainLoop()
