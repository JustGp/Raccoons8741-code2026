import tkinter as tk
from tkinter import ttk
global a, b, c, d, e
a = -165.1733 # Base Offset
b = 28.2919 # Scales with effective voltage
c = -15.0539 # Scales with time
d = -13.6174 # Scales with the interaction of voltage and time
e = 4.0463 # Scales with the interaction of voltage and time squared

def distance_calculator(PV, t):
    D = a + b*PV + c*t + d*PV*t + e*(PV**2)*t
    return D

def to_non_negative_float(value: str) -> float:
    """Parse user input to a non-negative float; fallback to 0.0."""
    try:
        return max(0.0, float(value))
    except ValueError:
        return 0.0


def calculate_distance(*_args) -> None:
    voltage = to_non_negative_float(voltage_var.get())
    time_value = to_non_negative_float(time_var.get())
    distance = distance_calculator(voltage, time_value)
    distance_var.set(f"{distance:.2f} cm")


root = tk.Tk()
root.title("Voltage-Time Distance Calculator")
root.geometry("420x220")
root.resizable(False, False)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

header = ttk.Label(
    main,
    text="Distance from Effective Voltage and Time",
    font=("Segoe UI", 12, "bold"),
)
header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

voltage_var = tk.StringVar(value="12")
time_var = tk.StringVar(value="5")
distance_var = tk.StringVar(value="60.00 m")

# Recalculate whenever either input changes.
voltage_var.trace_add("write", calculate_distance)
time_var.trace_add("write", calculate_distance)

ttk.Label(main, text="Effective Voltage:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
voltage_entry = ttk.Entry(main, textvariable=voltage_var, width=14)
voltage_entry.grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(main, text="V").grid(row=1, column=2, sticky="w", pady=6)

ttk.Label(main, text="Time:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
time_entry = ttk.Entry(main, textvariable=time_var, width=14)
time_entry.grid(row=2, column=1, sticky="w", pady=6)
ttk.Label(main, text="s").grid(row=2, column=2, sticky="w", pady=6)

separator = ttk.Separator(main, orient="horizontal")
separator.grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(main, text="Distance:", font=("Segoe UI", 10, "bold")).grid(
    row=4, column=0, sticky="w", padx=(0, 8)
)
ttk.Label(main, textvariable=distance_var, font=("Segoe UI", 10, "bold")).grid(
    row=4, column=1, columnspan=2, sticky="w"
)

ttk.Label(main, text="Formula: distance = effectiveVoltage x time", foreground="#4a5560").grid(
    row=5, column=0, columnspan=3, sticky="w", pady=(12, 0)
)

calculate_distance()
voltage_entry.focus_set()
root.mainloop()
