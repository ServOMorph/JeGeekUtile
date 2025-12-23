import pyautogui

pyautogui.FAILSAFE = True

def move_to(x: int, y: int, duration: float | None = None):
    pyautogui.moveTo(x, y, duration=duration if duration else 0)

def click(x: int, y: int, button: str = "left"):
    pyautogui.click(x, y, button=button)

def double_click(x: int, y: int):
    pyautogui.doubleClick(x, y)

def scroll(amount: int):
    pyautogui.scroll(amount)
