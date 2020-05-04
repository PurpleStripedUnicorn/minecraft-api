
class CompileError(Exception):

    ''' Base exception during compiling '''

def err_format (filename, ln, err):
    return 'ERROR: ({} on line {}) {}'.format(filename, ln, err)