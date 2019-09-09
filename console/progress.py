# -*- coding: future_fstrings -*-
'''
    .. console - Comprehensive utility library for ANSI terminals.
    .. © 2018, Mike Miller - Released under the LGPL, version 3+.

    Experimental Progress Bar functionality.

    A demo is available via command-line::

        ▶ python3 -m console.progress [-l] [-d]  # label and debug modes

    TODO:
        - include label in width calc  :-/
        - gradients/rainbar
        - additional tests
'''
import time

from console import fg, bg, fx, _CHOSEN_PALETTE
from console.screen import sc
from console.utils import clear_line, len_stripped
from console.detection import (detect_unicode_support, get_available_palettes,
                               get_size, os_name)

# accuracy thresholds, in seconds
TIMEDELTAS = (60, 300)  # one, five minutes

# Theme-ing info:
icons = dict(
    # name:      first, complete, empty, last, done, err_lo, err_hi, err_lbl
    ascii       = ('[', '#', '-', ']', '+', '<', '>', 'ERR'),
    blocks      = (' ', '▮', '▯', ' ', '✓', '⏴', '⏵', '✗'),
    # empty white bullet wrong size, breaks alignment:
    bullets     = (' ', '•', '•', ' ', '✓', '⏴', '⏵', '✗'),
    dies        = (' ', '⚅', '⚀', ' ', '✓', '⏴', '⏵', '✗'),
    horns       = ('🤘', '⛧', '⛤', '🤘', '✓', '⏴', '⏵', '✗'),
    segmented   = ('▕', '▉', '▉', '▏', '✓', '⏴', '⏵', '✗'),
    faces       = (' ', '☻', '☹', ' ', '✓', '⏴', '⏵', '✗'),
    wide_faces  = (' ', '😎', '😞', ' ', '✓', '⏴', '⏵', '✗'),
    stars       = ('(', '★', '☆', ')', '✓', '⏴', '⏵', '✗'),
    shaded      = ('▕', '▓', '░', '▏', '✓', '⏴', '⏵', '✗'),
    triangles   = ('▕', '▶', '◁', '▏', '✓', '⏴', '⏵', '✗'),
    spaces      = ('▕', ' ', ' ', '▏', '✓', '⏴', '⏵', '✗'),
)

# icon/style indexes
# 0    1    2    3    4     5     6     7
_if, _ic, _ie, _il, _id, _iel, _ieh, _ieb = range(8)


# styles
_dim_green = fx.dim + fg.green
_err_color = fg.lightred
styles = dict(
    dumb        = (str,) * 6,
    amber       = (
                    fx.dim + fg.i208,   # first
                    fg.i208,            # complete
                    fg.i172,            # empty
                    fx.dim + fg.i172,   # last
                    fg.i172,            # done
                    _err_color,         # error
                  ),
    amber_mono  = (
                    fx.dim + fg.i208,   # first
                    fx.reverse + fg.i208, # complete
                    fg.i172,   # empty
                    fx.dim + fg.i172,   # last
                    fx.dim + fx.reverse + fg.i208,  # done
                    _err_color,         # error
                  ),
    reds        = (
                    fx.dim + fg.red,    # first
                    fg.lightred,        # complete
                    fg.i236,            # empty
                    fg.i236,            # last
                    fg.red,             # done
                    _err_color,         # error
                  ),
    simple      = (
                    str,                # first
                    str,                # complete
                    fx.dim,             # empty
                    str,                # last
                    fx.dim,             # done
                    _err_color,         # error
                  ),
    greyen      = (
                    _dim_green,         # first
                    fg.green,           # complete
                    fg.i236,            # empty
                    fx.dim + fg.i236,   # last
                    _dim_green,         # done
                    _err_color,         # error
                  ),
    ocean       = (
                    _dim_green,         # first
                    fg.green,           # complete
                    fg.blue,            # empty
                    fx.dim + fg.blue,   # last
                    _dim_green,         # done
                    _err_color,         # error
                  ),
    ocean8       = (
                    fx.dim + fg.i70,    # first
                    fg.i70,             # complete
                    fg.i24,             # empty
                    fx.dim + fg.i24,    # last
                    fx.dim + fg.i70,    # done
                    _err_color,         # error
                  ),
    greyen_bg   = (
                    fx.dim + fg.i70,    # first
                    fx.bold + bg.i70,   # complete
                    fx.dim + bg.i236,   # empty
                    fx.dim + fg.i236,   # last
                    bg.i22,             # done
                    _err_color,         # error
                  ),
)

# figure default styles
unicode_support = detect_unicode_support()
icons['default']  = icons['ascii']
if os_name == 'nt':  # default to ascii on Windows
    pass
elif unicode_support:
    icons['default']  = icons['blocks']

_pals = get_available_palettes(_CHOSEN_PALETTE)
if _pals and 'extended' in _pals:
    styles['default'] = styles['ocean8']
elif _pals:
    styles['default'] = styles['ocean']
else:
    styles['default'] = styles['dumb']

themes = dict(
    basic_color = dict(icons='ascii', styles='default'),
    basic = dict(icons='ascii', styles='dumb'),
    dies = dict(icons='dies', styles='simple'),
    heavy_metal = dict(icons='horns', styles='reds'),
    shaded = dict(icons='shaded', styles='ocean'),
    solid = dict(icons='spaces', styles='greyen_bg'),
    warm_shaded = dict(icons='shaded', styles='amber'),
)
themes['default'] = themes['basic_color']


class ProgressBar:
    ''' A stylable bar graph for displaying the current progress of task
        completion.

        Example::

            import time  # demo purposes only
            from console.screen import sc
            from console.progress import ProgressBar

            with sc.hidden_cursor():

                items = range(256)      # example tasks

                # set total if needed
                bar = ProgressBar(total=len(items))

                for i in items:
                    print(bar(i), flush=True, end='')
                    time.sleep(.1)

                print()

        Arguments:
            clear_left: False       # True to clear at 0, or non-zero int offset
            debug: None             # Turn on debug output
            done: False             # True on completion, moderates style
            expand: False           # Set width to full terminal width
            label_fmt:  '%2.0f%%'   # Precision, defaults to no decimal places
            label_mode:  True       # Turn on label
            oob_error:  False       # Out of bounds error occurred
            timedelta: (60, 300)    # Thresholds to add. label precision | None
            total:  100             # Set the total number of items
            unicode_support: bool   # Detection result, determines default icons
            width: 32               # Width of bar plus start/end chars, not lbl

        Theming Arguments:
            icons:  (,,,)           # Tuple of chars
            styles: (,,,)           # Tuple of ANSI styles
            theme: 'name'           # String name of combined icon & style set
    '''
    debug = None
    done = False
    expand = False
    label_fmt = '%2.0f%%'
    label_mode = True
    oob_error = False
    timedelta = TIMEDELTAS
    total = 100
    unicode_support = unicode_support
    width = 32

    theme = 'default'
    icons = icons[theme]
    styles = styles[theme]

    _clear_left = True
    _min_width = 12
    _num_complete_chars = 0
    _remainder = 0

    def __init__(self, **kwargs):
        # configure instance
        for key, val in kwargs.items():
            if key == 'theme':
                self.icons = icons[themes[val]['icons']]
                self.styles = styles[themes[val]['styles']]
                if val.startswith('basic'):
                    self.unicode_support = False
                elif val == 'solid':
                    self.label_mode = 'internal'
            elif key == 'icons':
                self.icons = icons[val]
                if val == 'ascii':
                    self.unicode_support = False
            elif key == 'styles':
                self.styles = styles[val]
            elif key == 'expand' and val:
                width = get_size()[0]
                if self.label_mode != 'internal':
                    width -= len(self.label_fmt % 100)
                self.width = width
                self.expand = val
            else:
                setattr(self, key, val)

        _icons = self.icons
        padding = len(_icons[_if]) + len(_icons[_il])
        if self.width < self._min_width:
            self.width = self._min_width
        self.iwidth = self.width - padding      # internal width

        # configure styles
        _styles = self.styles
        self._first = _styles[_if](_icons[_if])
        self._comp_style = _styles[_ic]
        self._empt_style = _styles[_ie]
        self._last = _styles[_il](_icons[_il])
        self._err_style = _styles[_iel]

        # dynamic label fmt, set to None to disable
        self._start = time.time()

    def __str__(self):
        ''' Renders the current state as a string. '''
        if self._cached_str:
            return self._cached_str

        # shall we clear the line to the left?
        pieces = [self._clear_left if self._clear_left else '']

        if self.label_mode == 'internal':  # solid theme
            pieces.append(self._render_internal_label())
        else:
            pieces.append(self._render())

        self._cached_str = rendered = ''.join(pieces)
        if self.debug:
            pieces.append(
                f' r:{self.ratio:5.2f} ncc:{self._num_complete_chars:2d} '
                f'rm:{self._remainder!r} '
                f'nec:{self._num_empty_chars:2d} '
                f'l:{len_stripped(rendered)}'
            )
            self._cached_str = rendered = ''.join(pieces)  # again :-/
        return rendered

    def __repr__(self):
        return repr(self.__str__())

    def __call__(self, complete):
        ''' Sets the value of the bar graph. '''
        # convert ints to float from 0…1 per-one-tage
        self.ratio = ratio = complete / self.total

        # find num complete and empty chars
        ncc = self._get_ncc(self.iwidth, ratio)  # for overriding
        if ncc < 0:  # restrict from 0 to iwidth
            ncc = self._remainder = 0
        if ncc > self.iwidth:
            ncc = self.iwidth
            self._remainder = 0
        self._num_complete_chars = ncc
        self._num_empty_chars = self.iwidth - ncc

        self._update_status()
        self._cached_str = None  # clear cache
        return self

    def _get_ncc(self, width, ratio):
        ''' Get the number of completed whole characters. '''
        return round(self.iwidth * ratio)

    @property
    def clear_left(self):
        return self._clear_left

    @clear_left.setter
    def clear_left(self, value):
        ''' Converts a given integer to an escape sequence. '''
        if value is True:
            value = 0
        if type(value) is int:
            self._clear_left = f'{clear_line(1)}{sc.mv_x(value)}'
        elif type(value) in (bool, type(None)):
            self._clear_left = value
        else:
            raise TypeError('type %s not valid.' % type(value))

    def _update_status(self):
        ''' Check bounds for errors and update label accordingly. '''
        # figure label
        label = ''
        label_mode = self.label_mode

        # change label fmt based on time - when slow, go to higher-res display
        if self.timedelta:
            delta = time.time() - self._start
            if delta > self.timedelta[1]:
                self.label_fmt = '%5.2f%%'
            elif delta > self.timedelta[0]:
                self.label_fmt = '%4.1f%%'

        ratio = self.ratio
        if 0 <= ratio < 1:  # in progress
            if label_mode:
                label = self.label_fmt % (ratio * 100)
            if self.oob_error:  # now fixed, reset
                self._first = self.styles[_if](self.icons[_if])
                self._last = self.styles[_il](self.icons[_il])
                self._comp_style = self.styles[_ic]
                self.oob_error = False
                self.done = False
        else:
            if ratio == 1:  # done
                self.done = True
                self._comp_style = self.styles[_id]
                self._last = self.styles[_if](self.icons[_il])
                if label_mode:
                    label = self.icons[_id]
                if self.oob_error:  # now fixed, reset
                    self._first = self.styles[_if](self.icons[_if])
                    self.oob_error = False

            # error - out of bounds :-/
            elif ratio > 1:
                self.done = True
                self.oob_error = True
                self._last = self._err_style(self.icons[_ieh])
                if label_mode and not label_mode == 'internal':
                    label = self._err_style(self.icons[_ieb])
            else:  # < 0
                self.oob_error = True
                self._first = self._err_style(self.icons[_iel])
                if label_mode and not label_mode == 'internal':
                    label = self._err_style(self.icons[_ieb])
        self._lbl = label

    def _render(self):
        ''' Standard rendering of bar graph. '''
        cm_chars = self._comp_style(self.icons[_ic] * self._num_complete_chars)
        em_chars = self._empt_style(self.icons[_ie] * self._num_empty_chars)
        return f'{self._first}{cm_chars}{em_chars}{self._last} {self._lbl}'

    def _render_internal_label(self):
        ''' Render with a label inside the bar graph. '''
        ncc = self._num_complete_chars
        bar = self._lbl.center(self.iwidth)
        cm_chars = self._comp_style(bar[:ncc])
        em_chars = self._empt_style(bar[ncc:])
        return f'{self._first}{cm_chars}{em_chars}{self._last}'


class HiDefProgressBar(ProgressBar):
    ''' A ProgressBar with increased, sub-character cell resolution,
        approx 8x.

        Most useful in constrained environments, i.e. a small terminal window.

        Arguments:
            width: 8 or greater
            partial_chars - sequence of characters to show progress
    '''
    icons = icons['segmented']
    min_width = 8
    partial_chars = ('░', '▏', '▎', '▍', '▌', '▋', '▊', '▉')
    partial_chars_len = len(partial_chars)
    # matching bg helps partial char look a bit more natural:
    partial_char_extra_style = bg.i236

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'partial_chars' in kwargs:  # re-calc
            self.partial_chars_len = len(self.partial_chars)

    def _get_ncc(self, width, ratio):
        ''' Get the number of complete chars.

            This one figures the _remainder for the partial char as well.
        '''
        sub_chars = round(width * ratio * self.partial_chars_len)
        ncc, self._remainder = divmod(sub_chars, self.partial_chars_len)
        return ncc

    def _render(self):
        ''' figure partial character '''
        p_char = ''
        if not self.done and self._remainder:
            p_style = self._comp_style
            if self.partial_char_extra_style:
                if p_style is str:
                    p_style = self.partial_char_extra_style
                else:
                    p_style = p_style + self.partial_char_extra_style

            p_char = p_style(self.partial_chars[self._remainder])
            self._num_empty_chars -= 1

        cm_chars = self._comp_style(self.icons[_ic] * self._num_complete_chars)
        em_chars = self._empt_style(self.icons[_ie] * self._num_empty_chars)
        return f'{self._first}{cm_chars}{p_char}{em_chars}{self._last} {self._lbl}'


if __name__ == '__main__':

    import sys

    # set defaults
    ProgressBar.debug = '-d' in sys.argv
    ProgressBar.label_mode = '-l' in sys.argv
    ProgressBar._clear_left = False  # class default

    bars = [
        ('basic, expanded:\n',
                            ProgressBar(theme='basic', expand=True)),
        ('basic clr:',      ProgressBar(theme='basic_color')),
        ('* default:',      ProgressBar()),
        ('shaded:',         ProgressBar(theme='shaded')),
        ('bullets:',        ProgressBar(icons='bullets', style='ocean8')),
        ('warm-shaded:',    ProgressBar(theme='warm_shaded')),
        ('faces:',          ProgressBar(theme='shaded', icons='faces')),
        # ('wide faces:',     ProgressBar(style='simple', icons='wide_faces')),
        ('hvy-metal:',      ProgressBar(theme='heavy_metal')),
        ('segmented:',      ProgressBar(icons='segmented')),
        ('triangles:',      ProgressBar(theme='shaded', icons='triangles')),
        ('solid, expanded:\n',
                            ProgressBar(theme='solid', expand=True)),
        ('solid mono:',     ProgressBar(theme='solid', styles='amber_mono')),

        ('high-def:',       HiDefProgressBar(styles='greyen')),
        ('dies:',           HiDefProgressBar(theme='dies', # clear_left=4,
                                             partial_chars='⚀⚁⚂⚃⚄⚅',
                                             partial_char_extra_style=None)),
    ]

    # print each in progress
    from console.utils import cls
    cls()

    with sc.hidden_cursor():
        try:
            for i in range(0, 101):
                print()
                for label, bar in bars:
                    print(f' {label:12}', bar(i), sep='')

                time.sleep(.1)
                if i != 100:
                    cls()
            time.sleep(2)
        except KeyboardInterrupt:
            pass

    # print each with a number of values
    print()
    for label, bar in bars:

        # reset once
        if bar.done:
            bar.done = False
            bar._comp_style = bar.styles[_ic]
            bar._last = bar.styles[_il](bar.icons[_il])
            bar.label_fmt = ProgressBar.label_fmt

        print(label)
        #~ # for complete in (-2, 0, 51, 100, 150, 84, 100):
        for complete in (-2, 0, 51, 100, 155):
            if bar.expand:
                print(bar(complete))
            else:
                print(' ', bar(complete))
        print()
