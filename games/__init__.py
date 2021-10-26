from .games import *

supported_games = {
    name.upper(): cls
    for name, cls in games.__dict__.items()
    if isinstance(cls, type) and name != "Game"
}
