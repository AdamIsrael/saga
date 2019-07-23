#!/usr/bin/env python3
# from pandocfilters import (
#     toJSONFilter,
#     RawInline,
#     Str,
#     Para,
#     HorizontalRule,
# )
# import sys

# """
# Pandoc filter that replaces a HorizontalRule with a scene break
# """


# def rtf(s):
#     return RawInline('rtf', s)

# def scene_break(key, value, fmt, meta):
#     # if key == 'HorizontalRule' and format == 'md':

#     if key == 'HorizontalRule' and fmt == 'rtf':
#         # sys.stderr.write('Got key: {}\n'.format(key))
#         # print("Yay!")
#         # return Str("\\qc #")
#         # return Para('\\qc #')
#         # return rtf('\\qc #')
#         # return HorizontalRule()
#         return RawBlock('\\qc #\n', 'rtf')

# if __name__ == "__main__":
#     toJSONFilter(scene_break)

from panflute import *

def increase_header_level(elem, doc):
    if type(elem) == HorizontalRule:
        # TODO: Format this nicer
        
        return(RawBlock('{\pard \\qc \\f0 \\sa180 \\li0 \\fi0 # \\par}\n', 'rtf'))

def main(doc=None):
    return run_filter(increase_header_level, doc=doc)

if __name__ == "__main__":
    main()