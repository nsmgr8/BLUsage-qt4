#!/usr/bin/env python

import os
import apt
import subprocess

def main():
    if not os.environ['USER'] == 'root':
        print 'This program requires root access.'
        print 'Use `sudo ./install.py`'
        raise SystemExit(1)

    acq_progress = apt.progress.text.AcquireProgress()
    inst_progress = apt.progress.base.InstallProgress()

    cache = apt.Cache(apt.progress.text.OpProgress())
    cache.update()
    cache.open()
    cache.commit(acq_progress, inst_progress)

    pyside = cache['python-pyside']
    version = '1.0.3'
    if not [v for v in pyside.versions if v >= version]:
        print "It requires pyside >=", version
        print 'Do you want to install it from PPA? (Y/n)',
        if raw_input() == 'n':
            print 'Could not install it. Quitting...'
            raise SystemExit(1)

        command = 'add-apt-repository ppa:pyside'.split()
        try:
            subprocess.check_call(command)
            cache.update()
            cache.open()
            cache.commit(acq_progress, inst_progress)
            pyside = cache['python-pyside']
            if not [v for v in pyside.versions if v >= version]:
                print 'Could not find required pyside package.'
                print 'You might try changing to main repository server.'
                raise SystemExit(1)
        except:
            print 'Could not add PPA repository. Quitting...'
            raise SystemExit(1)

    if not pyside.is_installed:
        for pkg in ['qtcore', 'qtgui', 'qtnetwork']:
            cache['python-pyside.%s' % pkg].mark_install()

    soup = cache['python-beautifulsoup']
    if not soup.is_installed:
        soup.mark_install()

    cache.commit(acq_progress, inst_progress)

    print
    print 'Installation is successful!'

if __name__ == '__main__':
    main()

