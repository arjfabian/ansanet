"""
  ▟▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜▙
  █   ░▒▓███▓▒░░▒▓████▓▒░░▒▓████▓▒░░▒▓███▓▒░░▒▓████▓▒░░▒▓█████▓▒░▒▓█████▓▒░  █
  █  ░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░ ░▒▓█▓▒░    █
  █  ░▒▓█▓███▓▒░▒▓█▓▒▓█▓▒░░▒▓███▓▒░▒▓█▓███▓▒░▒▓█▓▒▓█▓▒░▒▓█████▓▒░ ░▒▓█▓▒░    █
  █  ░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░    █
  █  ░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓████▓▒░▒▓█▓▒▓█▓▒░▒▓█▓▒▓█▓▒░▒▓█████▓▒░ ░▒▓█▓▒░    █
  ▜▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟▛

  TUI MANAGER
  ===========
  Handles the rendering of elements on the Text User Interface (TUI) and
  controls the cursor, using ANSI control codes.
  The screen is assumed to have a minimum resolution of 80 lines, 25 chars.

  TODO:
    - Adapt the size to higher resolutions.
"""


import sys

# --- ANSI Color Configuration ---
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

# --- ANSI Terminal Control Codes ---
C_CURSOR_HOME = "\033[H"       # Moves cursor to 1;1 (Home)
C_CLEAR_SCREEN = "\033[2J"      # Clears entire screen
C_HIDE_CURSOR = "\033[?25l"     # Hides the cursor
C_SHOW_CURSOR = "\033[?25h"     # Shows the cursor

def clear_screen():
    """Clears the terminal screen using ANSI code."""
    # Use sys.stdout.write for direct, immediate output
    sys.stdout.write(C_CLEAR_SCREEN)
    sys.stdout.flush()

def draw_screen():
    """
    Test function to verify fixed-position ANSI cursor drawing.
    This function draws the fixed header and footer.
    """
    
    # 1. Clear the entire screen
    clear_screen()
    
    # 2. Move to Row 24, Column 1 and draw the Footer/Menu
    sys.stdout.write("\033[24;1H")
    sys.stdout.write(f"\n [M]anage | [L]ogs | [Q]uit                                                     {C_RESET}")
    sys.stdout.write("\033[97;45m")
    
    # 3. Move to Row 1, Column 1 and draw the Header
    sys.stdout.write("\033[1;1H")
    # sys.stdout.write("\033[97;45m")
    sys.stdout.write(" ANSANET v1.0                                                                   ")
    sys.stdout.write("\n\n")
    sys.stdout.write("\033[49;100m")
    sys.stdout.write(f" ╔{'═' * 57}╦{'═' * 18}╗ ")
    sys.stdout.write(f" ║ Messages{' ' * 48}║   Active hosts   ║ ")
    sys.stdout.write(f" ╠{'═' * 57}╬{'═' * 18}╣ ")
    for _ in range(16):
        sys.stdout.write(f" ║{' ' * 57}║ {'·' * 16} ║ ")
    sys.stdout.write(f" ╚{'═' * 57}╩{'═' * 18}╝ ")

    # 8. Wait for me to press a key.
    sys.stdout.write(C_SHOW_CURSOR) # Show cursor for typing
    sys.stdout.write("\033[2;1H")
    input(f"{C_BOLD}{C_YELLOW}Press any key to exit: {C_RESET}")

    
    # 6. Go back to Row 2, Column 1 (content area)
    sys.stdout.write("\033[3;1H")
    
    # 7. Print "hello world!" (Test content)
    sys.stdout.write(f"{C_GREEN}Hello world! This is row 2.{C_RESET}\n")
    sys.stdout.write(f"The terminal cursor should now be on row 3.{C_RESET}\n\n")

    # Flush all output immediately
    sys.stdout.flush()
    
