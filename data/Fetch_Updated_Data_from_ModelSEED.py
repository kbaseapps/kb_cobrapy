#!/usr/bin/env python
from urllib.request import urlopen
import sys,json

MSD_git_url = "https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/"
MSD_commit = "v1.0"

Biochem_Files = ["compounds.tsv",
                 "reactions.tsv",
                 "Aliases/Unique_ModelSEED_Reaction_ECs.txt",
                 "Aliases/Unique_ModelSEED_Reaction_Names.txt",
                 "Aliases/Unique_ModelSEED_Compound_Names.txt",
                 "Aliases/Unique_ModelSEED_Reaction_Aliases.txt",
                 "Aliases/Unique_ModelSEED_Compound_Aliases.txt",
                 "Structures/Unique_ModelSEED_Structures.txt"]

for biochem_file in Biochem_Files:
    print("Copying "+biochem_file)
    remote_file = urlopen(MSD_git_url+MSD_commit+"/Biochemistry/"+biochem_file)
    with open("Biochemistry/"+biochem_file,'w') as local_file:
        for line in remote_file.readlines():
            line=line.decode('utf-8')
            local_file.write(line)
