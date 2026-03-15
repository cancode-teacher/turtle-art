import turtle

### SETUP ###
screen = turtle.Screen()
screen.title("Motif")
screen.setup(width=900, height=300)
screen.bgcolor("#ffffff")
screen.tracer(3, 10)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.penup()

### HELPER ###
def pick_colour(colour):
    """Set the fill AND outline colour for the next shape."""
    t.fillcolor(colour)
    t.pencolor(colour)


### FUNCTIONS FOR DRAWING SHAPES ###
def draw_diamond(x, y, half_width, half_height, colour):
    """
    Draw a solid diamond (rhombus) centred at (x, y).
    half_width  = how far the diamond reaches left and right
    half_height = how far the diamond reaches up and down
    """
    pick_colour(colour)
    t.goto(x, y + half_height)   # top point
    t.pendown()
    t.begin_fill()
    t.goto(x + half_width, y)    # right point
    t.goto(x, y - half_height)   # bottom point
    t.goto(x - half_width, y)    # left point
    t.goto(x, y + half_height)   # back to top
    t.end_fill()
    t.penup()


def draw_small_square(x, y, size, colour):
    """
    Draw a solid square with its bottom-left corner at (x, y).
    size = length of each side
    colour = what colour will be used
    """
    pick_colour(colour)
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.left(90)
    t.end_fill()
    t.penup()


def draw_stair_step(x, y, step_size, levels, direction, colour):
    """
    Draw a staircase block used in the border corners.
    x, y        = starting bottom-left position of the tallest column
    step_size   = width and height of each single square step
    levels      = how many steps tall the staircase is
    direction   = 1 means columns go RIGHT, -1 means columns go LEFT
    """
    for i in range(levels):
        col_x = x + direction * i * step_size
        col_height = levels - i               # tallest column first, shortest last
        for j in range(col_height):
            draw_small_square(col_x, y + j * step_size, step_size, colour)


### SECTION DRAWING FUNCTIONS ###
def draw_centre_diamonds(cx, cy, colour1, colour2, colour3, colour4, colour5):
    """
    Draw the layered nested diamonds in the centre of the motif.
    The largest diamond is drawn first (background colour),
    then each inner diamond is drawn on top.
    cx, cy = centre point of the whole diamond stack
    Colours from outer to inner
    """
    # --- Outermost ring ---
    draw_diamond(cx, cy, half_width=160, half_height=90, colour=colour1)

    # --- Second ring ---
    draw_diamond(cx, cy, half_width=128, half_height=72, colour=colour2)

    # --- Third ring ---
    draw_diamond(cx, cy, half_width=96, half_height=54, colour=colour3)

    # --- Fourth ring ---
    draw_diamond(cx, cy, half_width=64, half_height=36, colour=colour4)

    # --- Innermost ---
    draw_diamond(cx, cy, half_width=32, half_height=18, colour=colour5)


def draw_top_border(start_x, y, num_blocks, block_size, colour1, colour2):
    """
    Draw the repeating rectangular border blocks along the top edge.
    The pattern from the image is: 2 coloured blocks, then a gap (background colour), repeating.
    start_x    = x position of the first block's left edge
    y          = y position of the bottom of the border row
    num_blocks = how many blocks to draw
    block_size = width and height of each small square
    """
    x = start_x
    for i in range(num_blocks):
        # Pattern: colour, colour, background repeating in groups of 3
        if i % 3 == 2:
            draw_small_square(x, y, block_size, colour1)
        else:
            draw_small_square(x, y, block_size, colour2)
        x += block_size   # move right to the next block position


def draw_bottom_border(start_x, y, num_blocks, block_size, colour1, colour2):
    """
    Draw the repeating rectangular border blocks along the bottom edge.
    Mirror of the top border.
    """
    draw_top_border(start_x, y, num_blocks, block_size, colour1, colour2)


def draw_left_stair_border(cy, block_size, colour):
    """
    Draw the stair-step geometric border on the LEFT side of the motif.
    The staircase is symmetric around cy (vertical centre).
    cy         = y centre of the whole motif
    block_size = size of each small square
    """
    levels = 4
    total_height = levels * block_size

    # Anchor x so the tallest column sits near the left edge
    stair_left_x = -450

    # Upper staircase: tallest column on the left, steps down going right
    # Sits in the upper half, bottom edge at cy
    pick_colour(colour)
    draw_stair_step(
        x=stair_left_x,
        y=cy,
        step_size=block_size,
        levels=levels,
        direction=1,
        colour=colour
    )

    # Lower staircase: mirror of upper, sits below cy
    # Flip vertically: tallest column bottom starts at cy - total_height
    pick_colour(colour)
    draw_stair_step(
        x=stair_left_x,
        y=cy - total_height,
        step_size=block_size,
        levels=levels,
        direction=1,
        colour=colour
    )


def draw_right_stair_border(cy, block_size, colour):
    """
    Draw the stair-step geometric border on the RIGHT side of the motif.
    Exact mirror of the left stair border.
    cy         = y centre of the whole motif
    block_size = size of each small square
    """
    levels = 4
    total_height = levels * block_size

    # Anchor x so the tallest column sits near the right edge
    stair_right_x = 450 - block_size

    # Upper staircase: tallest column on the right, steps down going left
    draw_stair_step(
        x=stair_right_x,
        y=cy,
        step_size=block_size,
        levels=levels,
        direction=-1,
        colour=colour
    )

    # Lower staircase: mirror of upper
    draw_stair_step(
        x=stair_right_x,
        y=cy - total_height,
        step_size=block_size,
        levels=levels,
        direction=-1,
        colour=colour
    )


### MAIN CODE ###
BLOCK = 20   # Size of each small square in the border
CY    = 0    # Vertical centre of the canvas
CX    = 0    # Horizontal centre of the canvas

# -- STEP 1: Draw the background strip --
background_colour = "#F9EE55"
draw_small_square(-450, -100, 900, background_colour)   # wide flat rectangle for the background band

# -- STEP 2: Draw the top border row of small squares --
top_border_colour = "#750A9D"
draw_top_border(start_x=-450, y=80, num_blocks=45, block_size=BLOCK, colour1=background_colour, colour2=top_border_colour)

# -- STEP 3: Draw the bottom border row of small squares --
bottom_border_colour = "#750A9D"
draw_bottom_border(start_x=-450, y=-100, num_blocks=45, block_size=BLOCK, colour1=background_colour, colour2=bottom_border_colour)

# -- STEP 4: Draw the stair-step border on the LEFT side --
left_stair_colour = "#750A9D"
draw_left_stair_border(cy=CY, block_size=BLOCK, colour=left_stair_colour)

# -- STEP 5: Draw the stair-step border on the RIGHT side --
right_stair_colour = "#750A9D"
draw_right_stair_border(cy=CY, block_size=BLOCK, colour=right_stair_colour)

# -- STEP 6: Draw the big nested diamond shape in the centre --
diamond1 = "#0BB73E"
diamond2 = "#17EBE4"
diamond3 = "#0A5EAD"
diamond4 = "#D399F5"
diamond5 = "#E911CF"
draw_centre_diamonds(cx=CX, cy=CY, colour1=diamond1, colour2=diamond2, colour3=diamond3, colour4=diamond4, colour5=diamond5)

### FINISH ###
turtle.done()   # keep the window open