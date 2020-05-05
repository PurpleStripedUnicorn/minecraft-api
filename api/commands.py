
import os

from api.command import Command, CommandContainer
from api.context import Context
from api.errors import CompileError, err_format
from api.tools import removeWhitespace

commands = CommandContainer()

@commands('namespace', r'^[A-Za-z0-9_]+$')
def cmdNamespace (cp, line):
    ''' namespace definition line is ignored when compiling, since it has
    already been searched for, namespace definitions have to be inside the main 
    context '''
    print(len(cp.contextStack))
    if len(cp.contextStack) != 1:
        raise cp.raiseError('namespace definition outside main context')

@commands('def', r'[A-Za-z0-9_]+ *\{ *$')
def cmdDef (cp, line):
    fname = removeWhitespace(line.split(' ')[1].split('{')[0])
    cp.contextStack.append(Context(os.path.join(cp.mainfolder, 'functions',
    fname + '.mcfunction')))