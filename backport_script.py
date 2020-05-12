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
                if os.path.isdir(d):
                    file_path.append(d)
                elif fnmatch(d, f'{component}*.dsc'):
                    dsc.append(d)
        terminal_menu = TerminalMenu(['doc', 'nodoc'])
        mode_sel = terminal_menu.show()
        ppa = input('Enter ppa: ')
        distro = input('Enter distro: ')
        if mode_sel == 1:
            for i in file_path:
                for line in fileinput.input(f'{i}/debian/control', inplace=True):
                    if '<!nodoc>' in line and not 'Build-Profiles:' in line:
                        line.replace(line, '')
                        line.rstrip('\r\n')
                    print(line)
                for line in fileinput.input(f'{i}/debian/rules', inplace=True):
                    if 'DH_VERBOSE=1' in line:
                        env = 'export DEB_BUILD_PROFILES=nodoc'
                        line.replace(line, line+env)
                        line.rstrip('\r\n')
                    print(line)
                command = f'cd {i}; dpkg-source -b .'
                subprocess.call(command, shell=True)
        for d in dsc:
            command = f'backportpackage -u {ppa} -d {distro} {d}'
            subprocess.call(command, shell=True)


if __name__ == "__main__":
    main()
