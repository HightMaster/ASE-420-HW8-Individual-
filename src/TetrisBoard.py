from src.PygameDelegate import PygameDelegate
pygame = PygameDelegate()

from src.RandomDelegate import RandomDelegate
random = RandomDelegate()

NUM_OF_SHAPE_GRID_ROWS = 4
NUM_OF_SHAPE_GRID_COLUMNS = 4
ACCOUNT_FOR_NEXT_ROW = 4

COLORS = (
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# codesmell - params should be assinged to a var and var used instead of param
# codesmell - long class
class TetrisBoard:
    def __init__(self):
        self.size_of_grid_block = 20
        self.start_x_position = 100
        self.start_y_position = 60
        self.grid_block_height = 0
        self.grid_block_width = 0        
        self.current_figure_type = 0
        self.current_figure_color = 0
        self.current_rotation = 0
        self.shift_in_x = 0
        self.shift_in_y = 0
        self.window_size = (400, 500)
        self.game_state = "start"  # or "gameover"
        self.game_field = []
        self.Figures = (
            [(1, 5, 9, 13), (4, 5, 6, 7)],
            [(4, 5, 9, 10), (2, 6, 5, 9)],
            [(6, 7, 9, 10), (1, 5, 6, 10)],
            [(1, 2, 5, 9), (0, 4, 5, 6), (1, 5, 9, 8), (4, 5, 6, 10)],
            [(1, 2, 6, 10), (5, 6, 7, 9), (2, 6, 10, 11), (3, 5, 6, 7)],
            [(1, 4, 5, 6), (1, 4, 5, 9), (4, 5, 6, 9), (1, 5, 6, 9)],
            [(1, 2, 5, 6)],
        )

    def create_figure(self, starting_shift_x, starting_shift_y):
        self.set_shift_in_x(starting_shift_x)
        self.set_shift_in_y(starting_shift_y)
        start_of_range = 0
        self.set_current_figure_type(random.randint(start_of_range, len(self.Figures) - 1))
        self.set_current_figure_color(random.randint(start_of_range, len(COLORS) - 1))
        default_rotation = 0
        rotation_identifier = default_rotation
        self.set_current_rotation(rotation_identifier)


    def check_intersection(self):
        is_intersection = False
        game_field = self.get_game_field()
        for current_row in range (NUM_OF_SHAPE_GRID_ROWS) :
            for current_column in range (NUM_OF_SHAPE_GRID_COLUMNS) :
                if current_row * ACCOUNT_FOR_NEXT_ROW  + current_column in self.get_shape():
                    is_emplty = 0
                    if current_row + self.get_shift_in_y() > self.get_grid_block_height() - 1 or \
                    current_column + self.get_shift_in_x() > self.get_grid_block_width() - 1 or \
                    current_column + self.get_shift_in_x() < is_emplty or \
                    game_field[current_row + self.get_shift_in_y()][ current_column  + self.get_shift_in_x()] > is_emplty:
                        is_intersection = True
        return is_intersection
   
    """The freeze_figure method has a bug where it looks like it is not freezing a figure to the board.
        This bug does not appear to be consistent, with most figures being frozen as they should.
        This bug involves the create_figure method. This bug happens when you change create_figure from
        a global method to either an internal method or a called method. I have not been able to figure out why,
        but all other functions work. I think it may have to do with the refreshing of the game."""
    # maybe make a board_managment class with freeze, clear, check if filled, delete and all moves (maybe draw_figure)
    def freeze_figure(self):
        game_field = self.get_game_field()
        self.starting_shift_x = 3
        self.starting_shift_y = 0
        for current_row in range (NUM_OF_SHAPE_GRID_ROWS) :
            for current_column in range (NUM_OF_SHAPE_GRID_COLUMNS) :
                if current_row * ACCOUNT_FOR_NEXT_ROW  + current_column in self.get_shape():
                    game_field[ current_row + self.get_shift_in_y()][ current_column  + self.get_shift_in_x()] = self.get_current_figure_color()
        self.clear_lines()
        self.create_figure(self.starting_shift_x, self.starting_shift_y) 
        if self.check_intersection():
            self.set_game_state("gameover")

    def clear_lines(self):
        start_of_range = 1
        for current_row in range(start_of_range, self.get_grid_block_height()):
            if self.check_if_row_is_filled(current_row):
                self.delete_row(current_row)

    def check_if_row_is_filled(self, current_row):
        is_emplty = 0
        game_field = self.get_game_field()
        for current_column in range(self.get_grid_block_width()):
            if game_field[ current_row ][ current_column ] == 0:
                is_emplty += 1
        return is_emplty == 0
            
    def delete_row(self, current_row):
        end_of_range = 1
        size_of_step_through_range = -1
        game_field = self.get_game_field()
        for current_row_above in range(current_row, end_of_range, size_of_step_through_range):
            for current_column in range(self.get_grid_block_width()):
                game_field[current_row_above][ current_column ] = game_field[current_row_above - 1][ current_column ]
    # maybe make moves sub classes of a moves class and use poly
    def move_to_bottom(self):
        
        while not self.check_intersection():
            self.set_shift_in_y(self.get_shift_in_y() + 1)
        self.set_shift_in_y(self.get_shift_in_y() - 1)
        self.freeze_figure()

    def move_down(self):
        
        self.set_shift_in_y(self.get_shift_in_y() + 1)
        if self.check_intersection():
            self.set_shift_in_y(self.get_shift_in_y() - 1)
            self.freeze_figure()

    def move_sideways(self, player_change_in_x):
        old_x = self.get_shift_in_x()
        self.set_shift_in_x(self.get_shift_in_x() + player_change_in_x)
        if self.check_intersection():
            self.set_shift_in_x(old_x)

    def rotate_figure(self):      
        old_rotation = self.get_current_rotation()
        self.set_current_rotation((self.get_current_rotation() + 1) % len(self.Figures[self.get_current_figure_type()])) #codesmell
        if self.check_intersection():
            self.set_current_rotation(old_rotation)

    def draw_figure(self, screen):
        for current_row in range (NUM_OF_SHAPE_GRID_ROWS) :
            for current_column in range (NUM_OF_SHAPE_GRID_COLUMNS) :
                p = current_row * ACCOUNT_FOR_NEXT_ROW  +  current_column 
                if p in self.get_shape():
                    pygame.draw.rect(screen, COLORS[self.get_current_figure_color()],
                                    [self.get_start_x_position()  + self.get_size_of_grid_block() * ( current_column  + self.shift_in_x) + 1,
                                    self.get_start_y_position() + self.get_size_of_grid_block() * ( current_row + self.shift_in_y) + 1,
                                    self.get_size_of_grid_block() - 2, self.get_size_of_grid_block() - 2])

    # make a class that connects pygame to this one and remove pygame form class
    def draw_game_board(self, screen):
        screen.fill(WHITE)
        game_field = self.get_game_field()

        for current_row in range(self.get_grid_block_height()):
            for current_column in range(self.get_grid_block_width()):
                pygame.draw.rect(screen, GRAY, [self.get_start_x_position() + self.get_size_of_grid_block() *  current_column , self.get_start_y_position() + self.get_size_of_grid_block() * current_row, self.get_size_of_grid_block(), self.get_size_of_grid_block()], 1)
                if game_field[ current_row ][ current_column ] > 0:
                    pygame.draw.rect(screen, COLORS[game_field[ current_row ][ current_column ]],
                                    [self.get_start_x_position() + self.get_size_of_grid_block() * current_column + 1, self.get_start_y_position() + self.get_size_of_grid_block() * current_row + 1, self.get_size_of_grid_block() - 2, self.get_size_of_grid_block() - 1])

    def initialize_board(self, height, width):

        self.set_grid_block_height(height)
        self.set_grid_block_width(width)
        self.set_game_field([])
        self.set_game_state("start")
        is_empty = 0
        for current_row in range(self.get_grid_block_height()):
            new_line = [ is_empty ] * self.get_grid_block_width() # polymorphism using * 
            self.append_to_game_field(new_line)


    # Getter and setter for size_of_grid_block
    def get_size_of_grid_block(self):
        return self.size_of_grid_block

    def set_size_of_grid_block(self, value):
        self.size_of_grid_block = value

    # Getter and setter for start_x_position
    def get_start_x_position(self):
        return self.start_x_position

    def set_start_x_position(self, value):
        self.start_x_position = value

    # Getter and setter for start_y_position
    def get_start_y_position(self):
        return self.start_y_position

    def set_start_y_position(self, value):
        self.start_y_position = value

    # Getter and setter for grid_block_height
    def get_grid_block_height(self):
        return self.grid_block_height

    def set_grid_block_height(self, value):
        self.grid_block_height = value

    # Getter and setter for grid_block_width
    def get_grid_block_width(self):
        return self.grid_block_width

    def set_grid_block_width(self, value):
        self.grid_block_width = value
    
        # Getter and setter methods for current_figure_type
    def get_current_figure_type(self):
        return self.current_figure_type

    def set_current_figure_type(self, value):
        self.current_figure_type = value

    # Getter and setter methods for current_figure_color
    def get_current_figure_color(self):
        return self.current_figure_color

    def set_current_figure_color(self, value):
        self.current_figure_color = value

    # Getter and setter methods for current_rotation
    def get_current_rotation(self):
        return self.current_rotation

    def set_current_rotation(self, value):
        self.current_rotation = value

    # Getter and setter methods for shift_in_x
    def get_shift_in_x(self):
        return self.shift_in_x

    def set_shift_in_x(self, value):
        self.shift_in_x = value

    # Getter and setter methods for shift_in_y
    def get_shift_in_y(self):
        return self.shift_in_y

    def set_shift_in_y(self, value):
        self.shift_in_y = value

    def get_shape(self):
        return self.Figures[self.current_figure_type][self.current_rotation]
    
        # Getter and setter for window_size
    def get_window_size(self):
        return self.window_size

    def set_window_size(self, value):
        self.window_size = value

    # Getter and setter for game_state
    def get_game_state(self):
        return self.game_state

    def set_game_state(self, value):
        if value == "start" or value == "gameover":
            self.game_state = value
        else:
            self.game_state = "gameover"

    # Getter and setter for game_field
    def get_game_field(self):
        return self.game_field

    def set_game_field(self, value):
        self.game_field = value

    # Method to append to game_field
    def append_to_game_field(self, value):
        self.game_field.append(value)
