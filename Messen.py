###############################################################################
# Use:  This program is used when an Experiment is run and the data is collec-
#       ted it lets the user input data and dumps it in a json file for further
#       analysis.
# Author: Alexander Becker (becker(dot)alexander42(at)gmail(dot)com)
# Version: 0.0
################################# Imports #####################################

import json
import numpy as np
import time
from datetime import datetime
import copy
################################# Version info ################################
version = 0.5

################################# User interface Strings ######################
eingabefehler = 'Keine gueltige eingabe'
welcheeingabe = 'Welche der Daten ist falsch (nummer des Datensatzes): '
eingaberichtig = 'Sind die gezeigten Daten richtig? (y/n): '

################################# Useful static stuff #########################
# Here we can assign Units to the desired measurement that are automatically added if the measurement is found in the following table
bekannte_messgroessen = {'Spannung':'V','Strom':'A','Kraft':'N','Flussdichte':'B','Stromdichte':'A/m^2','Strecke':'m','Flaeche':'m^2','Zeit':'s','Lichtmenge':'lm'}

# Here we store the Metadata type that should be collected and a describing String that is printed to the user when prompted to enter the required data
# the allowed datatypes are specified in the third field and can be 'str' for string, 'int' for integer and 'float' for float
metadaten = [['Messgroesse','Bitte geben Sie die Messgroesse (z.B. Spannug, Strom...) an: ','str'],['Einheit','Bitte geben Sie die Einheit der Messgroesse an (Nur SI einheit ohne Vorfaktor) an : ','str'],['Messgeraet','Bitte geben Sie das Messgeraet an: ','str'],['Messbereich','Bitte geben Sie den Messbereich als exponenten der Zehnerpotenz (z.B. \'-3\' fuer milli...) an: ','int'],['Toleranz','Bitte geben Sie die Toleranz in Einheiten des Messbereiches (z.B. \'0.1\' fuer eine Toleranz von 0.1 mV mit \'-3\' im Messbereich) an: ','float']]

################################# Functions ###################################
#------------------------------------------------------------------------------
def input_with_type_check(printstring='',input_type='str',errormsg='Error',escape_sequence='ende'):
    read_data = input(printstring)
    if(read_data != escape_sequence):
        if input_type == 'str':
            try:
                return str(read_data)
            except ValueError:
                print (errormsg)
                return None
        elif input_type == 'int':
            try:
                return  int(read_data)
            except ValueError:
                print (errormsg)
                return None
        elif input_type == 'float':
            try:
                return float(read_data)
            except ValueError:
                print (errormsg)
                return None
    else:
        return escape_sequence

#------------------------------------------------------------------------------
def max_length_of_column(table):
    maxlengthlist = []
    for i in range(len(table[0])):          # we take the first row of the table to be the width
        lengthlist = []                     # This list holds the length of all the elements of a column
        for row in table:
            lengthlist.append(len(str(row[i])))
        maxlengthlist.append(max(lengthlist))
    return maxlengthlist
#------------------------------------------------------------------------------


################################# Main code ###################################


print ("Sie haben ein neues Experiment begonnen.")
# TODO We still need to collect data about the experiment such as name of the experimentator date and time and so on
# Prompt the user for the Name of the Experiment to put in the Filename
Name_of_experiment = None
while Name_of_experiment is None:
    Name_of_experiment = input_with_type_check('Bitte geben Sie den Namen der Messung an:','str','Error','Unbenannt')
# Now before the exeriment we collect metadata about it and store it in a dict.
print ("Bitte geben Sie nun die zu messenden Groessen ein (z.B. Spannung, Strom ...)\n")

#------------------------------------------------------------------------------
#Here we start to collect metadata (specified in the metadaten table) for the experiment 
# the messgroessen is a list of lists that store the metadata for each column of mesurements
messgroessen = []
i = 0
# here we ask the user for the metadata specified in the metadaten list. we also Print the descriptive texts and check for type integrity
while i==0 or answer=='y' or answer == 'Y':
    aktuelle_messgroesse = []
    i = 0
    while i < len(metadaten):
        eingabe = input_with_type_check(metadaten[i][1],metadaten[i][2],eingabefehler,'ende')
        if eingabe is not None:
            aktuelle_messgroesse.append(eingabe)
            i += 1
        if(i==1):
            if aktuelle_messgroesse[0] in bekannte_messgroessen:
                aktuelle_messgroesse.append(bekannte_messgroessen[aktuelle_messgroesse[0]])
                i+=1
    messgroessen.append(aktuelle_messgroesse)
    del aktuelle_messgroesse
    answer = input("Soll eine weitere Messgroesse eingestellt werden(y/n):")
print ('\n')
del answer
del eingabe

#------------------------------------------------------------------------------
#Now we start to collect the data that is measured during the experiment
messungen = []
aktuelle_messung = [None,None]
i = 0
while aktuelle_messung[-2] is not 'ende':
    # Initialise Variables
    aktuelle_messung = []
    print ('------------------------------')
    print ('%i. Messung: '%(i+1))
    j = 0
    while j in range(len(messgroessen)):
        messung = input_with_type_check(messgroessen[j][0]+' in '+messgroessen[j][1]+': ','float',eingabefehler)
        if(messung != None) and (messung != 'ende'):
            aktuelle_messung.append(messung)
            j += 1
        elif messung is 'ende':
            aktuelle_messung.append(messung)
            break
    aktuelle_messung.append(datetime.isoformat(datetime.now()))
    messungen.append(aktuelle_messung)
    i += 1
del messungen[-1]
print ('Die Messreihe wurde erfolgreich bendet.')

#------------------------------------------------------------------------------
# In this Part of the Program we want to display the data to the experimentator
# and let him edit it to correct obvious mistakes.

# Display data
answer = input('Moechten Sie sich ihre gemessenene Ergebnisse anzeigen lassen (y/n): ')
if answer is 'y' or answer is 'Y':
    print ('Metadaten zu den erfassten Messgroessen: ')
    for messgroesse in messgroessen:
        print ('-'*40)
        messungsgroessenindex = 1
        for j in range(len(messgroesse)):
            print ( str(messungsgroessenindex)+'. '+metadaten[j][0]+': '+ str(messgroesse[j]), end='\n')
            messungsgroessenindex += 1
        print ('='*40)
        while input(eingaberichtig) == ('n' or 'N'):
            answer = input_with_type_check(welcheeingabe,'int','Bitte geben Sie eine Zahl an!')
            # TODO here there is something wrong try to fix that at some point
            correctedvalue = None
            while correctedvalue == None or correctedvalue == 'ende':
                correctedvalue = input_with_type_check(metadaten[answer-1][0]+': ',metadaten[answer-1][-1])
            if correctedvalue is not (None or 'ende'):
                messgroesse[answer-1] = correctedvalue

    print ('\n\nErfasste Daten:')
    print ('='*40)
    # now we build a printable table
    messungskopie = copy.deepcopy(messungen)
    messungsindex = 1
    for messung in messungskopie:
        messung.insert(0,messungsindex)
        messungsindex += 1
    tabelle = [['Messung']]
    for messgroesse in messgroessen:
        tabelle[0].append(messgroesse[0])
    for messung in messungskopie:
        tabelle.append(messung)
    #determin the longeset string in the table for width adjustment
    maxlength = max_length_of_column(tabelle)
    # print the table
    for row in tabelle:
        for i in range(len(messgroessen)+1):
            print (str(row[i]).rjust(maxlength[i]+1),end='|')
        print ('')
#we want to export the metadata as descriptors for the messgroessen array so we have to collaps it
komprimierte_metadaten = []
for metadatum in metadaten:
    komprimierte_metadaten.append(metadatum[0])
metadaten = komprimierte_metadaten

# last thing to do is write the collected data into a file using json
filename = time.strftime('%Y-%m-%d-%H%M-'+Name_of_experiment)
with open(filename,'w') as file:
    json.dump({'Name_of_experiment':Name_of_experiment,'messungen':messungen,'messgroessen':messgroessen,'metadaten':metadaten},file)

####################################### THE END ###############################