
.. raw:: html

    <pre id='logo' class='center'>
    <span style="color:#729fcf">&#9484;───────────────</span><span style="color:#3465a4">────────────&#9488;</span>
    <span style="color:#729fcf">│</span>   <span style="color:#729fcf">&#9487;&#9473;&#9592;&#9487;</span><span style="color:#3465a4">&#9473;&#9491;&#9487;&#9491;&#9595;&#9487;&#9473;&#9491;&#9487;&#9473;&#9491;&#9595;</span>  </span><span style="color:#3465a4">&#9487;&#9473;</span><span style="color:#b4b8b0">&#9592;</span>   <span style="color:#b4b8b0">│</span>
    <span style="color:#3465a4">│</span>   <span style="color:#3465a4">&#9475;</span>  </span><span style="color:#3465a4">&#9475;</span> </span><span style="color:#3465a4">&#9475;&#9475;&#9495;&#9515;&#9495;&#9473;&#9491;</span><span style="color:#b4b8b0">&#9475;</span> </span><span style="color:#b4b8b0">&#9475;&#9475;</span>  <span style="color:#b4b8b0">&#9507;&#9592;</span>    </span><span style="color:#b4b8b0">│</span>
    <span style="color:#3465a4">│</span>   <span style="color:#3465a4">&#9495;&#9473;&#9592;&#9495;</span><span style="color:#b4b8b0">&#9473;&#9499;&#9593;</span> </span><span style="color:#b4b8b0">&#9593;&#9495;&#9473;&#9499;&#9495;&#9473;&#9499;&#9495;&#9473;&#9592;&#9495;&#9473;</span><span style="color:#555">&#9592;</span>   <span style="color:#555">│</span>
    <span style="color:#b4b8b0">&#9492;───────────────</span><span style="color:#555">────────────&#9496;</span>
    </pre>

.. container:: center

    | *"In your satin tights,*
    | *fighting for your rights,*
    | *and the old red, white, and blue…"*
    | *—Wonder Woman theme*

|


Another One, eh 🤔?
=======================

    *"First I was afraid, I was petrified…"—Gloria Gaynor*


.. raw:: html


    <pre class=center>
     ▏
    ⸝<><><>⸜
    <>✶><><><><>
    <><><><><><✦<>
    (<><><><><><><>)
    <><><><><><><>
    .  <>✶><><><><> .
    : .   `<><><>´    .:
     ::            .      ⭒:
    .⭒.      .       .     .:.
    .:.      .         ⭒     : .
    .: :     :          .      ::.
    .:  :     ⭒           .:     .⭒ :
    :⭒. :      .              :      : ..
    . .                         .      .  .
    </pre>



Background
---------------

    *"CHARLIE DON'T SURF!"—Lt. Col. Kilgore*

So ANSI escape codes for terminals have been standard on UNIX
with the belt-and-suspenders crowd since the late seventies,
and even saw use on DOS, VMS, the Amiga, and BBSs back in the day.
With the advent of macOS,
a whole new generation of lumber-sexuals have exposed *themselves(?)*
to the terminal environment/command-line shells…
*and liked it*.
 🤔

.. figure:: _static/dilbert_95-06-24.png
    :align: center
    :figwidth: 80%
    :class: o8

    Dilbert, desde `1995-06-24 <https://dilbert.com/strip/1995-06-24>`_


"I'm a PC"
~~~~~~~~~~~~~~

    *“Oooh! Oooh! Oooh!”—Arnold Horshack*\
    `† <https://www.vulture.com/2012/08/why-welcome-back-kotters-horshack-mattered.html>`_

.. figure:: _static/mac_pc.jpg
    :align: right
    :figwidth: 40%
    :class: o8


Not on Windows NT, though.  Big nopity-nope in that department—\
negatory.

Amazingly,
with recent versions of Windows 10
the Ballmer/Suit barrier was finally breached,
allowing *multi-decade-late*
`improvements
<https://devblogs.microsoft.com/commandline/windows-10-creators-update-whats-new-in-bashwsl-windows-console/>`_
to be made to its until-now pathetic "console."
Often still known as the "DOS Prompt" since it has been frozen that long.
Vaguely analogous to today's virtual terminals,
as an AMC Gremlin, Pacer, or Ford Pinto might compare to a BMW.
But now, it's supercharged with VT power.
But, don't bother with it, it's kind of a waste of time.

Huh, why?
Well,
now that `Windows Terminal <https://en.wikipedia.org/wiki/Windows_Terminal>`_
exists, I'd recommend that instead 1000%.
Even though not currently complete,
it is getting there quickly and much better than a "souped up Yugo."

So, now all the top/extant computing platforms support ANSI escape sequences,
again!
What's old is new… err, again.
Add in Unicode, hyperlinks,
and millions of colors and it's now better than ever.

We need great command-line/TUI tools and that's where ``console`` fits in.

.. container:: center

    *That's the way, uhh huh, uhh huh, I like it…*

.. figure:: _static/kc3.png
    :align: center
    :figwidth: 60%

    (Cue
    `KC and the Sunshine Band,
    <https://www.youtube.com/watch?v=R9DjX6JBpHI>`_
    *uhh-huh, uhh-huh*
    on
    Soul Train…)


Batteries Not Included
------------------------

    *"What'chu talkin' 'bout, Willis?"—Arnold Jackson*

In the Python world,
there hasn't been easy-to-use support for terminal sequences in the standard
library,
beyond curses and termios
(which mildly overlap in functionality with this package and themselves).

Those are low-level interfaces however,
focused on "full screen" terminal apps and tty control respectively,
while continuing to abstract hardware that now only exists in
`museums. <https://en.wikipedia.org/wiki/List_of_computer_museums>`_

The ANSI standard may have won,
but styling a text snippet here and there or setting a title without a bunch
of ugly C-style function calls was thought too…
trivial perhaps?

.. rubric:: Terminfo?

.. figure:: _static/logan_unacceptable.jpg
    :align: right
    :figwidth: 60%


Besides the difficulty factor mentioned,
this classic answer to this problem also suffers in that it is:

- Not available or installed on Windows

- Not up to date on older OS variants

- Not up to date with capability support, i.e. lags the real world:

    - Tons of obsolete capabilities *are* supported, crowding the docs

    - "True color," lagged for almost a decade (though now has some support)

    - Extended xterm capabilities not supported

    - Many terminals claim xterm support but aren't completely compatible

    - New or experimental capabilities are *not* supported, eg:

        - Bracketed paste
        - Clipboard
        - Curly/colored underlines
        - Hyper-links

      (And the maintainers have been resistant to add them. :-/)

Turns out that terminfo is a big pain in the butt and not even a full solution
for all the trouble.
The console package has implemented support however,
although it is new.
Set the environment variable, ``PY_CONSOLE_USE_TERMINFO=1`` to try it out.

However, generally the standard detection should work fine on common terminal
emulators.
console will default to using terminfo if it sees that the terminal is remote
via an SSH connection,
or if the above environment variable has been set.


Meanwhile, over at the Cheeseshop…
------------------------------------

    *"Not much of a cheese shop really, is it?"—Monty Python*

And so, now there are ad-hoc ANSI codes being generated in every command-line
app and eleventy micro-libs on "the" PyPI doing the same.
Looks to be a fun exercise and somewhat of a rite of passage to create one.

(On that note:  Good luck finding an appropriate name on PyPI for yours—Taken!)

.. raw:: html

    <div class="center rounded p1 dark">
    <span class=dots>·····•·····</span>&nbsp;&nbsp;
    <i>
    <span id=bas>ᗣ</span><span id=pok>ᗣ</span>
    <span id=sha>ᗣ</span><span id=spe>ᗣ</span>&nbsp;
    <span id=pac>ᗧ</span></i>&nbsp;&nbsp;
    <span class=dots>·····•·····</span>&nbsp;&nbsp;&nbsp;<br>

    <i style="opacity: .7">waka waka waka</i>&nbsp;&nbsp;&nbsp;
    </div>


Often Missing
~~~~~~~~~~~~~~~

    *"Them Dukes! Them Dukes…"—Sheriff Rosco P. Coltrane*

While many of the ANSI modules in the cheeseshop have plenty going for them in
areas of focus,
they generally aren't very comprehensive──\
usually providing 8 colors
and a few styles/effects like bold and underline.

.. figure:: _static/irac_05.jpg
    :align: right
    :figwidth: 50%


Unfortunately,
one or more important items are often missing:

    - Styles, cursor movements, clearing the screen,
      setting titles, hyperlinks, full-screen, etc.

    - Multiple Palettes:

      - 8 color - always
      - 16 color - sometimes
      - 256 extended color - rare
      - Nearest 8-bit color - rarer
      - 16M color - rarer
      - Standard color names, like X11 & Webcolors - rarest/None

    - Querying the terminal, auto-detection, support and deactivation.
    - Python3 support/still maintained
    - Have tests


Nice to haves
~~~~~~~~~~~~~~~~~

    | *"You've got to, know when to hold 'em… know when to fold 'em…"*
    | *—Kenny Rogers*

Most are relatively easy to use,
but may still miss one of these nice to haves:

    - Composable objects
    - Concise names

        - Avoidance of capital, mixed, or camel-case names on instances.
        - Avoidance of extra punctuation, parens, brackets, quotes, etc.

    - Nearest neighbor downgrade for unsupported palettes.
    - Progress Bars
    - Hyperlinks


Result: The Console Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/irac_01.jpg
    :align: center
    :figwidth: 80%

    Diana @ The IRAC-Z Console


Looking over at PyPI with the criteria above finds many interesting pieces but
far from the full Monty.
So, had some fun building my own of course.
Looked at and picked out a few design cues from several of these:

.. hlist::
    :columns: 2

    - ansi
    - ansicolors
    - blessed
    - `blessings <https://pypi.org/project/blessings/>`_ (context managers)
    - click.style and utilities (reminded me of pause)
    - colorama.ansi (palette collection objects)
    - `colorful <https://tuxtimo.me/posts/colorful-python>`_
        (why terminfo is a bust)
    - colorize
    - escape
    - fabric.colors
    - kolors
    - pycolor
    - pygments (nearest indexed color)
    - style
    - termcolor
    - ptpython, urwid
    - rich - text
    - tqdm - progress

etc.
Have thought about doing a widget library as well,
but feels like it should be another package layered on top.
