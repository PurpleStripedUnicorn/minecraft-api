
import os

from api.command import Command, CommandContainer
from api.context import Context
from api.tools import removeWhitespace

commands = CommandContainer()

@commands('namespace', r'^[A-Za-z0-9_]+$')
def cmdNamespace (cp, line):
    pass

@commands('def', r'[A-Za-z0-9_]+ *\{ *$')
def cmdDef (cp, line):
    fname = removeWhitespace(line.split(' ')[1].split('{')[0])
    cp.contextStack.append(Context(os.path.join(cp.mainfolder, 'functions',
    fname + '.mcfunction')))