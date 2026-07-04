import scipy.io.wavfile as wav
import sounddevice as sd
from pygame import *

# 1. Фікс конфлікту звукових потоків: налаштовуємо Pygame ПЕРЕД ініціалізацією
mixer.pre_init(44100, -16, 2, 512)
init()
mixer.init()

# Налаштування аудіо та файлів
fs = 44100
recording = None
is_recording = False
voice_file = "voice_record.wav"
minus_track = "MinusDuHast.mp3"

mixer.music.set_volume(0.5)

# Налаштування вікна
w_size = 1200, 600
win = display.set_mode(w_size)
display.set_caption("Запис вокалу під мінус")
clock = time.Clock()

# Шрифти та інтерфейс
font.init()
font_big = font.SysFont("Arial", 32)
btn_rect = Rect(425, 250, 350, 80)
rect_color = "white"
btn_text = "Запис"


def start_voice_record():
    global recording
    # Записуємо із запасом часу (наприклад, 60 секунд)
    recording = sd.rec(int(fs * 60), samplerate=fs, channels=1, dtype="int16")


def stop_voice_record():
    global recording
    sd.stop()
    if recording is not None:
        wav.write(voice_file, fs, recording)


def play_song():
    mixer.music.stop()
    mixer.stop()
    try:
        mixer.music.load(minus_track)
        mixer.music.play()
    except error:
        print(f"Не вдалося завантажити мінус: {minus_track}")

    try:
        voice_sound = mixer.Sound(voice_file)
        voice_sound.play()
    except error:
        print("Не вдалося відтворити записаний голос.")


# Головний цикл
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
            exit()

        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):
                if not is_recording:
                    # === ПОЧАТОК ЗАПИСУ ===
                    rect_color = "red"
                    btn_text = "Стоп та прослухати"
                    is_recording = True

                    # Спочатку запускаємо запис мікрофона
                    start_voice_record()

                    # 2. Фікс: Робимо мікроскопічну паузу (0.1 сек),
                    # щоб Sounddevice захопив мікрофон, і лише ТЕПЕР вмикаємо мінус
                    time.wait(100)

                    try:
                        mixer.music.load(minus_track)
                        mixer.music.play()
                    except error:
                        print("Мінус не знайдено для фону")
                else:
                    # === ЗУПИНКА ТА ВІДТВОРЕННЯ ===
                    rect_color = "white"
                    btn_text = "Запис"
                    is_recording = False

                    mixer.music.stop()
                    stop_voice_record()
                    time.wait(200)  # Пауза для збереження файлу
                    play_song()

    # Малювання інтерфейсу
    win.fill("grey")
    draw.rect(win, rect_color, btn_rect)

    text_surface = font_big.render(btn_text, True, "black")
    text_x = btn_rect.x + (btn_rect.width - text_surface.get_width()) // 2
    text_y = btn_rect.y + (btn_rect.height - text_surface.get_height()) // 2
    win.blit(text_surface, (text_x, text_y))

    display.update()
    clock.tick(30)
