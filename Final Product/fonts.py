import tkinter.font as tkfont


def configure():
    # family = "Segoe UI"
    family = "Georgia"
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=20, family=family)
    text_font = tkfont.nametofont("TkTextFont")
    text_font.configure(size=15, family=family)
    fixed_font = tkfont.nametofont("TkFixedFont")
    fixed_font.configure(size=15, family=family)
