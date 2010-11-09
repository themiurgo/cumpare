"""

    Cumpari is a python library and program for file comparison.
    Copyright (C) 2010 Antonio Lima <anto87@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""


import hashlib
import os
import itertools

# Comparer functions

def filehash_md5(fname):
    with open(fname) as file:
        h = hashlib.md5()
        fcontent = file.read()
        h.update(fcontent)
        return h.hexdigest()

def filehash_sha1(fname):
    with open(fname) as file:
        h = hashlib.sha1()
        fcontent = file.read()
        h.update(fcontent)
        return h.hexdigest()

class Comparer(object):
    def __init__(self, fnames, compfunc):
        self.fnames = fnames
        self.fdict = dict()
        self.compfunc = compfunc

    def compare(self):
        compfunc = self.compfunc
        for fname in self.fnames:
            attr = compfunc(fname)
            if attr not in self.fdict:
                self.fdict[attr] = [fname]
            else:
                self.fdict[attr].append(fname)
        return self.similarGroups()

    def similarGroups(self):
        return [group for group in self.fdict.itervalues() if 
len(group)>1]

class SizeComparer(Comparer):
    def __init__(self, fnames):
        Comparer.__init__(self, fnames, os.path.getsize)

class HashMD5Comparer(Comparer):
    def __init__(self, fnames):
        Comparer.__init__(self, fnames, filehash_md5)

class HashSHA1Comparer(Comparer):
    def __init__(self, fnames):
        Comparer.__init__(self, fnames, filehash_sha1)

class CumpareJob(object):
    """Defines a new dupes finding job"""

    def __init__(self, directory, size=True, sha1=True, md5=False):
        self.directory = directory
        self.size_opt = size
        self.sha1_opt = sha1
        self.md5_opt = md5

    @property
    def fnames(self):
        return [os.path.join(root,fname)
            for root, dirs, files in os.walk(self.directory)
            for fname in files]

    def execute(self):
        fnames = self.fnames
        groups = None
        
        if self.size_opt:
            comp = SizeComparer(fnames)
            groups = comp.compare()
        if self.md5_opt:
            fnames = itertools.chain(*groups)
            comp = HashMD5Comparer(fnames)
            groups = comp.compare()
        if self.sha1_opt:
            fnames = itertools.chain(*groups)
            comp = HashSHA1Comparer(fnames)
            groups = comp.compare()
        return groups

if __name__ == "__main__":
    job = CumpareJob(".")
    print job.execute()
