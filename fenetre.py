import pygame
from pygame.locals import *
from  RuzzleGame import *
import sys

HEIGHT = 4
WIDTH = 4
pygame.init()
size = width, height = 1440, 650
R = Ruzzle()

#Ouverture de la fenêtre Pygame
screen = pygame.display.set_mode(size)

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Fonts
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 20)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

smallFontSpace = 21

# Set the pygame window name 
pygame.display.set_caption('Grid Solver')

# loading and pasting of the background "fond"
fond = pygame.image.load("ruzzle.jpg").convert()
screen.blit(fond, (0, 0))

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Draw board
def draw_board(board):
	cells = []
	for i in range(HEIGHT):
		row = []
		for j in range(WIDTH):

			# Draw rectangle for cell
			rect = pygame.Rect(
				board_origin[0] + j * cell_size,
				board_origin[1] + i * cell_size,
				cell_size, cell_size
			)
			pygame.draw.rect(screen, WHITE, rect)
			pygame.draw.rect(screen, BLACK, rect, 5)

			# Populate Grid
			letter = moveFont.render((str(board[i][j])).upper(), True, BLACK)
			letterTextRect = letter.get_rect()
			letterTextRect.center = rect.center
			screen.blit(letter, letterTextRect)


def message_to_screen(msg):
	tmp0 = 0
	tmp1 = 0
	tmp2 = 0
	tmp3 = 0
	tmp4 = 0
	for words in msg:
		screen_text = smallFont.render(words, True, BLACK)
		tmp0 += smallFontSpace
		if tmp0 <= height - 50:
			screen.blit(screen_text, [width*5/8+50, tmp0])
		elif tmp0 > height - 50 and tmp1 < height - 50:
			tmp1 += smallFontSpace
			screen.blit(screen_text, [width*5/8+50 + 100, tmp1])
		elif tmp1 > height - 50 and tmp2 <= height - 50:
			tmp2 += smallFontSpace
			screen.blit(screen_text, [width*5/8+50 + 200, tmp2])
		elif tmp2 > height - 50 and tmp3 <= height - 50:
			tmp3 += smallFontSpace
			screen.blit(screen_text, [width*5/8+50 + 300, tmp3])
		else:
			tmp4 += smallFontSpace
			screen.blit(screen_text, [width*5/8+50 + 400, tmp4])


draw_board(R.grid)
message_to_screen(R.find_all())
print(R.grid)
print(R.find_all())

# Update the screen
pygame.display.flip()

# Quit loop
continuer = 1
while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 0
