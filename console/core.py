'''
    .. console - Comprehensive utility library for ANSI terminals.
    .. © 2018, Mike Miller - Released under the LGPL, version 3+.

    Complicated Gobbyldegook supporting simpler interfaces is located here.

    Classes below not meant to be instantiated by client code.
'''
import sys
import logging
import re

from . import _CHOSEN_PALETTE
from .constants import CSI
from .disabled import dummy, empty
try:
    import webcolors
except ImportError:
    webcolors = None


_END = CSI + '0m'
ALL_PALETTES = ('basic', 'extended', 'truecolor')  # variants 'x11', 'web'
log = logging.getLogger(__name__)

# Palette attribute name finders, now we've got two problems.
# Not a huge fan of regex but here they nicely enforce the naming rules:
_hd = r'[0-9A-Fa-f]'  # hex digits
_index_finder = re.compile(r'^i_?\d{1,3}$', re.A)                   # i_DDD
_nearest_finder = re.compile(f'^n_?{_hd}{{3}}$', re.A)              # n_HHH
_true_finder = re.compile(f'^t_?({_hd}{{3}}|{_hd}{{6}})$', re.A)    # t_HHH
_x11_finder = re.compile(r'^x\w{4,64}$', re.A)                      # x_NAME
_web_finder = re.compile(r'^w\w{4,64}$', re.A)                      # x_NAME

# X11 colors support
_x11_color_map = {}
X11_RGB_FILE = None  # Windows
if sys.platform == 'linux':
    X11_RGB_FILE = '/etc/X11/rgb.txt'
elif sys.platform == 'darwin':
    X11_RGB_FILE = '/opt/X11/share/X11/rgb.txt'


class _BasicPaletteBuilder:
    ''' ANSI code container for styles, fonts, etc.

        A base-class that modifies the attributes of child container classes on
        initialization.  Integer attributes are recognized as ANSI codes to be
        wrapped with a manager object to provide mucho additional
        functionality.  Useful for the basic 8/16 color/fx palettes.
    '''
    def __new__(cls, autodetect=True, palettes=None):
        ''' Override new() to replace the class entirely on deactivation.

            Arguments:
                autodetect  - Attempt to detect palette support.
                palettes    - If autodetect disabled, set palette support
                              explicitly.  str, seq, or None
        '''
        self = super().__new__(cls)
        if autodetect:
            if _CHOSEN_PALETTE:  # enable "up to" the chosen palette level:
                palettes = ALL_PALETTES[:ALL_PALETTES.index(_CHOSEN_PALETTE)+1]
            else:
                self = dummy                        # None, deactivate
                palettes = ()                       # skipen-Sie

        else:  # set palette manually
            if type(palettes) in (list, tuple):     # carry on
                pass
            elif type(palettes) is str:             # make iterable
                palettes = (palettes,)
            elif type(palettes) is None:            # Ah, Shaddap-a ya face
                self = dummy
                palettes = ()                       # skipen-Sie
            else:
                raise TypeError('%r not in type (str, list, tuple)' % palettes)

        self._palette_support = palettes
        return self

    def __init__(self, **kwargs):
        # look for integer attributes to wrap in a basic palette:
        for name in ['default'] + dir(self):        # default needs to go 1st!
            if not name.startswith('_'):
                value = getattr(self, name)
                if type(value) is int:
                    if 'basic' in self._palette_support:
                        attr = _PaletteEntry(self, name.upper(), value)
                    else:
                        attr = empty
                    setattr(self, name, attr)

    def __repr__(self):
        return f'{self.__class__.__name__}(palettes={self._palette_support})'


class _HighColorPaletteBuilder(_BasicPaletteBuilder):
    ''' Container/Router for ANSI extended & truecolor palettes. '''

    def __init__(self, x11_rgb_filename=X11_RGB_FILE, **kwargs):
        super().__init__(**kwargs)
        self._x11_rgb_filename = x11_rgb_filename

    def __getattr__(self, name):
        ''' Traffic cop - called only when an attribute is missing,
            once per palette entry attribute.

            The "basic" palette will never get here, as it is already defined.
        '''
        key = name[1:].lstrip('_')  # rm potential prefix

        # follow the yellow brick road…
        if _index_finder.match(name):       # INDEXED aka EXTENDED
            if 'extended' in self._palette_support:  # build entry
                return self._get_extended_palette_entry(name, key)
            else:
                return empty

        elif _nearest_finder.match(name):   # NEAREST
            if 'extended' in self._palette_support:  # build entry
                from .proximity import find_nearest_color_hexstr
                nearest_idx = find_nearest_color_hexstr(key)
                return self._get_extended_palette_entry(name, str(nearest_idx))
            else:
                return empty

        elif _true_finder.match(name):      # TRUE
            if len(key) == 3:  # double chars:  b0b -> bb00bb
                key = ''.join([ch*2 for ch in key])
            if 'truecolor' in self._palette_support:  # build entry
                return self._get_true_palette_entry(name, key)
            else:
                return empty

        elif _x11_finder.match(name):       # X11
            if 'truecolor' in self._palette_support:
                return self._get_x11_palette_entry(name, key)
            else:
                return empty

        elif _web_finder.match(name):       # WEBCOLORS
            if 'truecolor' in self._palette_support:
                if webcolors:
                    return self._get_web_palette_entry(name, key)
                else:
                    return empty
            else:
                return empty

        else:  # look for names
            if webcolors:
                try:
                    log.debug('attempting webcolor lookup for %r.', name)
                    return self._get_web_palette_entry(name, name)  # whole name
                except ValueError:
                    pass
            # try X11
            if X11_RGB_FILE:
                try:
                    return self._get_x11_palette_entry(name, name)  # whole name
                except KeyError:
                    pass
            # Emerald city
            raise AttributeError('%r is not a recognized attribute name.'
                                 % name)

    def _get_extended_palette_entry(self, name, index):
        ''' Compute extended entry, once on the fly. '''
        values = [self._start_codes_extended, index]
        return self._create_entry(name, values)

    def _get_true_palette_entry(self, name, hexdigits):
        ''' Compute truecolor entry, once on the fly. '''
        values = [self._start_codes_true]
        # convert hex attribute name, ex 'BB00BB', to ints to 'R', 'G', 'B':
        values.extend(str(int(hexdigits[idx:idx+2], 16)) for idx in (0, 2 ,4))

        return self._create_entry(name, values)

    def _get_x11_palette_entry(self, name, color_name):
        ''' Find X11 entry, once on the fly. '''
        values = [self._start_codes_true]
        if not _x11_color_map:
            _load_x11_color_map(self._x11_rgb_filename)
        # convert name to 'R', 'G', 'B':    - below:  empty tuple
        values.extend(_x11_color_map[color_name.lower()])

        return self._create_entry(name, values)

    def _get_web_palette_entry(self, name, color_name):
        ''' Find webcolor entry, once on the fly. '''
        values = [self._start_codes_true]
        values.extend(str(i) for i in webcolors.name_to_rgb(color_name.lower()))
        return self._create_entry(name, values)  # TODO:

    def _create_entry(self, name, values):
        ''' Render first values as string and place as first code,
            save, and return attr.
        '''
        attr = _PaletteEntry(self, name.upper(), ';'.join(values))
        setattr(self, name, attr)  # now cached
        return attr

    def clear(self):
        ''' Cleanse the palette to clear memory.
            Useful for truecolor, perhaps.
        '''
        self.__dict__.clear()


class _PaletteEntry:
    ''' Palette Entry Attribute

        Enables:

        - Rendering to an escape sequence string.
        - Addition of attributes, to create a combined, single sequence.
        - Allows entry attributes to be called, for use as a text wrapper.
        - Use as a Context Manager via the "with" statement.

        Arguments:
            parent  - Parent palette
            name    - Display name, used in demos.
            code    - Associated ANSI code number.
            out     - Stream to print to, when using a context manager.
    '''
    def __init__(self, parent, name, code):
        self.parent = parent
        self.default = (parent.default if hasattr(parent, 'default')
                                       else parent.end)  # style
        self.name = name
        self._codes = [str(code)]           # the initial code
        self._out = sys.stdout              # for redirection

    def __add__(self, other):
        ''' Add: self + other '''
        if isinstance(other, str):
            return str(self) + other

        elif isinstance(other, _PaletteEntry):
            # Make a copy, so codes don't pile up after each addition
            # Render initial values once as string and place as first code:
            newcodes = self._codes + other._codes
            #~ log.debug('codes for new instance: %r', newcodes)  # noisy
            attr = _PaletteEntry(self.parent, self.name,
                                 ';'.join(newcodes))
            same_category = self.parent is other.parent
            #~ log.debug('palette entries match: %s', same_category)  # noisy

            if not same_category:  # different, use end instead of default
                attr.default = _END

            return attr
        else:
            raise TypeError('Addition to type %r not supported.' % type(other))

    def __radd__(self, other):
        ''' Reverse add: other + self '''
        return other + str(self)

    def __bool__(self):
        return bool(self._codes)

    def __enter__(self):
        log.debug(repr(str(self)))
        print(self, file=self._out, end='')

    def __exit__(self, type, value, traceback):
        print(self.default, file=self._out, end='')

    def __call__(self, text, *styles):
        # if category different, copy uses end instead of default, see addition
        for attr in styles:
            self += attr

        return f'{self}{text}{self.default}'

    def __str__(self):
        return f'{CSI}{";".join(self._codes)}m'

    def __repr__(self):
        return self.__str__()

    def template(self, placeholder='{}'):
        ''' Returns a template string from this Entry with its attributes.

            Placeholder can be '%s', '{}', '${}' or other depending on your
            needs.
        '''
        return f'{self}{placeholder}{self.default}'

    def set_output(self, outfile):
        ''' Set's the output file, currently only useful with context-managers.

            Note:
                This function is experimental and may not last.
        '''
        self._out = outfile


def _load_x11_color_map(filename=X11_RGB_FILE):
    ''' Load and parse X11's rgb.txt '''
    try:
        with open(filename) as infile:

            for line in infile:
                if line.startswith('!') or line.isspace():
                    continue

                tokens = line.rstrip().split(maxsplit=3)
                key = tokens[3]
                if ' ' in key:  # skip names with spaces to match webcolors
                    continue

                _x11_color_map[key.lower()] = tuple(token for token in tokens[:3])
    except IOError as err:
        log.debug('error: X11 palette not found. %s', err)
