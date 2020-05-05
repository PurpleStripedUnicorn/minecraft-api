
import os
import random

from api.command import Command, CommandContainer
from api.context import Context
from api.errors import CompileError
from api.tools import removeWhitespace

commands = CommandContainer()

@commands('namespace', r'^[A-Za-z0-9_]+$')
def cmdNamespace (cp, line):
    ''' namespace definition line is ignored when compiling, since it has
    already been searched for, namespace definitions have to be inside the main 
    context '''
    if len(cp.contextStack) != 1:
        raise cp.raiseError('namespace definition outside main context')

@commands('def', r'[A-Za-z0-9_]+ *\{ *$')
def cmdDef (cp, line):
    ''' function definition '''
    fname = removeWhitespace(line.split(' ')[1].split('{')[0])
    if fname.startswith('0x'):
        cp.raiseError('function names cannot start with "0x"')
    cp.contextStack.append(Context(os.path.join(cp.mainfolder, 'functions',
    fname + '.mcfunction')))

def cmdExecute (cp, line):
    ''' format for all commands associated with the vanilla `execute` command,
    e.g. `if`, `unless`, `as` '''
    # remove whitespace and '{' from the statement
    statement = removeWhitespace(removeWhitespace(line)[:-1])
    # generate a random function name
    fname = '0x{:08x}'.format(random.randint(0, 16 ** 8 - 1))
    # write execute command to current output file
    with open(cp.currentOutputfile, 'a') as f:
        f.write('execute {} run function {}:{}\n'.format(statement, cp.namespace,
        fname))
    # create new context for the function file
    cp.contextStack.append(Context(os.path.join(cp.mainfolder, 'functions',
    fname + '.mcfunction')))

# `execute` associated commands:

commands('if', r'^.+\{ *$')(cmdExecute)
commands('unless', r'^.+\{ *$')(cmdExecute)
commands('at', r'^.+\{ *$')(cmdExecute)
commands('as', r'^.+\{ *$')(cmdExecute)
commands('positioned', r'^.+\{ *$')(cmdExecute)
