# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 11:42:39 2017

@author: ibari
"""
from __future__ import division
import numpy as np
from pathlib import Path

# ------- Result and Memorize Classes ------- #
class Memorize(dict):
    """ Memorize results.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())
    
class SpatialResults(dict):
    """ Represents the statistical result.

    Returns
    ----------
    Note:
            The returns are attributes.
            
    data : ndarray or tuple
        Imported image arrays.

    filename : str or tuple
        Filenames of imported images.

    size : int or tuple
        Pixelsize of imported images
    
    geotransform : tuple
        Geotransform information.
                    
    projection : tuple
        Projection information.
                    
    pixel_width : int, float or tuple
        Pixel width size.
                    
    pixel_height : int, float or tuple
        Pixel height size.

    origin_x : int or tuple
        Origin x coordinate.

    origin_y : int or tuple
        Origin y coordinate.
        
    dataset : gdal_object
        gdal.Open instance.
        
    bands : int or tuple
        Image bands.

    np_dtype : np.dtype
        Numpy datatype.
        
    gdal_dtype : gdal.dtype
        Gdal datatype.
     
    working_dir : str
        Workind directory. 
        
    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific module. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())

# ------- GIS operations ------- #
def nan_to_num(arrays, no_data=-99999):
    """
    Convert nan values to a value
    """
    arrays[np.isnan(arrays)] = no_data

def subset (data, x, y):
    """
    Note
    ----------        
    Subsetting an Image with coordinates.
    
    Parameters
    ----------
    data : array
        Data to subset.
    
    area : tuple with lists
        Subset coordinates like (... x = [450,477], y = [0,10]).

    Returns
    -------
    array_like
    
    """
# Subsetting an Image with a
    if isinstance(data, tuple):
        arrays = []
        for i in range(len(data)):
            arrays_subset = data[i][x[0]:x[1], y[0]:y[1]]
            nan_to_num(arrays_subset)
            arrays.append(arrays_subset)

        data = tuple(data)

    else:
        data = data[x[0]:x[1], y[0]:y[1]]
        nan_to_num(data)

    return data

# ------- Data and Executable Tests ------- #
def test_data(data, verbose=1):
    """Data Test
    Test if the imported data fulfilled the requirements. Requires a ImportResult class instance

    """
    col = data.shape[1]
    _col = col[1:] == col[:-1]

    row = data.shape[0]
    _row = row[1:] == row[:-1]

    size = data.size
    _size = size[1:] == size[:-1]
    
    if verbose is 2:
        if (_col and _row and _size):
            print "Status: All requirements are fulfilled"
    
    if (_col != True or _row != True):
        raise AssertionError("Status: Input dimensions must agree", 
                             'shapes: cols = {1}, rows = {2}'.format(col, row))        
    
    if (_col is not True or _row is not True or _size is not True):
        raise AssertionError("Status: Input dimensions and size must agree", 
                             'shapes: cols = {1}, rows = {2}, size: {3}'.format(col, row, size))
        
def test_import_type(file_name):
    string_check = test_string(file_name)
    tuple_check = test_tuple(file_name)
    
    if tuple_check:
        tuple_str_check = tuple([type(item) == str for item in file_name])
        tuple_str_check = np.all(np.all(tuple_str_check) == True)
    else:
        tuple_str_check = None
        
    return string_check, tuple_check, tuple_str_check

def test_string(data):
    return isinstance(data, str)

def test_tuple(data):
    return isinstance(data, tuple)

def check_executable(name):
    """Check whether executable is on PATH."""
    from distutils.spawn import find_executable
    
    executable_list = []
    if test_tuple(name):
        for item in name:
            executable_temp = find_executable(item) is not None
            executable_list.append(executable_temp)
            
        return np.any(np.asarray(executable_list) == True)
    
    else:
        return find_executable(name) is not None

def check_is_file(files):
    # This is only temporary. Insert here the DIR path with DEMs.
    dir_name = "C:\\Users\\ibari\\Documents"
    files = Path(dir_name + '\\' + files)
    try:
        my_abs_path = files.resolve()
    except WindowsError:
        
        # Maybe Download the DEM File?
        print ("File doesn´t exist")# doesn't exist
    else:
        print ("File exist")















