
class Context:

    ''' Redefine input/output streams or variable definitions by stacking this
    on top of the last context '''

    def __init__ (self, outputfile=None):
        self.outputfile = outputfile
