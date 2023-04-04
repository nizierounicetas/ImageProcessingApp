import tkinter as tk
from tkinter import filedialog, font, messagebox
from PIL import Image, ImageTk
from functions import *

class ImageProcessingApp:
    f_types = [('PNG Images', '*.png'),
               ('JPG Images', '*.jpg *.jpeg'),
               ('GIF Images', '*.gif'),
               ('Icons', '*.ico')]

    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Image processing")
        self.master.minsize(500, 500)
        self.master.iconbitmap(resource_path("pics/image.ico"))
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.original_image = None
        self.processed_image = None
        self.processed_image_raw = None

        self.nonlinear_parameter = tk.IntVar()

        self.contrast = tk.DoubleVar()
        self.brightness = tk.IntVar()
        self.popup_cancelled = False

        menubar = tk.Menu(self.master, background='blue', font=font.Font(weight=font.BOLD))

        image_menu = tk.Menu(menubar, tearoff=0)
        image_menu.add_command(label='Open', command=self.load_image)
        image_menu.add_command(label='Reset', command=self.reset_image)
        image_menu.add_command(label='Apply', command=self.apply_image)
        image_menu.add_separator()
        image_menu.add_command(label='Save result', command=self.save_image)
        menubar.add_cascade(label='Image', menu=image_menu)

        nonlinear_filter_menu = tk.Menu(menubar, tearoff=0)
        nonlinear_filter_menu.add_command(label='minimum', command=lambda: self.process_nonlinear(np.min))
        nonlinear_filter_menu.add_command(label='median', command=lambda: self.process_nonlinear(np.median))
        nonlinear_filter_menu.add_command(label='maximum', command=lambda: self.process_nonlinear(np.max))
        menubar.add_cascade(label='Nonlinear filter', menu=nonlinear_filter_menu)

        contrast_menu = tk.Menu(menubar, tearoff=0)
        contrast_menu.add_command(label='Linear contrast', command=self.process_linear_contrast)

        histogram_menu = tk.Menu(contrast_menu, tearoff=0)
        histogram_menu.add_command(label='RGB', command=self.process_histogram_equalization_RGB)
        histogram_menu.add_command(label='HSV(V)', command=self.process_histogram_equalization_HSV_V)
        contrast_menu.add_cascade(label='Histogram equalization', menu=histogram_menu)
        menubar.add_cascade(label='Contrast enhancement', menu=contrast_menu)

        self.master.config(menu=menubar)

        self.canvas = tk.Canvas(self.master, bg="grey", width=400, height=400)
        self.canvas.pack(anchor=tk.CENTER, expand=1)


    def apply_image(self):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return
        self.original_image = self.processed_image

    def reset_image(self):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        self.processed_image = self.original_image
        self.processed_image_raw = ImageTk.PhotoImage(self.original_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)

    def load_image(self):
        try:
            # Открываем диалоговое окно для выбора файла
            file_path = filedialog.askopenfilename(filetypes=self.f_types)

            if file_path is None or file_path == '':
                return

            # raw_image = Image.open(file_path).resize((400, 400))
            # self.image = ImageTk.PhotoImage(raw_image)
            self.original_image = self.processed_image = Image.open(file_path)
            self.processed_image_raw = ImageTk.PhotoImage(self.original_image)

            self.master.minsize(max(self.processed_image_raw.width() + 10, 500), max(self.processed_image_raw.height() + 10, 500))
            self.canvas.config(height=self.processed_image_raw.height(), width=self.processed_image_raw.width())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)

        except:
            messagebox.showerror(message='Error')

    def open_popup_nonlinear(self):
        popup = tk.Toplevel(self.master)
        popup.iconbitmap(resource_path("pics/image.ico"))
        popup.protocol("WM_DELETE_WINDOW", lambda: [self.set_popup_cancelled(True), popup.destroy()])

        width = 200
        height = 150
        x = self.master.winfo_x() + 10
        y = self.master.winfo_y() + 10

        popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        label = tk.Label(popup, text="Enter amount:")
        label.pack(side=tk.TOP, padx=10, pady=10)
        entry = tk.Entry(popup, textvariable=self.nonlinear_parameter)
        entry.pack(side=tk.TOP, padx=10, pady=10)

        button = tk.Button(popup, text="OK", command=lambda: [self.set_popup_cancelled(False), popup.destroy()])
        button.pack(side=tk.TOP, padx=10, pady=10)
        return popup

    def set_popup_cancelled(self, value):
        self.popup_cancelled = value

    def open_popup_linear_contrast(self):

        popup = tk.Toplevel(self.master)
        popup.iconbitmap(resource_path("pics/image.ico"))
        popup.protocol("WM_DELETE_WINDOW", lambda: [self.set_popup_cancelled(True), popup.destroy()])

        width = 200
        height = 200
        x = self.master.winfo_x() + 10
        y = self.master.winfo_y() + 10

        popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        label_contrast = tk.Label(popup, text="Enter contrast:")
        label_contrast.pack(side=tk.TOP, padx=10, pady=10)

        entry_contrast = tk.Entry(popup, textvariable=self.contrast)
        entry_contrast.pack(side=tk.TOP, padx=10, pady=10)

        label_brightness = tk.Label(popup, text="Enter brightness:")
        label_brightness.pack(side=tk.TOP, padx=10, pady=10)

        entry_brightness = tk.Entry(popup, textvariable=self.brightness)
        entry_brightness.pack(side=tk.TOP, padx=10, pady=10)

        button = tk.Button(popup, text="OK", command=lambda:[self.set_popup_cancelled(False), popup.destroy()])
        button.pack(side=tk.TOP, padx=10, pady=10)
        return popup

    def process_nonlinear(self, statistics_function):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        self.master.wait_window(self.open_popup_nonlinear())
        if self.popup_cancelled:
            return

        try:
            if self.nonlinear_parameter.get() <= 0:
                raise Exception

            numpy_image = np.array(self.original_image)
            opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            self.processed_image = Image.fromarray(nonlinear_filter(opencv_image,
                                                                                    self.nonlinear_parameter.get(),
                                                                                       statistics_function))
            self.processed_image_raw = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)
        except:
            messagebox.showerror(message='You should enter positive integer value', title='Error')

    def process_linear_contrast(self):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        self.master.wait_window(self.open_popup_linear_contrast())
        if self.popup_cancelled:
            return

        try:
            if self.contrast.get() < 0 or not -255 <= self.brightness.get() <= 255:
                raise Exception

            numpy_image = np.array(self.original_image)
            opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

            self.processed_image = Image.fromarray(linear_contrast(opencv_image, self.contrast.get(), self.brightness.get()))
            self.processed_image_raw = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)

        except:
            messagebox.showerror(
                message='Contrast value should be non-negative\nBrightness value should be integer in [-255;255]',
                                 title='Error')

    def save_image(self):
        if self.processed_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=self.f_types)

        if file_path:
            self.processed_image.save(file_path)
            messagebox.showinfo(message='Result is saved', title='Success')

    def process_histogram_equalization_RGB(self):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        numpy_image = np.array(self.original_image)
        opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        self.processed_image = Image.fromarray(histogram_equalization_RGB(opencv_image))
        self.processed_image_raw = ImageTk.PhotoImage(self.processed_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)


    def process_histogram_equalization_HSV_V(self):
        if self.original_image is None:
            messagebox.showinfo(message='Image is not chosen', title='Attention')
            return

        numpy_image = np.array(self.original_image)
        opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        self.processed_image = Image.fromarray(histogram_equalization_HSV(opencv_image))
        self.processed_image_raw = ImageTk.PhotoImage(self.processed_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.processed_image_raw)

    def on_closing(self):
        if tk.messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

    def start(self):
        self.master.mainloop()

if __name__ == "__main__":
    ImageProcessingApp().start()

# pyinstaller --windowed -F --add-data "pics/image.ico;pics" --icon=pics/image.ico -d bootloader main.py --name image_processing --onefile