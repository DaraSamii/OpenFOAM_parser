import re

header = '''
/*--------------------------------*- C++ -*----------------------------------*\\n
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  6
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
'''


FoamFile = '''
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "*1";
    object       *2;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
'''

controldict = {
"application" : {
    "value" : "simpleFoam",
    "comment" : "name of the solver to use for the project, example: [simpleFoam, icoFoam,..]"
},
"startFrom" : {
    "value": "startTime",
    "comment": "Controls the start time of the simulation.",
    "options": ["`firstTime`(Earliest time step)", "`startTime`(speciﬁed by startTime)", "`latestTime`(Most recent time step)"],
},
"startTime"  : {
    "value" :0,
    "comment": "Start time for the simulation"
},
"stopAt": {
    "value": "endTime",
    "comment": "Controls the end time of the simulation.",
    "opntions": ["`endTime`(speciﬁed by endTime)",
                "`writeNow`(Stops by the end of timestep and writes data)",
                 "`noWriteNow`(Stops by the end of  time tep and does not write data)",
                "`nextWrite`(Stops on completion of next write time, speciﬁed by writeControl)"],
},
"endTime" : {
    "value" :10,
    "comment": "End time for the simulation when stopAt `endTime`; is speciﬁed."},
"deltaT"  : {
    "value": 0.005,
    "comment": "Time step of the simulation.",
},
"writeControl"  : {
    "value" : "timeStep",
    "comment": 'Controls the timing of write output to ﬁle.',
    "options": ["`timeStep`(Writes data every writeInterval timesteps)",
                "`runTime`(Writes data every writeInterval seconds)",
                "`adjustableRunTime`(Writes data every writeInterval seconds,  adjusting timesteps to coincide with writeInterval)",
                "`cpuTime`(Writes data every writeInterval seconds of CPU time)",
                "`clockTime`(Writes data out every writeInterval seconds of real time)"]
},
"writeInterval" : {
    "value":100,
    "comment":"Scalar used in conjunction with writeControl",
},
"purgeWrite" : {
    "value":0,
    "comment":"Integer representing a limit on the number of time directories. To disable the purging, specify purgeWrite 0"
},
"writeFormat"   :  {
    "value":"binary",
    "comment":"Speciﬁes the format of the data ﬁles.",
    "options": ["`ascii`", "`binary`"]
},
"writePrecision" : {
    "value":6,
    "comment":"Integer used in conjunction with writeFormat"
},
"writeCompression": {
    "value":"off",
    "comment":"Switch to specify whether ﬁles are compressed with gzip",
    "options":["`on`","`off`"],
},
"timeFormat" : {
    "value":"general",
    "comment":"Choice of format of the naming of the time directories.",
    "options":["`fixed`(m.ddd where d is timePrecision)",
               "`scientific`(m.ddde + xx where d is timePrecision)",
               "`general`(Speciﬁes scientific format if the exponent is less than -4)"],
},
"timePrecision": {
    "value":6,
    "comment": "Integer used in conjunction with timeFormat described above", 
},
"graphFormat": {
    "value": "raw",
    "comment": "Format for graph data written by an application.",
    "options": ["`raw`(Raw ASCII format in columns)",
                "`gnuplot`(Data in gnuplot format)",
                "`csv`(Comma-separated values)",
                "`vtk`(Visualisation Toolkit (VTK) format)",
                "`ensight`(Ensight format)"]
},
"adjustTimeStep":{
    "value":"off",
    "comment":"witch used by some solvers to adjust the time step during the simulation, usually according to maxCo.",
    "options":["`on`","`off`"]
},
"maxCo":{
    "value": 1,
    "comment": "Maximum Courant number",
},
"runTimeModifiable": {
    "value": "on",
    "comment" : "dictionaries are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation",
    "options": ["`on`","`off`"],
}
}

functions = '''
functions
{
    // Function objects
}
 
// ************************************************************************* //
'''

help_site ="""
// https://www.openfoam.com/documentation/guides/latest/doc/guide-case-system-controldict.html
// https://doc.cfd.direct/openfoam/user-guide-v11/controldict \n\n\n
"""

def controldict_writer(controldict: dict, path="controldict"):
    with open(path,'w') as file:
        file.write(header  + FoamFile.replace('*1','system').replace('*2','controldict') + "\n\n")
        file.write(help_site)
        for i in controldict.keys():
            file.write("{:<20} {:<20} //{:<10}".format(i, str(controldict[i]["value"])+";", controldict[i]["comment"]))

            if "options" in controldict[i]:
                file.write("-- options: " + str(controldict[i]["options"]))

            file.write("\n\n")
        file.write(functions)


def contorldict_wizard():
    print("This is OpenFOAM controldict wizard program")
    print("we will walk through all configurations to create the Controldict file")

    while True:
        i = 1
        for key in controldict.keys():
            print("\n\n{}. choose {}:".format(i,key))
            print("\tDefault value: {}".format(controldict[key]['value']))
            print("\tDescprtion of the variable `{}`: {}".format(key,controldict[key]['comment']))
            if "options" in controldict[key]:
                opts = controldict[key]["options"]
                print("\tOptions:")
                for j in range(len(opts)):
                    print("\t\t{}. {}".format(j+1,opts[j]))
            
            i = i+1
            inp = input("\tChoose the value or select the index of the option, press enter to keep the default:")
            if inp == '':
                pass
            elif "options" in controldict[key]:
                controldict[key]["value"]= re.search(r'`([^`]+)`', opts[j-1]).group(1) 
            else:
                controldict[key]["value"] = inp
            
        
        final_dict = {key: value_dict['value'] for key, value_dict in controldict.items()}
        for variable,value in final_dict.items():
            print("{} : {}".format(variable,value))
            
        agree = input("Is the printed configration correct if yes press y or enter, if not press any key to do the configuration again [Y/n]:")
        if agree == "" or agree.lower()=="y":
            break
    controldict_writer(controldict)
    

if __name__ =="__main__":
    contorldict_wizard()