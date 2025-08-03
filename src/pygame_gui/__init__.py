import os
__version__ = "0.1.0"
__description__ = "A GUI library for pygame"
os.environ["SDL_IME_SHOW_UI"] = "1"
from .control.control import *
from .control import entry
