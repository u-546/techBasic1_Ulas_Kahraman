# main.py
# This is the game engine. It draws everything and reads all the story
# content from dialogue.json, so we never have to touch this file again
# just to add more story.

import pygame
import json
import sys

pygame.init()
pygame.mixer.init()

# ---------------- SETTINGS ----------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arsenia - v0.1")
clock = pygame.time.Clock()

# colours
BOX_FILL = (255, 235, 245)
BOX_BORDER = (255, 190, 215)
TEXT_COLOR = (90, 50, 70)
THOUGHT_COLOR = (140, 120, 165)
NARRATION_COLOR = (120, 105, 125)
BUTTON_FILL = (255, 255, 255)
BUTTON_HOVER = (255, 226, 238)
BUTTON_BORDER = (255, 190, 215)
NAME_ARSENIA = (235, 110, 160)
NAME_YOU = (110, 160, 215)

# dialogue box position
BOX_X = 655
BOX_Y = 100
BOX_W = 515
BOX_H = 495

# images
background_image = pygame.image.load("images/bg_room.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def load_sprite(path):
    image = pygame.image.load(path).convert_alpha()
    target_height = 900
    scale_factor = target_height / image.get_height()
    new_width = int(image.get_width() * scale_factor)
    return pygame.transform.smoothscale(image, (new_width, target_height))


character_sprites = {
    "default": load_sprite("images/default.png"),
    "happy": load_sprite("images/happy.png"),
    "crying": load_sprite("images/crying.png"),
    "angry": load_sprite("images/angry.png"),
    "superangry": load_sprite("images/superangry.png"),
    "sad": load_sprite("images/sad.png"),
    "sparkle": load_sprite("images/sparkle.png"),
    "surprised": load_sprite("images/surprised.png"),
    "embarrassed": load_sprite("images/embarrassed.png"),
    "pokerface": load_sprite("images/pokerface.png"),

}

# story
with open("dialogue.json", "r", encoding="utf-8") as file:
    dialogue_data = json.load(file)

# fonts for everyone
# each speaker gets their own font so the box feels less flat
arsenia_font = pygame.font.SysFont("comicsansms", 21)
you_font = pygame.font.SysFont("couriernew", 22)
narration_font = pygame.font.SysFont("georgia", 20, italic=True)

name_font = pygame.font.SysFont("segoeprint", 20, bold=True)
choice_font = pygame.font.SysFont("segoeprint", 15)
small_font = pygame.font.SysFont("segoeprint", 15)

# game variables
current_scene = None
current_sprite_name = "default"
affection = 50
shown_affection = 50.0     # for the smooth sliding meter bar
game_state = "DIALOGUE"    # "DIALOGUE", "CHOICE", or "ENDING"
choice_buttons = []

text_progress = 0.0        # how many characters of the text are revealed
TEXT_SPEED = 45.0          # characters per second

# keeps every past scene + affection value, so back can rewind all the way
scene_history = []


def wrap_text(text, use_font, max_width):
    """Splits text into a list of lines that fit inside max_width."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = (current_line + " " + word).strip()
        if use_font.size(test_line)[0] > max_width and current_line != "":
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)
    return lines


def load_scene(scene_name):
    """Moves to a new scene, sets the sprite, and works out the game state.
    This does NOT touch scene_history - that's handled separately, only
    at the moment a choice is actually made (see apply_choice)."""
    global current_scene, current_sprite_name, game_state, text_progress

    scene = dialogue_data[scene_name]

    # some scenes just decide which ending you get, then jump straight on
    if "ending_check" in scene:
        for rule in scene["ending_check"]:
            if affection >= rule["min"]:
                load_scene(rule["next"])
                return

    current_scene = scene_name
    current_sprite_name = scene["sprite"]
    text_progress = 0.0

    if scene.get("choices"):
        game_state = "DIALOGUE"      # click once to bring the choices up
    elif "next" in scene:
        game_state = "DIALOGUE"
    else:
        game_state = "ENDING"


def apply_choice(choice):
    """Saves the current scene + affection to history, THEN applies the
    choice's affection change and moves to the next scene."""
    global affection

    scene_history.append({"scene": current_scene, "affection": affection})

    points = choice.get("affection", 0)
    old_value = affection
    affection = max(0, min(100, affection + points))
    print(f"[AFFECTION] {choice['text'][:40]!r} {points:+d}  ({old_value} -> {affection})")

    load_scene(choice["next"])


def go_back():
    """Pops the last saved scene + affection off history and restores both."""
    global current_scene, current_sprite_name, game_state, text_progress, affection

    if len(scene_history) == 0:
        return

    previous = scene_history.pop()
    current_scene = previous["scene"]
    affection = previous["affection"]

    scene = dialogue_data[current_scene]
    current_sprite_name = scene["sprite"]
    text_progress = 0.0

    if scene.get("choices") or "next" in scene:
        game_state = "DIALOGUE"
    else:
        game_state = "ENDING"


def restart_game():
    global affection, shown_affection
    affection = 50
    shown_affection = 50.0
    scene_history.clear()
    print("[GAME] restarted")
    load_scene("start")


load_scene("start")

# load music
try:
    pygame.mixer.music.load("music/music1.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)          # -1 means loop forever
except pygame.error:
    print("[MUSIC] music/music1.wav not found - running without music")


# this is just for the back button itself, the logic above handles the data
back_button_rect = pygame.Rect(30, SCREEN_HEIGHT - 80, 130, 50)


def draw_back_button(surface):
    button_surface = pygame.Surface((back_button_rect.width, back_button_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, (255, 255, 255, 90), button_surface.get_rect(), border_radius=15)
    surface.blit(button_surface, (back_button_rect.x, back_button_rect.y))
    text_surface = small_font.render("< Back", True, (255, 255, 255))
    surface.blit(text_surface, (back_button_rect.x + 20, back_button_rect.y + 13))


# main loop
running = True
while running:

    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    scene = dialogue_data[current_scene]

    # work out who is talking, so we know which font and colour to use
    speaker = scene.get("speaker", "")
    if speaker == "Arsenia":
        active_font = arsenia_font
        body_color = TEXT_COLOR
    elif speaker == "You":
        active_font = you_font
        body_color = TEXT_COLOR
    elif speaker == "thought":
        active_font = narration_font
        body_color = THOUGHT_COLOR
    else:
        active_font = narration_font
        body_color = NARRATION_COLOR

    # work out the text and how much of it should be visible
    text_lines = wrap_text(scene["text"], active_font, BOX_W - 50)
    total_chars = sum(len(line) for line in text_lines)
    text_progress += TEXT_SPEED * dt
    text_finished = text_progress >= total_chars

    # game event states
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_state == "ENDING":
                restart_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if back_button_rect.collidepoint(mouse_pos):
                go_back()

            elif not text_finished:
                # first click just finishes printing the line
                text_progress = total_chars

            elif game_state == "DIALOGUE":
                if scene.get("choices"):
                    game_state = "CHOICE"
                elif "next" in scene:
                    load_scene(scene["next"])

            elif game_state == "CHOICE":
                for button in choice_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        apply_choice(button["choice"])
                        break

    # draw
    screen.blit(background_image, (0, 0))
    screen.blit(character_sprites[current_sprite_name], (10, 0))

    # dialogue box
    pygame.draw.rect(screen, BOX_BORDER,
                     (BOX_X - 6, BOX_Y - 6, BOX_W + 12, BOX_H + 12), border_radius=30)
    pygame.draw.rect(screen, BOX_FILL,
                     (BOX_X, BOX_Y, BOX_W, BOX_H), border_radius=25)

    text_y = BOX_Y + 30

    # name tag (only for people who actually speak out loud)
    if speaker == "Arsenia" or speaker == "You":
        name_color = NAME_ARSENIA if speaker == "Arsenia" else NAME_YOU
        name_surface = name_font.render(speaker, True, name_color)
        screen.blit(name_surface, (BOX_X + 25, BOX_Y + 22))
        pygame.draw.line(screen, BOX_BORDER,
                         (BOX_X + 25, BOX_Y + 52),
                         (BOX_X + BOX_W - 25, BOX_Y + 52), 2)
        text_y = BOX_Y + 66

    # the dialogue text, revealed a character at a time
    chars_left = int(text_progress)
    line_y = text_y
    for line in text_lines:
        if chars_left <= 0:
            break
        visible = line[:chars_left]
        chars_left -= len(line)
        screen.blit(active_font.render(visible, True, body_color), (BOX_X + 25, line_y))
        line_y += 32

    # choices
    if game_state == "CHOICE":
        choice_buttons = []
        choices = scene["choices"]
        button_h = 62
        gap = 10
        block_h = len(choices) * button_h + (len(choices) - 1) * gap
        button_y = BOX_Y + BOX_H - 28 - block_h

        for choice in choices:
            rect = pygame.Rect(BOX_X + 25, button_y, BOX_W - 50, button_h)
            hovered = rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, BUTTON_HOVER if hovered else BUTTON_FILL,
                             rect, border_radius=15)
            pygame.draw.rect(screen, BUTTON_BORDER, rect,
                             width=4 if hovered else 3, border_radius=15)

            lines = wrap_text(choice["text"], choice_font, rect.width - 30)
            start_y = rect.centery - (len(lines) * 20) // 2
            for i, line in enumerate(lines):
                surf = choice_font.render(line, True, TEXT_COLOR)
                screen.blit(surf, (rect.x + 15, start_y + i * 20))

            choice_buttons.append({"rect": rect, "choice": choice})
            button_y += button_h + gap

    # click prmopt
    elif game_state == "DIALOGUE" and text_finished:
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            hint = small_font.render("click to continue", True, (180, 150, 170))
            screen.blit(hint, (BOX_X + BOX_W - hint.get_width() - 25,
                               BOX_Y + BOX_H - 38))

    # to the ending
    elif game_state == "ENDING":
        msg = f"Final affection: {affection} / 100"
        surf = small_font.render(msg, True, (150, 110, 135))
        screen.blit(surf, (BOX_X + 25, BOX_Y + BOX_H - 62))
        surf2 = small_font.render("press R to play again  -  Esc to quit", True, (180, 150, 170))
        screen.blit(surf2, (BOX_X + 25, BOX_Y + BOX_H - 38))

    # this line is also just for the back button
    draw_back_button(screen)

    # the meter
    # slide the bar smoothly towards the real value
    shown_affection += (affection - shown_affection) * min(1.0, 6 * dt)

    meter_x, meter_y = 30, 30
    meter_w, meter_h = 220, 26

    pygame.draw.rect(screen, (255, 255, 255), (meter_x, meter_y, meter_w, meter_h), border_radius=13)
    filled = int((shown_affection / 100) * meter_w)
    if filled > 6:
        pygame.draw.rect(screen, (255, 110, 150), (meter_x, meter_y, filled, meter_h), border_radius=13)
    pygame.draw.rect(screen, (255, 180, 210), (meter_x, meter_y, meter_w, meter_h), width=3, border_radius=13)

    heart = small_font.render("<3", True, (255, 90, 130))
    screen.blit(heart, (meter_x + meter_w + 10, meter_y + 4))

    pygame.display.flip()

pygame.quit()
sys.exit()
