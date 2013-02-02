#!/usr/bin/env python
# encoding: utf-8

VERSION = (0, 0, 0, "b", 0) # PEP 386

def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        import os
        dir = os.path.abspath(os.path.dirname(__file__))
        hg_dir = os.path.normpath(os.path.join(dir, '../../'))
        if os.path.isdir(os.path.join(hg_dir, '.hg')):
            hg_rev='0'
            try:
                from mercurial import ui, hg, error
            except ImportError:
                pass
            else:
                try:
                    repo = hg.repository(ui.ui(), hg_dir)
                    c = repo['tip']
                    hg_rev = '%s' % c.rev()
                except error.RepoError:
                    pass
            version = '%s.dev%s' % (version, hg_rev)
    return version

__version__ = get_version()