
import os

def compileCode (inputfile: str, outputfolder: str):
    ''' Convert the code inside the `inputfile` to a minecraft datapack with as
    root folder the given `outputfolder` '''
    # for now, just output the given code into a new file inside the output 
    #   folder
    with open(inputfile) as fr:
        if not os.path.isdir(outputfolder):
            os.makedirs(outputfolder)
        with open(os.path.join(outputfolder, 'out.mcfunction'), 'w') as fw:
            fw.write(fr.read())