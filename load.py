import edmc_data
import tkinter as tk
from tkinter import ttk
import logging
import os
import ctypes

from config import config, appname
from builtins import object, str

focus_state_old = 0
focus_state_now = 0

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')

def plugin_start3(plugin_dir: str) -> str:
   logger.debug(f'I am loaded! My plugin name is {plugin_name}')
   return "EDMC UI Hide"

def dashboard_entry(cmdr: str, is_beta: bool, entry: dict[str, any]):
    global focus_state_old
    global focus_state_now
    focus_state_now = entry['GuiFocus']
    logger.debug(f'Current focus state is {focus_state_now}')
    if focus_state_now != focus_state_old:
        focus_state_old = focus_state_now
        logger.debug(f'Variable focus_state_old has been changed to {focus_state_old}')
        hideorshow()    
    else:
        logger.debug(f'Variable focus_state_old is unchanged at {focus_state_old} because focus_state_now is still {focus_state_now} - Doing nothing!') 
        pass

# Hide EDMC when GuiFocus is InternalPanel, SystemMap, Orrery, FSS, SAA or Codex
class hideorshow():
    def __init__(master: tk.Tk):
        edmc_handle = ctypes.windll.user32.FindWindowW(None, "E:D Market Connector")
        ed_handle = ctypes.windll.user32.FindWindowW(None, "Elite - Dangerous (CLIENT)")
        if (focus_state_old == 1) or (focus_state_old == 7) or (focus_state_old == 8) or (focus_state_old == 9) or (focus_state_old == 10) or (focus_state_old == 11):
            logger.debug(f'Now hiding EDMC')
            ctypes.windll.user32.ShowWindow(edmc_handle, 11)
        else:
            logger.debug(f'Now unhiding EDMC')
            ctypes.windll.user32.ShowWindow(edmc_handle, 4)
