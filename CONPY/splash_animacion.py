import pygame
from PIL import Image, ImageSequence
import os

def mostrar_splash_animado(screen, gif_path, width, height):
    frames = []
    gif = Image.open(gif_path)
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        frame = frame.resize((width, height))
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        frames.append(py_image)

    clock = pygame.time.Clock()
    frame_idx = 0
    total_frames = len(frames)
    splash_done = False
    waiting_click = False

    while not splash_done:
        screen.fill((0, 0, 0))
        screen.blit(frames[frame_idx], (0, 0))
        pygame.display.flip()

        frame_idx += 1
        if frame_idx >= total_frames:
            frame_idx = total_frames - 1
            waiting_click = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if waiting_click and event.type == pygame.MOUSEBUTTONDOWN:
                splash_done = True

        # Ajusta el framerate para mejorar fluidez del gif
        clock.tick(30)  # Puedes aumentar a 40 si lo quieres más rápido

