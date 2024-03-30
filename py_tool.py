import os

from tkinter import *
from tkinter import ttk as tk
from tkinter import messagebox

from zipfile import ZipFile
import rarfile
import csv
import collections
import subprocess
from PyPDF2 import PdfFileReader

"""
    Label	A widget used to display text on the screen
    Button	A button that can contain text and can perform an action when clicked
    Entry	A text entry widget that allows only a single line of text
    Text	A text entry widget that allows multiline text entry
    Frame	A rectangular region used to group related widgets or provide padding between widgets
"""

"""
    TODO
    STEP 1: DONE
        - open interface asking for path to files, also having a button triggering path finding on OS
        - lists files and folders in current path
    STEP 2: DONE
        - allows to read .zip content, other files and zip files.
        - read over texts and return used words
    STEP 3:
        - visualize .jpeg and .png files
    .csv, .zip, file reader + search keys words + non-linear graph
"""



def test():
    def frame_label_button(master_frm):
        # Module cannot be used as a type
        # type d_tk = dict[str, tk]
        # fields: d_tk = {}
        frame = tk.Frame(master_frm)
        frame.pack()
        tk.Label(frame, text="Hello World!").pack(side=LEFT, pady=5, padx=5)
        tk.Button(frame, text="Exit", command=window.destroy).pack(side=LEFT, pady=5, padx=5)
        
        # fields['lbl_hello_world'] = Label(frame, text="Hello World!")
        # fields['btn_exit'] = Button(frame, text="Exit", command=window.destroy)
        
        # for field in fields.values():
        #     # print(field.__class__)
        #     field.pack(side=LEFT, fill=X, pady=5, padx=5)
        pass
    
    window = Tk(className="tool")
    window.geometry("600x400")
    window.config(borderwidth=5, relief=GROOVE, padx=10, pady=10)

    # ------------------------------ LEFT SIDE ---------------------------

    frm_l = tk.Frame(window, relief=RIDGE, padding=2)
    frm_l.pack(anchor=NW, side=LEFT, expand=True, fill=BOTH)
    # frm_l.grid(column=0,row=0)


    frame_label_button(frm_l)
    frame_label_button(frm_l)

    # ------------------------ MIDDLE ------------------------

    # sep = tk.Separator(window,orient='vertical')
    # sep.pack(anchor=CENTER, expand=Y)

    # ----------------------------- RIGHT SIDE ---------------------------
    frm_r = tk.Frame(window, padding=10, relief=RIDGE)
    frm_r.pack(anchor=NE, side=RIGHT, expand=True, fill=BOTH)
    # frm.grid(column=1,row=0)

    tk.Label(frm_r, text="Hello World2!").grid(column=0, row=0)
    tk.Button(frm_r, text="Quit", command=window.destroy).grid(column=1, row=0)

    window.mainloop()
    
    
def tool():
    # search inserted directory for files
    def search_directory():
        directory = directory_entry.get()
        if os.path.isdir(directory):
            file_list.delete(0, END)
            for item in os.listdir(directory):
                file_list.insert(END, item)
        else:
            file_list.delete(0, END)
            file_list.insert(END, "Invalid directory")

    # selected file is highlighted
    def on_select(event):
        selected_item = event.widget.curselection()
        if selected_item:
            index = selected_item[0]
            filename = event.widget.get(index)
            print("Selected:", filename)
            file_path = os.path.join(directory_entry.get(), filename)
            if os.path.isdir(file_path):
                display_folder_contents(file_path)
            else:
                display_file_content(file_path)
    
    def display_folder_contents(folder_path):
        file_list_right.delete(0, END)
        for item in os.listdir(folder_path):
            file_list_right.insert(END, item)
    
    def extract_text_from_pdf(pdf_path):
        text = ''
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
        return text

    def display_file_content(file_path):
        if file_path.endswith(('.zip', '.rar')):
            if file_path.endswith('.zip'):
                with ZipFile(file_path, 'r') as zip_ref:
                    file_list_right.delete(0, END)
                    file_list_right.insert(END, "Files inside ZIP:")
                    for file_info in zip_ref.infolist():
                        file_list_right.insert(END, file_info.filename)
            elif file_path.endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    file_list_right.delete(0, END)
                    file_list_right.insert(END, "Files inside RAR:")
                    for file_info in rar_ref.infolist():
                        file_list_right.insert(END, file_info.filename)
        else:
            _, file_extension = os.path.splitext(file_path)
            if file_extension in ('.txt', '.doc'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        words = file.read().split()
                        word_counts = collections.Counter(words)
                        most_common_words = word_counts.most_common(50)
                        file_list_right.delete(0, END)
                        file_list_right.insert(END, "Most Used Words:")
                        for word, count in most_common_words:
                            file_list_right.insert(END, f"{word}: {count}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            elif file_extension in ('.pdf'):
                try:
                    # with open(file_path, 'rb') as file:
                    #     words = file.read().split()
                    #     word_counts = collections.Counter(words)
                    #     most_common_words = word_counts.most_common(50)
                    #     file_list_right.delete(0, END)
                    #     file_list_right.insert(END, "Most Used Words:")
                    file_list_right.delete(0, END)
                    text = extract_text_from_pdf(file_path)
                    file_list_right.insert(END, text)
                    for word, count in most_common_words:
                        file_list_right.insert(END, f"{word}: {count}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            elif file_extension in ('.csv', '.tsv'):
                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        keys = next(reader)
                        file_list_right.delete(0, END)
                        file_list_right.insert(END, "Keys:")
                        for key in keys:
                            file_list_right.insert(END, key)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            elif file_extension in ('.py', '.js', '.c'):
                try:
                    preview = subprocess.check_output(['head', '-n', '20', file_path])
                    file_list_right.delete(0, END)
                    file_list_right.insert(END, "File Preview:")
                    file_list_right.insert(END, preview.decode('utf-8'))
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showinfo("Info", "Unsupported file type.")

    # Create main window
    root = Tk()
    root.geometry("700x400")
    root.title("Directory Explorer")

    # ---------------------------- left frame
    left_frame = tk.Frame(root, padding="10")
    left_frame.grid(row=0, column=0, sticky=(W, N, E, S))

    # Directory input field and search button
    directory_label = tk.Label(left_frame, text="Directory:")
    directory_label.grid(row=0, column=0, sticky=W)

    directory_entry = tk.Entry(left_frame, width=30)
    directory_entry.grid(row=0, column=1, sticky=(W, E))

    search_button = tk.Button(left_frame, text="Search", command=search_directory)
    search_button.grid(row=0, column=2, sticky=W)

    # File list
    file_list_label = tk.Label(left_frame, text="Files:")
    file_list_label.grid(row=1, column=0, sticky=W)

    file_list = Listbox(left_frame, width=40)
    file_list.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=(W, E, N, S))
    file_list.bind("<<ListboxSelect>>", on_select)

    # ---------------------------- right frame
    right_frame = tk.Frame(root, padding="10")
    right_frame.grid(row=0, column=1, sticky=(W, N, E, S))
    
    # File list on the right
    file_list_right_label = tk.Label(right_frame, text="Selected File Content:")
    file_list_right_label.pack()

    file_list_right = Listbox(right_frame, width=60)
    file_list_right.pack(fill=BOTH, expand=True)
    
    # Expand columns and rows
    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
    # left_frame.columnconfigure(1, weight=1)
    # left_frame.rowconfigure(2, weight=1)
    
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Run the application
    root.mainloop()
    

def main():
    # test()
    tool()

if __name__ == "__main__":
    main()
