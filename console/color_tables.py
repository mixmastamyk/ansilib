'''
    .. console - Comprehensive utility library for ANSI terminals.
    .. © 2018, Mike Miller - Released under the LGPL, version 3+.

    Tables for ANSI color palettes.
'''

x11_color_map = {}  # loaded from disk, name: (r, g, b)

# 256 color table for finding rgb values for indexes, useful for clr downgrade:
index_to_rgb8 = {
      '0': (0, 0, 0),
      '1': (128, 0, 0),
      '2': (0, 128, 0),
      '3': (128, 128, 0),
      '4': (0, 0, 128),
      '5': (128, 0, 128),
      '6': (0, 128, 128),
      '7': (192, 192, 192),
      '8': (128, 128, 128),
      '9': (255, 0, 0),
     '10': (0, 255, 0),
     '11': (255, 255, 0),
     '12': (0, 0, 255),
     '13': (255, 0, 255),
     '14': (0, 255, 255),
     '15': (255, 255, 255),
     '16': (0, 0, 0),
     '17': (0, 0, 95),
     '18': (0, 0, 135),
     '19': (0, 0, 175),
     '20': (0, 0, 215),
     '21': (0, 0, 255),
     '22': (0, 95, 0),
     '23': (0, 95, 95),
     '24': (0, 95, 135),
     '25': (0, 95, 175),
     '26': (0, 95, 215),
     '27': (0, 95, 255),
     '28': (0, 135, 0),
     '29': (0, 135, 95),
     '30': (0, 135, 135),
     '31': (0, 135, 175),
     '32': (0, 135, 215),
     '33': (0, 135, 255),
     '34': (0, 175, 0),
     '35': (0, 175, 95),
     '36': (0, 175, 135),
     '37': (0, 175, 175),
     '38': (0, 175, 215),
     '39': (0, 175, 255),
     '40': (0, 215, 0),
     '41': (0, 215, 95),
     '42': (0, 215, 135),
     '43': (0, 215, 175),
     '44': (0, 215, 215),
     '45': (0, 215, 255),
     '46': (0, 255, 0),
     '47': (0, 255, 95),
     '48': (0, 255, 135),
     '49': (0, 255, 175),
     '50': (0, 255, 215),
     '51': (0, 255, 255),
     '52': (95, 0, 0),
     '53': (95, 0, 95),
     '54': (95, 0, 135),
     '55': (95, 0, 175),
     '56': (95, 0, 215),
     '57': (95, 0, 255),
     '58': (95, 95, 0),
     '59': (95, 95, 95),
     '60': (95, 95, 135),
     '61': (95, 95, 175),
     '62': (95, 95, 215),
     '63': (95, 95, 255),
     '64': (95, 135, 0),
     '65': (95, 135, 95),
     '66': (95, 135, 135),
     '67': (95, 135, 175),
     '68': (95, 135, 215),
     '69': (95, 135, 255),
     '70': (95, 175, 0),
     '71': (95, 175, 95),
     '72': (95, 175, 135),
     '73': (95, 175, 175),
     '74': (95, 175, 215),
     '75': (95, 175, 255),
     '76': (95, 215, 0),
     '77': (95, 215, 95),
     '78': (95, 215, 135),
     '79': (95, 215, 175),
     '80': (95, 215, 215),
     '81': (95, 215, 255),
     '82': (95, 255, 0),
     '83': (95, 255, 95),
     '84': (95, 255, 135),
     '85': (95, 255, 175),
     '86': (95, 255, 215),
     '87': (95, 255, 255),
     '88': (135, 0, 0),
     '89': (135, 0, 95),
     '90': (135, 0, 135),
     '91': (135, 0, 175),
     '92': (135, 0, 215),
     '93': (135, 0, 255),
     '94': (135, 95, 0),
     '95': (135, 95, 95),
     '96': (135, 95, 135),
     '97': (135, 95, 175),
     '98': (135, 95, 215),
     '99': (135, 95, 255),
    '100': (135, 135, 0),
    '101': (135, 135, 95),
    '102': (135, 135, 135),
    '103': (135, 135, 175),
    '104': (135, 135, 215),
    '105': (135, 135, 255),
    '106': (135, 175, 0),
    '107': (135, 175, 95),
    '108': (135, 175, 135),
    '109': (135, 175, 175),
    '110': (135, 175, 215),
    '111': (135, 175, 255),
    '112': (135, 215, 0),
    '113': (135, 215, 95),
    '114': (135, 215, 135),
    '115': (135, 215, 175),
    '116': (135, 215, 215),
    '117': (135, 215, 255),
    '118': (135, 255, 0),
    '119': (135, 255, 95),
    '120': (135, 255, 135),
    '121': (135, 255, 175),
    '122': (135, 255, 215),
    '123': (135, 255, 255),
    '124': (175, 0, 0),
    '125': (175, 0, 95),
    '126': (175, 0, 135),
    '127': (175, 0, 175),
    '128': (175, 0, 215),
    '129': (175, 0, 255),
    '130': (175, 95, 0),
    '131': (175, 95, 95),
    '132': (175, 95, 135),
    '133': (175, 95, 175),
    '134': (175, 95, 215),
    '135': (175, 95, 255),
    '136': (175, 135, 0),
    '137': (175, 135, 95),
    '138': (175, 135, 135),
    '139': (175, 135, 175),
    '140': (175, 135, 215),
    '141': (175, 135, 255),
    '142': (175, 175, 0),
    '143': (175, 175, 95),
    '144': (175, 175, 135),
    '145': (175, 175, 175),
    '146': (175, 175, 215),
    '147': (175, 175, 255),
    '148': (175, 215, 0),
    '149': (175, 215, 95),
    '150': (175, 215, 135),
    '151': (175, 215, 175),
    '152': (175, 215, 215),
    '153': (175, 215, 255),
    '154': (175, 255, 0),
    '155': (175, 255, 95),
    '156': (175, 255, 135),
    '157': (175, 255, 175),
    '158': (175, 255, 215),
    '159': (175, 255, 255),
    '160': (215, 0, 0),
    '161': (215, 0, 95),
    '162': (215, 0, 135),
    '163': (215, 0, 175),
    '164': (215, 0, 215),
    '165': (215, 0, 255),
    '166': (215, 95, 0),
    '167': (215, 95, 95),
    '168': (215, 95, 135),
    '169': (215, 95, 175),
    '170': (215, 95, 215),
    '171': (215, 95, 255),
    '172': (215, 135, 0),
    '173': (215, 135, 95),
    '174': (215, 135, 135),
    '175': (215, 135, 175),
    '176': (215, 135, 215),
    '177': (215, 135, 255),
    '178': (215, 175, 0),
    '179': (215, 175, 95),
    '180': (215, 175, 135),
    '181': (215, 175, 175),
    '182': (215, 175, 215),
    '183': (215, 175, 255),
    '184': (215, 215, 0),
    '185': (215, 215, 95),
    '186': (215, 215, 135),
    '187': (215, 215, 175),
    '188': (215, 215, 215),
    '189': (215, 215, 255),
    '190': (215, 255, 0),
    '191': (215, 255, 95),
    '192': (215, 255, 135),
    '193': (215, 255, 175),
    '194': (215, 255, 215),
    '195': (215, 255, 255),
    '196': (255, 0, 0),
    '197': (255, 0, 95),
    '198': (255, 0, 135),
    '199': (255, 0, 175),
    '200': (255, 0, 215),
    '201': (255, 0, 255),
    '202': (255, 95, 0),
    '203': (255, 95, 95),
    '204': (255, 95, 135),
    '205': (255, 95, 175),
    '206': (255, 95, 215),
    '207': (255, 95, 255),
    '208': (255, 135, 0),
    '209': (255, 135, 95),
    '210': (255, 135, 135),
    '211': (255, 135, 175),
    '212': (255, 135, 215),
    '213': (255, 135, 255),
    '214': (255, 175, 0),
    '215': (255, 175, 95),
    '216': (255, 175, 135),
    '217': (255, 175, 175),
    '218': (255, 175, 215),
    '219': (255, 175, 255),
    '220': (255, 215, 0),
    '221': (255, 215, 95),
    '222': (255, 215, 135),
    '223': (255, 215, 175),
    '224': (255, 215, 215),
    '225': (255, 215, 255),
    '226': (255, 255, 0),
    '227': (255, 255, 95),
    '228': (255, 255, 135),
    '229': (255, 255, 175),
    '230': (255, 255, 215),
    '231': (255, 255, 255),
    '232': (8, 8, 8),
    '233': (18, 18, 18),
    '234': (28, 28, 28),
    '235': (38, 38, 38),
    '236': (48, 48, 48),
    '237': (58, 58, 58),
    '238': (68, 68, 68),
    '239': (78, 78, 78),
    '240': (88, 88, 88),
    '241': (98, 98, 98),
    '242': (108, 108, 108),
    '243': (118, 118, 118),
    '244': (128, 128, 128),
    '245': (138, 138, 138),
    '246': (148, 148, 148),
    '247': (158, 158, 158),
    '248': (168, 168, 168),
    '249': (178, 178, 178),
    '250': (188, 188, 188),
    '251': (198, 198, 198),
    '252': (208, 208, 208),
    '253': (218, 218, 218),
    '254': (228, 228, 228),
    '255': (238, 238, 238),
}

# colors 0..15: 16 basic colors
# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
cmd_palette4 = (
    (0, 0, 0),          # 0     black
    (128, 0, 0),        # 1     red
    (0, 128, 0),        # 2     green
    (128, 128, 0),      # 3     yellow
    (0, 0, 128),        # 4     blue
    (128, 0, 128),      # 5     magenta/purple
    (0, 128, 128),      # 6     cyan
    (192, 192, 192),    # 7     white/grey

    (128, 128, 128),    # 8     bright black
    (255, 0, 0),        # 9     bright red
    (0, 255, 0),        # 10    bright green
    (255, 255, 0),      # 11    bright yellow
    (0, 0, 255),        # 12    bright blue
    (255, 0, 255),      # 13    bright magenta
    (0, 255, 255),      # 14    bright cyan
    (255, 255, 255),    # 15    bright white
)

# New palette, 1709, Fall Creators Update, 2017-10-17, build 16299
# https://blogs.msdn.microsoft.com/commandline/2017/08/02/updating-the-windows-console-colors/
cmd1709_palette4 = (
    (12, 12, 12),       # 0     black
    (197, 15, 31),      # 1     red
    (19, 161, 14),      # 2     green
    (193, 156, 0),      # 3     yellow
    (0, 55, 218),       # 4     blue
    (136, 23, 152),     # 5     magenta/purple
    (58, 150, 221),     # 6     cyan
    (204, 204, 204),    # 7     white/grey

    (118, 118, 118),    # 8     bright black
    (231, 72, 86),      # 9     bright red
    (22, 198, 12),      # 10    bright green
    (249, 241, 165),    # 11    bright yellow
    (59, 120, 255),     # 12    bright blue
    (180, 0, 158),      # 13    bright magenta
    (97, 214, 214),     # 14    bright cyan
    (242, 242, 242),    # 15    bright white
)

linuxcon_palette4 = (   # ubuntu config from: /etc/vtrgb
    (1, 1, 1),          # 0     black
    (222, 56, 43),      # 1     red
    (57, 181, 74),      # 2     green
    (255, 199, 6),      # 3     yellow
    (0, 111, 184),      # 4     blue
    (118, 38, 113),     # 5     magenta/purple
    (44, 181, 233),     # 6     cyan
    (204, 204, 204),    # 7     white/grey

    (128, 128, 128),    # 8     bright black
    (255, 0, 0),        # 9     bright red
    (0, 255, 0),        # 10    bright green
    (255, 255, 0),      # 11    bright yellow
    (0, 0, 255),        # 12    bright blue
    (255, 0, 255),      # 13    bright magenta
    (0, 255, 255),      # 14    bright cyan
    (255, 255, 255),    # 15    bright white
)

# https://en.wikipedia.org/wiki/Tango_Desktop_Project#Palette
# https://blogs.n1zyy.com/andrew/2009/02/02/tango-color-scheme-for-xfce-terminal/
tango_palette4 = (
    (0x2e, 0x34, 0x34), # 0     black
    (0xcc, 0x00, 0x00), # 1     red
    (0x4e, 0x9a, 0x06), # 2     green
    (0xc4, 0xa0, 0x00), # 3     yellow
    (0x34, 0x65, 0xa4), # 4     blue
    (0x75, 0x50, 0x7b), # 5     magenta/purple
    (0x06, 0x98, 0x9a), # 6     cyan
    (0xd3, 0xd7, 0xcf), # 7     white/grey

    (0x55, 0x57, 0x53), # 8     bright black
    (0xef, 0x29, 0x29), # 9     bright red
    (0x8a, 0xe2, 0x34), # 10    bright green
    (0xfc, 0xe9, 0x4f), # 11    bright yellow
    (0x72, 0x9f, 0xcf), # 12    bright blue
    (0xad, 0x7f, 0xa8), # 13    bright magenta
    (0x34, 0xe2, 0xe2), # 14    bright cyan
    (0xee, 0xee, 0xec), # 15    bright white
)

solarized_dark_palette4 = (
    (0x07, 0x36, 0x42), # 0     black
    (0xDC, 0x32, 0x2F), # 1     red
    (0x85, 0x99, 0x00), # 2     green
    (0xB5, 0x89, 0x00), # 3     yellow
    (0x26, 0x8B, 0xD2), # 4     blue
    (0xD3, 0x36, 0x82), # 5     magenta/purple
    (0x2A, 0xA1, 0x98), # 6     cyan
    (0xEE, 0xE8, 0xD5), # 7     white/grey

    (0x00, 0x2B, 0x36), # 8     bright black
    (0xCB, 0x4B, 0x16), # 9     bright red),
    (0x58, 0x6E, 0x75), # 10    bright green),
    (0x65, 0x7B, 0x83), # 11    bright yellow),
    (0x83, 0x94, 0x96), # 12    bright blue),
    (0x6C, 0x71, 0xC4), # 13    bright magenta),
    (0x93, 0xA1, 0xA1), # 14    bright cyan),
    (0xFD, 0xF6, 0xE3), # 15    bright white),
)

termapp_palette4 = (
    (0, 0, 0),          # 0     black
    (194, 54, 33),      # 1     red
    (37, 188, 36),      # 2     green
    (173, 173, 39),     # 3     yellow
    (73, 46, 225),      # 4     blue
    (211, 56, 211),     # 5     magenta/purple
    (51, 187, 200),     # 6     cyan
    (203, 204, 205),    # 7     white/grey

    (129, 131, 131),    # 8     bright black
    (252, 57, 31),      # 9     bright red
    (49, 231, 34),      # 10    bright green
    (234, 236, 35),     # 11    bright yellow
    (88, 51, 255),      # 12    bright blue
    (249, 53, 248),     # 13    bright magenta
    (20, 240, 240),     # 14    bright cyan
    (233, 235, 235),    # 15    bright white
)

iterm_palette4 = (
    (0, 0, 0),          # 0     black
    (201, 27, 0),       # 1     red
    (0, 194, 0),        # 2     green
    (199, 196, 0),      # 3     yellow
    (2, 37, 199),       # 4     blue
    (201, 48, 199),     # 5     magenta/purple
    (0, 197, 199),      # 6     cyan
    (199, 199, 199),    # 7     white/grey

    (103, 103, 103),    # 8     bright black
    (255, 109, 103),    # 9     bright red
    (95, 249, 103),     # 10    bright green
    (254, 251, 103),    # 11    bright yellow
    (104, 113, 255),    # 12    bright blue
    (255, 118, 255),    # 13    bright magenta
    (95, 253, 255),     # 14    bright cyan
    (255, 255, 254),    # 15    bright white
)

vga_palette4 = (
    (0, 0, 0),          # 0     black
    (170, 0, 0),        # 1     red
    (0, 170, 0),        # 2     green
    (170, 85, 0),       # 3     yellow
    (0, 0, 170),        # 4     blue
    (170, 0, 170),      # 5     magenta/purple
    (0, 170, 170),      # 6     cyan
    (170, 170, 170),    # 7     white/grey

    (85, 85, 85),       # 8     bright black
    (255, 85, 85),      # 9     bright red
    (85, 255, 85),      # 10    bright green
    (255, 255, 85),     # 11    bright yellow
    (85, 85, 255),      # 12    bright blue
    (255, 85, 255),     # 13    bright magenta
    (85, 255, 255),     # 14    bright cyan
    (255, 255, 255),    # 15    bright white
)

xterm_palette4 = (
    (0x00, 0x00, 0x00),  # 0     black
    (0xcd, 0x00, 0x00),  # 1     red
    (0x00, 0xcd, 0x00),  # 2     green
    (0xcd, 0xcd, 0x00),  # 3     yellow
    (0x00, 0x00, 0xee),  # 4     blue
    (0xcd, 0x00, 0xcd),  # 5     magenta/purple
    (0x00, 0xcd, 0xcd),  # 6     cyan
    (0xe5, 0xe5, 0xe5),  # 7     white/grey

    (0x7f, 0x7f, 0x7f),  # 8     bright black
    (0xff, 0x00, 0x00),  # 9     bright red
    (0x00, 0xff, 0x00),  # 10    bright green
    (0xff, 0xff, 0x00),  # 11    bright yellow
    (0x5c, 0x5c, 0xff),  # 12    bright blue
    (0xff, 0x00, 0xff),  # 13    bright magenta
    (0x00, 0xff, 0xff),  # 14    bright cyan
    (0xff, 0xff, 0xff),  # 15    bright white
)

_new_palette4 = (
    (),   # 0     black
    (),   # 1     red
    (),   # 2     green
    (),   # 3     yellow
    (),   # 4     blue
    (),   # 5     magenta/purple
    (),   # 6     cyan
    (),   # 7     white/grey

    (),   # 8     bright black
    (),   # 9     bright red
    (),   # 10    bright green
    (),   # 11    bright yellow
    (),   # 12    bright blue
    (),   # 13    bright magenta
    (),   # 14    bright cyan
    (),   # 15    bright white
)
