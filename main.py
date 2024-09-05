import os
import requests
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Spinbox
import threading


def download_file(url, save_path, log_widget, timeout=2):
    log_widget.config(state=tk.NORMAL)
    log_widget.insert(tk.END, f"Processing: {url}\n")
    log_widget.yview(tk.END)
    log_widget.config(state=tk.DISABLED)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"Success: {save_path} downloaded.\n")
        log_widget.yview(tk.END)
        log_widget.config(state=tk.DISABLED)
        return True
    except requests.exceptions.HTTPError as http_err:
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"Failed: {save_path} not found (HTTP Error: {http_err}).\n")
        log_widget.yview(tk.END)
        log_widget.config(state=tk.DISABLED)
        return False
    except Exception as err:
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"Failed: Error occurred while downloading {save_path} ({err}).\n")
        log_widget.yview(tk.END)
        log_widget.config(state=tk.DISABLED)
        return False


def download_latest_stock_data(log_widget, start_button, timeout_input):
    start_button.config(state=tk.DISABLED)
    timeout = int(timeout_input.get())
    date = datetime.now()
    attempts = 0

    while True:
        date_str = date.strftime("%d-%m-%Y")
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"\nAttempt {attempts + 1}: Checking for files on {date_str}\n")
        log_widget.yview(tk.END)
        log_widget.config(state=tk.DISABLED)

        csv_url = f"https://raw.githubusercontent.com/aimatochysia/stock-results/main/stock_data_{date_str}.csv"
        txt_url = f"https://raw.githubusercontent.com/aimatochysia/stock-results/main/debug_stock_scrapper_{date_str}.txt"
        csv_file = f"stock_data_{date_str}.csv"
        txt_file = f"debug_stock_scrapper_{date_str}.txt"

        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"Getting CSV: {csv_url}\n")
        log_widget.yview(tk.END)
        log_widget.config(state=tk.DISABLED)
        csv_downloaded = download_file(csv_url, csv_file, log_widget, timeout)

        if csv_downloaded:
            log_widget.config(state=tk.NORMAL)
            log_widget.insert(tk.END, f"Getting TXT: {txt_url}\n")
            log_widget.yview(tk.END)
            log_widget.config(state=tk.DISABLED)
            txt_downloaded = download_file(txt_url, txt_file, log_widget, timeout)

            if txt_downloaded:
                folder_selected = filedialog.askdirectory()
                if folder_selected:
                    os.rename(csv_file, os.path.join(folder_selected, csv_file))
                    os.rename(txt_file, os.path.join(folder_selected, txt_file))
                    log_widget.config(state=tk.NORMAL)
                    log_widget.insert(tk.END, f"\nSuccess: Both CSV and TXT files downloaded and saved to {folder_selected}.\n")
                    log_widget.yview(tk.END)
                    log_widget.config(state=tk.DISABLED)
                else:
                    log_widget.config(state=tk.NORMAL)
                    log_widget.insert(tk.END, "\nDownload canceled: No directory selected.\n")
                    log_widget.yview(tk.END)
                    log_widget.config(state=tk.DISABLED)
                break
        else:
            log_widget.config(state=tk.NORMAL)
            log_widget.insert(tk.END, f"Skipping TXT: CSV for {date_str} not available, going back one day.\n")
            log_widget.yview(tk.END)
            log_widget.config(state=tk.DISABLED)

        date -= timedelta(days=1)
        attempts += 1

    start_button.config(state=tk.NORMAL)
    messagebox.showinfo("Download Complete", "Stock data download completed.")


def start_download(log_widget, start_button, timeout_input):
    download_thread = threading.Thread(target=download_latest_stock_data, args=(log_widget, start_button, timeout_input))
    download_thread.start()


def create_gui():
    window = tk.Tk()
    window.title("Stock Data Downloader")

    window.config(bg="#2E2E2E")

    title_label = tk.Label(window, text="Stock Data Downloader", font=("Arial", 18, "bold"), bg="#2E2E2E", fg="#D3D3D3")
    title_label.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="w")

    instruction_label = tk.Label(window, text="Click 'Start Download' to fetch the latest stock data.\nAdjust the timeout if needed.", font=("Arial", 12), bg="#2E2E2E", fg="#D3D3D3")
    instruction_label.grid(column=0, row=1, padx=10, pady=(0, 10), sticky="n")

    log_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20, bg="#1E1E1E", fg="#D3D3D3", insertbackground='white')
    log_widget.grid(column=0, row=2, padx=10, pady=10)
    log_widget.config(state=tk.DISABLED)

    timeout_label = tk.Label(window, text="Timeout (seconds):", bg="#2E2E2E", fg="#D3D3D3")
    timeout_label.grid(column=0, row=3, padx=10, pady=5, sticky="e")
    timeout_input = Spinbox(window, from_=1, to=10, width=5, bg="#1E1E1E", fg="#D3D3D3", insertbackground='white')
    timeout_input.grid(column=1, row=3, padx=10, pady=5, sticky="w")
    timeout_input.delete(0, "end")
    timeout_input.insert(0, "2")

    start_button = tk.Button(window, text="Start Download", command=lambda: start_download(log_widget, start_button, timeout_input), bg="#2b6f13", fg="#D3D3D3", activebackground="#6A6A6A")
    start_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)
    window.mainloop()

create_gui()
