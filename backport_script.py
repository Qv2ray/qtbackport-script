#!/usr/bin/env python3

import subprocess
from simple_term_menu import TerminalMenu
from fnmatch import fnmatch
import os
import fileinput
import re

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
            if os.path.isdir(d):
                file_path.append(d)
            elif fnmatch(d, '*.dsc'):
                dsc.append(d)
        terminal_menu = TerminalMenu(['doc', 'nodoc'])
        mode_sel = terminal_menu.show()
        ppa = input('Enter ppa: ')
        distro = input('Enter distro: ')
        if distro == 'focal':
            for i in file_path:
                    for line in fileinput.input(f'{i}/debian/control', inplace=True):
                        line = line.rstrip('\r\n')
                        print(line.replace('debhelper-compat (= 13)', 'debhelper-compat (= 12)'))
        if mode_sel == 1:
            for i in file_path:
                for line in fileinput.input(f'{i}/debian/rules', inplace=True):
                    line = line.rstrip('\r\n')
                    print(re.sub('.*DH_VERBOSE=1', 'export DEB_BUILD_PROFILES=nodoc', line))
                for line in fileinput.input(f'{i}/debian/control', inplace=True):
                    line = line.rstrip('\r\n')
                    if 'nodoc' in line and not 'Build-Profiles:' in line:
                        pass
                    else:
                        print(line)
                command = f'cd {i}; dpkg-source -b .'
                subprocess.call(command, shell=True)
        for d in dsc:
            command = f'backportpackage -u {ppa} -d {distro} -y {d}'
            subprocess.call(command, shell=True)


if __name__ == "__main__":
    main()
