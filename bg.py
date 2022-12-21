import threading, random, os, subprocess, datetime, signal


def unbiased_choice(collection: list) -> str:
    """
    Less biased random generator, for your viewing pleasures. ;)
    """
    if len(collection) < 2: return collection[0]
    cx = None
    cy = None

    while (cx == cy):
        cx = random.choice(collection)
        cy = random.choice(collection)

    return cx

def set_bg(wallpaper: str) -> subprocess.Popen:
    return subprocess.Popen(['swaybg', '-i', wallpaper, '--mode', 'fill'])


def get_time_string() -> str:
    hour: int = datetime.datetime.today().hour

    if hour >= 0 and hour <= 12: return 'morning'
    elif hour > 12 and hour <= 16: return 'afternoon'
    elif hour > 16 and hour <= 18: return 'evening'
    elif hour > 18 and hour <= 24: return 'night'


def logic_threaded(process):
    last_time: str = get_time_string()
    home: str = os.path.expanduser('~')

    while True:
        if get_time_string() != last_time:
            print(f'[BG-THREAD]: Time changed: {last_time} -> {get_time_string()}')
            last_time = get_time_string()
            os.kill(process.pid, signal.SIGTERM)

            new_wallpaper: str = unbiased_choice(os.listdir(f'{home}/Wallpapers/{last_time}'))
            process = set_bg(f'{home}/Wallpapers/{last_time}/{new_wallpaper}')


if __name__ == '__main__':
    print('[BG]: Killing already existing SwayBG instances.')
    subprocess.call(['killall', 'swaybg'])

    home: str = os.path.expanduser('~')
    time_of_day: str = get_time_string()
    wallpaper: str = unbiased_choice(os.listdir(f'{home}/Wallpapers/{time_of_day}'))

    print(f'[BG]: Time of day: {time_of_day}')
    print('[BG]: ', wallpaper, 'chosen!')
    process = set_bg(f'{home}/Wallpapers/{time_of_day}/{wallpaper}')

    threading.Thread(target = logic_threaded, args = (process,)).start()
