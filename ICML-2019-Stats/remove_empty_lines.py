import os


datasetFolderName = "datasets/" 
fileName = datasetFolderName + "initial_accepted_papers_ICML19.txt"

def remove_empty_lines(fileName):
    if not os.path.isfile(fileName):
        print("{} does not exist ".format(fileName))
        return
    with open(fileName) as filehandle:
        lines = filehandle.readlines()

    with open(fileName, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)   

remove_empty_lines(fileName)