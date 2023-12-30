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
    location     *1;
    object       *2;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
'''


import os

def dimmention_maker(Mass=0 , Length=0, Time=0, Temperature=0, Quantity=0, Current=0, Luminous=0):
    dimmention = "[{} {} {} {} {} {} {}];".format(Mass , Length, Time, Temperature, Quantity, Current, Luminous)

    comment =""
    if Mass != 0:
        comment += "kg^{} ".format(Mass)
    if Length != 0:
        comment += "m^{} ".format(Length)
    if Time != 0:
        comment += "s^{} ".format(Time)
    if Temperature != 0:
        comment += "C^{} ".format(Temperature)
    if Quantity != 0:
        comment += "mol^{} ".format(Quantity)
    if Current != 0:
        comment += "A^{} ".format(Current)
    if Luminous != 0:
        comment += "cd^{} ".format(Luminous)
    
    comment = comment.strip().replace(" ",".")

    return "{:<20} {:<20} //{:<20} {:<20}".format("dimensions",dimmention, comment,"[Mass  Length  Time  Temperature  Quantity  Current  Luminous]")


list_boundaries = ["inlet","outlet","wall"]
 

def boundary_maker(list_boundaries):
    bd_dict = {}
    for bd in list_boundaries:
        bd_dict[bd] = {"type": None, "value": None}

    return bd_dict

def boundary_wizard():

    variable_name = input("Name of the variable: ")
    Mass = input("What is the order of Mass:")
    if Mass == '':
       Mass = 0 
    Length = input("What is the order of Length:")
    if Length == '':
       Length = 0 
    Time = input("What is the order of Time:")
    if Time == '':
       Time = 0 
    Temperature = input("What is the order of Temperature:")
    if Temperature == '':
       Temperature = 0 
    Quantity = input("What is the order of Quantity:")
    if Quantity == '':
       Quantity = 0 
    Current = input("What is the order of Current:")
    if Current == '':
       Current = 0 
    Luminous = input("What is the order of Luminous:")
    if Luminous == '':
       Luminous = 0 

    dim = dimmention_maker(Mass,Length,Time,Temperature,Quantity,Current,Luminous)

    scalOrvec = int(input("is this variable a 1.scale or 2.vector?:"))

    internalField = ""
    if scalOrvec == 1:
        internalField = "uniform    " + str(input("What is the value for this variable in internalField?:"))
    elif scalOrvec == 2:
        x_intermalFeild = input("What is the value of this variable in `x direction` in internalField?:")
        y_intermalFeild = input("What is the value of this variable in `y direction` in internalField?:")
        z_intermalFeild = input("What is the value of this variable in `z direction` in internalField?:")

        internalField = "uniform     ({} {} {})".format(x_intermalFeild, y_intermalFeild, z_intermalFeild)

    list_boundaries = []
    num_boundaries = int(input("What are the numbers of the boundaries"))
    for i in range(num_boundaries):
        name = input("Enter the name of the boundary {}: ".format(i))
        list_boundaries.append(name)
    
    boundary_dict = boundary_maker(list_boundaries)

    boundary_types = [
                        "fixedValue",
                        "surfaceNormalFixedValue",
                        "fixedGradient",
                        "zeroGradient",
                        "inletOutlet",
                        "totalPressure",
                        "fixedFlux",
                        "waveTransmissive",
                        "symmetry",
                        "cyclic",
                        "slip",
                        "noSlip"]
    
    for key in boundary_dict.keys():
        print("what is the tpye of the buondary {}".format(key))
        for i in range(len(boundary_types)):
            print("{}. {}".format(i+1, boundary_types[i]))
        boundary_dict[key]["type"] = boundary_types[int(input("please enter the index :"))-1]
        print("what is the value of the buondary {}".format(key))
        boundary_dict[key]["value"] = input("please enter the value :")

    with open("./0/{}".format(variable_name),"w") as file:
        file.write(header)
        if scalOrvec == 1:
            file.write(FoamFile.replace("*1","volScalarField"))
        elif scalOrvec == 2:
            file.write(FoamFile.replace("*1","volVectorField"))

        file.write("\n\n" + dim + "\n\n")

        file.write("{:<20} {:<20}".format("internalField", internalField))

        file.write("\n\nboundaryField\n{")
        for key in boundary_dict.keys():
            file.write("\t\t{}\n\t\t{{".format(key))
            for key2 in boundary_dict[key].keys():
                file.write("\n{:>10} {:<10} {:<10}".format("",key2, boundary_dict[key][key2] + ";"))
            file.write("\n\t\t}\n")
        file.write("}")
        file.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
boundary_wizard()