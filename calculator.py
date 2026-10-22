
import tkinter as tk
import ast
import operator

root = tk.Tk()
root.title("Calculator")
root.geometry("390x590")
root.resizable(False, False)
root.configure(bg="#202020")

expression = tk.StringVar(value="0")

display = tk.Entry(
    root,
    textvariable=expression,
    font=("Segoe UI", 36),
    bg="#202020",
    fg="white",
    bd=0,
    justify="right",
    insertbackground="white"
)
display.pack(fill="x", padx=15, pady=(35, 25), ipady=10)

frame = tk.Frame(root, bg="#202020")
frame.pack(expand=True, fill="both", padx=4, pady=4)

def press(value):
    current = expression.get()

    if value == "C":
        expression.set("0")
    elif value == "⌫":
        expression.set(current[:-1] or "0")
    elif value == "=":
        try:
            expression.set(str(calculate(current)))
        except Exception:
            expression.set("Error")
    elif value == "±":
        try:
            expression.set(str(-float(current)))
        except ValueError:
            pass
    elif value == "x²":
        try:
            expression.set(str(float(current) ** 2))
        except ValueError:
            expression.set("Error")
    elif value == "√":
        try:
            expression.set(str(float(current) ** 0.5))
        except ValueError:
            expression.set("Error")
    elif value == "1/x":
        try:
            expression.set(str(1 / float(current)))
        except (ValueError, ZeroDivisionError):
            expression.set("Error")
    elif value == "%":
        try:
            expression.set(str(float(current) / 100))
        except ValueError:
            expression.set("Error")
    else:
        if current == "0" or current == "Error":
            expression.set(value)
        else:
            expression.set(current + value)

def calculate(text):
    # Safely evaluate basic arithmetic expressions
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Invalid expression")

    return evaluate(ast.parse(text, mode="eval"))

buttons = [
    ["MC", "MR", "M+", "M−", "MS", "M▼"],
    ["%", "CE", "C", "⌫"],
    ["1/x", "x²", "√", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="]
]

def button_click(value):
    conversions = {"×": "*", "÷": "/", "−": "-"}
    if value == "CE":
        expression.set("0")
    elif value in ("MC", "MR", "M+", "M−", "MS", "M▼"):
        return
    else:
        press(conversions.get(value, value))

for r, row in enumerate(buttons):
    frame.rowconfigure(r, weight=1)
    for c, value in enumerate(row):
        frame.columnconfigure(c, weight=1)

        color = "#303030"
        if value == "=":
            color = "#D7A1E8"
        elif value in ("%", "CE", "C", "⌫", "1/x", "x²", "√",
                       "÷", "×", "−", "+"):
            color = "#353535"

        btn = tk.Button(
            frame,
            text=value,
            font=("Segoe UI", 14),
            bg=color,
            fg="white",
            activebackground="#505050",
            activeforeground="white",
            bd=0,
            command=lambda v=value: button_click(v)
        )
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

root.mainloop()
