# importing values
import numpy as np
from scipy.optimize import minimize
import pandas as pd

import csv

# time calculation
fps = 30
start_time = 22*fps + 19
end_time = 25*fps + 17
E_skill_time = (end_time - start_time ) / 30

stats_file_name = 'C:/Users/Michael/Desktop/GenshinPrograms/GenshinOptimization-main/GenshinOptimization-main/Output/stats.csv'
rolls_file_name = 'C:/Users/Michael/Desktop/GenshinPrograms/GenshinOptimization-main/GenshinOptimization-main/Output/rolls.csv'

# code for getting user input from console
#inputParameters =   input("Please enter character and enemy data in the form (CharName,CharLVL,SM,EnemyName,EnemyLVL)")

inputParameters = 'Kazuha,90, 6.6219, Hilichurl,90'

# getting a list of weapon names from the user input
#inputWeaponNameList =   input("Please enter weapon names and levels (Weapon#1Name, Weapon#2Name, etc...)")

inputWeaponNameList = ['BlackcliffLongsword','FavoniusSword', 'IronSting', 'LionsRoar', 'PrototypeRancour', 'RoyalLongsword', 'SacrificialSword', 'BlackSword', 'Flute', 'SwordOfDescension', 'FesteringDesire', 'AquilaFavonia', 'SkywardBlade', 'SummitShaper', 'PrimordialJadeCutter', 'FreedomSworn']

weaponNameList = inputWeaponNameList

def optimize (inputParameters, weaponName):

    stats_List = []
    rolls_List = []

    split_string = inputParameters.split(",")

    #extracting values from string list
    charName = split_string[0]
    charLVL = float(split_string[1])
    skillMultiplier = float(split_string[2])
    enemyName =  split_string[3]
    enemyLVL = float(split_string[4])

    # hard coding weapon level 90
    weaponLVL = 90

    #making intermediate variable global to the script
    CharBaseATK = 0
    CharATKB = 0
    CharCD = 0
    CharCR = 0
    CharEB = 0

    WeapBaseATK = 0
    WeapATKB = 0
    WeapCD = 0
    WeapCR = 0
    WeapEB = 0

    # opening CSV with character data and putting it into a dataframe
    with open('C:/Users/Michael/Desktop/GenshinPrograms/GenshinOptimization-main/GenshinOptimization-main/CharLVL90.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)
        print(data.index)
        dfC = pd.DataFrame(data, columns = ['Name','Base ATK','ATK%', 'CR','CD','EB','Type'])
        #print (df)  #for printing the CSV data if you want to see it

    # opening CSV with weapon data and putting it into a dataframe
    with open('C:/Users/Michael/Desktop/GenshinPrograms/GenshinOptimization-main/GenshinOptimization-main/WeaponLVL90.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)
        print(data.index)
        dfW = pd.DataFrame(data, columns = ['Name','Base ATK','ATK%', 'CR','CD','EB'])

    # populating character variables with csv data
    for i in range(31) :
        if str(dfC.iloc[i+1, 0]) == str(charName) :
            CharBaseATK = float(dfC.iloc[i+1, 1]) # character Base Atk
            CharATKB = float(dfC.iloc[i+1, 2])
            CharCR = float(dfC.iloc[i+1, 3])
            CharCD = float(dfC.iloc[i+1, 4])
            CharEB = float(dfC.iloc[i+1, 5]) 
            print('Character Stats:', 'Base ATK = ', CharBaseATK,'CritRate = ',  CharCR,'CritDMG = ',  CharCD,'ElemBonus = ',  CharEB)

    # populating weapon variables with csv data
    for i in range(56) :
        if str(dfW.iloc[i+1, 0]) == str(weaponName) :
            WeapBaseATK = float(dfW.iloc[i+1, 1]) # character Base Atk
            WeapATKB = float(dfW.iloc[i+1, 2])
            WeapCR = float(dfW.iloc[i+1, 3])
            WeapCD = float(dfW.iloc[i+1, 4])
            WeapEB = float(dfW.iloc[i+1, 5])
            print('Weapon Stats:','Base ATK = ', WeapBaseATK,'CritRate = ', WeapCR,'CritDMG = ', WeapCD,'ElemBonus = ', WeapEB)

    TotalBaseATK = CharBaseATK + WeapBaseATK # finding total base attack

    # filling other variables with either hardcode or user input
    SM = skillMultiplier # skill multiplier (assuming LVL 6 charged atk)
    CharLVL = charLVL
    EnemyLVL = enemyLVL
    DefDrop = 0
    EnemyRes = 0.1 # Hilichurl Anemo resistance
    BaseHP = 13348 # Kazuha base HP
    EB = 0.538 + CharEB + WeapEB + 0.15 # accounting for anemo goblet, 2 pc VV effect

    C1 = (1+EB)*(SM)*((100+CharLVL)/(100 + CharLVL + 100 + EnemyLVL)) *(1-EnemyRes) #calculating C1
    C2 = TotalBaseATK # setting C2 to the total base attack

    #print("C1 = " + str(C1))
    #print("C2 = " + str(C2))

    def objective(x) :

        a = x[0] #ATK%
        f = x[1] #flat atk
        z = x[2] #HP%
        h = x[3] #flat hp
        r = x[4] #crit rate
        d = x[5] #crit dmg
        e = x[6] #elemental mastery

        """
        # HP SCALING CALCS

        #HPatkBonusES = (0.0506)*(BaseHP*(0.466+1+0.0495*z)+254*h+4780)

        # conditional for reaching max HP bonus cap
        #if (HPatkBonusES > 4*C2) :
            #HPatkBonusES = 4*C2

        #print("HP ES bonus max = " + str(4*C2))
        #print("HP ES bonus = " + str(HPatkBonusES))

        #print((-1)*C1*(C2*(1+0.466+CharATKB+WeapATKB+0.0495*a)+311+f*16.5+HPatkBonusES))
        #print(1+(0.311+WeapCR+CharCR+0.033*r)*(WeapCD+CharCD+0.066*d))

        """
        number_of_reactions = 2
        EM =  115.2 + 187 + 165 + e # iron sting 165 

        RxnM = 1.2
        LvlM = 0.0025*(CharLVL)**3 - 0.446*(CharLVL)**2 + 40.531*(CharLVL) - 1119.5
        ResM = 0.9
        EMbonus = (16*EM)/(2000 + EM)

        attack_Term = (C2*(1+CharATKB+WeapATKB+0.0495*a)+311+f*16.5)
        crit_Term = (1+(0.311+WeapCR+CharCR+0.033*r)*(WeapCD+CharCD+0.066*d))
        skill_Damage = (-1)*C1*attack_Term*crit_Term

        reaction_Damage = RxnM*LvlM*(1 + EMbonus + 0.6)*ResM #computing the damage of one swirl reaction 0.6 is VV set effect
        print("Reaction Damage = " + str(reaction_Damage))


    #assuming CR% / EB% / ATK%
        return skill_Damage - number_of_reactions*reaction_Damage

    def constraint1(x) :
        return x[0]+x[1]+x[2]+x[3]+x[4]+x[5]+x[6]-20
    
    def printStats(x) :

        a = x[0] #ATK%
        f = x[1] #flat atk
        z = x[2] #HP%
        h = x[3] #flat hp
        r = x[4] #crit rate
        d = x[5] #crit dmg
        e = x[6] #elemental mastery

        HPatkBonusES = (0.0506)*(BaseHP*(0.466+1+0.0495*z)+254*h+4780)

        '''
        # conditional for reaching max HP bonus cap
        if (HPatkBonusES > 4*C2) :
            HPatkBonusES = 4*C2
        '''

        ATK = C2 + C2*(1+CharATKB + WeapATKB + 0.0495*a)+311+f*16.5
        #+0.018*(BaseHP*(1+0.0495*z)+254*h+4780)
        HP = BaseHP*(1+0.0495*z)+254*h+4780
        CR = 0.331+CharCR+WeapCR+0.033*r
        CD = CharCD+WeapCD+0.066*d
        EM = 115.2 + 187 + 165 + e

        #print("Avg Optimized DMG = " + str(objective(sol.x)))
        #print("Total ATK = " + str(ATK))
        #print("Total HP = " + str(HP))
        #print("Total CR = " + str(CR))
        #print("Total CD = " + str(CD))

        stats_List.append((-1)*objective(sol.x))
        stats_List.append(ATK)
        stats_List.append(HP)
        stats_List.append(CR)
        stats_List.append(CD)
        stats_List.append(EM)
        
        rolls_List.append(a)
        rolls_List.append(f)
        rolls_List.append(z)
        rolls_List.append(h)
        rolls_List.append(r)
        rolls_List.append(d)
        rolls_List.append(e)

        #print(str((-1)*objective(sol.x)))
        #print(str(ATK))
        #print(str(HP))
        #print(str(CR))
        #print(str(CD))

    #x0 = [1,1,1,1,1,1]
    x0 = [0,0,0,18,0,0,0] # initialization
    print(objective(x0))

    highBound = (0.0, 20.0)
    lowBound = (0.0, 15)
    bnds = (highBound,highBound,highBound,highBound,lowBound,lowBound, lowBound)
    con1 = {'type': 'eq', 'fun': constraint1}

    cons = [con1]

    sol = minimize(objective, x0, method = 'SLSQP', bounds=bnds, constraints = cons)

    #print(sol)
    printStats(sol.x)

    print(stats_List)
    print(rolls_List)

    return stats_List, rolls_List

Stats_DMG = []
Stats_ATK = []
Stats_HP = []
Stats_CR = []
Stats_CD = []
Stats_EM = []

Rolls_ATK = []
Rolls_F_ATK = []
Rolls_HP = []
Rolls_F_HP = []
Rolls_CR = []
Rolls_CD = []
Rolls_EM = []

for i in weaponNameList:

    Stats = optimize(inputParameters, i)[0]
    Rolls = optimize(inputParameters, i)[1]

    Stats_DMG.append(Stats[0])
    Stats_ATK.append(Stats[1])
    Stats_HP.append(Stats[2])
    Stats_CR.append(Stats[3])
    Stats_CD.append(Stats[4])
    Stats_EM.append(Stats[5])

    Rolls_ATK.append(Rolls[0])
    Rolls_F_ATK.append(Rolls[1])
    Rolls_HP.append(Rolls[2])
    Rolls_F_HP.append(Rolls[3])
    Rolls_CR.append(Rolls[4])
    Rolls_CD.append(Rolls[5])
    Rolls_EM.append(Rolls[6])

print(Stats_DMG)
print("Weapons List", weaponNameList)

for i in range(len(weaponNameList)):
    print(Stats_DMG[i], Stats_ATK[i], Stats_HP[i], Stats_CR[i], Stats_CD[i], Stats_EM[i])

stats_List = [Stats_DMG, Stats_ATK, Stats_HP, Stats_CR, Stats_CD, Stats_EM]
rolls_List = [Rolls_ATK, Rolls_F_ATK, Rolls_HP, Rolls_F_HP, Rolls_CR, Rolls_CD, Rolls_EM]

stats_DataFrame = pd.DataFrame(stats_List, columns = ['BlackcliffLongsword','FavoniusSword', 'IronSting', 'LionsRoar', 'PrototypeRancour', 'RoyalLongsword', 'SacrificialSword', 'BlackSword', 'Flute', 'SwordOfDescension', 'FesteringDesire', 'AquilaFavonia', 'SkywardBlade', 'SummitShaper', 'PrimordialJadeCutter', 'FreedomSworn'])
rolls_DataFrame = pd.DataFrame(rolls_List, columns = ['BlackcliffLongsword','FavoniusSword', 'IronSting', 'LionsRoar', 'PrototypeRancour', 'RoyalLongsword', 'SacrificialSword', 'BlackSword', 'Flute', 'SwordOfDescension', 'FesteringDesire', 'AquilaFavonia', 'SkywardBlade', 'SummitShaper', 'PrimordialJadeCutter', 'FreedomSworn'])

print(stats_DataFrame)

stats_DataFrame.to_csv(stats_file_name, sep=',', index = False)
rolls_DataFrame.to_csv(rolls_file_name, sep=',', index = False)
