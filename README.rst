Bangla Lion Usage Viewer
========================

:author: M Nasimul Haque

A cross-platform desktop viewer for Bangla Lion internet bandwidth usage.

Screenshot
==========

KDE (Kubuntu)

.. image:: http://farm6.static.flickr.com/5320/5901636265_4c3a799a16.jpg

Gnome (Ubuntu)

.. image:: http://farm7.static.flickr.com/6099/5902393690_379a0582d0.jpg

Requirements
============

This is built on PySide - a python binding for Qt4 by Nokia. A Qt4 runtime
along with a python installation is required. It also requires BeautifulSoup,
a python (x)html parser.

Installation
============

Download the source code from github_ and unzip it to a folder. The rest of the
document assumes that it has been downloaded to `~/Downloads` folder and
extracted to `blusage` folder.

Linux
-----

Ubuntu (>= Lucid)
.................

The source distribution includes a install script for Ubuntu (including Lucid
and greater). To install it just open up a terminal and run the following
commands.

    $ cd ~/Downloads/blusage/
    $ sudo ./install_ubuntu.py

This will install all the dependencies and BLUsage itself. After a successful
installation, you can run BlUsage either from the command line through
`blusage` command or double click the shortcut installed on your desktop.

Other Linux
...........

For other linux distributions you need to install the following from your
package manager.

    1. pyside >= 1.0.3
    2. python BeautifulSoup > 3

After satisfying the requirements you can either double click the `main.py`
file or run it from the commandline via

    $ cd ~/Downloads/blusage
    $ ./main.py

Mac OS X
--------

There exists a specific software for Mac. You can find it `here
<https://github.com/nsmgr8/BLUsage/>`_. In case you want to run this on your
Mac, follow the steps from `Other Linux`_.

Windows
-------

I haven't tested this on Windows. However, given all the requirements installed
properly. It should run fine.

License
=======

The source code is licensed under MIT license. Please hack it to suit yourself.

The MIT License (MIT)
---------------------

Copyright (c) 2011 M. Nasimul Haque

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

.. _github: https://github.com/nsmgr8/BLUsage-qt4

