#!/usr/bin/env python3
"""
Space Mining Empire - GUI Version
"""

import tkinter as tk
from game.gui_engine import GameGUI

def main():
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()