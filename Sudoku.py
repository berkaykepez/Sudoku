import pygame
import random

pygame.init()

# Defining Sudoku game constants
WIDTH, HEIGHT = 540, 640
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
BUTTON_SIZE = 60
FONT = pygame.font.SysFont("comicsans", 40)
BUTTON_FONT = pygame.font.SysFont("comicsans", 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Function to drawing the Sudoku Grid
def draw_grid(window):
    for i in range(GRID_SIZE + 1):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness) # To draw 10 horizontal lines
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness) # To draw 10 vertical lines

# Function to drawing the Sudoku Numbers on the Grid
def draw_numbers(window, board, temp_board):
    # GRID_SIZE is 9, so it will loop 81 times
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if temp_board[i][j] != 0:  # Checking if the current cell is not empty
                color = BLACK if board[i][j] != 0 else BLUE  # Black for pre-filled random generated board, Blue for player input
                text = FONT.render(str(temp_board[i][j]), 1, color) # 1 is for antialiasing
                window.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 10))

# Function to drawing the number selection buttons from 1 to 9 in the bottom of the game window
def draw_buttons(window, available_numbers, temp_board):
    for i, num in enumerate(available_numbers):
        button_rect = pygame.Rect(i * BUTTON_SIZE, WIDTH, BUTTON_SIZE, BUTTON_SIZE)
        
        # Checking how many times the number is placed on the board
        number_count = sum(row.count(num) for row in temp_board)
        if number_count == 9:
            color = GREY
        else:
            color = BUTTON_HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        
        pygame.draw.rect(window, color, button_rect)
        text = BUTTON_FONT.render(str(num), 1, BLACK)
        window.blit(text, (i * BUTTON_SIZE + 20, WIDTH + 10))

# Function to drawing the selected cell by player selects
def draw_selected(window, pos):
    pygame.draw.rect(window, RED, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)

# Function to updating the screen after starting a new game
def update_screen(window, board, temp_board, pos=None, available_numbers=None):
    window.fill(WHITE)
    draw_grid(window)
    draw_numbers(window, board, temp_board)
    if available_numbers:
        draw_buttons(window, available_numbers, temp_board)
    if pos:
        draw_selected(window, pos)
    pygame.display.update()

# Function to check if a move is valid
def is_valid_move(board, row, col, num):
    
    # Checking if the move is valid in row
    if num in board[row]:
        return False
    # Checking if the move is valid in column
    for i in range(GRID_SIZE):
        if board[i][col] == num:
            return False
    # Checking the 3x3 sub-grid to see if a move is valid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# Function to find an empty space
def find_empty(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return (i, j)
    return None

# Function to solve the board using backtracking
def solve_board(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid_move(board, row, col, i):
            board[row][col] = i

            if solve_board(board):
                return True

            board[row][col] = 0 # If solve_board returns false, clear the cell and try the next number 

    return False

# Function to generating a random Sudoku board
def generate_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Randomly fill the diagonal 3x3 sub-grids
    for i in range(0, GRID_SIZE, 3):
        fill_box(board, i, i)

    # Solving the board
    solve_board(board)

    # Removing random elements to create a new puzzle
    remove_elements(board)

    return board

# Function to filling a 3x3 sub-grids randomly
def fill_box(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

# Function to remove elements to create a puzzle
def remove_elements(board, difficulty=45):
    for _ in range(difficulty):
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        while board[row][col] == 0:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
        board[row][col] = 0

# Main function
def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    # Generate a random Sudoku board
    board = generate_board()
    temp_board = [row[:] for row in board]  # Temporary board to store user inputs

    selected = None
    available_numbers = list(range(1, 10))  # Numbers available for selection
    selected_number = None
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if pos[1] < WIDTH:  # If the click is within the grid area
                    clicked_row = pos[1] // CELL_SIZE
                    clicked_col = pos[0] // CELL_SIZE
                    # Ensure the selection is within the 9x9 grid
                    if clicked_row < GRID_SIZE and clicked_col < GRID_SIZE:
                        selected = (clicked_row, clicked_col)
                        selected_number = None  # Clear the number selection when square is picked
                else:  # If the click is within the button area
                    button_index = pos[0] // BUTTON_SIZE
                    if button_index < len(available_numbers) and selected:
                        selected_number = available_numbers[button_index]  # Select the number
                        row, col = selected
                        if temp_board[row][col] == 0 and is_valid_move(temp_board, row, col, selected_number):
                            temp_board[row][col] = selected_number  # Place the selected number
                            selected = None  # Clear the selection after placing
                        selected_number = None  # Clear the number selection after placing

            if event.type == pygame.KEYDOWN:
                if selected and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    # Convert the keypress to the corresponding number (1-9)
                    selected_number = event.key - pygame.K_0
                    row, col = selected
                    if temp_board[row][col] == 0 and is_valid_move(temp_board, row, col, selected_number):
                        temp_board[row][col] = selected_number
                        selected = None  # Clear the selection after placing

                # Allowing player to deleting numbers entered by player with backspace or delete key
                if event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                    if selected:
                        row, col = selected
                        if board[row][col] == 0:  # Only allow deleting in cells where the original board is empty
                            deleted_number = temp_board[row][col]
                            temp_board[row][col] = 0  # Clear the cell
                            selected = None  # Deselect after clearing the cell

        update_screen(window, board, temp_board, selected, available_numbers)

    pygame.quit()

if __name__ == "__main__":
    main()