import tkinter as tk
from tkinter import ttk, PhotoImage
import gspread
import datetime
import socket
import os
import time
import pathlib
from pathlib import Path


def add_simple_warning(warn_type):
    print(f"WARNING - {warn_type}, skipping...")
    ID_label.config(text=warn_type)

def add_simple_error(error_type, instructions):
    print(f"ERROR - {error_type}")
    ID_label = ttk.Label(window, text=f"{instructions}, close this window, and try again.")
    ID_label.pack()
    window.mainloop()
    quit()

# Initialize the Tkinter window
window = tk.Tk()
window.title("NRG Login System")

# check if there's a not-empty spreadsheet_url.txt file. Does not check for validity.
url_file_path = f"{pathlib.Path().resolve()}/spreadsheet_url.txt"
if not Path(url_file_path).is_file():
    with open(url_file_path, 'w') as f:
        f.write("")
    add_simple_error("No URL File, Creating...","Please paste spreadsheet URL into spreadsheet_url.txt")
elif os.path.getsize(url_file_path) == 0:
    add_simple_error("Empty URL File","Please paste spreadsheet URL into spreadsheet_url.txt")
else:
    with open(url_file_path) as f:
        spreadsheet_url = f.readline()

# Check internet connection
try:
    socket.setdefaulttimeout(3)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
except socket.error:
    add_simple_error("No internet","No Internet. Please reconnect")

#check for credentials.json
credentials_file_path = f"{pathlib.Path().resolve()}/credentials.json"
if not Path(credentials_file_path).is_file():
    add_simple_error("No credentials.json","Please create and add a credentials.json")

#Set style, and add images and static text
s = ttk.Style()
s.configure('.', font=('Helvetica', 32))
image = PhotoImage(file="logo.png")
image_label = ttk.Label(window, image=image)
how_to_use_label = ttk.Label(window, text="Enter your Student ID:")
image_label.pack()
how_to_use_label.pack()

# Authenticate with Google Sheets
gc = gspread.oauth(credentials_filename=credentials_file_path)
#gc = gspread.oauth()
print(f"Opening spreadsheet: {spreadsheet_url}")
spreadsheet = gc.open_by_url(spreadsheet_url)

worksheet = spreadsheet.worksheet("[BACKEND] Logs")
ID_sheet = spreadsheet.worksheet("[BACKEND] ID List")

def single_upload(log_type, cell_value, input_id):
    worksheet.batch_update([{
        'range': f'A{cell_value}:C{cell_value}',
        'values': [[int(input_id), datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), log_type]]
    }])

# Function to upload data to the spreadsheet
def upload_data(log_type):
    start_time = time.time()
    ID_label.config(text=None)
    input_id = entry.get()
    if not input_id:
        return

    person_cell = ID_sheet.find(input_id)
    if not input_id.isnumeric() or person_cell is None:
        add_simple_warning("Invalid ID")
    else:
        vital_info = ID_sheet.batch_get([f'B{person_cell.row}:D{person_cell.row}','G1','I1'])
        cell_value = int(vital_info[1][0][0])
        enough_rows = vital_info[2][0][0]
        person_namestatus = vital_info[0][0]
        if person_namestatus[1] == log_type and not log_type == "logoutall":
            add_simple_warning("Already Done")
        else:
            if enough_rows == "FALSE":
                worksheet.append_rows([[None,None,None,f'=IFERROR(IF(C{cell_value+i}="logout",B{cell_value+i} - INDEX(B$2:B{cell_value-1+i}, MAX(IF((A$2:A{cell_value-1+i}=A{cell_value+i})*(C$2:C{cell_value-1+i}="login"), ROW(A$2:A{cell_value-1+i})-ROW(A$2)+1))),))'] for i in range(200)],"USER_ENTERED")
                print("Appended 200 new rows")
            if log_type == "logoutall" and person_namestatus[2] == "TRUE":
                logged_in_cells = ID_sheet.findall("login", None, 3)
                if logged_in_cells == []:
                    add_simple_warning("Everyone's already Logged Out")
                else:
                    logged_in_IDs_nested = ID_sheet.batch_get([f"A{x.row}" for x in logged_in_cells])
                    logged_in_IDs_flat = [[int(inner_list[0][0])] for inner_list in logged_in_IDs_nested]
                    single_upload("logoutall", cell_value, input_id)
                    cell_value += 1
                    worksheet.update(logged_in_IDs_flat, f'A{cell_value}:A{cell_value + len(logged_in_IDs_flat) - 1}')
                    batchlogoutdate = [[datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "logout"]] * len(logged_in_IDs_flat)
                    worksheet.update(batchlogoutdate, f'B{cell_value}:C{cell_value + len(logged_in_IDs_flat) - 1}')
                    ID_label.config(text=f"Goodnight, {person_namestatus[0]}!")
                    print(f"Logged out {len(logged_in_IDs_flat)} users")
            elif log_type == "logoutall":
                add_simple_warning(f"{person_namestatus[0]} can't log everyone out.")
            else:
                single_upload(log_type, cell_value, input_id)
                ID_label.config(text=f"{log_type} {person_namestatus[0]}")

            os.system("echo picture placeholder")  # TODO - change to take a picture
            #https://raspberrypi-guide.github.io/electronics/using-usb-webcams#setting-up-and-using-a-usb-webcam https://www.luisllamas.es/en/commandcam/
            print(f"{log_type} by {person_namestatus[0]} took {time.time() - start_time} seconds")

        entry.delete(0, tk.END)


# Entry widget for user input
entry = ttk.Entry(window,font=('helvetica',32),justify='center')
entry.pack()

# Buttons for login, logout, and logout all
button_login = ttk.Button(
    window,
    text="Login",
    width=25,
    command=lambda: upload_data("login")
)
button_logout = ttk.Button(
    window,
    text="Logout",
    width=25,
    command=lambda: upload_data("logout")
)
button_logout_all = ttk.Button(
    window,
    text="Logout All",
    width=25,
    command=lambda: upload_data("logoutall")
)

button_login.pack()
button_logout.pack()
button_logout_all.pack()

# Label for displaying messages
ID_label = ttk.Label(window)
ID_label.pack()

# Start the Tkinter main loop
print("Initialzation complete, launching GUI...")
window.mainloop()
