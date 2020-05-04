
def removeWhitespace (txt: str) -> str:
    ''' Remove whitespace at both the end and the start of a string '''
    while len(txt) > 0 and txt[0] in ' \t\n':
        txt = txt[1:]
    while len(txt) > 0 and txt[-1] in ' \t\n':
        txt = txt[:-1]
    return txt