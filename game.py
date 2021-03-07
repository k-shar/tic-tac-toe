import pygame
import pygame.freetype
from constants import *
from window_resizing import *
from game_logic import *
import time


def game(screen):

    # -- define surfaces --
    # surfaces start with non-zero size
    # they will be scaled up on a VIDEORESIZE event
    # (automatically called on first cycle by pygame)

    # window is the outermost container
    # used to fix an aspect ratio for the whole game
    window = pygame.Surface((1, 1))

    # -- left and right side divide the window in two --
    # left for the player input and computer output
    left_side = pygame.Surface((1, 1))
    main_board = pygame.Surface((200, 200))

    # display whos turn and if won lost or draw
    left_title_obj = TextSurface("Human to move", AQUA, 0.6)
    # display stats below analysis board
    right_title_obj = TextSurface("", PINK, 0.6)

    # buttons for the options menu
    button_group = pygame.sprite.Group()
    reset_button = Button("Reset", (171, 0, 0), 0.6)
    player_move = Button("Human Moves", (171, 0, 0), 0.6)
    ai_move = Button("Ai Moves", (171, 0, 0), 0.6)

    button_group.add(reset_button)
    button_group.add(player_move)
    button_group.add(ai_move)

    # right for computer evaluation and to see what the computer is thinking
    right_side = pygame.Surface((1, 1))
    options_selector = pygame.Surface((1, 1))
    analysis_board = pygame.Surface((1, 1))

    # methods from game_logic.py
    tile_group = generate_board(main_board, "main")
    fill_board(tile_group)

    analysis_tile_group = generate_board(analysis_board, "analysis")
    fill_board(analysis_tile_group)

    # mouse pointer is relative to the window
    # as a offset is applied (writtent in tiles.py)
    # -- in the future dont use sprite groups of length 1
    main_board_mouse_sprite_group = pygame.sprite.Group()
    options_selector_mouse_sprite_group = pygame.sprite.Group()

    main_board_mouse_sprite = MousePointer()
    options_selector_mouse_sprite = MousePointer()

    main_board_mouse_sprite_group.add(main_board_mouse_sprite)
    options_selector_mouse_sprite_group.add(options_selector_mouse_sprite)

    player_to_move = True
    board_won = False

    last_move_board = board.copy()
    tile_eval_for_display = [0] * 9
    FPS = 60

    def game_over_check(board):
        has_board_won = True

        player_won, ai_won, draw = check_if_won(board)
        if player_won:
            left_title_obj.text = "Player won!!"
        elif ai_won:
            left_title_obj.text = "ai won!!"
        elif draw:
            left_title_obj.text = "Draw!!"
        else:
            has_board_won = False
        return has_board_won

    clock = pygame.time.Clock()
    done = False
    showing_combinations = False
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'size': (805, 457), 'w': 805, 'h': 457}))

    while not done:

        # //-- reset the surfaces --//
        screen.fill(WHITE)
        window.fill(DARK_BLUE)
        left_side.fill(BLUE)
        main_board.fill(BLACK)
        right_side.fill(RED)
        options_selector.fill(PINK)
        analysis_board.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # //-- on screen resize --//
            if event.type == pygame.VIDEORESIZE:

                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                # how far away is the top left corner of main board from 0,0?
                main_offset = [0, 0]
                # how far away is the top left corner of options menu from 0,0?
                options_offset = [0, 0]

                # //-- scale surfaces with method from "window_resizing.py" --//
                window, window_pos, main_offset = resize_surfaces(0.95, window, screen, (16, 9), 0.5, 0.5, main_offset)
                options_offset = main_offset.copy()  # both need the offset of the window

                left_side, left_side_rect, main_offset = resize_surfaces(0.9, left_side, window, (8, 9), 0.25, 0.5, main_offset)
                main_board, main_board_rect, main_offset = resize_surfaces(0.8, main_board, left_side, (1, 1), 0.5, 15/24, main_offset)

                right_side, right_side_rect, options_offset = resize_surfaces(0.9, right_side, window, (8, 9), 0.75, 0.5, options_offset)
                options_selector, options_selector_rect, options_offset = resize_surfaces(0.9, options_selector, right_side, (20, 4), 0.5, 4/36, options_offset)
                analysis_board, analysis_board_rect, _ = resize_surfaces(0.65, analysis_board, right_side, (1, 1), 0.5, 1/2, None)

                # //-- update text objects --//
                left_title_obj.resize(0.95, left_side, (16, 4), 0.5, 5/36, None)
                right_title_obj.resize(0.95, left_side, (19, 4), 0.5, 15/17, None)

                player_move.resize(0.5, options_selector, (12, 3), 0.2, 0.5, None)
                reset_button.resize(0.5, options_selector, (4, 2), 0.515, 0.5, None)
                ai_move.resize(0.5, options_selector, (7, 2), 0.8, 0.5, None)

            # //-- mouse press --//
            if event.type == pygame.MOUSEBUTTONUP:
                # see if any buttons are clicked
                buttons_pressed = pygame.sprite.spritecollide(options_selector_mouse_sprite, button_group, False)
                if len(buttons_pressed) == 1:
                    showing_combinations = False

                    if buttons_pressed[0].text == "Reset":
                        for i in range(len(board)):
                            board[i] = "."
                        player_to_move = True
                        board_won = False
                        if player_to_move:
                            left_title_obj.text = "Human to move"
                        else:
                            left_title_obj.text = "AI is thinking"

                    elif buttons_pressed[0].text == "Human Moves":
                        player_to_move = True
                        left_title_obj.text = "Human to move"

                    elif buttons_pressed[0].text == "Ai Moves":
                        player_to_move = False
                        left_title_obj.text = "AI is thinking"

                # if player is trying to make a move AS O (player)
                if player_to_move and not board_won and not showing_combinations and event.button == 1:
                    tiles_collided = []
                    tiles_collided = pygame.sprite.spritecollide(main_board_mouse_sprite, tile_group, False)

                    if len(tiles_collided) > 0:
                        last_move_board = board.copy()
                        board[tiles_collided[0].key] = player
                        left_title_obj.text = "AI is thinking"
                        player_to_move = False
                        board_won = game_over_check(board)

                # if player is trying to make a move AS X (ai)
                elif player_to_move and not board_won and not showing_combinations and event.button == 3:
                    tiles_collided = []
                    tiles_collided = pygame.sprite.spritecollide(main_board_mouse_sprite, tile_group, False)

                    if len(tiles_collided) > 0:
                        last_move_board = board.copy()
                        board[tiles_collided[0].key] = ai
                        left_title_obj.text = "Player to move"
                        player_to_move = True
                        board_won = game_over_check(board)

                # if player is trying to clear a square (middle mouse)
                elif player_to_move and not board_won and not showing_combinations and event.button == 2:
                    tiles_collided = []
                    tiles_collided = pygame.sprite.spritecollide(main_board_mouse_sprite, tile_group, False)

                    if len(tiles_collided) > 0:
                        last_move_board = board.copy()
                        board[tiles_collided[0].key] = "."

        # print(board, main_board)
        flash_tiles(board, tile_group)

        # //-- draw text --//
        left_title_obj.display_text()
        right_title_obj.display_text()

        reset_button.display_text()
        player_move.display_text()
        ai_move.display_text()

        # //-- update sprite groups --//
        tile_group.update(main_board)
        analysis_tile_group.update(analysis_board)

        main_board_mouse_sprite_group.update(main_offset)
        options_selector_mouse_sprite_group.update(options_offset)
        button_group.update(options_selector)

        button_group.draw(options_selector)

        if not player_to_move and not board_won and not showing_combinations:

            number_of_boards_considered = 0
            list_of_boards_considered = []

            # find what move to play as the computer
            computer_move, number_of_boards_considered, list_of_boards_considered, tile_eval_for_display = find_computer_move(board, ai, player, number_of_boards_considered, list_of_boards_considered)

            showing_combinations = True
            n = 1

        if showing_combinations:
            FPS = 60
            try:
                for tile in analysis_tile_group.sprites():
                    tile.color = (random.randint(40, 50), random.randint(150, 160), random.randint(120, 130))

                flash_tiles(list_of_boards_considered[n], analysis_tile_group)

                # scale speed of analysis display dependant on size of things to display
                if len(list_of_boards_considered) // 60 == 0:
                    n += 1
                else:
                    n += len(list_of_boards_considered) // 60
                right_title_obj.text = f"Considered: {n}"

            except:
                # when index out of range, all boards have been shown

                showing_combinations = False

                player_to_move = True
                left_title_obj.text = "Human to move"
                last_move_board = board.copy()
                board[computer_move] = ai
                board_won = game_over_check(board)
        else:

            flash_tiles(last_move_board, analysis_tile_group)
            FPS = 60

            # show the evaluation of the position
            for i in range(9):
                # if there is no move on this tile, show outcome of playing that move
                if last_move_board[i] == ".":
                    # display the computers evaluation for the position
                    if tile_eval_for_display[i] == 0:
                        text = "draw"
                        analysis_tile_group.sprites()[i].color = (47,161,198)
                    else:
                        text = str(tile_eval_for_display[i])
                        if int(tile_eval_for_display[i]) > 0:
                            pass
                            #analysis_tile_group.sprites()[i].color = (int(abs(tile_eval_for_display[i]/20) * 255), 45, 45)
                        else:
                            pass
                         #   analysis_tile_group.sprites()[i].color = (49,abs(int(tile_eval_for_display[i]//20)) * 200, 87)
                
                    analysis_tile_group.sprites()[i].text = text
                    analysis_tile_group.sprites()[i].display_text()





        # //-- draw sprite groups --//
        tile_group.draw(main_board)

        analysis_tile_group.draw(analysis_board)

        main_board_mouse_sprite_group.draw(main_board)
        options_selector_mouse_sprite_group.draw(options_selector)

        # //-- blit surfaces onto eachother --//
        left_side.blit(main_board, (main_board_rect))
        left_side.blit(left_title_obj.image, (left_title_obj.rect))
        right_side.blit(right_title_obj.image, (right_title_obj.rect))
        window.blit(left_side, (left_side_rect))

        right_side.blit(options_selector, options_selector_rect)
        right_side.blit(analysis_board, analysis_board_rect)
        window.blit(right_side, (right_side_rect))

        screen.blit(window, (window_pos))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    # main
    pygame.display.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((480, 270), pygame.RESIZABLE)
    pygame.display.set_caption("Noughts and crosses")

    game(screen)
    pygame.quit()
