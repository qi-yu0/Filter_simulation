import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, lfilter

class FilterSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Filter Simulator")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.t = np.linspace(0, 1, 1000, endpoint=False)
        self.signal = np.sin(2 * np.pi * 5 * self.t)

        self.fs = 1000.0
        self.low_cutoff = 20.0
        self.high_cutoff = 80.0

        self.plot_signal()
        self.canvas.draw()

        self.create_widgets()

    def create_widgets(self):
        self.low_cutoff_label = tk.Label(self.root, text="Lowpass Cutoff Frequency")
        self.low_cutoff_label.pack()
        self.low_cutoff_scale = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_lowpass)
        self.low_cutoff_scale.set(self.low_cutoff)
        self.low_cutoff_scale.pack()

        self.high_cutoff_label = tk.Label(self.root, text="Highpass Cutoff Frequency")
        self.high_cutoff_label.pack()
        self.high_cutoff_scale = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_highpass)
        self.high_cutoff_scale.set(self.high_cutoff)
        self.high_cutoff_scale.pack()

    def butter_filter(self, data, cutoff, fs, btype, order=5):
        b, a = butter(order, cutoff / (0.5 * fs), btype=btype, analog=False)
        return lfilter(b, a, data)

    def plot_signal(self):
        self.ax.clear()
        self.ax.plot(self.t, self.signal, 'b-', label='Original Signal')
        self.ax.plot(self.t, self.butter_filter(self.signal, self.low_cutoff, self.fs, 'low'), 'r-', label='Lowpass Filtered Signal')
        self.ax.plot(self.t, self.butter_filter(self.signal, self.high_cutoff, self.fs, 'high'), 'g-', label='Highpass Filtered Signal')
        self.ax.legend()

    def update_lowpass(self, value):
        self.low_cutoff = float(value)
        self.plot_signal()
        self.canvas.draw()

    def update_highpass(self, value):
        self.high_cutoff = float(value)
        self.plot_signal()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    simulator = FilterSimulator(root)
    root.mainloop()
