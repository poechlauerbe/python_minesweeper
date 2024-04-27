import random
import os
import re

def check_neighbors(table, x, y):
	if table[y][x] != 0:
		return table
	sum = 0
	neighbors = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
	for dx, dy in neighbors:
		nx, ny = x + dx, y + dy
		if 0 <= nx < len(table[0]) and 0 <= ny < len(table):
			# Access the neighbor at (nx, ny)
			if table[ny][nx] == "*":
				sum += 1
	table[y][x] = str(sum)
	return table

def place_mines(table_solution, size_x, size_y):
	bomb = random.randint(0, size_x * size_y - 1)
	x = bomb % size_x
	y = bomb // size_x
	if table_solution[y][x] == "*":
		place_mines(table_solution, size_x, size_y)
	else:
		table_solution[y][x] = "*"
	return table_solution

def setup_game(size_x, size_y, num_mines):
	table_solution = setup_board(size_x, size_y, 0)
	random.seed()
	for i in range(num_mines):
		table_solution = place_mines(table_solution, size_x, size_y)
	for y in range(size_y):
		for x in range(size_x):
			table_solution = check_neighbors(table_solution, x, y)
	return table_solution

def setup_board(size_x, size_y, symbol = "#"):
	table = [[symbol for i in range(size_x)] for j in range(size_y)]
	return table

def print_table(table):
	os.system('clear')
	print("Minesweeper - " + str(num_mines) + " mines hidden\n")
	print("field: x: " + str(size_x) + " y: " + str(size_y) + "\n")
	for row in table:
		for cell in row:
			print(cell, end="  ")
		print("\n")
	return

def input_and_check(sign):
	while(sign == 'x'):
		inp = input("Enter the x coordinate: ")
		if (inp.isnumeric() and int(inp) >= 1 and int(inp) <= size_x):
			return int(inp) - 1
		else:
			print("Wrong input - please try again")
	while(sign == 'y'):
		inp = input("Enter the y coordinate: ")
		if (inp.isnumeric() and int(inp) >= 1 and int(inp) <= size_y):
			return int(inp) - 1
		else:
			print("Wrong input - please try again")


def set_flag(table):
	x = input_and_check('x')
	y = input_and_check('y')
	if table[y][x] == "F":
		# unflag
		table[y][x] = "#"
	elif table[y][x] == "#":
		# flag
		table[y][x] = "F"
	else:
		print("Invalid input")
		table = set_flag(table)
	return table

def reveal_neighbors(table, table_solution, x, y):
	neighbors = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
	for dx, dy in neighbors:
		nx, ny = x + dx, y + dy
		if 0 <= nx < len(table[0]) and 0 <= ny < len(table):
			if table_solution[ny][nx] == "0" and table[ny][nx] == "#":
				table[ny][nx] = table_solution[ny][nx]
				table = reveal_neighbors(table, table_solution, nx, ny)
			table[ny][nx] = table_solution[ny][nx]
	return table

def reveal(table, table_solution, flag = 0, x = 0):
	if flag == 0:
		x = input_and_check('x')
	y = input_and_check('y')
	if table[y][x] == "F":
		return table
	if table_solution[y][x] == "*":
		table[y][x] = table_solution[y][x]
		print_table(table)
		print("  ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ██╗")
		print(" ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║")
		print(" ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝██║")
		print(" ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚═╝")
		print(" ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██╗")
		print("  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝")
		return False
	elif table_solution[y][x] != "0":
		table[y][x] = table_solution[y][x]
	else:
		table[y][x] = table_solution[y][x]
		table = reveal_neighbors(table, table_solution, x, y)
	return table

def input_check(table, table_solution, size_x, size_y, num_mines):
	next_step = input("\nWhat you want to do? (f)lag, (r)eveal, (q)uit? ")
	if next_step == "f":
		table = set_flag(table)
	elif next_step == "r":
		table = reveal(table, table_solution)
	elif next_step == "q":
		print("Exiting game...")
		return False
	elif int(next_step) >= 1 and int(next_step) <= size_x:
		if not reveal(table, table_solution, 1, int(next_step) - 1):
			return False
	else:
		print("Invalid input")
		input_check(table, table_solution, size_x, size_y, num_mines)
	return table

def check_win(table, num_mines):
	sum = 0
	for y in range(len(table)):
		for x in range(len(table[0])):
			if table[y][x] == "#" or table[y][x] == "F":
				sum += 1
	if sum == num_mines:
		return True
	else:
		return False

def start_game():
	num = 0
	while True:
		os.system('clear')
		print("Welcome to Minesweeper!\n")
		print("Do you need any help - press 0 + Enter\n")
		print("Start new game:\n\n   - for easy: press 1 + Enter\n\n   - for medium: press 2 + Enter\n\n   - for hard: press 3 + Enter\n\n   - to quit: press q + Enter\n")
		if num == 0:
			inp = input("Enter your choice: ")
		else:
			inp = input("Wrong input - please try again: ")
		if inp == "1" or inp == "2" or inp == "3":
			break
		elif inp == "q" or inp == "Q":
			print("Exiting game...")
			exit()
		num = 1
		os.system('clear')
		if inp == "0":
			print("Welcome to Minesweeper!\n")
			print("Minesweeper is a single-player puzzle game. The objective of the game is to clear a rectangular board containing hidden mines without detonating any of them, with help from clues about the number of neighboring mines in each field. \n\nYou have to type in the x and y coordinates to reveal fields.\nIf you think on one spot is a bomb you can flag this spot.\nIf you want to remove the flag you can do this by flagging the same spot again.\n\nGood luck!\n\n")
			input("Press Enter to continue...")
			num = 0
	if inp == "1":
		global size_x
		global size_y
		global num_mines
		size_x = 10
		size_y = 10
		num_mines = 10
	elif inp == "2":
		size_x = 15
		size_y = 15
		num_mines = 40
	elif inp == "3":
		size_x = 20
		size_y = 20
		num_mines = 80

size_x = 10
size_y = 10
num_mines = 10


start_game()
table_solution = setup_game(size_x, size_y, num_mines)
table = setup_board(size_x, size_y)
print_table(table)

while table != False:
	table = input_check(table, table_solution, size_x, size_y, num_mines)
	if table == False:
		break
	else:
		print_table(table)
	if check_win(table, num_mines):
		print(" ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗██╗██╗██╗")
		print(" ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║██║██║██║")
		print("  ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║██║██║██║")
		print("   ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║╚═╝╚═╝╚═╝")
		print("    ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║██╗██╗██╗")
		print("    ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝╚═╝╚═╝")

		break
