
import os
import re
import shutil
from api.errors import CompileError


class Compiler:

    ''' Compiler object. This object handles input and output streams '''

    def __init__ (self, inputfile: str, outputfolder: str):
        self.inputStack = [ inputfile ]
        self.outputfolder = outputfolder
        # find the namespace definition
        self.namespace = self.findNamespace()
        # create folder structure for the datapack
        self.createFolders()

    def findNamespace (self) -> str:
        ''' find the namespace definition in the upper most file in the input
        stack, throws an error if none is given '''
        ln = 0
        for line in open(self.inputStack[0]).readlines():
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