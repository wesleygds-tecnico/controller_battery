###-------------------------------------------------------------------###
##------------------------ Importing libraries ------------------------##
###-------------------------------------------------------------------###

import socket
import time
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import threading
from  tkinter import ttk

import matplotlib.animation as animation
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
                                                        
###-------------------------------------------------------------------###
##------------------- Executes the plot animation ---------------------##
###-------------------------------------------------------------------###

def animate(i,axs):
    global x_time, y_PCon, y_PPV, y_Pbat, y_PG, y_SoC, y_SoCMin
    try:
        with open("HistoryServer.csv") as f:
            ncols = len(f.readline().split(','))
        
        logger = np.loadtxt("HistoryServer.csv", delimiter=',', skiprows=1, usecols=range(8,ncols))    

        if len(np.shape(logger)) > 1:
            logger = logger[-1,:]
            
        x_time = np.append(x_time, np.array(logger[0]))  
        y_PCon = np.append(y_PCon, np.array(logger[1]))
        y_PPV = np.append(y_PPV, np.array(logger[2]))
        y_Pbat = np.append(y_Pbat, np.array(logger[3]))
        y_PG = np.append(y_PG, np.array(logger[4]))        
        y_SoC = np.append(y_SoC, np.array(logger[5]))
        y_SoCMin = np.append(y_SoCMin, np.array(logger[6]))
            
        update_figs(i,axs)
        return x_time, y_PCon, y_PPV, y_Pbat, y_PG, y_SoC, y_SoCMin, i
    except Exception as e:
        print(f"ultima linha {e}")
        return x_time, y_PCon, y_PPV, y_Pbat, y_PG, y_SoCMin, i
    
###-------------------------------------------------------------------###
##--------------------- Execute the program screen --------------------##
###-------------------------------------------------------------------###

def config_tkinter():
    root = ctk.CTk()
    root.attributes('-fullscreen', True)

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root.title("Embedding in Tk")

    button = ctk.CTkButton(master=root, text="Quit", command=lambda: _quit(root))
    combobox = ctk.CTkOptionMenu(master=root,
                                       values=["Self-Consumption", "Peak Shaving", "Electricity Price Adjustment", "Reactive Power for Voltage Support", "Active Power for Frequency Support"])
    combobox.place(x=250, y=725)
    combobox.set("Self-Consumption")  # set initial value

    """
    dialog = ctk.CTkInputDialog(text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())


    button = ctk.CTkButton(master=root, text="Open Dialog")
    button.place(x=50, y=725)
    """
    button.place(x=50, y=725)
    return root

###-------------------------------------------------------------------###
##--------------------------- Stop script -----------------------------##
###-------------------------------------------------------------------###

def _quit(root):
    root.quit()     # stops mainloop
    root.destroy()
    s.close()       #this is necessary on Windows to prevent
                    #Fatal Python Error: PyEval_RestoreThread: NULL tstate
                        

###-------------------------------------------------------------------###
##---------------------- Write data to the history --------------------##
###-------------------------------------------------------------------###

def write_to_csv(data,file_name,header): 
    historyData = [{'F': "Self Consumption",
                            'LP': " ",
                            'PPS': " ",
                            'id': " ",                    
                            'Cap': " ",
                            'PDMax': " ",
                            'PCMax': " ",
                            'RT': data["RT"], 
                            'AT': float(data["AT"]),
                            'PCon': float(data["PCon"]),
                            'PPV': float(data["PPV"]),
                            'Pbat': float(data["Pbat"]),
                            'PG': float(data["PG"]),
                            'SoC': float(data["SoC"]),
                            'SoCMin': float(data["SoCMin"])}]

    with open(file_name, 'a', newline='') as csvfile:
        addRow = csv.DictWriter(csvfile, fieldnames = header)
        addRow.writerows(historyData)

###-------------------------------------------------------------------###
##--------------------------- Plot graphs -----------------------------##
###-------------------------------------------------------------------###

def update_figs(i,axs):
    FirstPoint = 0
    axs[0].cla()
    axs[0].plot(x_time,y_PCon, label = 'Load')
    axs[0].plot(x_time,y_PPV, label = 'PV Output')
    axs[0].legend()
    axs[0].grid(which='major', color='k', linestyle='--', linewidth=0.5)
    axs[0].grid(which='minor', color='k', linestyle=':', linewidth=0.5)
    #axs[0].set_xlabel("Time [Min]")
    axs[0].set_ylabel("Power [W]")
    axs[0].set_xlim(FirstPoint,i+FirstPoint+1)
    
    axs[1].cla()
    axs[1].plot(x_time,-y_Pbat, label = 'Battery Power Transit')
    axs[1].plot(x_time,y_PG, label = 'Grid Power')
    axs[1].legend()
    axs[1].grid(color='k', linestyle='--', linewidth=0.5)
    axs[1].grid(which='major', color='k', linestyle='--', linewidth=0.5)
    axs[1].grid(which='minor', color='k', linestyle=':', linewidth=0.5)
    #axs[1].axhline(0,color='k')
    #axs[1].set_xlabel("Time [Min]")
    axs[1].set_ylabel("Power [W]")    
    axs[1].set_xlim(FirstPoint,i+FirstPoint+1)

    axs[2].cla()
    axs[2].plot(x_time,y_SoC, label = 'State of Charge')
    axs[2].plot(x_time,y_SoCMin, color = 'k', label = 'State of Charge Min.')    
    axs[2].legend()
    axs[2].grid(which='major', color='k', linestyle='--', linewidth=0.5)
    axs[2].grid(which='minor', color='k', linestyle=':', linewidth=0.5)
    axs[2].set_xlabel("Time [Min]")
    axs[2].set_ylabel("State of Charge [%]")    
    axs[2].set_xlim(FirstPoint,i+FirstPoint+1)

"""
    axs[2].cla()
    axs[2].plot(x_time,y_PG, label = 'Grid Power')    
    axs[2].legend()
    axs[2].grid(color='k', linestyle='--', linewidth=0.5)
    axs[2].set_xlim(0,i+1)
"""

###-------------------------------------------------------------------###
##------------------------- Receive BBB message -----------------------##
###-------------------------------------------------------------------###

def get_message(DataRequirement):
    #print('Get Message')
    s.send(str.encode(json.dumps(DataRequirement))) 
    message = s.recv(2048)
    #print(message)
    """
    response = {"response": "ok"}
    response = json.dumps(response)
    response = str.encode(response)
    conn.sendall(response)
    """
    #time.sleep(5)
    data = json.loads(message)
    return data


###-------------------------------------------------------------------###
##--------------------- Write message to history ----------------------##
###-------------------------------------------------------------------###

def handle_message(msg,file_name,history_header):
    #change handler for a chain of command pattern

    #if msg["type"] == "log": 
    if msg != " ":
        #print("A mensagem está sendo escrita")
        write_to_csv(msg,file_name,history_header)
    #elif msg["type"] == "log-finish":
    elif msg == " ":
        return False
    return True

def handle_connection(s,file_name,history_header):
    
    while True:
        msg = get_message(DataRequirement)
        #print("A mensagem está a chegar")

        handle_message(msg,file_name, history_header)

        if not msg:
            break
    
    
    
    """
        if status == False:
            conn.close()
            ani_1.pause()
        

        #print('Conectado em', ender)
        ActualTimeInitiated = time.time()

    conn.close()
    """
        
if __name__ == "__main__":
    
    """"
    HOST = socket.gethostname()
    print(HOST)
    PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',PORT))

    history_header = ['F','LP','PPS','id','Cap','PDMax','PCMax','RT','AT','PCon','PPV','Pbat','PG','SoC','SoCMin']
    file_name = "HistoryServer.csv"
    

    s.listen()
    print("Waiting for client connection")
    """
    ###-------------------------------------------------------------------###
    ##--------------------- Stablish connect with BBB ---------------------##
    ###-------------------------------------------------------------------###

    HOST = '192.168.7.2' #It is possible that you need to change this IP Address
    PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected")

    history_header = ['F','LP','PPS','id','Cap','PDMax','PCMax','RT','AT','PCon','PPV','Pbat','PG','SoC','SoCMin']
    file_name = "HistoryServer.csv"    
    
    DataRequirement = {'Require': 'Data'}
    
    global conn
    global ani_1
    global data

    ###-------------------------------------------------------------------###
    ##--------------- Loop for send, receive and plot info ----------------##
    ###-------------------------------------------------------------------###

    while True:
        
        #conn, ender = s.accept()

        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = history_header)
            writer.writeheader()
        

        connection_handler = threading.Thread(target=handle_connection, args=(s,file_name,history_header))
        connection_handler.start()
        root = config_tkinter()        
    
        x_time = []
        
        y_PCon = []

        y_PPV = []

        y_Pbat = []

        y_PG = []

        y_SoC = []

        y_SoCMin = []

        fig, axs = plt.subplots(3,1,figsize=(16,8))

        axs = axs.flatten()

        plotcanvas = FigureCanvasTkAgg(fig, root)
        plotcanvas.get_tk_widget().place(x=-125, y=-75)
        
        ani_1 = animation.FuncAnimation(fig, animate, interval=2400,fargs=(axs,))
        root.mainloop()