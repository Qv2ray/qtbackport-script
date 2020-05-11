#!/usr/bin/env python3

import subprocess
from simple_term_menu import TerminalMenu


def main():
    qtbase = [
        'qtbase-opensource-src', 'qtxmlpatterns-opensource-src', 'qtdeclarative-opensource-src', 'qtlocation-opensource-src',
        'qtsensors-opensource-src', 'qtwebsockets-opensource-src', 'qtwebchannel-opensource-src', 'qtwebkit-opensource-src', 'qttools-opensource-src'
    ]

    qtextra = []

    terminal_menu = TerminalMenu(['qtbase', 'qtextra'])
    main_sel = terminal_menu.show()
    if main_sel == 0:
        command = f"apt-get source {' '.join(qtbase)}"
        subprocess.call(command, shell=True)
    elif main_sel == 1:
        while True:
            qt_components = input('Enter the extra component name:')
            if not qt_components == 'exit':
                qtextra.append(qt_components)
            else:
                break
        command = f"apt-get source {' '.join(qtextra)}"


if __name__ == "__main__":
    main()
