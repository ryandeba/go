import turtle
import time
import app

# --- Configuration Parameters ---
GRID_SIZE = 9       # N x N grid (e.g., 8 rows and 8 columns)
CELL_SIZE = 50      # Size of each square cell in pixels
DRAW_SPEED = 0      # Fastest drawing speed for setup (0 is fastest)

board = app.Board(size=GRID_SIZE)

def draw_grid_setup():
    """Sets up the turtle screen and draws the N x N grid."""
    
    # --- Screen Setup ---
    screen = turtle.Screen()
    screen.setup(
        width=(GRID_SIZE * CELL_SIZE) + 100, 
        height=(GRID_SIZE * CELL_SIZE) + 100
    )
    screen.title("Turtle Clickable Grid")
    screen.bgcolor("tan")
    
    # Set the coordinate system: 
    # Top-left corner will be (-HalfWidth, +HalfHeight)
    half_size = (GRID_SIZE * CELL_SIZE) / 2
    screen.setworldcoordinates(
        -half_size, 
        -half_size, 
        half_size, 
        half_size
    )

    # --- Drawing Turtle Setup ---
    t = turtle.Turtle()
    t.speed(DRAW_SPEED)
    t.hideturtle()
    t.penup()
    
    # --- Drawing Logic ---
    t.color("gray")
    
    # Start at the bottom-left corner of the grid
    start_x = -half_size + (CELL_SIZE / 2)
    start_y = -half_size + (CELL_SIZE / 2)
    
    # 1. Draw Horizontal Lines
    for i in range(GRID_SIZE):
        y = start_y + (i * CELL_SIZE)
        t.goto(start_x, y) # Move to the start of the line
        t.pendown()
        t.forward((GRID_SIZE - 1) * CELL_SIZE) # Draw across the grid width
        t.penup()

    # 2. Draw Vertical Lines
    t.setheading(90) # Face up (90 degrees)
    for j in range(GRID_SIZE):
        x = start_x + (j * CELL_SIZE)
        t.goto(x, start_y) # Move to the start of the line
        t.pendown()
        t.forward((GRID_SIZE - 1) * CELL_SIZE) # Draw up the grid height
        t.penup()
        
    return screen

def log_click_coordinates(x, y):
    """
    Callback function executed when the turtle screen is clicked.
    Calculates and logs the grid coordinates (column, row).
    """
    
    # --- Click Detection Logic ---
    
    # 1. Convert the Turtle coordinates (centered at 0,0) to 
    #    a 0-indexed pixel distance from the top-left corner.
    
    # Get the grid's total width/height (e.g., 400 pixels)
    total_dim = GRID_SIZE * CELL_SIZE
    
    # Shift x/y from centered coordinates (e.g., -200 to +200) 
    # to standard pixel coordinates (e.g., 0 to 400)
    shifted_x = x + (total_dim / 2)
    shifted_y = y + (total_dim / 2)
    
    # 2. Calculate the Column and Row index using integer division
    # Column (x-axis)
    column_x = int(shifted_x // CELL_SIZE)
    # Row (y-axis) - In screen coordinates, positive Y is UP. 
    # We want Row 0 to be the TOP row, so we need to reverse the index.
    # A click in the top cell (near max Y) should be row 0.
    row_y = int(GRID_SIZE - 1 - (shifted_y // CELL_SIZE))

    # --- Log and Feedback ---
    
    print(f"--- Click Detected ---")
    print(f"Raw Turtle Coordinates: (X: {x:.2f}, Y: {y:.2f})")
    print(f"Calculated Grid Cell: (Column: {column_x}, Row: {row_y})")
    
    color = board.place_stone(column_x, row_y)
    highlight_cell(column_x, row_y, 'black' if color == 1 else 'white')

    board.print()

def highlight_cell(col, row, color):
    """Draws a temporary highlight on the clicked cell."""
    
    highlighter = turtle.Turtle()
    highlighter.hideturtle()
    highlighter.speed(0)
    highlighter.penup()
    highlighter.color(color)
    
    # 1. Calculate the Turtle coordinates for the cell's bottom-left corner.
    
    # Determine the origin shift again
    half_dim = (GRID_SIZE * CELL_SIZE) / 2
    
    # Calculate x-coordinate of the bottom-left corner
    # col * CELL_SIZE is the distance from the left edge (0,0 shifted)
    # Subtract half_dim to get back to the centered Turtle coordinates
    cell_x = (col * CELL_SIZE) - half_dim
    
    # Calculate y-coordinate of the bottom-left corner
    # Since row 0 is the TOP row, we need to map row index to its y-position.
    # The bottom row is GRID_SIZE - 1. 
    # The bottom-left corner's y-coord is based on its row relative to the bottom.
    relative_row = (GRID_SIZE - 1 - row) # e.g., row 0 (top) -> relative_row 7 (bottom)
    cell_y = (relative_row * CELL_SIZE) - half_dim
    
    # 2. Draw the highlight
    highlighter.goto(cell_x, cell_y)
    highlighter.begin_fill()
    highlighter.fillcolor(color)
    highlighter.pensize(3)
    highlighter.pendown()
    
    for _ in range(4):
        highlighter.forward(CELL_SIZE)
        highlighter.left(90)
        
    highlighter.end_fill()
    highlighter.penup()

    # 3. Clear the highlight after a brief moment
    # We can use the screen's ontimer to schedule the erase
    # turtle.Screen().ontimer(highlighter.clear, 500) # Clear after 500 milliseconds

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Setup the screen and draw the grid
    main_screen = draw_grid_setup()
    
    # 2. Bind the click event
    # 'onclick' takes the function to call and the mouse button (1=Left, 2=Middle, 3=Right)
    main_screen.onclick(log_click_coordinates, btn=1)
    
    # 3. Start the Turtle event loop
    main_screen.mainloop()
