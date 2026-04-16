import random
import numpy as np

STATES_DATA = [
    ("Alabama", 9, 3700000, -25.5),
    ("Alaska", 3, 590000, -10.1),
    ("Arizona", 11, 4400000, -0.1),
    ("Arkansas", 6, 2300000, -27.6),
    ("California", 54, 22000000, 29.2),
    ("Colorado", 10, 4000000, 13.5),
    ("Connecticut", 7, 2600000, 20.1),
    ("Delaware", 3, 780000, 19.0),
    ("Florida", 30, 14500000, 3.4),
    ("Georgia", 16, 7600000, -0.5),
    ("Hawaii", 4, 950000, 29.5),
    ("Idaho", 4, 1450000, -30.8),
    ("Illinois", 19, 8500000, 17.1),
    ("Indiana", 11, 4800000, -16.0),
    ("Iowa", 6, 2300000, -8.2),
    ("Kansas", 6, 2200000, -14.7),
    ("Kentucky", 8, 3400000, -25.9),
    ("Louisiana", 8, 3200000, -18.6),
    ("Maine", 4, 1250000, 9.1),
    ("Maryland", 10, 4200000, 33.2),
    ("Massachusetts", 11, 5100000, 33.1),
    ("Michigan", 15, 7700000, 2.8),
    ("Minnesota", 10, 4100000, 7.1),
    ("Mississippi", 6, 2200000, -16.5),
    ("Missouri", 10, 4400000, -15.4),
    ("Montana", 4, 900000, -16.4),
    ("Nebraska", 5, 1250000, -19.2),
    ("Nevada", 6, 2000000, 2.4),
    ("New Hampshire", 4, 1100000, 7.4),
    ("New Jersey", 14, 6400000, 15.9),
    ("New Mexico", 5, 1400000, 10.8),
    ("New York", 28, 12600000, 23.1),
    ("North Carolina", 16, 7300000, -1.4),
    ("North Dakota", 3, 650000, -33.3),
    ("Ohio", 17, 8200000, -8.0),
    ("Oklahoma", 7, 2400000, -33.1),
    ("Oregon", 8, 3200000, 16.0),
    ("Pennsylvania", 19, 8800000, 0.8),
    ("Rhode Island", 4, 820000, 20.8),
    ("South Carolina", 9, 3800000, -11.7),
    ("South Dakota", 3, 700000, -26.2),
    ("Tennessee", 11, 4700000, -23.3),
    ("Texas", 40, 17600000, -5.6),
    ("Utah", 6, 1900000, -20.5),
    ("Vermont", 3, 580000, 35.1),
    ("Virginia", 13, 6000000, 10.1),
    ("Washington", 12, 5400000, 19.2),
    ("West Virginia", 4, 1200000, -38.9),
    ("Wisconsin", 10, 4400000, 0.9),
    ("Wyoming", 3, 470000, -43.4),
]

TURNOUT = 0.7 # Percent voters
MOMENTUM = 3.6 # Potential swing average at a national level
MOMENTUM_VOLATILITY = 0.6
REP_CANDIDATE_ENERGY = 0 # How motivating republican candidate gets voter turnout. Higher number means more Republican turnout
DEM_CANDIDATE_ENERGY = 0 # How motivating democrat candidate gets voter turnout. Higher number means more Democrat turnout
CANDIDATE_VOLATILITY = 0.2

def main():
    state = STATES_DATA[0]
    state_votes_cast = np.random.normal(state[2]*TURNOUT,state[2]*0.02)
    margin = np.random.normal(state[3],0.015)+\ # Typical margin of error
                np.random.normal(MOMENTUM,MOMENTUM_VOLATILITY)-\
                np.random.normal(REP_CANDIDATE_ENERGY,CANDIDATE_VOLATILITY)+\
                np.random.normal(DEM_CANDIDATE_ENERGY,CANDIDATE_VOLATILITY)
    if(margin > 0): # Democrat won state
        dem_pct = 0.5 + (margin/2)
        rep_pct = 0.5 - (margin/2)
        dem_votes = round(state_votes_cast*dem_pct)
        rep_votes = state_votes_cast - dem_votes
    elif(margin < 0):
        rep_pct = 0.5 + (margin/2)
        dem_pct = 0.5 - (margin/2)
        rep_votes = round(state_votes_cast*rep_pct)
        dem_votes = state_votes_cast - rep_votes
    else:    
        rep_pct = 0.5
        dem_pct = 0.5
        rep_votes = state_votes_cast//2
        dem_votes = rep_votes
        
    print(f"{state[0]:\n" +
    f"Democrat Votes: {dem_votes:,.0f}\n" +
    f"Republican Votes: {rep_votes:,.0f}\n" +
    f"Democrat Percent: {dem_pct*100:,.3f}%\n" +
    f"Republican Percent: {rep_pct*100:,.3f}%\n")

if __name__ == "__main__":
    main()