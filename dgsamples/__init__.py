from . import _registerdata

allsamples = _registerdata._runit()

from_root = _registerdata._from_root

for _s in allsamples:
    exec(_s+'=allsamples[_s]')

# Import version number
from ._version import __version__
