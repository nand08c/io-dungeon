import sys
import pygame

from graphics.layout import Layout
from graphics.log_view import LogView


def main():
    pygame.init()
    screen_w, screen_h = 800, 600
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("io-dungeon - Layout demo")
    clock = pygame.time.Clock()

    tile_px = (48, 48)
    cols, rows = 20 * 2, 15 * 2
    layout = Layout(cols, rows, tile_px)
    layout.fill_with_color(color=(100, 140, 100), border_color=(40, 80, 40), border_width=2)

    # LogView demo
    log = LogView(font_size=16, bg_color=(10, 10, 10, 200), text_color=(230,230,230))
    log.set_bottom_right((screen_w, screen_h), margin=(10, 10), width_ratio=0.45, height_ratio=0.45)
    # Load initial messages from sample file (if present)
    log.load_from_file("data/log_samples.txt")

    # Create a timed event to generate messages periodically
    LOG_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(LOG_EVENT, 2000)  # cada 2000 ms
    gen_count = 0

    cam_x = 0
    cam_y = 0
    speed = 300  # px/s

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                log.toggle()
            elif event.type == LOG_EVENT:
                gen_count += 1
                log.add_message(f"Auto message #{gen_count}: evento de demostración.")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cam_x -= int(speed * dt)
        if keys[pygame.K_RIGHT]:
            cam_x += int(speed * dt)
        if keys[pygame.K_UP]:
            cam_y -= int(speed * dt)
        if keys[pygame.K_DOWN]:
            cam_y += int(speed * dt)
        if keys[pygame.K_PLUS]:
            speed += 100 * dt
        if keys[pygame.K_MINUS]:
            speed -= 100 * dt
            speed = max(100, speed)
        if keys[pygame.K_c]:
            log.hide()
        if keys[pygame.K_v]:
            log.show()

        # Clamp camera to layout bounds
        max_x = max(0, cols * tile_px[0] - screen_w)
        max_y = max(0, rows * tile_px[1] - screen_h)
        cam_x = max(0, min(cam_x, max_x))
        cam_y = max(0, min(cam_y, max_y))

        screen.fill((0, 0, 0))
        layout.render(screen, (cam_x, cam_y))
        # Render log view on top
        log.render(screen)

        fps = int(clock.get_fps())
        pygame.display.set_caption(f"io-dungeon - Layout demo - FPS: {fps}")
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error al ejecutar el demo:", e, file=sys.stderr)
        raise