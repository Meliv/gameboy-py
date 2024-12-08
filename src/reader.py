from games import Game

def get_bytes(game: Game, start: int, end: int) -> bytes:
    with open(f"etc/roms/{game.value}.gb", "rb") as f:
        f.seek(start)
        return f.read(end - start)


def get_game_name(game: Game) -> str: return bytes([b for b in get_bytes(game, 0x0134, 0x0143) if b != 0x00]).decode('ASCII')    