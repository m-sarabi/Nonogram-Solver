import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Checks if the filled cell is within the row/column constraints
# cell: position in the table
# tab: the table list
# is_row: True if checking the row constraints, otherwise False
# val: the value that we put on the cell position (1 or 0)
def isvalid(cell, tab, is_row, val):
    line_sum = 0  # row/column sum
    if is_row:  # calculating the line_sum and defining general variables for uniting the row/column function
        for i in tab[cell[0]]:
            if i == 1:
                line_sum += i
        line_c = tab[cell[0]][:cell[1] + 1]  # the row/col values up to current cell position
        constraints = row_con[cell[0]]  # current row/cell constraints
        length = cols  # length of the row/col
    else:
        for i in tab:
            if i[cell[1]] == 1:
                line_sum += i[cell[1]]
        constraints = col_con[cell[1]]
        line_c = []
        for i in tab[:cell[0] + 1]:
            line_c.append(i[cell[1]])
        cell = [cell[1], cell[0]]
        length = rows

    if line_sum > sum(constraints):  # if sum of the all black cells are longer than what it should be, then go back!
        return False

    string = ''  # converting the line_c to a string
    groups = []
    for i in line_c:
        if i == 1:
            string += '1'
        elif i == 0:
            string += ' '

    # splitting the string above into groups array which represents individual groups of '1'
    group_str = string.strip().split(' ')
    for i in range(len(group_str)):
        group_str[i] = group_str[i].strip()
    while '' in group_str:
        group_str.remove('')
    for i in group_str:
        groups.append(len(i))

    # Maybe not necessary? if the number of current groups are more than what it should be
    if len(groups) > len(constraints):
        return False

    # if we filled a cell, the current group should not be longer than the current group as constraints say
    if val == 1 and groups[-1] > constraints[len(groups) - 1]:
        return False
    # if we made a cell white, then current group should not be shorter than the current group
    elif val == 0 and groups and groups[-1] < constraints[len(groups) - 1]:
        return False

    # if we reached the end of the row/col, number and length of the groups should match the constraints
    if cell[1] == length - 1:
        if groups != constraints:
            return False
    return True


# verify function to see if we are within the row/col constraints
def Verify(cell, tab, val):
    return isvalid(cell, tab, True, val) and isvalid(cell, tab, False, val)


# find the next empty cell
def empty_cell(tab):
    for i in range(len(row_con)):
        for j in range(len(col_con)):
            if tab[i][j] == -1:
                cell = [i, j]
                return cell
    return False


# Backtrack Solving function
def backtrack(tab):
    cell = empty_cell(tab)
    if not cell:
        return True

    for i in [1, 0]:
        tab[cell[0]][cell[1]] = i
        if Verify(cell, tab, i):
            if backtrack(tab):
                return True
        if i == 0:
            tab[cell[0]][cell[1]] = -1
    return False


# Logically finds the cells that should be filled by overlapping the two extreme situation
# to-do: merge the row and column overlapping functions
def overlap_row(tab):
    # looping through the rows
    for i in range(rows):
        # difference of the length of the row and all necessary filled cells including the one empty cell between
        diff = len(tab[0]) - (sum(row_con[i]) + len(row_con[i]) - 1)
        n = 0  # for keeping track of the current cell
        # if the cell group is longer than the difference, there has to be some filled cells
        # finds the position and fill them
        for j in row_con[i]:
            for k in range(j):
                if k == (j - 1) and j > diff:
                    for m in range(j - diff):
                        tab[i][n - m] = 1
                n += 1
            n += 1

        row_sum = 0  # sum of the current row filled cells
        for j in tab[i]:
            if j == 1:
                row_sum += 1

        # if sum is equal to the sum of row constraints, we have filled the whole row (1)
        # make the rest of the cells white (0)
        if row_sum == sum(row_con[i]):
            for j in range(cols):
                if tab[i][j] == -1:
                    tab[i][j] = 0


# the same thing as overlap_row, this time going through columns
def overlap_col(tab):
    for i in range(cols):
        diff = len(tab) - (sum(col_con[i]) + len(col_con[i]) - 1)
        n = 0
        for j in col_con[i]:
            for k in range(j):
                if k == (j - 1) and j > diff:
                    for m in range(j - diff):
                        tab[n - m][i] = 1
                n += 1
            n += 1

        col_sum = 0
        for j in tab:
            if j[i] == 1:
                col_sum += j[i]

        if col_sum == sum(col_con[i]):
            for j in range(rows):
                if tab[j][i] == -1:
                    tab[j][i] = 0


def generate_table():
    global rows, cols, colcon_entry, rowcon_entry, solve_button, tab_labels, frame_table
    rows = row_entry.get()
    cols = col_entry.get()
    if not rows or not cols:
        return
    rows = int(rows)
    cols = int(cols)
    tab_labels = []
    colcon_entry = []
    rowcon_entry = []
    frame_table = tk.Frame(main, bg='lightgray')
    frame_table.grid(row=1, column=0, padx=10)
    for i in range(cols):
        colcon_entry.append(tk.Entry(frame_table, width=5))
        colcon_entry[i].grid(row=0, column=i + 1, ipady=8)
    for i in range(rows):
        rowcon_entry.append(tk.Entry(frame_table, width=5))
        rowcon_entry[i].grid(row=i + 1, column=0, ipady=8)
    for i in range(rows):
        tab_labels.append([])
        for j in range(cols):
            tab_labels[i].append(tk.Label(frame_table, width=4, height=2))
            tab_labels[i][j].grid(row=i + 1, column=j + 1, padx=1, pady=1)
    solve_button["state"] = tk.NORMAL
    new_btn['state'] = tk.NORMAL
    build_button['state'] = tk.DISABLED


def solve_function():
    global row_con, col_con
    row_con = []
    col_con = []
    for i in range(rows):
        if rowcon_entry[i].get():
            row_con.append(rowcon_entry[i].get())
            row_con[i] = row_con[i].split(' ')
        else:
            print('ERROR')
            return

    for i in range(cols):
        if colcon_entry[i].get():
            col_con.append(colcon_entry[i].get())
            col_con[i] = col_con[i].split(' ')
        else:
            print('ERROR')
            return
    for i in range(rows):
        for j in range(len(row_con[i])):
            row_con[i][j] = int(row_con[i][j])
    for i in range(cols):
        for j in range(len(col_con[i])):
            col_con[i][j] = int(col_con[i][j])

    table = []
    for ii in range(rows):
        table.append([])
        for jj in range(cols):
            table[ii].append(-1)

    overlap_row(table)
    overlap_col(table)
    success = backtrack(table)
    if not success:
        tk.messagebox.showinfo('ERROR', 'Puzzle can not be solved!')
    else:
        for i in range(rows):
            for j in range(cols):
                if table[i][j] == 0:
                    tab_labels[i][j]['bg'] = 'white'
                elif table[i][j] == 1:
                    tab_labels[i][j]['bg'] = 'black'


def new_board():
    frame_table.destroy()
    solve_button["state"] = tk.DISABLED
    new_btn['state'] = tk.DISABLED
    build_button['state'] = tk.NORMAL


rowcon_entry = []
colcon_entry = []
row_con = []
col_con = []
tab_labels = []

main = tk.Tk()
# main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)

main.title('Nonogram Solver')
main.config(bg='alice blue')
frame_menu = tk.Frame(main, bg='MistyRose', highlightbackground='green', highlightthickness=1)
frame_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

frame_table = tk.Frame(main, bg='lightgray')
# frame_table.grid(row=0, column=1, padx=10)

rows_frame = tk.Frame(frame_menu, bg='MistyRose')
tk.Label(frame_menu, text="Rows").grid(row=0, column=0, padx=5, pady=5)
row_entry = tk.Entry(frame_menu, width=10)
row_entry.grid(row=0, column=1, padx=5, pady=5)

# tk.ttk.Separator(frame_menu, orient=tk.VERTICAL).grid(row=0, column=1, rowspan=2, sticky='ns', padx=(0, 10))

tk.Label(frame_menu, text="Cols").grid(row=0, column=2, padx=5, pady=5)
col_entry = tk.Entry(frame_menu, width=10)
col_entry.grid(row=0, column=3, padx=5, pady=5)

tk.ttk.Separator(frame_menu, orient=tk.VERTICAL).grid(row=0, column=4, rowspan=2, sticky='ns', padx=15)
# tk.ttk.Separator(frame_menu).grid(row=6, sticky='ew')
rows = 0
cols = 0
build_button = tk.Button(frame_menu, text='Build', command=generate_table, width=5)
build_button.grid(row=0, column=5, padx=5, pady=5)

new_btn = tk.Button(frame_menu, text='New', command=new_board, state=tk.DISABLED, width=5)
new_btn.grid(row=0, column=6, padx=5, pady=5)

tk.ttk.Separator(frame_menu, orient=tk.VERTICAL).grid(row=0, column=7, rowspan=2, sticky='ns', padx=15)

solve_button = tk.Button(frame_menu, text='Solve', command=solve_function, state=tk.DISABLED, width=5)
solve_button.grid(row=0, column=8, padx=5, pady=5, rowspan=2)


main.resizable(0, 0)
main.geometry('760x700')
main.mainloop()
