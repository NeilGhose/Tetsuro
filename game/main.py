import asyncio
from game import *

win_size = (800, 600)
win = None
paused = False
game = None
is_over = False
difficulty = 0
button_format = [2, 2, 1]
buttons = None

menu = None

running = True
prev_k = None

game_over = None
quit = False

def exit(button):
    quit = True
    pg.quit()
    quit()

def reset(button):
        global paused, is_over
        game.reset()
        paused = False
        is_over = False

def increase_delay(button):
    game.delay += 100
    game.reset() 

def toggle_tutorial(button):
    game.tutorial = not game.tutorial
    name = "Tutorial On" if game.tutorial else "Tutorial Off"
    if not game.tutorial and len(game.transition_obstacles) > 0:
        game.tutorial_obstacles = []
    button.change_name(name)

def change_difficulty(button):
    global difficulty
    difficulty = (difficulty + 1)%3
    game.stage.base_p = [.8, .5, .3][difficulty]
    name = "Difficulty: " + ["Easy", "Medium", "Hard"][difficulty]
    if not game.start or time.time() - game.start_time < 20:
        game.stage.p = game.stage.base_p
    button.change_name(name)

def resume(button):
    global paused
    paused = False

async def main():
    pg.init()
    global win_size, win, paused, game, is_over, difficulty, button_format, buttons, menu, running, prev_k, game_over
    win = pg.display.set_mode(win_size, RESIZABLE)
    game = Game(win, win_size)
    buttons = {
        "Reset": reset,
        "Tutorial On": toggle_tutorial,
        "Difficulty: Easy": change_difficulty,
        "Quit Game": exit,
        "Resume": resume,
        }
    menu = Menu(win, button_format, buttons, y_buffer=0.05, x_buffer=0.05, win_size=win_size)
    prev_k = pg.key.get_pressed()
    game_over = GameOverScreen(win, win_size)
    pg.display.set_caption("Tetsuro")

    while running:
        if quit:
            return
        # pg.time.delay(10)

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                return
            if event.type == pg.VIDEORESIZE:
                menu.resize(event.size)
                game.resize(event.size)
                game_over.resize(event.size)

        k = pg.key.get_pressed()
                
        if check_key(k, prev_k, pg.K_ESCAPE):
            paused = not paused
            if paused:
                menu.draw()
                game.pause()

        if check_key(k, prev_k, pg.K_r):
            reset(None)

        if paused:
            menu.run(events)
        else:
            win.fill((0,0,0))
            is_over = game.run(events, k, prev_k) or is_over
            if is_over:
                game.start = False
                game.music.pause()
                game_over.draw(game.score)

        pg.display.update()
        prev_k = k

        await asyncio.sleep(0)

    pg.quit()
    quit()

asyncio.run(main())