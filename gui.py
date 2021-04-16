import sys, matplotlib
import tkinter as tk
import matplotlib.figure
import tkinter.messagebox as msg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from plot import Plot
matplotlib.use('TkAgg')


class PlotGui:
    """Class creates and maintains GUI interface for drawing functions plots"""
    def __init__(self):
        self.help_on = False
        self.plot_figure = None
        self.gui()

    def gui(self):
        """
        main function to coordinate GUI creation functions
        """
        self.root = self.gui_main()
        self.gui_frame_top()
        self.gui_frame_middle_1()
        self.gui_frame_middle_2()
        self.gui_frame_bottom()
        self.root.mainloop()
        return None

    def gui_main(self):
        """
        function creates GUI's main root
        :return: root
        """
        self.x_max = 800
        self.y_max = 450
        root = tk.Tk()
        root.title("Kąstruktor funkcji")
        root.geometry(f"{self.x_max}x{self.y_max}+200+100")
        root.resizable(False, False)
        return root

    def gui_frame_top(self):
        """
        function maintains top side of the GUI
        """
        # rysowanie wzorów latexa na płótnie zapożyczyłem stąd: https://stackoverflow.com/questions/36636185/is-it-possible-for-python-to-display-latex-in-real-time-in-a-text-box
        # Frame top
        self.ft = tk.Frame(self.root, height=120, width=760,
                           highlightbackground='black', highlightthickness=1)
        self.ft.place(x=20, y=10)

        self.func_pattern = tk.StringVar(self.ft)
        self.func_pattern.trace_add("write", self.update_latex)

        self.fig = matplotlib.figure.Figure(figsize=(11, 1), dpi=70)
        self.canvas_pattern = FigureCanvasTkAgg(self.fig, master=self.ft)
        self.canvas_pattern.get_tk_widget().grid(row=0, column=0, columnspan=3)
        self.canvas_pattern._tkcanvas.grid(row=0, column=0, columnspan=3)

        self.update_latex()

        self.label_wprowadz = tk.Label(self.ft, text="Wprowadź wzór funkcji:")
        self.label_wprowadz.config(font=("Courier", 14))
        self.label_wprowadz.grid(row=1, column=1)

        self.entry_pattern = tk.Entry(self.ft, width=126, justify=tk.CENTER, textvariable=self.func_pattern,
                                      highlightbackground='grey', highlightthickness=1)
        self.entry_pattern.grid(row=2, column=0, columnspan=3)
        return None

    def gui_frame_middle_1(self):
        """
        function maintains upper middle side of the GUI
        """
        # frame middle left
        fm1l = tk.Frame(self.root, height=90, width=570)
        fm1l.place(x=20, y=160)

        button_sin = tk.Button(fm1l, text="sin{x}", width=7, command=partial(self.button_func_insert, "\\sin{x}"))
        button_sin.grid(row=0, column=0, padx=5, pady=5)

        button_cos = tk.Button(fm1l, text="cos{x}", width=7, command=partial(self.button_func_insert, "\\cos{x}"))
        button_cos.grid(row=0, column=1, padx=5, pady=5)

        button_tg = tk.Button(fm1l, text="tg{x}", width=7, command=partial(self.button_func_insert, "\\tg{x}"))
        button_tg.grid(row=1, column=0, padx=5, pady=5)

        button_ctg = tk.Button(fm1l, text="ctg{x}", width=7, command=partial(self.button_func_insert, "\\ctg{x}"))
        button_ctg.grid(row=1, column=1, padx=5, pady=5)

        button_pow = tk.Button(fm1l, text="{x}^{a}", width=7, command=partial(self.button_func_insert, "{x}^{a}"))
        button_pow.grid(row=0, column=2, padx=5, pady=5)

        button_sqrt = tk.Button(fm1l, text="sqrt{2}{x}", width=7, command=partial(self.button_func_insert, "\\sqrt{2}{x}"))
        button_sqrt.grid(row=0, column=3, padx=5, pady=5)

        button_ln = tk.Button(fm1l, text="ln{x}", width=7, command=partial(self.button_func_insert, "\\ln{x}"))
        button_ln.grid(row=1, column=2, padx=5, pady=5)

        button_log = tk.Button(fm1l, text="log{a}{x}", width=7, command=partial(self.button_func_insert, "\\log{a}{x}"))
        button_log.grid(row=1, column=3, padx=5, pady=5)

        button_plus = tk.Button(fm1l, text="+", width=7, command=partial(self.button_func_insert, "+"))
        button_plus.grid(row=0, column=4, padx=5, pady=5)

        button_minus = tk.Button(fm1l, text="-", width=7, command=partial(self.button_func_insert, "-"))
        button_minus.grid(row=0, column=5, padx=5, pady=5)

        button_multi = tk.Button(fm1l, text="*", width=7, command=partial(self.button_func_insert, "*"))
        button_multi.grid(row=1, column=4, padx=5, pady=5)

        button_divide = tk.Button(fm1l, text="/", width=7, command=partial(self.button_func_insert, "/"))
        button_divide.grid(row=1, column=5, padx=5, pady=5)

        button_lpar = tk.Button(fm1l, text="(", width=7, command=partial(self.button_func_insert, "("))
        button_lpar.grid(row=0, column=6, padx=5, pady=5)

        button_rpar = tk.Button(fm1l, text=")", width=7, command=partial(self.button_func_insert, ")"))
        button_rpar.grid(row=0, column=7, padx=5, pady=5)

        button_abs = tk.Button(fm1l, text="|x|", width=7, command=partial(self.button_func_insert, "\\abs{x}"))
        button_abs.grid(row=1, column=6, padx=5, pady=5)

        button_frac = tk.Button(fm1l, text="frac{x}{y}", width=7, command=partial(self.button_func_insert, "\\frac{x}{y}"))
        button_frac.grid(row=1, column=7, padx=5, pady=5)


        # frame middle right
        fm1r = tk.Frame(self.root, height=90, width=180)
        fm1r.place(x=600, y=145)

        self.xlabel = tk.StringVar(fm1r)
        self.ylabel = tk.StringVar(fm1r)

        label_opis_osi = tk.Label(fm1r, text="Opis osi:")
        label_opis_osi.config(font=("Courier", 12))
        label_opis_osi.grid(row=0, column=1, columnspan=3)

        label_x = tk.Label(fm1r, text="x:")
        label_x.config(font=("Courier", 12))
        label_x.grid(row=1, column=0)

        label_y = tk.Label(fm1r, text="y:")
        label_y.config(font=("Courier", 12))
        label_y.grid(row=2, column=0, pady=10)

        entry_x = tk.Entry(fm1r, width=25, justify=tk.CENTER, textvariable=self.xlabel,
                           highlightbackground='grey', highlightthickness=1)
        entry_x.grid(row=1, column=1, columnspan=3, sticky='s')

        entry_y = tk.Entry(fm1r, width=25, justify=tk.CENTER, textvariable=self.ylabel,
                           highlightbackground='grey', highlightthickness=1)
        entry_y.grid(row=2, column=1, columnspan=3, pady=10)

        return None

    def button_func_insert(self, func):
        """
        button command for inserting their functions in pattern entry box
        :param func: func string in latex-like syntax
        """
        self.entry_pattern.insert("insert", func)
        return None

    def gui_frame_middle_2(self):
        """
        function maintains lower middle side of the GUI
        """
        # frame middle left
        fm2l = tk.Frame(self.root, height=90, width=400)
        fm2l.place(x=20, y=250)

        # entry labels
        label_xmin = tk.Label(fm2l, text="x min")
        label_xmin.config(font=("Courier", 12))
        label_xmin.grid(row=0, column=1, sticky='w', padx=5)

        label_xmax = tk.Label(fm2l, text="x max")
        label_xmax.config(font=("Courier", 12))
        label_xmax.grid(row=0, column=3, sticky='w', padx=20)

        label_ymin = tk.Label(fm2l, text="y min")
        label_ymin.config(font=("Courier", 12))
        label_ymin.grid(row=0, column=5, sticky='w', padx=20)

        label_ymax = tk.Label(fm2l, text="y max")
        label_ymax.config(font=("Courier", 12))
        label_ymax.grid(row=0, column=7, sticky='w', padx=5)

        # entry boxes
        self.xmin = tk.StringVar(fm2l)
        self.xmax = tk.StringVar(fm2l)
        self.ymin = tk.StringVar(fm2l)
        self.ymax = tk.StringVar(fm2l)

        entry_xmin = tk.Entry(fm2l, width=10, justify=tk.CENTER, textvariable=self.xmin)
        entry_xmin.config(highlightbackground='grey', highlightthickness=1)
        entry_xmin.grid(row=1, column=0, columnspan=2, padx=5)

        entry_xmax = tk.Entry(fm2l, width=10, justify=tk.CENTER, textvariable=self.xmax)
        entry_xmax.config(highlightbackground='grey', highlightthickness=1)
        entry_xmax.grid(row=1, column=2, columnspan=2, padx=20)

        entry_ymin = tk.Entry(fm2l, width=10, justify=tk.CENTER, textvariable=self.ymin)
        entry_ymin.config(highlightbackground='grey', highlightthickness=1)
        entry_ymin.grid(row=1, column=4, columnspan=2, padx=20)

        entry_ymax = tk.Entry(fm2l, width=10, justify=tk.CENTER, textvariable=self.ymax)
        entry_ymax.config(highlightbackground='grey', highlightthickness=1)
        entry_ymax.grid(row=1, column=6, columnspan=2, padx=5)

        # checkboxes
        self.check_zapisz = tk.IntVar()
        self.check_siatka = tk.IntVar(value=1)
        self.check_legenda = tk.IntVar(value=1)
        self.check_nowy = tk.IntVar(value=1)

        cbutton_zapisz = tk.Checkbutton(fm2l, variable=self.check_zapisz)
        cbutton_zapisz.grid(row=3, column=0, columnspan=2)

        cbutton_siatka = tk.Checkbutton(fm2l, variable=self.check_siatka)
        cbutton_siatka.grid(row=3, column=2, columnspan=2)

        cbutton_legenda = tk.Checkbutton(fm2l, variable=self.check_legenda)
        cbutton_legenda.grid(row=3, column=4, columnspan=2)

        cbutton_nowy = tk.Checkbutton(fm2l, variable=self.check_nowy)
        cbutton_nowy.grid(row=3, column=6, columnspan=2)

        label_zapisz = tk.Label(fm2l, text="zapisz")
        label_zapisz.config(font=("Courier", 11))
        label_zapisz.grid(row=2, column=0, columnspan=2)

        label_siatka = tk.Label(fm2l, text="siatka")
        label_siatka.config(font=("Courier", 11))
        label_siatka.grid(row=2, column=2, columnspan=2)

        label_legenda = tk.Label(fm2l, text="legenda")
        label_legenda.config(font=("Courier", 11))
        label_legenda.grid(row=2, column=4, columnspan=2)

        label_nowy = tk.Label(fm2l, text="nowy")
        label_nowy.config(font=("Courier", 11))
        label_nowy.grid(row=2, column=6, columnspan=2)

        # frame middle right
        fm2r = tk.Frame(self.root, height=90, width=350)
        fm2r.place(x=430, y=250)

        self.title_label = tk.StringVar(fm2r)

        label_title = tk.Label(fm2r, text="Tytuł wykresu:")
        label_title.config(font=("Courier", 14))
        label_title.grid(row=0, column=1, pady=10)

        entry_title = tk.Entry(fm2r, width=58, justify=tk.CENTER, textvariable=self.title_label,
                               highlightbackground='grey', highlightthickness=1)
        entry_title.grid(row=1, column=0, columnspan=3)

        return None

    def gui_frame_bottom(self):
        """
        function maintains bottom middle side of the GUI
        """
        fb = tk.Frame(self.root, height=90, width=450)
        fb.place(x=155, y=360)

        button_exit = tk.Button(fb, text="Zakończ\n[Esc]", justify=tk.CENTER,
                                width=20, height=5, command=self.program_end)
        button_exit.grid(row=0, column=0)

        button_draw = tk.Button(fb, text="Rysuj\n[Enter]", justify=tk.CENTER,
                                width=20, height=5, command=self.plot_draw)
        button_draw.grid(row=0, column=1)

        button_pomoc = tk.Button(fb, text="Pomoc", justify=tk.CENTER,
                                width=20, height=5, command=self.help_show)
        button_pomoc.grid(row=0, column=2)

        self.root.bind('<Escape>', self.program_end)
        self.root.bind('<Return>', self.plot_draw)

        return None

    def gui_frame_added(self):
        """
        function maintains added part of the GUI (with plot)
        """
        if self.x_max == 800:
            self.x_max += 700
            self.root.geometry(f"{self.x_max}x{self.y_max}")

        fa = tk.Frame(self.root, height=430, width=690)
        fa.place(x=820, y=10)

        canvas = FigureCanvasTkAgg(self.plot_figure, master=fa)
        canvas.get_tk_widget().pack()
        canvas.draw()
        return None

    def update_latex(self, *args):
        """
        function maintains pattern visualisation
        :param args: just to avoid errors
        """
        self.text_to_convert = self.func_pattern.get()
        self.assist = LatexAssist(self.text_to_convert)
        if self.assist.is_correct:
            text = f"${self.adjust_latex(self.text_to_convert)}$"
        else:
            text = f"{self.text_to_convert}"

        self.fig.clear()
        self.fig.text(0.01, 0.4, text, fontsize=23)
        self.canvas_pattern.draw()
        return None

    def adjust_latex(self, text):
        """
        function converts latex-like pattern to pure latex mathematical pattern
        :param text: latex-like pattern
        :return: converted latex pattern
        """
        finder = 0
        for _ in range(text.count("\\")):
            finder = text.find("\\", finder)
            if finder == -1: break
            if text[finder:finder+4] in ["\\sin", "\\cos", "\\tg{", "\\ctg", "\\ln{"]:
                text = self.adjust_latex_insert_par(text, text.find("{", finder))
            elif text[finder:finder+4]=="\\log":
                first_brace_start = text.find("{", finder)
                first_brace_end = LatexAssist(text, just_check=False, just_find=True, ind_start=first_brace_start).ind
                second_brace_start = first_brace_end+1
                text = self.adjust_latex_insert_par(text, second_brace_start)
            finder +=1
        finder = 0
        for _ in range(text.count("^")):
            finder = text.find("^", finder)
            if finder == -1: break
            text = self.adjust_latex_insert_par(text, finder-1)
            finder +=3

        text = text.replace("\\tg{", "\\tan{")
        text = text.replace("\\ctg{", "\\cot{")
        text = text.replace("\\log{", "\\log_{")
        text = text.replace("(", "\\left(")
        text = text.replace(")", "\\right)")
        if "\\sqrt{" in text:
            for _ in range(text.count("\\sqrt{")):
                brace_start = text.find("\\sqrt{")+5
                brace_end = LatexAssist(text, just_check=False, just_find=True, ind_start=brace_start).ind
                root = text[brace_start+1:brace_end]
                text = text[:text.find("\\sqrt{")]+"^{"+root+"}\\sqrt"+text[brace_end+1:]
        if "\\abs{" in text:
            for _ in range(text.count("\\abs{")):
                brace_start = text.find("\\abs{")+4
                brace_end = LatexAssist(text, just_check=False, just_find=True, ind_start=brace_start).ind
                text = text.replace("\\abs{", "\\left|", 1)
                text = text[:brace_end+1] + "\\right|" + text[brace_end+2:]
        return text

    def adjust_latex_insert_par(self, text, ind_start):
        """
        function inserts parentheses before and after function arguments when it is needed to keep pattern legibly
        (it is used by self.adjust_latex function)
        :param text: pattern
        :param ind_start: ind of one of function brackets
        :return: modified pattern
        """
        if text[ind_start] == "{":
            ind_end = LatexAssist(text, just_check=False, just_find=True, ind_start=ind_start).ind
            text = text[:ind_start+1]+"("+text[ind_start+1:ind_end]+")"+text[ind_end:]
        else:
            ind_end = LatexAssist(text, just_check=False, just_find=True, ind_start=ind_start).ind
            if ind_start-ind_end > 2:
                text = text[:ind_end+1]+"("+text[ind_end+1:ind_start]+")"+text[ind_start:]
        return text

    def plot_draw(self, *args):
        """
        button command for creating function's plot with inserted data. Shows info box if plot cannot be created due to
        argument or pattern issues
        :param args: just to avoid errors
        """
        if self.assist.is_correct:
            args = [self.text_to_convert, self.check_zapisz.get(), self.check_siatka.get(), self.check_legenda.get(), self.check_nowy.get()]
            for i in [self.xmin, self.xmax, self.ymin, self.ymax,
                      self.xlabel, self.ylabel, self.title_label]:
                if i.get() != "":
                    args.append(i.get())
                else:
                    args.append(None)
            args.append(self.plot_figure)

            try:
                self.plot_figure = Plot(*args).figure
                self.gui_frame_added()
            except (ValueError, ZeroDivisionError) as e:
                msg.showinfo("Błędna dziedzina",
                             "Sprawdź, czy podana została poprawna dziedzina funkcji")
            except NameError:
                msg.showinfo("Błędny wzór",
                             "Sprawdź, czy wzór funkcji zapisany jest poprawnie. Zwróć uwagę czy zmienna zapisana jest jako 'x'.")
        else:
            msg.showinfo("Błędny wzór",
                         "Sprawdź, czy wzór funkcji zapisany jest poprawnie. Spróbuj zapisać go korzystając z podanych przycisków.")

        return None

    def help_show(self, *args):
        """
        button command for showing help text; prevents from displaying more than one help window at the time
        :param args: just to avoid errors
        """
        if not self.help_on:
            self.help_box = HelpBox(self)
            self.help_on = True
        else:
            self.help_box.window.focus_force()
        return None

    def program_end(self, *args):
        """
        used to end program and close GUI
        :param args: just to avoid errors
        """
        self.root.destroy()
        sys.exit(0)


class LatexAssist:
    """Class checks if pattern has correct latex-like syntax"""
    def __init__(self, text, just_check=True, just_find=False, ind_start=None):
        """
        :param text: pattern
        :param just_check: True if class is needed to be used for checking if the syntax is correct
        :param just_find: True if class is needed to be used for finding second parenthesis
        :param ind_start: ind of first parenthesis
        """
        if just_check:
            self.is_correct = self.latex_syntax(text, False)
        if just_find and ind_start:
            self.ind = self.brace_search(text, ind_start)

    def latex_syntax(self, text, can_be_empty=True):
        """
        main function which coordinates checking the correctness of the syntax. It uses latex_power, latex_func_names,
        latex_parentheses and latex_brackets functions
        :param text: pattern
        :param can_be_empty: param used in recursive process, its better to turn it to False to mark empty pattern as incorrect
        :return: bool
        """
        if not can_be_empty and text == "": return False
        if " " in text: return False
        if text.count("{") != text.count("}"): return False
        if text.count("(") != text.count(")"): return False

        if "(" in text:
            if not self.latex_parentheses(text): return False

        elif text.find("^") != -1:
            if not self.latex_power(text): return False

        elif text.find("\\") != -1:
            if not self.latex_func_names(text): return False

        elif text.find("{") != -1:
            if not self.latex_brackets(text): return False

        return True

    def latex_parentheses(self, text):
        """
        function checks if parentheses' syntax is correct (if used)
        :param text: pattern
        :return: bool
        """
        par_start = text.find("(")
        par_end = self.brace_search(text, par_start)
        text_1 = text[:par_start]
        text_2 = text[par_start + 1:par_end]
        text_3 = text[par_end + 1:]
        if not self.latex_syntax(text_1+"1"+text_3): return False
        if not self.latex_syntax(text_2, False): return False
        return True

    def latex_power(self, text):
        """
        function checks if power operations' syntax is correct (if such operation is used)
        :param text: pattern
        :return: bool
        """
        pow = text.find("^")
        if pow + 1 >= len(text): return False
        if 1 < pow < len(text) - 2 and text[pow - 1] == "}" and text[pow + 1] == "{":
            text_1 = text[: self.brace_search(text, pow - 1)]
            text_2 = text[self.brace_search(text, pow - 1) + 1: pow - 1]
            text_3 = text[pow + 2: self.brace_search(text, pow + 1)]
            text_4 = text[self.brace_search(text, pow + 1) + 1:]
            if not self.latex_syntax(text_1+"1"+text_4): return False
            if not self.latex_syntax(text_2, False): return False
            if not self.latex_syntax(text_3, False): return False
        else:
            return False
        return True

    def latex_func_names(self, text):
        """
        function checks if functions' syntax is correct (if they are used)
        :param text: pattern
        :return: bool
        """
        func_names_one = ["sin", "cos", "tg", "ctg", "ln", "abs"]
        func_names_two = ["sqrt", "log", "frac"]
        bslash = text.find("\\")
        brace_start = text.find("{", bslash + 1)
        if brace_start == -1: return False
        brace_end = self.brace_search(text, brace_start)
        func_name = text[bslash + 1:brace_start]

        if func_name in func_names_one:
            text_1 = text[:bslash]
            text_2 = text[brace_start + 1:brace_end]
            text_3 = text[brace_end + 1:]
            if not self.latex_syntax(text_1+"1"+text_3): return False
            if not self.latex_syntax(text_2, False): return False

        elif func_name in func_names_two:
            if brace_end + 1 >= len(text): return False
            if text[brace_end + 1] == "{":
                brace_start_2 = brace_end + 1
                brace_end_2 = self.brace_search(text, brace_start_2)
                if not brace_end_2: return False
                text_1 = text[:bslash]
                text_2 = text[brace_start + 1:brace_end]
                text_3 = text[brace_start_2 + 1:brace_end_2]
                text_4 = text[brace_end_2 + 1:]
                if not self.latex_syntax(text_1+"1"+text_4): return False
                if not self.latex_syntax(text_2, False): return False
                if not self.latex_syntax(text_3, False): return False
            else:
                return False

        else:
            return False

        return True

    def latex_brackets(self, text):
        """
        function checks if brackets' syntax is correct (if used)
        :param text: pattern
        :return: bool
        """
        brace_start = text.find("{")
        brace_end = self.brace_search(text, brace_start)
        text_1 = text[:brace_start]
        text_2 = text[brace_start + 1:brace_end]
        text_3 = text[brace_end + 1:]
        if not self.latex_syntax(text_1+"1"+text_3): return False
        if not self.latex_syntax(text_2, False): return False
        return True

    def brace_search(self, text, brace_start_ind):
        """
        function finds matching ending parenthesis or bracket
        :param text: expression
        :param brace_start_ind: first of parentheses' pair
        :return: ind of second parenthesis
        """
        start_end_dict = {"{": "}", "}": "{",
                          "(": ")", ")": "("}
        brace = text[brace_start_ind]
        reversed_brace = start_end_dict[brace]
        open_count = 1
        if brace in ["{", "("]:
            for i in range(brace_start_ind+1, len(text)):
                if text[i] == brace: open_count+=1
                elif text[i] == reversed_brace: open_count-=1
                if open_count == 0:
                    return i
            return False
        elif brace in ["}", ")"]:
            for i in range(brace_start_ind-1, -1, -1):
                if text[i] == brace: open_count+=1
                elif text[i] == reversed_brace: open_count-=1
                if open_count == 0:
                    return i
            return False
        else:
            return False


class HelpBox:
    """Class is used to create and maintain GUI's help window"""
    def __init__(self, gui):
        """
        :param gui: mother-GUI
        """
        self.gui = gui
        self.root = gui.root
        self.box_main()
        self.box_body()
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)

    def box_main(self):
        """
        function creates main window
        """
        self.window = tk.Toplevel(self.root)
        self.window.focus_force()
        self.window.title("Pomoc")
        self.window.geometry("800x550+1000+100")
        self.window.resizable(False,False)
        return None

    def box_body(self):
        """
        function creates window's body
        """
        frame = tk.Frame(self.window, height=530, width=780)
        frame.place(x=10, y=5)

        box = tk.Text(frame, height=33, width=97)
        box.pack()
        box.insert(tk.END, "Funkcje", ("h1"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Aby funkcje były poprawnie interpretowane muszą być zapisane w pseudo-LaTeX'owym formacie:\n"
                           "należy używać funkcji, lub kombinacji funkcji z tych podanych na przyciskach. Format wpisywania "
                           "ich:\n\\Nazwa_funkcji{Argumenty} lub \\Nazwa_funkcji{Argumenty1}{Argumenty2}. "
                           "Pewność że wykres jest\nnarysowany poprawnie jest wtedy gdy na górze wyświetla się poprawnie "
                           "wzór funkcji.", ("p"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Działania", ("h1"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Korzystając z potęgowania należy wpisywać podstawę i wykładnik w nawiasach klamrowych. "
                           "Korzystając z innych działań arytmetycznych nie musimy brać argumentów w nawiasy, jednak "
                           "jeśli działanie tego wymaga, możemy\nużyć nawiasów okrągłych.", ("p"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Coś nie działa?", ("h1"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Sprawdź czy:\n\tnazwy funkcji rozpoczynają się od '\\',\n\targumenty funkcji są podane w "
                           "nawiasach klamrowych,\n\targument oznaczony jest jako 'x',\n\tdobrze określone są zakresy "
                           "argumentów oraz wartości.", ("p"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Czy trzeba podawać wszystkie wartości?", ("h1"))
        box.insert(tk.END, "\n")
        box.insert(tk.END, "Nie trzeba - do narysowania wykresu wystarczy podać poprawny wzór funkcji. Niepodanie opisu "
                           "osi lub tytułu\nskutkuje niezamieszczeniem tych danych na wykresie. Niepodanie zakresu x skutkuje "
                           "stworzeniem wykresu\nna dziedzinie [0, 20], a niepodanie zakresu y dostosowywuje zakres "
                           "automatycznie. Rysując wiele funkcji\nna jednym wykresie warto jednak podać zakresy - inaczej "
                           "widok będzie ustalony na podstawie automatycznych\nwartości przyjętych dla ostatniej z "
                           "podanych funkcji.", ("p"))
        box.tag_add("h1", "1.0", "1.0")
        box.tag_add("p", "1.0", "1.0")
        box.tag_config("h1", justify=tk.CENTER, font=("Times New Roman", 20))
        box.tag_config("p", font=("Times New Roman", 13))
        box.config(state=tk.DISABLED)

        self.window.bind('<Escape>', self.window_close)

        return None

    def window_close(self, *args):
        """
        function maintain help closing process
        :param args: just to avoid errors
        """
        self.root.focus_force()
        self.gui.help_on = False
        self.window.destroy()
        return None
