import math  # używane w eval
import numpy as np
from matplotlib.figure import Figure


class Plot:
    """A tool to convert latex-like function pattern to python mathematical function and to generate plot figure"""
    def __init__(self, pattern, save, grid, legend, new,
                 xmin, xmax, ymin, ymax, xlabel, ylabel, title, plot):
        """
        :param pattern: string of pattern written in latex-like syntax
        :param save: 0 not to save or 1 to save
        :param grid: 0 not to show or 1 to show
        :param legend: 0 not to show (and either will not be shown in future plots when plotting on same figure) or 1 to show
        :param new: 0 to use previous plot fig (if such exists) 1 to use new plot fig
        :param xmin: starting argument (can be None then will be taken as default)
        :param xmax: ending argument (can be None then will be taken as default)
        :param ymin: min shown value (can be None then will be taken as default)
        :param ymax: max shown value (can be None then will be taken as default)
        :param xlabel: x label describe (can be None then x label's describe will not be shown)
        :param ylabel: y label describe (can be None then y label's describe will not be shown)
        :param title: plot title (can be None then plot title will not be shown)
        :param plot: plot figure (can be None if such don't exists)
        """
        self.pattern = self.latex_multiply(pattern)
        self.pattern = self.latex_pseudo_to_math(self.pattern)
        self.figure = self.plotting_main(save, grid, legend, new, xmin, xmax, ymin, ymax, xlabel, ylabel, title, plot)

    def latex_multiply(self, text):
        """
        function's purpose is to prevent invalid syntax that is quite natural for users: don't using multiply signs
        between expressions. It inserts those signs when it's needed
        :param text: pattern
        :return: converted pattern
        """
        num, dot, func, alpha, par = False, False, False, False, False
        i=0
        while True:
            if text[i] in ["+", "-", "*", "/"]:
                num, dot, func, alpha, par = False, False, False, False, False

            elif text[i].isdecimal() or text[i]==".":
                if text[i].isdecimal() and (alpha or func or par):
                    text = text[:i]+"*"+text[i:]
                    i-=1
                elif text[i].isdecimal(): num = True
                elif text[i]=="." and dot==False and num==True: dot = True
                else: raise ValueError

            elif text[i].isalpha():
                if num or func or alpha or par:
                    text = text[:i]+"*"+text[i:]
                    i-=1
                else: alpha = True

            elif text[i]=="\\":
                if num or alpha or func or par:
                    text = text[:i]+"*"+text[i:]
                    i-=1
                elif text[i:i+3] in ["\\tg", "\\ln"]:
                    text_1 = text[:i+4]
                    text_2 = self.latex_multiply(text[i+4:self.brace_search(text, i+3)])
                    text_3 = text[self.brace_search(text, i+3):]
                    text = text_1 + text_2 + text_3
                    i+=3+len(text_2)+1
                    func = True
                elif text[i:i+4] in ["\\sin", "\\cos", "\\ctg", "\\abs"]:
                    text_1 = text[:i+5]
                    text_2 = self.latex_multiply(text[i+5:self.brace_search(text, i+4)])
                    text_3 = text[self.brace_search(text, i+4):]
                    text = text_1 + text_2 + text_3
                    i+=4+len(text_2)+1
                    func = True
                elif text[i:i+4] == "\\log":
                    first_brace_start = i+4
                    first_brace_end = self.brace_search(text, first_brace_start)
                    second_brace_start = first_brace_end+1
                    second_brace_end = self.brace_search(text, second_brace_start)

                    text_1 = text[:first_brace_start+1]
                    text_2 = self.latex_multiply(text[first_brace_start+1:first_brace_end])
                    text_3 = self.latex_multiply(text[second_brace_start+1:second_brace_end])
                    text_4 = text[second_brace_end:]
                    text = text_1 + text_2 +"}{"+ text_3 + text_4
                    i+=4+len(text_2)+2+len(text_3)+1
                    func = True
                elif text[i:i+5] in ["\\sqrt", "\\frac"]:
                    first_brace_start = i+5
                    first_brace_end = self.brace_search(text, first_brace_start)
                    second_brace_start = first_brace_end+1
                    second_brace_end = self.brace_search(text, second_brace_start)

                    text_1 = text[:first_brace_start+1]
                    text_2 = self.latex_multiply(text[first_brace_start+1:first_brace_end])
                    text_3 = self.latex_multiply(text[second_brace_start+1:second_brace_end])
                    text_4 = text[second_brace_end:]
                    text = text_1 + text_2 +"}{"+ text_3 + text_4
                    i+=5+len(text_2)+2+len(text_3)+1
                    func = True

            elif text[i]=="(":
                if num or alpha or func or par:
                    text = text[:i]+"*"+text[i:]
                    i-=1
                else:
                    text_1 = text[:i+1]
                    text_2 = self.latex_multiply(text[i+1:self.brace_search(text,i)])
                    text_3 = text[self.brace_search(text,i):]
                    text = text_1 + text_2 + text_3
                    i+=len(text_2) + 1
                    par = True

            elif text[i]=="{" and "^" in text:
                if num or alpha or func or par:
                    text = text[:i]+"*"+text[i:]
                    i-=1
                else:
                    first_brace_start = i
                    first_brace_end = self.brace_search(text, first_brace_start)
                    second_brace_start = first_brace_end+2
                    second_brace_end = self.brace_search(text, second_brace_start)

                    text_1 = text[:first_brace_start+1]
                    text_2 = self.latex_multiply(text[first_brace_start+1:first_brace_end])
                    text_3 = self.latex_multiply(text[second_brace_start+1:second_brace_end])
                    text_4 = text[second_brace_end:]
                    text = text_1 + text_2 +"}^{"+ text_3 + text_4
                    i+=len(text_2)+3+len(text_3)+1
                    func = True

            i+=1
            if i>=len(text):break
        return text

    def latex_pseudo_to_math(self, text):
        """
        main function to coordinate converting syntax from latex-like to python math. It uses latex_func_one,
        latex_func_two, latex_power and latex_const
        :param text: latex-like function pattern
        :return: text converted to python math
        """
        if "\\" in text:
            text = self.latex_func_two(text)
            text = self.latex_func_one(text)

        if "^" in text:
            text = self.latex_power(text)

        if "e" in text or "pi" in text:
            text = self.latex_const(text)
        return text

    def latex_func_one(self, text):
        """
        function's purpose is to safely convert one-argument functions from latex-like syntax to python
        :param text: pattern
        :return: converted pattern
        """
        text_start = text
        if text.find("\\sin") != -1:
            name_start = text.find("\\sin")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(math.sin({arg}))" + text[arg_end+1:]

        if text.find("\\cos") != -1:
            name_start = text.find("\\cos")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(math.cos({arg}))" + text[arg_end+1:]

        if text.find("\\tg") != -1:
            name_start = text.find("\\tg")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(math.tan({arg}))" + text[arg_end+1:]

        if text.find("\\ctg") != -1:
            name_start = text.find("\\ctg")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(1/(math.tan({arg})))" + text[arg_end+1:]

        if text.find("\\ln") != -1:
            name_start = text.find("\\ln")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(math.log({arg}))" + text[arg_end+1:]

        if text.find("\\abs") != -1:
            name_start = text.find("\\abs")
            name_end = text.find("{", name_start+1)
            arg_start = name_end+1
            arg_end = self.brace_search(text, arg_start-1)

            arg = text[arg_start:arg_end]
            text = text[:name_start] + f"(abs({arg}))" + text[arg_end+1:]

        if text == text_start:
            return text
        else:
            return self.latex_pseudo_to_math(text)

    def latex_func_two(self, text):
        """
        function's purpose is to safely convert two-argument functions from latex-like syntax to python
        :param text: pattern
        :return: converted pattern
        """
        text_start = text
        if text.find("\\sqrt") != -1:
            name_start = text.find("\\sqrt")
            name_end = text.find("{", name_start+1)
            arg1_start = name_end+1
            arg1_end = self.brace_search(text, arg1_start-1)
            arg2_start = arg1_end+2
            arg2_end = self.brace_search(text, arg2_start-1)

            arg1 = text[arg1_start:arg1_end]
            arg2 = text[arg2_start:arg2_end]
            text = text[:name_start] + f"(({arg2})**(1/{arg1}))" + text[arg2_end+1:]

        if text.find("\\log") != -1:
            name_start = text.find("\\log")
            name_end = text.find("{", name_start+1)
            arg1_start = name_end+1
            arg1_end = self.brace_search(text, arg1_start-1)
            arg2_start = arg1_end+2
            arg2_end = self.brace_search(text, arg2_start-1)

            arg1 = text[arg1_start:arg1_end]
            arg2 = text[arg2_start:arg2_end]
            text = text[:name_start] + f"(math.log(({arg2}), ({arg1})))" + text[arg2_end+1:]

        if text.find("\\frac") != -1:
            name_start = text.find("\\frac")
            name_end = text.find("{", name_start+1)
            arg1_start = name_end+1
            arg1_end = self.brace_search(text, arg1_start-1)
            arg2_start = arg1_end+2
            arg2_end = self.brace_search(text, arg2_start-1)

            arg1 = text[arg1_start:arg1_end]
            arg2 = text[arg2_start:arg2_end]
            text = text[:name_start] + f"(({arg1})/({arg2}))" + text[arg2_end+1:]

        if text == text_start:
            return text
        else:
            return self.latex_pseudo_to_math(text)

    def latex_power(self, text):
        """
        function's purpose is to safely convert power expression functions from latex-like syntax to python
        :param text: pattern
        :return: converted pattern
        """
        text_start = text
        power_ind = text.find("^")
        brace_1_end = power_ind-1
        brace_1_start = self.brace_search(text, brace_1_end)
        brace_2_start = power_ind+1
        brace_2_end = self.brace_search(text, brace_2_start)

        arg1 = text[brace_1_start+1:brace_1_end]
        arg2 = text[brace_2_start+1:brace_2_end]
        text = text[:brace_1_start] + f"(({arg1})**({arg2}))" + text[brace_2_end+1:]

        if text == text_start:
            return text
        else:
            return self.latex_pseudo_to_math(text)

    def latex_const(self, text):
        """
        function converts all 'pi' and 'e' to 'math.pi' and 'math.e'. It also prevents from accidentally using 'math.math.pi' etc
        :param text: expression
        :return: converted expression
        """
        if text.find("e") != -1:
            const_pos = text.find("e")
            if text[const_pos-5:const_pos] != "math.":
                text = text.replace("e", "math.e", 1)

            const_pos = text.find("e")
            checked = text[:const_pos + 1]
            unchecked = text[const_pos+1:]
            text = checked + self.latex_const(unchecked)

        if text.find("pi") != -1:
            const_pos = text.find("pi")
            if const_pos <5 or text[const_pos-5:const_pos] != "math.":
                text = text.replace("pi", "math.pi", 1)

            const_pos = text.find("pi")
            checked = text[:const_pos+2]
            unchecked = text[const_pos+2:]
            text = checked + self.latex_const(unchecked)

        return text

    def brace_search(self, text, brace_start_ind):
        """
        metod copied from LatexAssist due not to import whole class; usage: finding matching ending parenthesis or bracket
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

    def plotting_main(self, save, grid, legend, new, xmin, xmax, ymin, ymax, xlabel, ylabel, title, plot):
        """
        main function to coordinate constructing a plot when params are given. It uses plotting_args, plotting_values and
        plotting_plot functions. Function pattern must be assigned to self.pattern as a string of python math function
        where 'x' is argument

        :param save: 0 not to save or 1 to save
        :param grid: 0 not to show or 1 to show
        :param legend: 0 not to show (and either will not be shown in future plots when plotting on same figure) or 1 to show
        :param new: 0 to use previous plot fig (if such exists) 1 to use new plot fig
        :param xmin: starting argument (can be None then will be taken as default)
        :param xmax: ending argument (can be None then will be taken as default)
        :param ymin: min shown value (can be None then will be taken as default)
        :param ymax: max shown value (can be None then will be taken as default)
        :param xlabel: x label describe (can be None then x label's describe will not be shown)
        :param ylabel: y label describe (can be None then y label's describe will not be shown)
        :param title: plot title (can be None then plot title will not be shown)
        :param plot: plot figure (can be None if such don't exists)
        :return: plot figure
        """
        xs = self.plotting_args(xmin, xmax)
        ys = self.plotting_values(xs)
        plot = self.plotting_plot(save, grid, legend, new, xs, ys, ymin, ymax, xlabel, ylabel, title, plot)
        return plot

    def plotting_args(self, xmin, xmax):
        """
        function generates plotting arguments. If one of xmin, xmax (or both) are not given, they will be taken as default
        :param xmin: starting argument (can be None then will be taken as default)
        :param xmax: ending argument (can be None then will be taken as default)
        :return: arguments numpy linspace
        """
        if xmin and ("e" or "pi" in xmin): xmin = str(eval(self.latex_const(xmin)))
        if xmax and ("e" or "pi" in xmax): xmax = str(eval(self.latex_const(xmax)))

        if not xmin and not xmax:
            xmin, xmax = 0, 20
        elif xmin and not xmax:
            xmax = float(xmin)+20
        elif not xmin and xmax:
            xmin = float(xmax)-20

        xmin, xmax = float(xmin), float(xmax)

        if xmax<xmin:
            raise ValueError
        elif xmax == xmin:
            raise ValueError
        else:
            length = abs(xmax-xmin)
            if length<10: length = 20
            return np.linspace(xmin, xmax, int((length*500)//1))

    def plotting_values(self, xs):
        """
        function calculates function values. Pattern must be assigned to self.pattern variable as a string where 'x' is
        argument. Function prevent from generating wrong plots due to asymptotic function tangent
        :param xs: numpy linspace of arguments
        :return: numpy array of values
        """
        ys = []
        for x in xs:
            ys.append(eval(self.pattern.replace("x", f"{str(x)}")))
        ys = np.array(ys)
        if "tan" in self.pattern:
            ys[:-1][np.diff(ys) > 200] = np.nan
        return ys

    def plotting_plot(self, save, grid, legend, new, xs, ys, ymin, ymax, xlabel, ylabel, title, plot):
        """
        function generates and personalises plot using given values
        :param save: 0 not to save or 1 to save
        :param grid: 0 not to show or 1 to show
        :param legend: 0 not to show (and either will not be shown in future plots when plotting on same figure) or 1 to show
        :param new: 0 to use previous plot fig (if such exists) 1 to use new plot fig
        :param xs: numpy linspace of arguments (but can be just a list)
        :param ys: numpy linspace of values (but can be just a list)
        :param ymin: min shown value (can be None then will be taken as default)
        :param ymax: max shown value (can be None then will be taken as default)
        :param xlabel: x label describe (can be None then x label's describe will not be shown)
        :param ylabel: y label describe (can be None then y label's describe will not be shown)
        :param title: plot title (can be None then plot title will not be shown)
        :param plot: plot figure (can be None if such don't exists)
        :return: plot fig
        """
        if new or not plot:
            if plot:
                fig = plot
                fig.clear()
            else:
                fig = Figure(figsize=(9, 6), dpi=72)
        else:
            fig = plot

        if not ymin or not ymax:
            if not ymin and not ymax: ymin, ymax = min(ys)-0.2, max(ys)+0.2
            if ymin and not ymax: ymax = max(ys)+0.2
            if not ymin and ymax: ymin = min(ys)-0.2

        ymin, ymax = float(ymin), float(ymax)

        ax = fig.add_subplot(111)
        ax.plot(xs, ys, figure=fig, label=self.pattern if legend else "_"+self.pattern)
        ax.set_xlim(xs[0], xs[-1])
        ax.set_ylim(ymin, ymax)

        if title:
            ax.set_title(title, fontsize=16)

        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, rotation=90, fontsize=14)

        if legend:
            ax.legend(loc='upper right', prop={'size': 12})
        else:
            pass

        if grid:
            ax.grid(True)
        else:
            ax.grid(False)

        if save:
            if title:
                fig.set_figheight(17)
                fig.set_figwidth(21)
                ax.set_title(title, fontsize=40)
                ax.set_xlabel(xlabel, fontsize=35)
                ax.set_ylabel(ylabel, rotation=90, fontsize=35)
                ax.tick_params(labelsize=20)
                if legend:
                    ax.legend(loc='upper right', prop={'size': 31})

                fig.savefig(f"{title.replace(' ', '_')}.png")

                fig.set_figheight(6)
                fig.set_figwidth(9)
                ax.set_title(title, fontsize=16)
                ax.set_xlabel(xlabel, fontsize=14)
                ax.set_ylabel(ylabel, rotation=90, fontsize=14)
                ax.tick_params(labelsize=10)
                if legend:
                    ax.legend(loc='upper right', prop={'size': 12})
            else:
                fig.set_figheight(17)
                fig.set_figwidth(21)
                ax.set_xlabel(xlabel, fontsize=35)
                ax.set_ylabel(ylabel, rotation=90, fontsize=31)
                ax.tick_params(labelsize=20)
                if legend:
                    ax.legend(loc='upper right', prop={'size': 30})

                fig.savefig("wykres.png")

                fig.set_figheight(6)
                fig.set_figwidth(9)
                ax.set_xlabel(xlabel, fontsize=14)
                ax.set_ylabel(ylabel, rotation=90, fontsize=14)
                ax.tick_params(labelsize=10)
                if legend:
                    ax.legend(loc='upper right', prop={'size': 12})

        return fig
