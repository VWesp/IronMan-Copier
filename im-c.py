import argparse
import time
from shutil import copyfile
import os
from appJar import gui


app = gui("", "400x200")

input = None
output = None
file_ending = None
output_file = None
copy_index = 0
file_loaded = False


def appMode():

    app.addLabel("title", "IronMan-Copier")
    app.setLabelBg("title", "orange")

    app.addButtons(["Input file"], pressInput)
    app.addButtons(["Output folder"], pressOutput)

    app.addButtons(["Copy", "Delete", "Copy Back", "Close"], pressButton)
    app.disableButton("Copy")
    app.disableButton("Copy Back")
    app.disableButton("Delete")

    app.addEmptyLabel("Input")
    app.addEmptyLabel("Output")

    app.addStatusbar()
    app.setStatusbar("Copy index: ")



def pressInput():

    global input

    local_input = app.openBox(title="Choose input file")
    if(len(local_input)):
        input = local_input
        app.setLabel("Input", "Input: " + input.split("/")[-1])
        app.enableButton("Copy")



def pressOutput():

    global output

    local_output = app.directoryBox(title="Choose output folder")
    if(len(local_output)):
        output = local_output
        app.setLabel("Output", "Output: " + output.split("/")[-1])



def pressButton(button):

    global file_loaded

    if(button == "Copy"):
        if(output != None):
            if(not file_loaded):
                loadFile()
                file_loaded = True

            app.enableButton("Copy Back")
            app.enableButton("Delete")
            copyFile()
        else:
            app.warningBox("An output directory must be specified!")
    if(button == "Delete"):
        deleteCopies()
    if(button == "Copy Back"):
        copy_back = app.openBox(title="Choose to copy back")
        copyfile(copy_back, input)
    if(button == "Close"):
        app.stop()



def loadFile():

    global output_file
    global file_ending

    file = input.split("/")[-1].split(".")
    file_name = file[0]
    file_ending = ""
    if(len(file) > 1):
        file_ending = "." + file[-1]
    else:
        file_ending = ".sav"

    output_file = (output + "/" + file_name).replace("//", "/")



def copyFile():

    global copy_index

    copy_index += 1
    copyfile(input, output_file + "_copy" + str(copy_index) + file_ending)
    app.setStatusbar("Copy index: " + str(copy_index))



def deleteCopies():

    global copy_index

    delete = app.yesNoBox("Remove copies", "Do you want to remove all copies except the most recent one?")

    if(delete):
        copyfile(output_file + "_copy" + str(copy_index) + file_ending, output_file + "_recentCopy" + file_ending)
        while(copy_index):

            os.remove(output_file + "_copy" + str(copy_index) + file_ending)
            copy_index -= 1

        app.setStatusbar("Copy index: ")



appMode()
app.go()
