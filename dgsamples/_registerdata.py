import os
import tinytools as tt
import inspect


def _runit():
    # Go into each directory and look for interesting things per pseudo-code:
    #
    # if ".TIL found":
    #     "return all .TILs and stop"
    # elif ".TIF found" :
    #     "return all .TIFs and stop"
    # elif ".shp or .json found" :
    #     "return all .shp and .json then stop"
    #
    # then use "filename_map.PVL" to add quick access entries
    # on the OrderedBunch

    pkg_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    return _from_root(pkg_dir)


def _from_root(test_root):
    """
    Return the dgsamples in the given test_root.
    :param test_root: Path to a dgsamples-compliant folder
    :return: OrderedBunch
    """

    pkg_dirs = tt.files.search(test_root, '*', ret_files=False, ret_dirs=True)

    # Setup the data structure to be populated
    pkg_samples = tt.bunch.OrderedBunch()

    # Return files from each of the sample directories
    for d in pkg_dirs:
        # Set sample folder info bunch structure to populated
        name = os.path.basename(d)
        pkg_samples[name] = tt.bunch.OrderedBunch()

        # Set package name
        if os.path.isdir(d):
            pkg_samples[name]['path'] = d

        # Check for notes
        tmpnote = tt.files.search(d, 'notes.txt', case_sensitive=False)
        if tmpnote:
            with open(tmpnote[0], 'r') as f:
                pkg_samples[name]['notes'] = f.read()

        # Look for TIL files
        tmptil = tt.files.search(d, '*.TIL', case_sensitive=False, depth=3)

        # Look for TIF files
        tmptif = tt.files.search(d, ['*.TIF', '*.TIFF'],
                                 case_sensitive=False, depth=3)
        # Look for vector files
        tmpvec = tt.files.search(d, ['*.SHP', '*.json', '*.geojson'],
                                 case_sensitive=False, depth=3)

        if tmptil:
            pkg_samples[name]['files'] = tmptil
        elif tmptif:
            pkg_samples[name]['files'] = tmptif
        elif tmpvec:
            pkg_samples[name]['files'] = tmpvec

        try:
            pvls = tt.files.search(d, 'filename_map.pvl', ret_files=True, ret_dirs=False, case_sensitive=False,
                                   depth=1)
            [pvl] = pvls # ensure that there is one and only one filename using python's list unpacking
            name_map = tt.pvl.read_from_pvl(pvl)
        except:
            name_map = {}

        for k, v in name_map.iteritems():
            v = tt.files.search(d, '*' + v, depth=3)
            if v[0] in pkg_samples[name]['files']:
                pkg_samples[name][k] = v[0]

    return pkg_samples
