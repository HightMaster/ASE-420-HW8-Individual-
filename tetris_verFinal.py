import pygame
from src.TetrisBoard import TetrisBoard


def main():   

    board = TetrisBoard()
 
    # Pygame related init
    pygame.init()
    screen = pygame.display.set_mode(board.get_window_size())
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # we need pressing_down, fps, and counter to move_down() the Tetris Figure
    fps = 200
    counter = 0
    pressing_down = False

    game_block_height = 20
    game_block_width = 10

    board.initialize_board(game_block_height, game_block_width) # code smell - what is 20 and 10? Can we use keyword argument? 
    
    starting_shift_x = 3 
    starting_shift_y = 0

    board.create_figure(starting_shift_x, starting_shift_y)
    done = False
    level = 1
    interval = 100000
    interval_of_auto_move = 2

    event_key_action_list = {
        pygame.K_UP: lambda: board.rotate_figure(),
        pygame.K_DOWN: "true",
        pygame.K_LEFT: lambda: board.move_sideways(-1),
        pygame.K_RIGHT: lambda: board.move_sideways(1),
        pygame.K_SPACE: lambda: board.move_to_bottom()
    }


    while not done:
        counter += 1
        if counter > interval:
            counter = 0
            
        # Check if we need to automatically go down
        if counter % (fps // interval_of_auto_move // level) == 0 or pressing_down: 
            if board.get_game_state() == "start":
                board.move_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in event_key_action_list:
                    if event_key_action_list[event.key] == "true":
                        pressing_down = True
                    method_to_run = event_key_action_list[event.key]
                    if callable(method_to_run):
                        method_to_run()


            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
                
        board.draw_game_board(screen = screen)
        
        # code smell - how many values duplication Figures[current_figure_type][current_rotation]
        board.draw_figure(screen = screen)

        if board.get_game_state() == "gameover":
            done = True

        # refresh the screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()