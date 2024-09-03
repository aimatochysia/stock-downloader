import requests
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
from threading import Thread
import time


def download_files():
    def download_task():
        
        directory = filedialog.askdirectory()
        if not directory:
            return

        
        label_status.config(text="Downloading files... Please wait.")
        root.update_idletasks()

        
        today = datetime.now()
        for i in range(30):  
            date = today - timedelta(days=i)
            date_str = date.strftime("%d-%m-%Y")
            
            csv_url = f"https://raw.githubusercontent.com/aimatochysia/stock-results/main/stock_data_{date_str}.csv"
            txt_url = f"https://raw.githubusercontent.com/aimatochysia/stock-results/main/debug_stock_scrapper_{date_str}.txt"
            
            
            csv_response = requests.get(csv_url)
            if csv_response.status_code == 200:
                with open(f"{directory}/stock_data_{date_str}.csv", 'wb') as csv_file:
                    csv_file.write(csv_response.content)
            
            
            txt_response = requests.get(txt_url)
            if txt_response.status_code == 200:
                with open(f"{directory}/debug_stock_scrapper_{date_str}.txt", 'wb') as txt_file:
                    txt_file.write(txt_response.content)
            
            
            if csv_response.status_code == 200 and txt_response.status_code == 200:
                break

        
        label_status.config(text="Download complete.")
        root.update_idletasks()

    
    Thread(target=download_task).start()


def create_gui():
    global root, label_status
    root = tk.Tk()
    root.title("Stock Data Downloader")
    label_instruction = tk.Label(root, text="Click the button below to download the latest stock screening:", padx=20, pady=10)
    label_instruction.pack()
    label_status = tk.Label(root, text="", padx=20, pady=10)
    label_status.pack()
    btn_download = tk.Button(root, text="Download Latest Data", command=download_files, padx=20, pady=10)
    btn_download.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
