# from betsafe import main as df_betsafe
# from XBet import main as df_1xBET
import pandas as pd
import numpy as np

# visualize both dataframes
# betsafe_df=df_betsafe()
# print(betsafe_df.head())

# melbet_df=df_1xBET()
# print(melbet_df.head())

# get the different datasets from the two betting sites
betsafe_df=pd.read_csv("betsafe.csv")
XBet_df=pd.read_csv("1XBet.csv")


# get the matchnames of both datasets
betsafe_df_indices=np.array(betsafe_df["Unnamed: 0"])
XBet_df_indices=np.array(XBet_df["Unnamed: 0"])

# make the matchnames the indexes
betsafe_df.index=list(range(0,len(betsafe_df_indices),1))

print(betsafe_df)
# print(betsafe_df_indices)
# print(XBet_df_indices)

# drill down the individual arrays into simplified arrays for comparison
new_betsafe_matchArr=[]
new_xbet_matchArr=[]

# stripped arrays 
for matchName in betsafe_df_indices:
    match_ARR=matchName.split("vs")
    new_betsafe_matchArr.append(np.array(match_ARR))
for matchNamez in XBet_df_indices:
    match_ARRz=matchNamez.split("vs")
    new_xbet_matchArr.append(np.array(match_ARRz))

# each team name for the XBET
xbetTeamNames=[]
for teams in new_xbet_matchArr:
    for team in teams:
        xbetTeamNames.append(team)

# each teamname for betsafe
betsafeTeamName=np.array(new_betsafe_matchArr).flatten()

# arr for containing which index value has matches in both arrays
countArr=[]

# compare the arrays
listBetsafe=list(betsafeTeamName)
for team in xbetTeamNames:
    if(team in listBetsafe):
        countArr.append(listBetsafe.index(team))
        print(f"{team} is in {listBetsafe.index(team)} of the betsafe")

print("the various counts")
print(countArr)
contigousARR=[]
# the array should take up consecutive numbers
for count,number in enumerate(countArr):
    if(count == len(countArr)-1):
        break
    else:
        if(count>0):
            if(number+1 == countArr[count+1] or number-1 == countArr[count-1]):
                contigousARR.append(number)
        elif (count == 0):
            if(number+1 == countArr[count+1]):
                contigousARR.append(number)

print("The contiguous array")
print(contigousARR)

newContiguousArr=[]
for count,number in enumerate(contigousARR):
    if(countArr[count]%2==0 and countArr[count+1]%2!=0):
        extended=[int(countArr[count]/2),int((countArr[count]/2))+1]
        newContiguousArr.extend(np.array(extended).flatten())

print(newContiguousArr)

# the very very last array
lastIndexes=[]
for index in newContiguousArr:
    if(index%2==0):
        lastIndexes.append(index)


print("the new betsafe df is")
betsafe_df.to_csv("new_betsafe.csv")
print(betsafe_df.index)

for index in list(betsafe_df.index):
    if(index not in lastIndexes):
        betsafe_df.drop(betsafe_df.index[index],axis=0,inplace=True)

print(betsafe_df)

# drop
# save the new dataframe












# for count,matches_betsafe_array in enumerate(new_betsafe_matchArr):
        #     for team_name_betsafe in list(matches_betsafe_array):
        #         if(team_name_betsafe == team_name_XBET):
        #             print(team_name_betsafe)
        #             print(team_name_XBET)
        #             print("a match is found on betsafe")
        #             print("The count is")
        #             print(count)
                   
        #         # compare from XBET to betsafe
        #         if(team_name_XBET in team_name_betsafe == True):
        #             print("we have found a match")
        #         else:
        #             # remove that row from the dataframe
                    
        #             betsafe_df.drop(betsafe_df.index[count],inplace=True)
        #             print(betsafe_df)