from tkinter import Tk, Canvas, Button, Frame
from random import randint

WIDTH = 540
HEIGHT= int(WIDTH)
BACKGROUND = "#FFFFFF"

CELLSIZE    = 10 # dimension CELLSIZE * CELLSIZE
CELLSNUMBER = (WIDTH*HEIGHT) // (CELLSIZE*CELLSIZE)

CELLS_ON_ROW = WIDTH // CELLSIZE
CELLS_ON_COLUMN = HEIGHT // CELLSIZE

DEBUG = False

def binarynot(bit):
	return (0 if bit == 1 else 1)

class Application(object):

	def __init__(self):

		self.tk = Tk()
		self.can = Canvas(self.tk, width = WIDTH, height = HEIGHT, background = BACKGROUND)

		self.binds()

		self.cells = CELLSNUMBER*[0]
		self.havechanged = [] # Indicates which cell have changed since last survival phase
		self.celladding_queue = []

		self.button_frame = Frame(self.tk)

		self.standby = False
		self.standby_button = Button(self.button_frame, text = "Standby", command = self.switch_standby)

		self.button_frame.grid(row = 0, column = 0)
		self.can.grid(row = 1, column = 0)
		self.standby_button.grid(row = 0, column = 0)

	def binds(self):
		self.can.focus_set()
		self.can.bind("<Button-1>", self.click)

		self

	def survival_phase(self):

		count = 0
		neighbours = 0
		living = False
		cells = self.cells
		old_state = 0

		todie = []
		toborn = []

		while count < CELLSNUMBER:

			old_state = cells[count]

			if count % CELLS_ON_ROW == 0: # If cells is on left border

				neighbours = cells[count + 1]

				if count == 0: # TOP LEFT
					neighbours += cells[count + CELLS_ON_ROW] + cells[count + CELLS_ON_ROW + 1] \
					+ cells[CELLS_ON_ROW - 1] + cells[2*CELLS_ON_ROW - 1] \
					+ cells[CELLSNUMBER - 1] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] \
					+ cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW + 1]

				elif count == (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW: # BOTTOM LEFT
					neighbours += cells[count - CELLS_ON_ROW] + cells[count - CELLS_ON_ROW + 1] \
					+ cells[CELLSNUMBER - 1] + cells[CELLSNUMBER - 1 - CELLS_ON_ROW] \
					+ cells[CELLS_ON_ROW - 1] + cells[0] + cells[1]

				else:
					neighbours += cells[count - CELLS_ON_ROW] + cells[count - CELLS_ON_ROW + 1] \
					+ cells[count + 1] + cells[count + CELLS_ON_ROW] + cells[count + CELLS_ON_ROW + 1] \
					+ cells[count - 1] + cells[count + CELLS_ON_ROW - 1] + cells[count + 2*CELLS_ON_ROW - 1]

			elif count < CELLS_ON_ROW: # If cells is on top border

				neighbours = cells[count + CELLS_ON_ROW]

				if count == 0: # TOP LEFT
					neighbours += cells[0] + cells[count + CELLS_ON_ROW + 1] \
					+ cells[CELLS_ON_ROW - 1] + cells[2*CELLS_ON_ROW - 1] \
					+ cells[CELLSNUMBER - 1] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] \
					+ cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW + 1]

				elif count == CELLS_ON_ROW - 1: # TOP RIGHT
					neighbours += cells[count - 1] + cells[count - 1 + CELLS_ON_ROW] \
					+ cells[0] + cells[CELLS_ON_ROW] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] \
					+ cells[CELLSNUMBER - 1] + cells[CELLSNUMBER - 2]

				else:
					neighbours += cells[count - 1] + cells[count + CELLS_ON_ROW - 1] \
					+ cells[count + 1] + cells[count + CELLS_ON_ROW + 1] + cells[count + (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] \
					+ cells[count + (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW - 1] + cells[count + (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW + 1]

			elif count >= (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW: # If cells is on bottom border

				neighbours = cells[count - CELLS_ON_ROW]
				
				if count == (CELLS_ON_COLUMN - 1) * CELLS_ON_ROW: # BOTTOM LEFT
					neighbours += cells[count + 1] + cells[count - CELLS_ON_ROW + 1] \
					+ cells[CELLSNUMBER - 1] + cells[CELLSNUMBER - 1 - CELLS_ON_ROW] \
					+ cells[CELLS_ON_ROW - 1] + cells[0] + cells[1] 

				elif count == CELLSNUMBER - 1: # BOTTOM RIGHT
					neighbours += cells[count - 1] + cells[count - 1 - CELLS_ON_ROW] \
					+ cells[0] + cells[CELLS_ON_ROW - 1] + cells[CELLS_ON_ROW - 2] \
					+ cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW - CELLS_ON_ROW] 

			elif count % CELLS_ON_ROW == CELLS_ON_ROW - 1: # If cells is on right border
				
				neighbours = cells[count - 1]

				if count == CELLS_ON_ROW - 1: # TOP RIGHT
					neighbours += cells[count + CELLS_ON_ROW] + cells[count - 1 + CELLS_ON_ROW] \
					+ cells[0] + cells[CELLS_ON_ROW] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] \
					+ cells[CELLSNUMBER - 1] + cells[CELLSNUMBER - 2] 

				elif count == CELLSNUMBER - 1: # BOTTOM RIGHT
					neighbours += cells[count - CELLS_ON_ROW] + cells[count - 1 - CELLS_ON_ROW] \
					+ cells[0] + cells[CELLS_ON_ROW - 1] + cells[CELLS_ON_ROW - 2] \
					+ cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW] + cells[(CELLS_ON_COLUMN - 1) * CELLS_ON_ROW - CELLS_ON_ROW] 

				else:
					neighbours += cells[count - 1 - CELLS_ON_ROW] + cells[count - 1 + CELLS_ON_ROW] \
					+ cells[count - CELLS_ON_ROW] + cells[count + CELLS_ON_ROW] + cells[count - CELLS_ON_ROW - 1] \
					+ cells[count - CELLS_ON_ROW - 1 - CELLS_ON_ROW] + cells[count - CELLS_ON_ROW - 1 - CELLS_ON_ROW] 

			else:
				neighbours = cells[count - 1] + cells[count + 1] + cells[count - CELLS_ON_ROW] \
				+ cells[count - CELLS_ON_ROW - 1] + cells[count - CELLS_ON_ROW + 1] \
				+ cells[count + CELLS_ON_ROW] + cells[count + CELLS_ON_ROW - 1] \
				+ cells[count + CELLS_ON_ROW + 1]

			living = cells[count] == 1

			# Underpopulation
			if living and neighbours < 2:
				todie.append(count)

			# Overpopulation
			elif living and neighbours > 3:
				todie.append(count)

			# Reproduction
			elif not living and neighbours == 3:
				toborn.append(count)

			if count in todie or count in toborn:
				self.havechanged.append(count)

			count += 1

		for cell in todie:
			cells[cell] = 0
		for cell in toborn:
			cells[cell] = 1

	def refresh_canvas_cells(self):

		x, y = 0, 0
		color = ""

		# DEBUG
		if DEBUG and len(self.havechanged) != 0:
			print("\n\t=== Refresh Phase ===")
			print("havechanged = {}".format(self.havechanged))
			# END

		for cell in self.havechanged:
			if DEBUG:
				print("cell N°{}, state : {}".format(cell, self.cells[cell]))
			x = (cell %  CELLS_ON_ROW) * CELLSIZE
			y = (cell // CELLS_ON_ROW) * CELLSIZE

			color = ("#000000" if self.cells[cell] == 1 else "#FFFFFF")

			self.can.create_rectangle(x, y, x + CELLSIZE, y + CELLSIZE, 
				fill = color, outline = color)

		# DEBUG
		if DEBUG and len(self.havechanged) != 0:
			print("\t=== END refresh ===\n\n")
			# END

		for cell in self.celladding_queue:
			if DEBUG:
				print("cell N°{}, state : {}".format(cell, self.cells[cell]))
			x = (cell %  CELLS_ON_ROW) * CELLSIZE
			y = (cell // CELLS_ON_ROW) * CELLSIZE

			color = ("#000000" if self.cells[cell] == 1 else "#FFFFFF")

			self.can.create_rectangle(x, y, x + CELLSIZE, y + CELLSIZE, 
				fill = color, outline = color)

		self.can.update_idletasks()

	def reset_changed_cells(self):
		self.havechanged = []

	def reset_adding_queue(self):
		self.celladding_queue = []

	def click(self, mouseclick):
		self.switch_cell(mouseclick.x, mouseclick.y)

	def switch_cell(self, x, y):
		
		cellnum = self.determine_cell_from_pixel(x, y)

		print("Click == cell N°{}, new state : {}".format(cellnum, self.cells[cellnum]))
		if not cellnum in self.celladding_queue:
			self.celladding_queue.append(cellnum)

	def pixel_neighbourhood_bordered(self, x, y, radius):

		pixels = []

		if x - radius < 0:
			for i in range(1, radius + 1):
				pixels.append((x + i, y))
				if y == 0:
					pixels.extend([(x + i, y + i), (x, y + i)])
				elif y == HEIGHT - 1:
					pixels.extend([(x + i, y - i), (x, y - i)])
				else:
					pixels.extend([(x + i, y + i), (x, y + i),
						(x + i, y - i), (x, y - i)]) # LEFT

		elif x + radius > WIDTH - 1:
			for i in range(1, radius + 1):
				pixels.append((x - i, y))
				if y == 0:
					pixels.extend([(x - i, y + i), (x, y + i)])
				elif y == HEIGHT - 1:
					pixels.extend([(x - i, y - i), (x, y - i)])
				else:
					pixels.extend([(x - i, y + i), (x, y + i),
						(x - i, y - i), (x, y - i)]) # RIGHT

		elif y - radius < 0:
			for i in range(1, radius + 1):
				pixels.append((x, y + i))
				if x == 0:
					pixels.extend([(x + i, y), (x + i, y + i)])
				elif x == WIDTH - 1:
					pixels.extend([(x - i, y), (x - i, y + i)])
				else:
					pixels.extend([(x + i, y), (x + i, y + i), 
						(x - i, y), (x - i, y + i)]) # TOP

		elif y + radius > HEIGHT - 1:
			for i in range(1, radius + 1):
				pixels.append((x, y - i))
				if x == 0:
					pixels.extend([(x + i, y), (x + i, y - i)])
				elif x == WIDTH - 1:
					pixels.extend([(x - i, y), (x - i, y - i)])
				else:
					pixels.extend([(x + i, y), (x + i, y - i), 
						(x - i, y), (x - i, y - i)]) # BOTTOM
		
		else:
			for i in range(1, radius + 1):
				pixels.extend([(x + i, y), (x + i, y - i),
					(x, y - i), (x - i, y - i), (x - i, y),
					(x - i, y + i), (x, y + i), (x + i, y + i)])

		return pixels

	def determine_cell_from_pixel(self, x, y):
		basex = x - (x % CELLSIZE)
		basey = y - (y % CELLSIZE)
		cellnum = (basey * CELLS_ON_ROW + basex) // CELLSIZE
		return cellnum

	def apply_user_cells(self):
		for cell in self.celladding_queue:
			self.cells[cell] = binarynot(self.cells[cell])

	def phase_loop(self):

		if not self.standby:
			self.survival_phase()
			self.apply_user_cells()
			self.refresh_canvas_cells()
			self.reset_changed_cells()

		else:
			self.apply_user_cells()
			self.refresh_canvas_cells()
		
		self.reset_adding_queue()

		self.tk.after(20, self.phase_loop)

	def switch_standby(self):
		self.standby = not self.standby
		

	def run(self):
		self.phase_loop()
		self.tk.mainloop()

def main():

	app = Application()
	app.run()

	return 0

main()