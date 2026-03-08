import tkinter as tk
from tkinter import ttk

# Constants
a = -165.1733  # Base Offset
b = 28.2919    # Scales with effective voltage
c = -15.0539   # Scales with time
d = -13.6174   # Scales with the interaction of voltage and time
e = 4.0463     # Scales with the interaction of voltage and time squared


def distance_calculator(PV, t):
    D = a + b*PV + c*t + d*PV*t + e*(PV**2)*t
    return D


def time_calculator(PV, D):
    t = (D - a - b*PV) / (c + d*PV + e*(PV**2))
    return t


def degrees_calculator(PV, t):
    θ = (217.15 * t + -16.78) * (PV / 8)
    return θ


def time_by_degrees_calculator(θ, PV):
    t = (θ * (8/PV) + 16.78) / 217.15
    return t


def to_non_negative_float(value: str) -> float:
    """Parse user input to a non-negative float; fallback to 0.0."""
    try:
        return max(0.0, float(value))
    except ValueError:
        return 0.0


# Root window setup
root = tk.Tk()
root.title("Calculator Suite")
root.geometry("450x280")
root.resizable(False, False)

# Create notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=8, pady=8)

# ============================================================================
# TAB 1: Distance Calculator
# ============================================================================
distance_frame = ttk.Frame(notebook, padding=16)
notebook.add(distance_frame, text="Distance")

distance_header = ttk.Label(
    distance_frame,
    text="Distance from Voltage and Time",
    font=("Segoe UI", 12, "bold"),
)
distance_header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

distance_voltage_var = tk.StringVar(value="12")
distance_time_var = tk.StringVar(value="5")
distance_result_var = tk.StringVar(value="0.00 cm")


def calculate_distance(*_args) -> None:
    voltage = to_non_negative_float(distance_voltage_var.get())
    time_value = to_non_negative_float(distance_time_var.get())
    distance = distance_calculator(voltage, time_value)
    distance_result_var.set(f"{distance:.2f} cm")


distance_voltage_var.trace_add("write", calculate_distance)
distance_time_var.trace_add("write", calculate_distance)

ttk.Label(distance_frame, text="Effective Voltage:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(distance_frame, textvariable=distance_voltage_var, width=14).grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(distance_frame, text="V").grid(row=1, column=2, sticky="w", pady=6)

ttk.Label(distance_frame, text="Time:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(distance_frame, textvariable=distance_time_var, width=14).grid(row=2, column=1, sticky="w", pady=6)
ttk.Label(distance_frame, text="s").grid(row=2, column=2, sticky="w", pady=6)

ttk.Separator(distance_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(distance_frame, text="Distance:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8))
ttk.Label(distance_frame, textvariable=distance_result_var, font=("Segoe UI", 10, "bold")).grid(row=4, column=1, columnspan=2, sticky="w")

calculate_distance()

# ============================================================================
# TAB 2: Time Calculator
# ============================================================================
time_frame = ttk.Frame(notebook, padding=16)
notebook.add(time_frame, text="Time")

time_header = ttk.Label(
    time_frame,
    text="Time from Voltage and Distance",
    font=("Segoe UI", 12, "bold"),
)
time_header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

time_voltage_var = tk.StringVar(value="12")
time_distance_var = tk.StringVar(value="60")
time_result_var = tk.StringVar(value="0.00 s")


def calculate_time(*_args) -> None:
    voltage = to_non_negative_float(time_voltage_var.get())
    distance = to_non_negative_float(time_distance_var.get())
    try:
        time_value = time_calculator(voltage, distance)
        time_result_var.set(f"{time_value:.2f} s")
    except ZeroDivisionError:
        time_result_var.set("Error")


time_voltage_var.trace_add("write", calculate_time)
time_distance_var.trace_add("write", calculate_time)

ttk.Label(time_frame, text="Effective Voltage:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(time_frame, textvariable=time_voltage_var, width=14).grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(time_frame, text="V").grid(row=1, column=2, sticky="w", pady=6)

ttk.Label(time_frame, text="Distance:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(time_frame, textvariable=time_distance_var, width=14).grid(row=2, column=1, sticky="w", pady=6)
ttk.Label(time_frame, text="cm").grid(row=2, column=2, sticky="w", pady=6)

ttk.Separator(time_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(time_frame, text="Time:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8))
ttk.Label(time_frame, textvariable=time_result_var, font=("Segoe UI", 10, "bold")).grid(row=4, column=1, columnspan=2, sticky="w")

calculate_time()

# ============================================================================
# TAB 3: Degrees Calculator
# ============================================================================
degrees_frame = ttk.Frame(notebook, padding=16)
notebook.add(degrees_frame, text="Degrees")

degrees_header = ttk.Label(
    degrees_frame,
    text="Degrees from Voltage and Time",
    font=("Segoe UI", 12, "bold"),
)
degrees_header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

degrees_voltage_var = tk.StringVar(value="8")
degrees_time_var = tk.StringVar(value="5")
degrees_result_var = tk.StringVar(value="0.00 °")


def calculate_degrees(*_args) -> None:
    voltage = to_non_negative_float(degrees_voltage_var.get())
    time_value = to_non_negative_float(degrees_time_var.get())
    degrees = degrees_calculator(voltage, time_value)
    degrees_result_var.set(f"{degrees:.2f} °")


degrees_voltage_var.trace_add("write", calculate_degrees)
degrees_time_var.trace_add("write", calculate_degrees)

ttk.Label(degrees_frame, text="Effective Voltage:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(degrees_frame, textvariable=degrees_voltage_var, width=14).grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(degrees_frame, text="V").grid(row=1, column=2, sticky="w", pady=6)

ttk.Label(degrees_frame, text="Time:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(degrees_frame, textvariable=degrees_time_var, width=14).grid(row=2, column=1, sticky="w", pady=6)
ttk.Label(degrees_frame, text="s").grid(row=2, column=2, sticky="w", pady=6)

ttk.Separator(degrees_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(degrees_frame, text="Degrees:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8))
ttk.Label(degrees_frame, textvariable=degrees_result_var, font=("Segoe UI", 10, "bold")).grid(row=4, column=1, columnspan=2, sticky="w")

calculate_degrees()

# ============================================================================
# TAB 4: Time by Degrees Calculator
# ============================================================================
time_degrees_frame = ttk.Frame(notebook, padding=16)
notebook.add(time_degrees_frame, text="Time by Degrees")

time_degrees_header = ttk.Label(
    time_degrees_frame,
    text="Time from Degrees and Voltage",
    font=("Segoe UI", 12, "bold"),
)
time_degrees_header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

time_degrees_degrees_var = tk.StringVar(value="45")
time_degrees_voltage_var = tk.StringVar(value="8")
time_degrees_result_var = tk.StringVar(value="0.00 s")


def calculate_time_by_degrees(*_args) -> None:
    degrees = to_non_negative_float(time_degrees_degrees_var.get())
    voltage = to_non_negative_float(time_degrees_voltage_var.get())
    try:
        time_value = time_by_degrees_calculator(degrees, voltage)
        time_degrees_result_var.set(f"{time_value:.2f} s")
    except ZeroDivisionError:
        time_degrees_result_var.set("Error")


time_degrees_degrees_var.trace_add("write", calculate_time_by_degrees)
time_degrees_voltage_var.trace_add("write", calculate_time_by_degrees)

ttk.Label(time_degrees_frame, text="Degrees:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(time_degrees_frame, textvariable=time_degrees_degrees_var, width=14).grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(time_degrees_frame, text="°").grid(row=1, column=2, sticky="w", pady=6)

ttk.Label(time_degrees_frame, text="Effective Voltage:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
ttk.Entry(time_degrees_frame, textvariable=time_degrees_voltage_var, width=14).grid(row=2, column=1, sticky="w", pady=6)
ttk.Label(time_degrees_frame, text="V").grid(row=2, column=2, sticky="w", pady=6)

ttk.Separator(time_degrees_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(time_degrees_frame, text="Time:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8))
ttk.Label(time_degrees_frame, textvariable=time_degrees_result_var, font=("Segoe UI", 10, "bold")).grid(row=4, column=1, columnspan=2, sticky="w")

calculate_time_by_degrees()

# Start the application
root.mainloop()
