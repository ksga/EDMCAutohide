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
flagsisindanger_old = 0
flagsisindanger_now = 0
#journal_underattack_old = 0
journal_underattack_now = 0

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')

def plugin_start3(plugin_dir: str) -> str:
   logger.debug(f'I am loaded! My plugin name is {plugin_name}')
   return "EDMC UI Hide"

def dashboard_entry(cmdr: str, is_beta: bool, entry: dict[str, any]):
    global focus_state_old
    global focus_state_now
    global flagsisindanger_old
    global flagsisindanger_now
    
    focus_state_now = entry['GuiFocus']
    flagsisindanger_now = entry['Flags'] & edmc_data.FlagsIsInDanger
    logger.debug(f'Current focus state is {focus_state_now}')
    logger.debug(f'Current danger state is {flagsisindanger_now}')
    if focus_state_now != focus_state_old:
        focus_state_old = focus_state_now
        logger.debug(f'Variable focus_state_old has been changed to {focus_state_old}')
        hideorshow()    
    elif flagsisindanger_now != flagsisindanger_old:
        flagsisindanger_old = flagsisindanger_now
        logger.debug(f'Variable flagsisindanger_old has been changed to {flagsisindanger_now}')
        hideorshow()            
    else:
        logger.debug(f'Variables focus_state_old is unchanged at {focus_state_old} and flagsisindanger_old is unchanged at {flagsisindanger_old} - Doing nothing!') 
        pass

def journal_entry(cmdr: str, is_beta: bool, system: str, station: str, entry: dict[str, any], state: dict[str, any]) -> None:
    global journal_underattack_now
    if entry['event'] == 'UnderAttack':
        journal_underattack_now = 1
        logger.debug(f'Variable journal_underattack_now has been changed to {journal_underattack_now}')
        hideorshow()    
    elif entry['event'] == 'StartJump':
        journal_underattack_now = 0
        logger.debug(f'StartJump changed variable journal_underattack_now has been changed to {journal_underattack_now}')
        hideorshow()    
    else:
        logger.debug(f'Journal update, but nothing useful')
        pass

# Hide EDMC when FlagsIsInDanger or GuiFocus is InternalPanel, SystemMap, Orrery, FSS, SAA or Codex - or if Journal says we are under attack
class hideorshow():
    def __init__(self: tk.Tk):
        edmc_handle = ctypes.windll.user32.FindWindowW(None, "E:D Market Connector")
        ed_handle = ctypes.windll.user32.FindWindowW(None, "Elite - Dangerous (CLIENT)")
        if (focus_state_old == 1) or (focus_state_old == 7) or (focus_state_old == 8) or (focus_state_old == 9) or (focus_state_old == 10) or (focus_state_old == 11):
            logger.debug(f'Now hiding EDMC - giufocus')
            ctypes.windll.user32.ShowWindow(edmc_handle, 11)
        elif flagsisindanger_now == 4194304:
            logger.debug(f'Now hiding EDMC - flagsdanger')
            ctypes.windll.user32.ShowWindow(edmc_handle, 11)        
        elif journal_underattack_now == 1:
            logger.debug(f'Now hiding EDMC - journalunderattack')
            ctypes.windll.user32.ShowWindow(edmc_handle, 11) 
        else:
            logger.debug(f'Now unhiding EDMC')
            ctypes.windll.user32.ShowWindow(edmc_handle, 4)
