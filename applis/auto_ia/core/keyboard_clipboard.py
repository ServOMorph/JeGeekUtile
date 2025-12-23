import pyperclip
import pyautogui

def copy_text(text: str) -> None:
    pyperclip.copy(text)

def paste_text() -> str:
    return pyperclip.paste()

def write_text(text: str):
    pyautogui.write(text)

def press_keys(keys: list[str]):
    pyautogui.hotkey(*keys)
