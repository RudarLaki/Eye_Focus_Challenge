import tkinter as tk
from ui.main_menu import MainMenu

def main():
    root = tk.Tk()
    root.title("Sequence Challenge Game")

    try:
        root.state("zoomed")
    except Exception:
        root.geometry(
            f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-50}"
        )

    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
