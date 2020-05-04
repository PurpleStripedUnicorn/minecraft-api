
from api.datapack import Compiler
import os

def compileCode (inputfile: str, outputfolder: str):
    ''' Convert the code inside the `inputfile` to a minecraft datapack with as
    root folder the given `outputfolder` '''
    # create a datapack compiler
    cp = Compiler(os.path.join(*inputfile.split('/')),
    os.path.join(*outputfolder.split('/')))
    # compile the code
    cp.comp()