import os
import json
from typing import Any
from datetime import datetime
from cryptographic_random import CryptographicRandom

class Election_Results:
    def __init__(self,
        state_results:list[dict[str,str|float|int]],
        winner:str,
        rep_electoral_votes:int,
        dem_electoral_votes:int,
        rep_total_votes:int,
        dem_total_votes:int,
    ):
        self.state_results = state_results
        self.winner = winner
        self.rep_electoral_votes:int = rep_electoral_votes
        self.dem_electoral_votes:int = dem_electoral_votes
        self.rep_total_votes:int = rep_total_votes
        self.dem_total_votes:int = dem_total_votes
    
    def __str__(self):
        return f"Winner: {self.winner}\n\n" \
        f"Electoral College (Democrat - Republican):\n{self.dem_electoral_votes:,.0f} - {self.rep_electoral_votes:,.0f}\n\n"\
        f"Popular Vote (Democratic - Republican)\n{self.dem_total_votes:,.0f} - {self.rep_total_votes:,.0f}\n\n"

class Election_Simulator:
    def __init__(self):
        self.load_configuration()
        self.randomizer = CryptographicRandom(
                key=self.configuration.get("Random_Key",None), 
                msg=self.configuration.get("Random_Message",None),
                nonce=self.configuration.get("Nonce",None)
            )
        self.randomize_configuration()
    
    def load_configuration(self):
        try:
            config_path:str = "config.json"
            if(not(os.path.exists(config_path))):
                self.configuration = None
                return None
            with open(config_path,'r',encoding='utf-8') as file:
                configuration = json.load(file)
            if(not(self._verify_configuration(configuration=configuration))):
                self.configuration = None
                return None
            self.configuration:dict|None = configuration
        except:
            self.configuration = None
            return None

    def _verify_configuration(self,configuration:dict|Any):
        if(not(isinstance(configuration,dict))):
            return False
        required_keys:list[str] = [
            "STATES_DATA", "TURNOUT", "MOMENTUM", "MOMENTUM_VOLATILITY", "MOMENTUM_DISTRIBUTION",
            "REP_CANDIDATE_ENERGY", "DEM_CANDIDATE_ENERGY", "CANDIDATE_VOLATILITY", 
            "REP_CANDIDATE_DISTRIBUTION", "DEM_CANDIDATE_DISTRIBUTION"
        ]
        for key in required_keys:
            if(not(key in configuration.keys())):
                return False
        return True

    def randomize_configuration(self):
        self.configuration.update(
            MOMENTUM_DISTRIBUTION=self.randomizer.normal_random(mean=self.configuration["MOMENTUM"],standard_deviation=self.configuration["MOMENTUM_VOLATILITY"]),
            REP_CANDIDATE_DISTRIBUTION=self.randomizer.normal_random(mean=self.configuration["REP_CANDIDATE_ENERGY"],standard_deviation=self.configuration["CANDIDATE_VOLATILITY"]), 
            DEM_CANDIDATE_DISTRIBUTION=self.randomizer.normal_random(mean=self.configuration["DEM_CANDIDATE_ENERGY"],standard_deviation=self.configuration["CANDIDATE_VOLATILITY"]),
            TURNOUT=(self.randomizer.random() * 0.35) + 0.45 
        )

    def process_state(self,state):
        state_votes_cast = max(self.randomizer.normal_random(mean=state[2]*self.configuration["TURNOUT"],standard_deviation=state[2]*0.1),0)
        margin = (self.randomizer.normal_random(mean=state[3],standard_deviation=0.02)+ # Typical margin of error
                    self.configuration["MOMENTUM_DISTRIBUTION"]-
                    self.configuration["REP_CANDIDATE_DISTRIBUTION"]+
                    self.configuration["DEM_CANDIDATE_DISTRIBUTION"]
                )
        margin /= 100
        margin = max(-0.999, min(0.999, margin))
        if(margin > 0): # Democrat won state
            dem_pct = 0.5 + (margin/2)
            rep_pct = 0.5 - (margin/2)
            dem_votes = round(state_votes_cast*dem_pct)
            rep_votes = int(state_votes_cast - dem_votes)
            dem_electoral_votes = state[1]
            rep_electoral_votes = 0
        elif(margin < 0):
            rep_pct = 0.5 - (margin/2)
            dem_pct = 0.5 + (margin/2)
            rep_votes = round(state_votes_cast*rep_pct)
            dem_votes = int(state_votes_cast - rep_votes)
            dem_electoral_votes = 0
            rep_electoral_votes = state[1]
        else:    
            rep_pct = 0.5
            dem_pct = 0.5
            rep_votes = state_votes_cast//2
            dem_votes = rep_votes
            dem_electoral_votes = state[1]/2
            rep_electoral_votes = state[1]/2
            
        return {
            "State": state[0],
            "Dem_Votes": dem_votes,
            "Rep_Votes": rep_votes,
            "Dem_Percent": dem_pct,
            "Rep_Percent": rep_pct,
            "Dem_Electoral_Votes": dem_electoral_votes,
            "Rep_Electoral_Votes": rep_electoral_votes,
        }

    def run_simulated_election(self) -> Election_Results:
        rep_electoral_votes = 0
        dem_electoral_votes = 0
        rep_total_votes = 0
        dem_total_votes = 0
        state_results = []
        for state in self.configuration["STATES_DATA"]:
            state_result = self.process_state(state)
            state_results.append(state_result)
            rep_electoral_votes += state_result["Rep_Electoral_Votes"]
            dem_electoral_votes += state_result["Dem_Electoral_Votes"]
            rep_total_votes += state_result["Rep_Votes"]
            dem_total_votes += state_result["Dem_Votes"]
        if(rep_electoral_votes >= 270):
            winner = "Republican"
        elif(dem_electoral_votes >= 270):
            winner = "Democrat"
        elif((rep_electoral_votes == 269) and (dem_electoral_votes == 269)):
            winner = "Tie"
        else:
            winner = "None"
        return Election_Results(
            state_results=state_results,
            winner = winner,
            rep_electoral_votes=rep_electoral_votes,
            dem_electoral_votes=dem_electoral_votes,
            rep_total_votes=rep_total_votes,
            dem_total_votes=dem_total_votes
        )
        
def main():
    simulator:Election_Simulator = Election_Simulator()
    election_results:list[Election_Results] = []
    winners = {}
    for election_round in range(1_000):
        election_results.append(simulator.run_simulated_election())
        if(not(election_results[-1].winner in winners.keys())):
            winners[election_results[-1].winner] = 1
        else:
            winners[election_results[-1].winner] += 1
        simulator.randomize_configuration()
        if(election_round % 50_000 == 0):
            print(f"{datetime.now()} Rounds Done: {election_round:,.0f}")
    
    total_rep_electoral_votes:int = 0
    total_rep_popular_votes:int = 0
    total_dem_electoral_votes:int = 0
    total_dem_popular_votes:int = 0
    for result in election_results:
        total_rep_electoral_votes += result.rep_electoral_votes
        total_rep_popular_votes += result.rep_total_votes
        total_dem_electoral_votes += result.dem_electoral_votes
        total_dem_popular_votes += result.dem_total_votes
    avg_rep_electoral_votes:float = total_rep_electoral_votes / len(election_results)
    avg_dem_electoral_votes:float = total_dem_electoral_votes / len(election_results)
    avg_rep_popular_votes:float = total_rep_popular_votes / len(election_results)
    avg_dem_popular_votes:float = total_dem_popular_votes / len(election_results)

    print(
        f"Election Winners (Democrat - Republican - Tie - None)\n"
        f"""{winners.get("Democrat",0)} - {winners.get("Republican",0)} - {winners.get("Tie",0)} - {winners.get("None",0)}\n\n"""
        f"Average Electoral College (Democrat - Republican)\n"
        f"{avg_dem_electoral_votes:.3f} - {avg_rep_electoral_votes:.3f}\n\n"
        f"Average Popular Vote (Democrat - Republican)\n"
        f"{avg_dem_popular_votes:,.3f} - {avg_rep_popular_votes:,.3f}\n\n"
        f"{simulator.randomizer.__repr__()}"
    )
        
if __name__ == "__main__":
    main()