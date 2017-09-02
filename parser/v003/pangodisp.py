#!/usr/bin/env python

import sys, os, re
import pygtk, gobject, gtk
import pango
        
gray50_width  = 2
gray50_height = 2
gray50_bits   = '\x02\x01'
GTKLOGO_IMAGE = os.path.join(os.path.dirname(__file__),
                             'images', 'gtk-logo-rgb.gif')
FLOPPYBUDDY_IMAGE = os.path.join(os.path.dirname(__file__),
                                 'images', 'floppybuddy.gif')

# XPM data of Open-File icon
xpm_data = [
"16 16 3 1",
"       c None",
".      c #000000000000",
"X      c #FFFFFFFFFFFF",
"                ",
"   ......       ",
"   .XXX.X.      ",
"   .XXX.XX.     ",
"   .XXX.XXX.    ",
"   .XXX.....    ",
"   ..XXXXX..    ",
"   .X.XXX.X.    ",
"   .XX.X.XX.    ",
"   .XXX.XXX.    ",
"   .XX.X.XX.    ",
"   .X.XXX.X.    ",
"   ..XXXXX..    ",
"   .........    ",
"                ",
"                "
]

class PangoView(gtk.Window):
    def __init__(self, parent=None):
        # Create the toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        #self.set_border_width(0)

        self.set_default_size(800, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        #self.set_title("Pango test display");

        vpaned = gtk.VPaned()
        vpaned.set_border_width(5)
        self.add(vpaned)

        # For convenience, we just use the autocreated buffer from
        # the first text view; you could also create the buffer
        # by itself with gtk.text_buffer_new(), then later create
        # a view widget.

        view1 = gtk.TextView();
        self.buffer_1 = view1.get_buffer()
        #view2 = gtk.TextView(buffer_1)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        vpaned.add1(sw)

        sw.add(view1)

        #sw2 = gtk.ScrolledWindow()
        #sw2.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #vpaned.add2(sw2)+
        #sw2.add(view2)

        #self.create_tags(self.buffer_1)
        #self.insert_text(buffer_1)

        # get start of buffer; each insertion will revalidate the           
        # iterator to point to just after the inserted text.
        self.iter = self.buffer_1.get_iter_at_offset(0)

        #self.attach_widgets(view1)
        #self.attach_widgets(view2)
        #self.win = None
        self.show_all()

    # we manipulete the buffer through thise functions:
    def add_text(self, text):
        self.buffer_1.insert(self.iter, text)

    def add_text_tag(self, text, tags):
        #if tags == "":
        #    self.add_text(text)
        #else:
            self.buffer_1.insert_with_tags_by_name(self.iter, text, tags)

    def add_text_xtag(self, text, tags):        
        self.buffer_1.get_tag_table().add(tags)
        self.buffer_1.insert_with_tags(self.iter, text, tags)

    def create_tags(self, text_buffer):
        '''
        Create a bunch of tags. Note that it's also possible to
        create tags with gtk.text_tag_new() then add them to the
        tag table for the buffer, text_buffer.create_tag() is
        just a convenience function. Also note that you don't have
        to give tags a name; pass None for the name to create an
        anonymous tag.

        In any real app, another useful optimization would be to create
        a GtkTextTagTable in advance, and reuse the same tag table for
        all the buffers with the same tag set, instead of creating
        new copies of the same tags for every buffer.

        Tags are assigned default priorities in order of addition to the
        tag table. That is, tags created later that affect the same text
        property affected by an earlier tag will override the earlier
        tag. You can modify tag priorities with
        gtk.text_tag_set_priority().
        '''

        text_buffer.create_tag("heading",
                    weight=pango.WEIGHT_BOLD,
                    size=15 * pango.SCALE)

        text_buffer.create_tag("italic", style=pango.STYLE_ITALIC)

        text_buffer.create_tag("bold", weight=pango.WEIGHT_BOLD)

        text_buffer.create_tag("italicbold", weight=pango.WEIGHT_BOLD ,\
                            style=pango.STYLE_ITALIC)

                                # points times the pango.SCALE factor
        text_buffer.create_tag("big", size=20 * pango.SCALE)

        text_buffer.create_tag("xx-small", scale=pango.SCALE_XX_SMALL)

        text_buffer.create_tag("x-large", scale=pango.SCALE_X_LARGE)
        text_buffer.create_tag("large", scale=pango.SCALE_LARGE)

        text_buffer.create_tag("monospace", family="monospace")

        text_buffer.create_tag("green_foreground", foreground="green")
        text_buffer.create_tag("blue_foreground", foreground="blue")
        text_buffer.create_tag("red_foreground", foreground="red")

        text_buffer.create_tag("red_background", background="red")
        text_buffer.create_tag("blue_background", background="blue")
        text_buffer.create_tag("green_background", background="green")
    
        stipple = gtk.gdk.bitmap_create_from_data(None,
            gray50_bits, gray50_width, gray50_height)

        text_buffer.create_tag("background_stipple", background_stipple=stipple)

        text_buffer.create_tag("foreground_stipple", foreground_stipple=stipple)

        text_buffer.create_tag("big_gap_before_line", pixels_above_lines=30)

        text_buffer.create_tag("big_gap_after_line", pixels_below_lines=30)

        text_buffer.create_tag("double_spaced_line", pixels_inside_wrap=10)

        text_buffer.create_tag("not_editable", editable=False)

        text_buffer.create_tag("word_wrap", wrap_mode=gtk.WRAP_WORD)

        text_buffer.create_tag("char_wrap", wrap_mode=gtk.WRAP_CHAR)

        text_buffer.create_tag("no_wrap", wrap_mode=gtk.WRAP_NONE)

        text_buffer.create_tag("center", justification=gtk.JUSTIFY_CENTER)

        text_buffer.create_tag("right_justify", justification=gtk.JUSTIFY_RIGHT)

        text_buffer.create_tag("wide_margins",
                    left_margin=50, right_margin=50)

        text_buffer.create_tag("strikethrough", strikethrough=True)

        text_buffer.create_tag("underline",
                    underline=pango.UNDERLINE_SINGLE)

        text_buffer.create_tag("double_underline",
                    underline=pango.UNDERLINE_DOUBLE)

        text_buffer.create_tag("superscript",
                    rise=10 * pango.SCALE,      # 10 pixels
                    size=8 * pango.SCALE)       #  8 points

        text_buffer.create_tag("subscript",
                    rise=-10 * pango.SCALE,     # 10 pixels
                    size=8 * pango.SCALE)       #  8 points

        text_buffer.create_tag("rtl_quote",
                    wrap_mode=gtk.WRAP_WORD, direction=gtk.TEXT_DIR_RTL,
                    indent=30, left_margin=20, right_margin=20)

    def insert_text(self, text_buffer):
        return
        # use the current directory for the file
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file(GTKLOGO_IMAGE)
        except gobject.GError, error:
            #sys.exit("Failed to load image file gtk-logo-rgb.gif\n")
            pixbuf = gtk.gdk.pixbuf_new_from_xpm_data(xpm_data)
            pass

        scaled = pixbuf.scale_simple(32, 32, 'bilinear')
        pixbuf = scaled

        # get start of buffer; each insertion will revalidate the
        # iterator to point to just after the inserted text.
        iter = text_buffer.get_iter_at_offset(0)

        text_buffer.insert(iter, "The text widget can display text with "
            "all kinds of nifty attributes. It also supports multiple views "
            "of the same buffer; this demo is showing the same buffer in "
            "two places.\n\n")

        text_buffer.insert_with_tags_by_name(iter, "Font styles. ", "heading")

        text_buffer.insert(iter, "For example, you can have ")
        text_buffer.insert_with_tags_by_name(iter,
                            "italic", "italic")
        text_buffer.insert(iter, ", ");
        text_buffer.insert_with_tags_by_name(iter,
                            "bold", "bold")
        text_buffer.insert(iter, ", or ", -1)
        text_buffer.insert_with_tags_by_name(iter,
                            "monospace(typewriter)", "monospace")
        text_buffer.insert(iter, ", or ")
        text_buffer.insert_with_tags_by_name(iter,
                            "big", "big")
        text_buffer.insert(iter, " text. ")
        text_buffer.insert(iter, "It's best not to hardcode specific text "
            "sizes; you can use relative sizes as with CSS, such as ")
        text_buffer.insert_with_tags_by_name(iter,
                            "xx-small", "xx-small")
        text_buffer.insert(iter, " or ")
        text_buffer.insert_with_tags_by_name(iter,
                            "x-large", "x-large")
        text_buffer.insert(iter, " to ensure that your program properly "
            "adapts if the user changes the default font size.\n\n")

        text_buffer.insert_with_tags_by_name(iter, "Colors. ", "heading")

        text_buffer.insert(iter, "Colors such as ");
        text_buffer.insert_with_tags_by_name(iter,
                            "a blue foreground", "blue_foreground")
        text_buffer.insert(iter, " or ");
        text_buffer.insert_with_tags_by_name(iter,
                            "a red background",
                            "red_background")
        text_buffer.insert(iter, " or even ", -1);
        text_buffer.insert_with_tags_by_name(iter,
                            "a stippled red background",
                            "red_background",
                            "background_stipple")

        text_buffer.insert(iter, " or ", -1);
        text_buffer.insert_with_tags_by_name(iter,
                            "a stippled blue foreground on solid red background",
                            "blue_foreground",
                            "red_background",
                            "foreground_stipple")
        text_buffer.insert(iter, "(select that to read it) can be used.\n\n", -1);

        text_buffer.insert_with_tags_by_name(iter,
            "Underline, strikethrough, and rise. ", "heading")

        text_buffer.insert_with_tags_by_name(iter,
                            "Strikethrough",
                            "strikethrough")
        text_buffer.insert(iter, ", ", -1)
        text_buffer.insert_with_tags_by_name(iter,
                            "underline",
                            "underline")
        text_buffer.insert(iter, ", ", -1)
        text_buffer.insert_with_tags_by_name(iter,
                            "double underline",
                            "double_underline")
        text_buffer.insert(iter, ", ", -1)
        text_buffer.insert_with_tags_by_name(iter,
                            "superscript",
                            "superscript")
        text_buffer.insert(iter, ", and ", -1)
        text_buffer.insert_with_tags_by_name(iter,
                            "subscript",
                            "subscript")
        text_buffer.insert(iter, " are all supported.\n\n", -1)

        text_buffer.insert_with_tags_by_name(iter, "Images. ",
                            "heading")

        #text_buffer.insert(iter, "The buffer can have images in it: ", -1)
        #text_buffer.insert_pixbuf(iter, pixbuf)
        #text_buffer.insert_pixbuf(iter, pixbuf)
        #text_buffer.insert_pixbuf(iter, pixbuf)
        #text_buffer.insert(iter, " for example.\n\n", -1)

        text_buffer.insert_with_tags_by_name(iter, "Spacing. ",
                            "heading")

        text_buffer.insert(iter,
            "You can adjust the amount of space before each line.\n", -1)

        text_buffer.insert_with_tags_by_name(iter,
            "This line has a whole lot of space before it.\n",
            "big_gap_before_line", "wide_margins")
        text_buffer.insert_with_tags_by_name(iter,
            "You can also adjust the amount of space after each line; "
            "this line has a whole lot of space after it.\n",
            "big_gap_after_line", "wide_margins")

        text_buffer.insert_with_tags_by_name(iter,
            "You can also adjust the amount of space between wrapped "
            "lines; this line has extra space between each wrapped line "
            "in the same paragraph. To show off wrapping, some filler "
            "text: the quick brown fox jumped over the lazy dog. Blah "
            "blah blah blah blah blah blah blah blah.\n",
            "double_spaced_line", "wide_margins")

        text_buffer.insert(iter, "Also note that those lines have "
            "extra-wide margins.\n\n", -1)

        text_buffer.insert_with_tags_by_name(iter, "Editability. ", "heading")

        text_buffer.insert_with_tags_by_name(iter,
            "This line is 'locked down' and can't be edited by the "
            "user - just try it! You can't delete this line.\n\n",
            "not_editable")

        text_buffer.insert_with_tags_by_name(iter, "Wrapping. ", "heading")

        text_buffer.insert(iter,
            "This line(and most of the others in this buffer) is "
            "word-wrapped, using the proper Unicode algorithm. Word "
            "wrap should work in all scripts and languages that GTK+ "
            "supports. Let's make this a long paragraph to demonstrate: "
            "blah blah blah blah blah blah blah blah blah blah blah "
            "blah blah blah blah blah blah blah blah\n\n", -1);

        text_buffer.insert_with_tags_by_name(iter,
            "This line has character-based wrapping, and can wrap "
            "between any two character glyphs. Let's make this a long "
            "paragraph to demonstrate: blah blah blah blah blah blah "
            "blah blah blah blah blah blah blah blah blah blah blah "
            "blah blah\n\n", "char_wrap")

        text_buffer.insert_with_tags_by_name(iter,
            "This line has all wrapping turned off, so it makes the "
            "horizontal scrollbar appear.\n\n\n", "no_wrap")

        text_buffer.insert_with_tags_by_name(iter, "Justification. ",
                            "heading");

        text_buffer.insert_with_tags_by_name(iter,
            "\nThis line has center justification.\n", "center")

        text_buffer.insert_with_tags_by_name(iter,
            "This line has right justification.\n", "right_justify")

        text_buffer.insert_with_tags_by_name(iter,
            "\nThis line has big wide margins. Text text text text "
            "text text text text text text text text text text text "
            "text text text text text text text text text text text "
            "text text text text text text text text text text.\n",
            "wide_margins");

        text_buffer.insert_with_tags_by_name(iter,
            "Internationalization. ", "heading")

        text_buffer.insert(iter,
            "You can put all sorts of Unicode text in the buffer.\n\n"
            "German(Deutsch S\303\274d) Gr\303\274\303\237 Gott\nGreek"
            "(\316\225\316\273\316\273\316\267\316\275\316\271\316\272"
            "\316\254) \316\223\316\265\316\271\316\254 \317\203\316\261"
            "\317\202\nHebrew   \327\251\327\234\327\225\327\235\n"
            "Japanese(\346\227\245\346\234\254\350\252\236)\n\nThe "
            "widget properly handles bidirectional text, word wrapping, "
            "DOS/UNIX/Unicode paragraph separators, grapheme boundaries, "
            "and so on using the Pango internationalization framework.\n", -1)

        text_buffer.insert(iter, "Here's a word-wrapped quote in a "
            "right-to-left language:\n", -1)
        text_buffer.insert_with_tags_by_name(iter,
            "\331\210\331\202\330\257 \330\250\330\257\330\243 "
            "\330\253\331\204\330\247\330\253 \331\205\331\206 "
            "\330\243\331\203\330\253\330\261 \330\247\331\204\331"
            "\205\330\244\330\263\330\263\330\247\330\252 \330\252"
            "\331\202\330\257\331\205\330\247 \331\201\331\212 \330"
            "\264\330\250\331\203\330\251 \330\247\331\203\330\263"
            "\331\212\331\210\331\206 \330\250\330\261\330\247\331"
            "\205\330\254\331\207\330\247 \331\203\331\205\331\206"
            "\330\270\331\205\330\247\330\252 \331\204\330\247 \330"
            "\252\330\263\330\271\331\211 \331\204\331\204\330\261"
            "\330\250\330\255\330\214 \330\253\331\205 \330\252\330"
            "\255\331\210\331\204\330\252 \331\201\331\212 \330\247"
            "\331\204\330\263\331\206\331\210\330\247\330\252 \330"
            "\247\331\204\330\256\331\205\330\263 \330\247\331\204"
            "\331\205\330\247\330\266\331\212\330\251 \330\245\331"
            "\204\331\211 \331\205\330\244\330\263\330\263\330\247"
            "\330\252 \331\205\330\247\331\204\331\212\330\251 \331"
            "\205\331\206\330\270\331\205\330\251\330\214 \331\210"
            "\330\250\330\247\330\252\330\252 \330\254\330\262\330\241"
            "\330\247 \331\205\331\206 \330\247\331\204\331\206\330\270"
            "\330\247\331\205 \330\247\331\204\331\205\330\247\331\204"
            "\331\212 \331\201\331\212 \330\250\331\204\330\257\330\247"
            "\331\206\331\207\330\247\330\214 \331\210\331\204\331\203"
            "\331\206\331\207\330\247 \330\252\330\252\330\256\330\265"
            "\330\265 \331\201\331\212 \330\256\330\257\331\205\330\251 "
            "\331\202\330\267\330\247\330\271 \330\247\331\204\331\205\330"
            "\264\330\261\331\210\330\271\330\247\330\252 \330\247\331\204"
            "\330\265\330\272\331\212\330\261\330\251. \331\210\330\243"
            "\330\255\330\257 \330\243\331\203\330\253\330\261 \331\207"
            "\330\260\331\207 \330\247\331\204\331\205\330\244\330\263"
            "\330\263\330\247\330\252 \331\206\330\254\330\247\330\255"
            "\330\247 \331\207\331\210 \302\273\330\250\330\247\331\206"
            "\331\203\331\210\330\263\331\210\331\204\302\253 \331\201"
            "\331\212 \330\250\331\210\331\204\331\212\331\201\331\212"
            "\330\247.\n\n", "rtl_quote")

        text_buffer.insert(iter, "You can put widgets in the buffer: "
            "Here's a button: ", -1)

        anchor = text_buffer.create_child_anchor(iter)
        text_buffer.insert(iter, " and a menu: ", -1)
        anchor = text_buffer.create_child_anchor(iter)
        text_buffer.insert(iter, " and a scale: ", -1)
        anchor = text_buffer.create_child_anchor(iter)
        text_buffer.insert(iter, " and an animation: ", -1)
        anchor = text_buffer.create_child_anchor(iter)
        text_buffer.insert(iter, " finally a text entry: ", -1)
        anchor = text_buffer.create_child_anchor(iter)
        text_buffer.insert(iter, ".\n", -1)

        text_buffer.insert(iter, "\n\nThis demo doesn't demonstrate all "
            "the GtkTextBuffer features; it leaves out, for example: "
            "invisible/hidden text(doesn't work in GTK 2, but planned), "
            "tab stops, application-drawn areas on the sides of the "
            "widget for displaying breakpoints and such...", -1)

        # Apply word_wrap tag to whole buffer */
        start, end = text_buffer.get_bounds()
        text_buffer.apply_tag_by_name("word_wrap", start, end)

def main():
    PangoView()
    gtk.main()

if __name__ == '__main__':
    main()

