from panflute import *

def increase_header_level(elem, doc):
    if type(elem) == Header:

        header = stringify(elem)

        # TODO: Format this nicer
        # Check elem.level to know if this is a chapter heading or not

        """
        Rules:

        For chapter headings:
        - center
        - bold?
        four blank lines
        """
        # \\ql \\f0 \\sa180 \\li0 \\fi720
        if elem.level == 1:
            newheader = '{\\pard \\ql \\f0 \\qc ' + header + '\\par}\n'
            newheader += '{\\pard \\line \\line \\line \\line \\par}\n'

            return(RawBlock(newheader, 'rtf'))
        else:
            return []

def main(doc=None):
    return run_filter(increase_header_level, doc=doc)

if __name__ == "__main__":
    main()