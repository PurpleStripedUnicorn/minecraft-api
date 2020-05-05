
import os
import re
import shutil

from api.commands import commands
from api.context import Context
from api.errors import CompileError, err_format
from api.tools import removeWhitespace


class Compiler:

    ''' Compiler object. This object handles input and output streams '''

    def __init__ (self, inputfile: str, outputfolder: str):
        self.inputfile = inputfile
        self.outputfolder = outputfolder
        # find the namespace definition
        self.namespace = self.findNamespace()
        # create folder structure for the datapack
        self.createFolders()
        # create the context stack
        self.contextStack = [ Context(None) ]

    def findNamespace (self) -> str:
        ''' find the namespace definition in the upper most file in the input
        stack, throws an error if none is given '''
        ln = 0
        for line in open(self.inputfile).readlines():
            ln += 1
            if line.startswith('namespace '):
                if not re.match(r'^namespace [A-Za-z0-9_]+$', line):
                    raise CompileError('(ln. {})Invalid namespace definition'
                    .format(ln))
                return line[:-1].split(' ')[1]
        raise CompileError('No namespace definition found')

    def createFolders (self):
        ''' Create the folder structure for the datapack, removes any existing
        files inside the folder `outputfolder` '''
        # check if given path is not a file
        if os.path.isfile(self.outputfolder):
            raise CompileError('Given output folder is a file')
        # remove existing folder, if it exists
        if os.path.isdir(self.outputfolder):
            shutil.rmtree(self.outputfolder)
        # create directories, gather subfolders to create form the folders.txt
        #   file
        os.mkdir(self.outputfolder)
        os.mkdir(os.path.join(self.outputfolder, 'data'))
        os.mkdir(os.path.join(self.outputfolder, 'data', self.namespace))
        for line in open('api/folders.txt').readlines():
            os.mkdir(os.path.join(self.outputfolder, 'data', self.namespace,
            os.path.join(*line[:-1].split('/'))))

    @property
    def mainfolder (self) -> str:
        return os.path.join(self.outputfolder, 'data', self.namespace)

    @property
    def currentOutputfile (self):
        ''' Get the current output file (grabs the highest context which has
        an output file defined) '''
        # check if there is a context with an output file defined
        contextStack = self.contextStack
        if len([x for x in contextStack if x.outputfile != None]) == 0:
            return None
        return [x for x in contextStack if x.outputfile != None][-1].outputfile

    def isempty (self, line: str) -> bool:
        ''' Check if the given line considered to be a comment or an empty line
        '''
        return re.match(r'^([ \t\n]*|[ \t\n]*#.*)$', line)

    def iscontextremover (self, line: str) -> bool:
        ''' Check if the given line is a context remover command '}' '''
        return re.match(r'^[ \t\n]*\}[ \t\n]*$', line)

    def comp (self, inputfile=None):
        ''' Compile the code in the input file line by line (optionally, an
        input file can be given in stead of the standard input file) '''
        if inputfile == None:
            inputfile = self.inputfile
        # go through every line in the input file
        # keep track of the line number and the file currently being read
        self.ln = 0
        self.currentinput = inputfile
        for line in open(inputfile).readlines():
            self.ln += 1
            # check if line is not a comment or empty
            if self.isempty(line[:-1]):
                continue
            # check for context remover command '}'
            if self.iscontextremover(line[:-1]):
                self.contextStack.pop(-1)
                continue
            # check if the command exists
            # if it doesn't, it is regarded as a vanilla minecraft command
            found = False
            for cmd in commands:
                if cmd.matchpattern(self, line[:-1]):
                    if found:
                        raise CompileError(err_format(self.currentinput,
                        self.ln, 'Line matches multiple commands'))
                    cmd(self, line[:-1])
                    found = True
            if not found:
                with open(self.currentOutputfile, 'w') as f:
                    f.write(removeWhitespace(line) + '\n')
