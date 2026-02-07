import states_data
import numpy as np
from pandas import DataFrame
from dataclasses import dataclass

@dataclass
class Federal:
    voter_turnout:float # On a federal level, how many more or less voters are expected to turn out
    political_direction:float

@dataclass
class Federal_Rural:
    voter_turnout:float # On a federal level, how many more or less voters are expected to turn out in rural areas
    voter_turnout_volatility:float # How much does the rural voter turnout fluctuate from election to election? (higher means more unpredictable)

@dataclass
class Federal_Urban:
    voter_turnout:float # On a federal level, how many more or less voters are expected to turn out in urban areas
    voter_turnout_volatility:float # How much does the urban voter turnout fluctuate from election to election? (higher means more unpredictable)

@dataclass
class Urban:
    voter_percent:float # What percentage of the total voters are in urban areas
    voter_margin:float # How much more likely are urban voters to vote for one party over the other (positive for Republicans, negative for Democrats)
    voter_margin_volatility:float # How much does the urban voter turnout and political direction fluctuate from election to election? (higher means more unpredictable)

@dataclass
class Rural:
    voter_percent:float # What percentage of the total voters are in rural areas
    voter_margin:float # How much more likely are rural voters to vote for one party over the other (positive for Republicans, negative for Democrats)
    voter_margin_volatility:float # How much does the rural voter turnout and political direction fluctuate from election to election? (higher means more unpredictable)   

@dataclass
class State:
    name:str
    base_voters:int
    electoral_votes:int
    avg_margin:float
    margin_volatility:float
    voter_volatility:float
    rural_voters:Rural
    urban_voters:Urban
    
class ElectionSimulator():
    def __init__(self,federal:Federal,federal_urban:Federal_Urban,federal_rural:Federal_Rural,states:list[State]):
        self.federal:Federal = federal
        self.federal_rural:Federal_Rural = federal_rural
        self.federal_urban:Federal_Urban = federal_urban
        self.states:list[State] = states
        
    def simulate_state_election(self,state:State):
        # Simulate voter turnout
        total_number_of_votes:int = int(np.random.normal(loc=state.base_voters+(state.base_voters*self.federal.voter_turnout), 
                                           scale=state.voter_volatility))
        rural_base_votes = int(total_number_of_votes * state.rural_voters.voter_percent)
        rural_turnout = np.random.normal(loc=rural_base_votes, scale=rural_base_votes*self.federal_rural.voter_turnout_volatility)
        rural_votes = int(rural_turnout)
        
        rural_margin = np.random.normal(loc=state.rural_voters.voter_margin+self.federal.political_direction, scale=(state.rural_voters.voter_margin_volatility))
        rural_rep_votes = int(rural_votes * (0.5 + ((rural_margin / 100)/2)))
        rural_dem_votes = rural_votes - rural_rep_votes

        urban_base_votes = int(total_number_of_votes * state.urban_voters.voter_percent)
        urban_turnout = np.random.normal(loc=urban_base_votes, scale=urban_base_votes*self.federal_urban.voter_turnout_volatility)
        urban_votes = int(urban_turnout)

        urban_margin = np.random.normal(loc=state.urban_voters.voter_margin+self.federal.political_direction, scale=(state.urban_voters.voter_margin_volatility))
        urban_rep_votes = int(urban_votes * (0.5 + ((urban_margin / 100)/2)))
        urban_dem_votes = urban_votes - urban_rep_votes

        turnout = rural_votes + urban_votes
        rep_votes = rural_rep_votes + urban_rep_votes
        dem_votes = rural_dem_votes + urban_dem_votes

        if rep_votes > dem_votes:
            winner = 'Republican'
        elif dem_votes > rep_votes:
            winner = 'Democrat'
        else:
            winner = 'Tie'
        
        return [winner, turnout, rep_votes, dem_votes, (rep_votes/turnout*100 if turnout > 0 else 0), (dem_votes/turnout*100 if turnout > 0 else 0), rural_votes,rural_rep_votes, rural_dem_votes, urban_votes, urban_rep_votes, urban_dem_votes]
    
    def simulate_election(self):
        results = []
        for state in self.states:
            results.append(self.simulate_state_election(state))
        return results
        
def main():
    federal:Federal = Federal(voter_turnout=0.0, political_direction=0)
    federal_rural:Federal_Rural = Federal_Rural(voter_turnout=0.0, voter_turnout_volatility=0.0)
    federal_urban:Federal_Urban = Federal_Urban(voter_turnout=0.0, voter_turnout_volatility=0.0)
    simulator:ElectionSimulator = ElectionSimulator(federal=federal, federal_urban=federal_urban, federal_rural=federal_rural, states=states_data.states_data)
    
    results = simulator.simulate_election()
    df = DataFrame(results, columns=['Winner', 'Total_Turnout', 'Total_Rep_Votes', 'Total_Dem_Votes', 
                                        'Rep_Votes_Percent', 'Dem_Votes_Percent',
                                        'Total_Rural_Votes', 'Rural_Rep_Votes', 'Rural_Dem_Votes', 
                                        'Total_Urban_Votes', 'Urban_Rep_Votes', 'Urban_Dem_Votes'], 
                                        index=[state.name for state in states_data.states_data])
    print(df.to_csv(index=True,float_format='%.2f'))

if __name__ == "__main__":    
    main()