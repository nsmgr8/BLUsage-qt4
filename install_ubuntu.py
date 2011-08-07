#!/usr/bin/env python

import os
import apt
import subprocess
import glob
import shutil
import py_compile
import stat
import sys

install_path = '/usr/local/blusage'
main_pyc = os.path.join(install_path, 'main.pyc')
desktop_launcher = os.path.expanduser('~/Desktop/BLUsage.desktop')
png_file = os.path.join(install_path, 'blusage.png')

def install_blusage():
    if not os.path.exists(install_path):
        try:
            os.makedirs(install_path)
        except OSError:
            print 'ERROR: Cannot create install folder: %s' % install_path
            return

    pyfiles = [f for f in glob.glob('src/*.py') if not f.startswith('install')]
    installed_py = [os.path.join(install_path, f[4:]) for f in pyfiles]
    for src, dest in zip(pyfiles, installed_py):
        shutil.copyfile(src, dest)
        py_compile.compile(dest)
        os.remove(dest)

    shutil.copyfile('resources/blusage.png', png_file)
    shutil.copyfile('resources/BLUsage.desktop', desktop_launcher)

    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | \
                 stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    os.chmod(desktop_launcher, permission | stat.S_IWOTH | stat.S_IWGRP)
    os.chmod(main_pyc, permission)

    parent_folder = install_path.rsplit(os.sep, 1)[0]
    bin_folder = os.path.join(parent_folder, 'bin')
    if not os.path.exists(bin_folder):
        bin_folder = install_path

    bin_file = os.path.join(bin_folder, 'blusage')
    if os.path.exists(bin_file):
        os.remove(bin_file)
    os.symlink(main_pyc, bin_file)

def install_deps():
    acq_progress = apt.progress.text.AcquireProgress()
    inst_progress = apt.progress.base.InstallProgress()

    cache = apt.Cache(apt.progress.text.OpProgress())

    pyside = cache['python-pyside']
    version = '1.0.3'
    if not [v for v in pyside.versions if v >= version]:
        print "It requires pyside >=", version
        print 'Do you want to install it from PPA? (Y/n)',
        if raw_input() == 'n':
            print 'ERROR: Could not install it. Quitting...'
            raise SystemExit(1)

        command = 'add-apt-repository ppa:pyside'.split()
        try:
            subprocess.check_call(command)
            cache.update()
            cache.open()
            cache.commit(acq_progress, inst_progress)
            pyside = cache['python-pyside']
            if not [v for v in pyside.versions if v >= version]:
                print 'ERROR: Could not find required pyside package.'
                print 'You might try changing to main repository server.'
                raise SystemExit(1)
        except:
            print 'ERROR: Could not add PPA repository. Quitting...'
            raise SystemExit(1)

    cache['python-pyside'].mark_install()
    cache['python-beautifulsoup'].mark_install()

    cache.commit(acq_progress, inst_progress)

def install():
    install_deps()
    install_blusage()
    print
    print 'Installation is successful!'
    print 'You can run it by the command `blusage` in the terminal, or'
    print 'by clicking on the icon named `BLUsage` installed on your desktop'

def uninstall():
    if not os.path.exists(install_path):
        print 'BLUsage is not installed on your system.'
        return

    print 'Are you sure to uninstall BLUsage from your system? (y/N)',
    if raw_input() <> 'y':
        print 'Thanks for keeping it. :)'
        return

    shutil.rmtree(install_path)

    bin_file = os.path.join(install_path.rsplit(os.sep, 1)[0], 'blusage')
    for f in [bin_file, desktop_launcher]:
        if os.path.exists(f):
            os.remove(f)

    print 'BLUsage has been completely removed from your system! :('

if __name__ == '__main__':
    if not os.environ['USER'] == 'root':
        print 'ERROR: This program requires root access.'
        print 'Use `sudo %s`' % sys.argv[0]
        raise SystemExit(1)

    if '-u' in sys.argv:
        uninstall()
    else:
        install()

