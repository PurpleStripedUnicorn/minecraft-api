
import os
import re
from api.context import Context
from api.errors import CompileError, err_format
from api.tools import removeWhitespace

class CommandContainer:

    def __init__ (self):
        self.cmdlist = []

    def __call__ (self, cmdname: str, pattern: str):
        def tmp (fn):
            self.cmdlist.append(Command(cmdname, pattern, fn))
        return tmp

    def __iter__ (self):
        return iter(self.cmdlist)

class Command:

    def __init__ (self, cmdname: str, pattern: str, fn):
        self.cmdname = cmdname
        self.pattern = pattern
        self.fn = fn

    def matchpattern (self, cp, cmd):
        ''' Check if the given command matches the given pattern. If it is the
        right command but not the right pattern, an error is raised '''
        if not cmd.startswith(self.cmdname + ' ') and cmd != self.cmdname:
            return False
        args = cmd.split(' ', 1)[1] if len(cmd.split(' ', 1)) > 1 else ''
        if not re.match(self.pattern, args):
            raise CompileError(err_format(cp.currentinput, cp.ln,
            'Command does not match required pattern'))
        return True

    def __call__ (self, cp, line):
        return self.fn(cp, line)

        
commands = CommandContainer()



@commands('namespace', r'^[A-Za-z0-9_]+$')
def cmdNamespace (cp, line):
    pass

@commands('def', r'[A-Za-z0-9_]+ *\{ *$')
def cmdDef (cp, line):
    fname = removeWhitespace(line.split(' ')[1].split('{')[0])
    cp.contextStack.append(Context(os.path.join(cp.mainfolder, 'functions',
    fname + '.mcfunction')))