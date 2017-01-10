# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:46:16 2016

@author: losoip
"""


class DirectoryNotFoundError(OSError):
    pass


class FileFormatError(ValueError):
    pass


class CtabError(FileFormatError):
    pass


class MolError(FileFormatError):
    pass


class RdError(FileFormatError):
    pass


class RxnError(FileFormatError):
    pass


class TsvError(FileFormatError):
    pass


class IdError(KeyError):
    pass


class CompoundIdError(IdError):
    pass


class EnzymeIdError(IdError):
    pass


class ReactionIdError(IdError):
    pass
