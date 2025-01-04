from pygame import *
from buttons import ImageButton, Button
from mapa import window, WIDTH, BLOCK_SIZE, HEIGHT, draw_grid
import json
import os
init()

clock = time.Clock()

buttons = []
scroll_y = 0
scroll_speed = 20

block_state = []


def show_images():
    global scroll_y, buttons
    list_widget = Surface((200, 400))
    list_widget.fill((196, 196, 196))
    list_widget.set_alpha(120)
    window.blit(list_widget, (WIDTH - 220, 200))

    image_folder = 'images'
    y = 210 + scroll_y
    buttons.clear()
    try:
        for file_name in os.listdir(image_folder):
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(image_folder, file_name)
                img = image.load(img_path)
                scaled_img = transform.scale(img, (180, 180))
                button = ImageButton(WIDTH - 210, y, img, img_path)
                buttons.append(button)
                button.draw()
                y += img.get_height() + 10
    except:
        print('немає зображень чи папки "images"')


class Block:
    def __init__(self, img, x, y, width, height):
        self.img = transform.scale(image.load(img), (width, height))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


def snap_to_grid(x, y):
    return (x // BLOCK_SIZE) * BLOCK_SIZE, (y // BLOCK_SIZE) * BLOCK_SIZE

SPEED = 7
def update():
    keys = key.get_pressed()
    if keys[K_d]:
        for block in blocks:
            block.rect.x -= BLOCK_SIZE
    if keys[K_a]:
        for block in blocks:
            block.rect.x += BLOCK_SIZE
    if keys[K_w]:
        for block in blocks:
            block.rect.y += BLOCK_SIZE
    if keys[K_s]:
        for block in blocks:
            block.rect.y -= BLOCK_SIZE


is_show_grid = False
is_shap_grid = True
is_draw_mode = False
# кнопки налаштувань
btn_show_grid = Button(WIDTH - 200, 20, 150, 40, 'show grid', color_rect=(255, 0 , 0))
btn_snap_grid = Button(WIDTH - 200, btn_show_grid.rect.y + 50, 150, 40, 'snap grid', color_rect=(0, 175, 0))
btn_draw_mode = Button(WIDTH - 200, btn_snap_grid.rect.y + 50, 150, 40, 'Draw mode', color_rect=(255, 0, 0))
# кнопки збереження завантаження
btn_save_world = Button(WIDTH - 200, HEIGHT - 80, 150, 40, 'Save to json')
btn_load_world = Button(WIDTH- 200, btn_save_world.rect.y - 50, 150, 40, 'Load map')


blocks = []
block_type = None
is_drawing = False
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_g:
                if is_show_grid:
                    is_show_grid = False
                else:
                    is_show_grid = True
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                for button in buttons:
                    if button.clicked(e.pos):
                        block_type = button.img_path
                        print(f'Вибрано: {block_type}')
                if not is_drawing:
                    is_drawing = True
                else:
                    is_drawing = False
                if block_type and e.pos[0] <= WIDTH - 250:
                    x, y = e.pos
                    if is_shap_grid:
                        x, y = snap_to_grid(e.pos[0] - BLOCK_SIZE // 2, e.pos[1] - BLOCK_SIZE // 2)
                    blocks.append(Block(block_type, x, y, BLOCK_SIZE, BLOCK_SIZE))
                    block_state.append({"x": x, "y": y, "img": block_type})

                    if e.button == 4:
                        scroll_y += scroll_speed
                    if e.button == 5:
                        scroll_y -= scroll_speed
                    if e.button == 1:
                        for button in buttons:
                            if button.clicked(e.pos):
                                print(f'Вибрано: {button.img_path}')
                                block_type = button.img_path
            if btn_show_grid.clicked(e.pos):
                if is_show_grid:
                    is_show_grid = False
                    btn_show_grid.color_r = (255, 0, 0)
                else:
                    is_show_grid = True
                    btn_show_grid.color_r = (0, 175, 0)
            if btn_snap_grid.clicked(e.pos):
                if is_shap_grid:
                    is_shap_grid = False
                    btn_snap_grid.color_r = (255, 0, 0)
                else:
                    is_shap_grid = True
                    btn_snap_grid.color_r = (0, 175, 0)
            if btn_draw_mode.clicked(e.pos):
                if is_draw_mode:
                    is_draw_mode = False
                    btn_draw_mode.color_r = (255, 0, 0)
                else:
                    is_draw_mode = True
                    btn_draw_mode.color_r = (0, 175, 0)

            if btn_save_world.clicked(e.pos):
                try:
                    with open('world.json', 'w') as world:
                        world.write(json.dumps(block_state))
                except Exception as e:
                    print(f'Помилка збереження {e}')

            if btn_load_world.clicked(e.pos):
                try:
                    with open('world.json', 'r') as world:
                        map_list = json.load(world)
                        for i in range(len(map_list)):
                            x, y, img = map_list[i].values()
                            blocks.append(Block(img, x, y, BLOCK_SIZE, BLOCK_SIZE))
                            block_state.append({"x": x, "y": y, "img": img})
                except Exception as e:
                    print(f'Помилка завантаження {e}')

        if e.type == MOUSEMOTION:
            if is_drawing:
                if is_draw_mode and e.pos[0] <= WIDTH - 250:
                    if block_type and e.pos[0] <= WIDTH - 250:
                        x, y = e.pos
                        if is_shap_grid:
                            x, y = snap_to_grid(e.pos[0] - BLOCK_SIZE // 2, e.pos[1] - BLOCK_SIZE // 2)
                        blocks.append(Block(block_type, x, y, BLOCK_SIZE, BLOCK_SIZE))
                        block_state.append({"x": x, "y": y, "img": block_type})

    window.fill((0, 0, 0))
    for block in blocks:
        block.reset()
    # показ сітки
    if is_show_grid:
        draw_grid()
    draw.line(window, (196, 196, 196), (WIDTH - 250, 0), (WIDTH - 250, HEIGHT), 10)

    btn_show_grid.reset()
    btn_snap_grid.reset()
    btn_draw_mode.reset()
    btn_save_world.reset()
    btn_load_world.reset()
    show_images()

    display.update()
    clock.tick(60)

    update()


