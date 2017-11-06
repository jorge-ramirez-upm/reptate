import os
import sys
import cmd
import readline
from enum import Enum

class CmdMode(Enum):
    cmdline = 0
    batch = 1
    GUI = 2
    modes=["Command Line Interpreter", "Batch processing", "Graphical User Interface"]

    def print(self):
        print("cmdline: ", self.modes.value[0])
        print("batch: ", self.modes.value[1])
        print("GUI: ", self.modes.value[2])

class CmdBase(cmd.Cmd):
    """Basic Cmd Console that is inherited by most Reptate objects"""

    prompt = '> '
    mode = CmdMode.cmdline
    def __init__ (self, parent=None):
        """Constructor """
        print("CmdBase.__init__(self, parent=None) called")
        super(CmdBase, self).__init__()
        print("CmdBase.__init__(self, parent=None) ended")

        delims = readline.get_completer_delims()
        delims = delims.replace(os.sep, '')
        readline.set_completer_delims(delims)
        
    def do_shell(self, line):
        """Run a shell command"""
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)
        self.last_output = output

    def do_cd(self, line):
        """Change folder"""
        if os.path.isdir(line):
            os.chdir(line)
        else:
            print("Folder %s does not exist"%line)

    def __listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                #name += '/'
            res.append(name)
        return res


    def __complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self.__listdir('.')
        
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self.__listdir(tmp) if p.startswith(rest)]
                
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self.__listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']
        
    def complete_cd(self, text, line, begidx, endidx):
        "Completions for the cd command."
        test=line.split()
        if (len(test)>1):
            result=self.__complete_path(test[1])
        else:
            result=self.__complete_path()
        
        return result

    def do_ls(self, line):
        """
        List contents of current folder
        
        .. todo:: CONSIDER SUBFOLDERS TOO
        """
        dirs=os.listdir()
        for d in dirs:
            print("%s"%d)
    do_dir = do_ls

    def do_pwd(self, line):
        """Print the current folder"""
        print(os.getcwd())
    do_cwd = do_pwd

    def emptyline(self):
        pass

    def do_EOF(self, args):
        """Exit Console and Return to Parent or exit"""
        print("")
        return True
    do_up = do_EOF
    
    def do_quit(self, args):
        """Exit from the application"""
        if (CmdBase.mode==CmdMode.batch):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
        msg = 'Do you really want to exit RepTate?'
        shall = input("%s (y/N) " % msg).lower() == 'y'         
        if (shall):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
            
    
    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) #in self._locals, self._globals
        except Exception as e:
            print (e.__class__, ":", e)

    def do_console(self, line):
        """Print/Set current & available Console modes
           console --> print current mode
           console available --> print available modes
           console [cmdline, batch, GUI] --> Set the console mode to [cmdline, batch, GUI]
        """
        if (line==""):
            print("Current console mode: %s"%CmdMode.modes.value[CmdBase.mode.value])
        elif (line=="available"):
            c = CmdMode(0)
            c.print()
        elif (line in dict(CmdMode.__members__.items())):
            CmdBase.mode=CmdMode[line]
        else:
            print ("Console mode %s not valid"%line)

        if (self.mode==CmdMode.batch):
            self.prompt = ''
            
