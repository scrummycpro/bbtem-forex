import datetime
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

# Initialize data
now = datetime.datetime.now()
Pair = "EUR/USD"

# Function to calculate trading strategy
def calculate_strategy():
    x = [float(now_entry.get()), float(upper_entry.get()), float(lower_entry.get()), float(average_entry.get())]
    stop_loss = float(stop_loss_entry.get())
    time_frame = time_frame_var.get()
    
    buy = round(np.mean(x) + np.std(x) * 3)
    sell = round(np.mean(x) - np.std(x) * 3)

    buy_entry = buy - 3
    sell_limitA = buy_entry + stop_loss / 3
    sell_limitB = buy_entry + stop_loss / 2
    sell_limitC = buy_entry + stop_loss
    sell_entry = sell + 3
    buy_limitA = sell_entry - stop_loss / 3
    buy_limitB = sell_entry - stop_loss / 2
    buy_limitC = sell_entry - stop_loss

    all_points = [buy_entry, sell_limitA, sell_limitB, sell_limitC, sell_entry, buy_limitA, buy_limitB, buy_limitC]
    risk_range = round(np.std(all_points) - stop_loss)

    buy_trailing_stopA = buy_entry + risk_range
    buy_trailing_stopB = risk_range + buy_trailing_stopA
    buy_trailing_stopC = risk_range + buy_trailing_stopB
    buy_trailing_stopD = risk_range + buy_trailing_stopC

    sell_trailing_stopA = sell_entry - risk_range
    sell_trailing_stopB = sell_trailing_stopA - risk_range
    sell_trailing_stopC = sell_trailing_stopB - risk_range
    sell_trailing_stopD = sell_trailing_stopC - risk_range

    GainA = (sell_limitA - buy_entry) * 3
    GainB = (sell_limitB - sell_limitA) * 2
    Exit = sell_limitC - sell_limitB
    total_gain = GainA + GainB + Exit

    LevelA = 3 * risk_range
    LevelB = 1.5 * risk_range
    LevelC = 1 * risk_range
    LossEXIT = 0.5 * risk_range
    total_loss = LevelA + LevelB + LevelC + LossEXIT
    riskreward = (-total_loss / total_gain) * 10
    
    summary_text = f"""
    Pair: {Pair}
    Time Frame: {time_frame}
    Total Risk: ${total_loss}
    Total Reward: ${total_gain}
    Risk Ratio: {riskreward}
    
    Buy Entry: 1.{buy_entry}
    Sell Limits:
    - Point A: 1.{sell_limitA}
    - Point B: 1.{sell_limitB}
    - Point C: 1.{sell_limitC}
    
    Buy Trailing Stops:
    - Level 1: 1.{buy_trailing_stopA} (Sell 15,000 units)
    - Level 2: 1.{buy_trailing_stopB} (Sell 5,000 units)
    - Level 3: 1.{buy_trailing_stopC} (Sell 5,000 units)
    - Exit: 1.{buy_trailing_stopD} (Sell 5,000 units)
    
    Sell Entry: 1.{sell_entry}
    Buy Limits:
    - Point A: 1.{buy_limitA}
    - Point B: 1.{buy_limitB}
    - Point C: 1.{buy_limitC}
    
    Sell Trailing Stops:
    - Level 1: 1.{sell_trailing_stopA} (Buy 15,000 units)
    - Level 2: 1.{sell_trailing_stopB} (Buy 5,000 units)
    - Level 3: 1.{sell_trailing_stopC} (Buy 5,000 units)
    - Exit: 1.{sell_trailing_stopD} (Buy 5,000 units)
    
    How to Set Up:
    =============
    Chart to Use: {time_frame} chart
    ATR Period to Use: 89

    1. Select Bollinger Bands
    2. Periods: 10, Deviation: 3
    3. Enter Current Price, Upper, Lower, Median values

    I Believe {Pair} will go Up:
    ============================
    Step 1:
    Place your Buy order for 30,000 units @ 1.{buy_entry}, then place a sell limit of 10,000 units @ 1.{sell_limitA}, 1.{sell_limitB}, and 1.{sell_limitC}
    
    Step 2:
    Place a Sell Limit @ 1.{buy_trailing_stopA} for 15,000 units, and place a Sell Limit for 5,000 units @ 1.{buy_trailing_stopB}, 1.{buy_trailing_stopC}, and 1.{buy_trailing_stopD}
    
    I Believe {Pair} will go Down:
    =============================
    Step 1:
    Place your Sell order for 30,000 units @ 1.{sell_entry}, then place a buy limit of 10,000 units @ 1.{buy_limitA}, 1.{buy_limitB}, and 1.{buy_limitC}
    
    Step 2:
    Place a Buy Limit @ 1.{sell_trailing_stopA} for 15,000 units, and place a Buy Limit for 5,000 units @ 1.{sell_trailing_stopB}, 1.{sell_trailing_stopC}, and 1.{sell_trailing_stopD}
    """
    summary_label.config(text=summary_text)

# Create GUI
root = tk.Tk()
root.title(f"Trading Bot Summary - {Pair}")

# Create a main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
input_frame = ttk.Frame(canvas)

# Add that new frame to a window in the canvas
canvas.create_window((0, 0), window=input_frame, anchor="nw")

# Display current date and time
def display_time():
    now = datetime.datetime.now()
    time_label.config(text=f"Current Date: {now.month}-{now.day}-{now.year}\nCurrent Time: {now.hour}:{now.minute}")

# Create and place widgets for input fields
ttk.Label(input_frame, text="Enter Current Price:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
now_entry = ttk.Entry(input_frame)
now_entry.grid(row=1, column=0, padx=10, pady=5)

ttk.Label(input_frame, text="Enter Upper Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
upper_entry = ttk.Entry(input_frame)
upper_entry.grid(row=3, column=0, padx=10, pady=5)

ttk.Label(input_frame, text="Enter Lower Price:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10)
lower_entry = ttk.Entry(input_frame)
lower_entry.grid(row=5, column=0, padx=10, pady=5)

ttk.Label(input_frame, text="Enter Average Price:", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=10)
average_entry = ttk.Entry(input_frame)
average_entry.grid(row=7, column=0, padx=10, pady=5)

# Add stop loss input field
ttk.Label(input_frame, text="Enter Stop Loss:", font=("Arial", 12)).grid(row=8, column=0, padx=10, pady=10)
stop_loss_entry = ttk.Entry(input_frame)
stop_loss_entry.grid(row=9, column=0, padx=10, pady=5)

# Add time frame selection
ttk.Label(input_frame, text="Select Time Frame:", font=("Arial", 12)).grid(row=10, column=0, padx=10, pady=10)
time_frame_var = tk.StringVar(value="4hr")
time_frame_menu = ttk.Combobox(input_frame, textvariable=time_frame_var)
time_frame_menu['values'] = ("4hr", "8hr")
time_frame_menu.grid(row=11, column=0, padx=10, pady=5)

# Button to calculate strategy
ttk.Button(input_frame, text="Calculate Strategy", command=calculate_strategy).grid(row=12, column=0, padx=10, pady=10)

# Display time
time_label = ttk.Label(input_frame, text="", font=("Arial", 12))
time_label.grid(row=13, column=0, padx=10, pady=10)
display_time()

# Display summary
summary_label = ttk.Label(input_frame, text="", font=("Arial", 10))
summary_label.grid(row=14, column=0, padx=10, pady=10)

# Run the GUI loop
root.mainloop()
