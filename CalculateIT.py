import tkinter as tk
from functools import partial


class CalcWindow(tk.Frame):
    """A simple calculator program.

    The main window inherits from tkinter Frame module."""
    def __init__(self, parent=None):
        """The program is initialised with tk module of tkinter as a root.
        In the init method all the widgets are drawn."""
        tk.Frame.__init__(self, parent)
        self.grid(sticky='news')
        self.parent = parent
        self.drawGUI()
        self.drawScreen()
        self.drawButtons()

    def drawGUI(self):
        self.parent.geometry('300x400')
        self.parent.minsize(width=200, height=300)
        self.parent.maxsize(width=400, height=600)
        self.parent.title('CalculateIT')
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight=1)

    def drawScreen(self):
        self.displayVal = 0
        self.screen = tk.Text(self, height = 1, width = 30)
        self.screen.insert(tk.END, self.displayVal)
        self.screen.tag_config('value', justify = 'right')
        self.screen.tag_add('value', 1.0)
        self.screen.grid(row = 0, column = 0, sticky = 'ew', columnspan = 4)
        self.screen.config(state=tk.DISABLED)

    def insertChar(self, textWidget, character, indexLine):
        """Used to insert given modificator as long as it is eligible in the last number.

        textWidget(tk.Text obj)
        inputLine(str) - line extracted from tkinter text widget.
        character(str) - given modificator
        indexLine(str) - 'start' for the start of last number
                         'end' for the ending of last number"""
        tempLine = str(textWidget.get(1.0, tk.END))[::-1]
        currentInd = 1
        for char in tempLine:
            currentInd -= 1
            if char == character:
                return None
            elif char in ['-', 'x', '+', chr(247)]:
                textWidget.config(state=tk.NORMAL)
                if indexLine == 'end':
                    if tempLine[1] in ['-', 'x', '+', chr(247)]:
                        textWidget.insert(tk.END, '0')
                    textWidget.insert(tk.END, character)
                    textWidget.config(state=tk.DISABLED)
                else:
                    currentInd = len(textWidget.get(1.0, tk.END)) + currentInd
                    lengthInt = len(str(currentInd))
                    indexOfScreen = 1 + (currentInd/(10**lengthInt))
                    textWidget.insert(indexOfScreen, character)
                    self.screen.tag_add('value', 1.0)
                    textWidget.config(state=tk.DISABLED)

                return None
        textWidget.config(state=tk.NORMAL)
        if indexLine == 'end':
            textWidget.insert(tk.END, character)
        else:
            textWidget.insert(1.0, character)
            self.screen.tag_add('value', 1.0)
        textWidget.config(state=tk.DISABLED)
        return None

    def addModificator(self, screenWidget, modificator):
        tempStr = str(screenWidget.get(1.0, tk.END))
        if tempStr[-2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '%']:
            screenWidget.config(state=tk.NORMAL)
            screenWidget.insert(tk.END, modificator)
            screenWidget.config(state=tk.DISABLED)
        elif tempStr[-2] == ',':
            screenWidget.config(state=tk.NORMAL)
            screenWidget.insert(tk.END, 0)
            screenWidget.insert(tk.END, modificator)
            screenWidget.config(state=tk.DISABLED)

    def typeVal(self, number):
        if self.screen.get(1.0, tk.END)[-2] != '%':
            self.screen.config(state=tk.NORMAL)
            if len(self.screen.get(1.0, tk.END)) == 2 and (self.screen.get(1.0) == '0'):
                self.screen.delete(1.0, tk.END)
            self.screen.insert(tk.END, number)
            self.screen.tag_add('value', 1.0)
            self.screen.config(state=tk.DISABLED)

    def clearValues(self):
        self.screen.config(state=tk.NORMAL)
        self.screen.delete(1.0, tk.END)
        self.screen.insert(tk.END, 0)
        self.screen.tag_add('value', 1.0)
        self.screen.config(state=tk.DISABLED)

    def changeSign(self):
        self.insertChar(self.screen, '-', 'beg')

    def makePercent(self):
        self.insertChar(self.screen, '%', indexLine = 'end')

    def makeCalc(self):
        theLine = self.screen.get(1.0, tk.END)

        def calculations(wholeLine):
            if len(wholeLine) == 0:
                return 0
            for char in wholeLine:
                if char == 'x' or char == chr(247):
                    if char == 'x':
                        split = wholeLine.split('x', 1)
                        return calculations(split[0]) * calculations(split[1])
                    else:
                        split = wholeLine.split(chr(247), 1)
                        return calculations(split[0]) / calculations(split[1])

                elif char == '+' or char == '-':
                    if char == '+':
                        split = wholeLine.split('+', 1)
                        return calculations(split[0]) + calculations(split[1])
                    else:
                        split = wholeLine.split('-', 1)
                        return calculations(split[0]) - calculations(split[1])
            for char in wholeLine:
                if char == '%':
                    return float(wholeLine[:-1])/100
            return float(wholeLine)

        self.screen.config(state=tk.NORMAL)
        self.screen.delete(1.0, tk.END)
        theValue = calculations(theLine[:-1])
        self.screen.insert(tk.END, theValue)
        self.screen.insert(tk.END, 0)
        self.screen.tag_add('value', 1.0)
        self.screen.config(state=tk.DISABLED)

    def addComa(self):
        self.insertChar(self.screen, '.', 'end')

    def drawButtons(self):

        gridCoords = []
        buttonList = ['AC', '+/-', '%', chr(247),
                      '1', '2', '3',  'x',
                      '4', '5', '6', '-',
                      '7', '8', '9', '+',
                      '0', '.', '=']
        for row in range(1, 6):
            self.rowconfigure(row, weight = 1)
            for column in range(4):
                gridCoords.append((row, column))
                self.columnconfigure(column, weight=1)
        for btn in range(len(buttonList)):
            if buttonList[btn] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                self.button = tk.Button(self, text=buttonList[btn], command=partial(self.typeVal, buttonList[btn]))
            elif buttonList[btn] == 'AC':
                self.button = tk.Button(self, text = buttonList[btn], command=self.clearValues)
            elif buttonList[btn] == '+/-':
                self.button = tk.Button(self, text = buttonList[btn], command=self.changeSign)
            elif buttonList[btn] == '%':
                self.button = tk.Button(self, text=buttonList[btn], command=self.makePercent)
            elif buttonList[btn] == '=':
                self.button = tk.Button(self, text=buttonList[btn], command=self.makeCalc)
            elif buttonList[btn] in [chr(247), "x", "-", "+"]:
                self.button = tk.Button(self, text=buttonList[btn], command=partial(self.addModificator, self.screen,
                                                                                    buttonList[btn]))
            elif buttonList[btn] == '.':
                self.button = tk.Button(self, text=buttonList[btn], command=self.addComa)

            self.button.grid(row=gridCoords[btn][0], column=gridCoords[btn][1], sticky='news')

def appIni():
    root = tk.Tk()
    app = CalcWindow(root)

    app.mainloop()


if __name__ == "__main__":
    appIni()
