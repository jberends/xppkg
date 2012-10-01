==============================================
XPpkg - Hassle free X-Plane package management
==============================================

Status
======
.. image:: https://secure.travis-ci.org/jberends/xppkg.png
    :target: http://travis-ci.org/jberends/xppkg

This project is in "Development Status :: 2 - Pre-Alpha".


Main Philisophy
===============

This document desribes the main philisophy why xppkg was created.

Main Pain
=========

Installation of Scenery, Aircraft, NavData, Plugins are a pain. The sim-community is flooded with good (and bad)
quality resources, and arranging and browsing all sites to find your own golden installation is always a pain.
After returning to X-plane from the FS world after a few years, nothing changed.

  * XPpkg is a hassle-free X-Plane package installer, much alike pip in python:
    to download, install and upgrade various X-Plane packages from various internet sources.

  * XPpkg for developers of packages for X-Plane should be a hassle free way to distribute their packages

Inspiration
===========

Main inspiration comes from my work within the \*NIX world (That is essential Linux and the \*NIX with the best graphical
UI on top: Mac OSX) and python.

Python Package Management Examples:

* pip installer for Python http://www.pip-installer.org/
* easy_install for Python
* PyPI is an important integration for both

Various Linux Examples:

* apt, apt-get, aptitude, dpkg originally created for Debian/GNU Linux
* rpm

Mac OSX Package Management Examples:

* Macports (http://www.macports.org), Homebrew (http://mxcl.github.com/homebrew/)

Other Examples:

* rubygems (http://rubygems.org/)

Website
=======
A github repository will function for now as the main place for collaboration at https://github.com/jberends/xppkg