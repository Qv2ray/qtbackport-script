#!/usr/bin/env python3

import subprocess
from simple_term_menu import TerminalMenu
from fnmatch import fnmatch
import os
import fileinput


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
            qt_components = input('Enter the extra component name: ')
            if not qt_components == 'exit':
                qtextra.append(qt_components)
            else:
                break
        command = f"apt-get source {' '.join(qtextra)}"
    if main_sel == 0:
        file_path = []
        dsc = []
        for d in os.listdir('.'):
            for component in qtbase:
                if fnmatch(d, f'{component}*') and os.path.isdir(d):
                    file_path.append(d)
                elif fnmatch(d, f'{component}*.dsc'):
                    dsc.append(d)
        terminal_menu = TerminalMenu(['doc', 'nodoc'])
        mode_sel = terminal_menu.show()
        for i in file_path:
            if mode_sel == 1:
                for line in fileinput.input(f'{i}/debian/rules', inplace=True):
                    line = line.rstrip('\r\n')
                    print(line.replace('#export DH_VERBOSE=1', '#export DH_VERBOSE=1\nexport DEB_BUILD_PROFILES=nodoc\n'))
                command = f'cd {i}; dpkg-source -b .'
                subprocess.call(command, shell=True)
            ppa = input('Enter ppa: ')
            distro = input('Enter distro: ')
            for d in dsc:
                command = f'backportpackage -u {ppa} -d {distro} {d}'
                subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
