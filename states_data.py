from election_simulator import State, Rural, Urban

alabama:State = State(
    name='Alabama',
    base_voters=2_000_000,
    electoral_votes=9,
    avg_margin=25,
    margin_volatility=4,
    voter_volatility=200_000,
    rural_voters=Rural(
        voter_percent=0.65,
        voter_margin=60,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.35,
        voter_margin=-30,
        voter_margin_volatility=5
    )
)

alaska:State = State(
    name='Alaska',
    base_voters=360_000,
    electoral_votes=3,
    avg_margin=10,
    margin_volatility=3,
    voter_volatility=30_000,
    rural_voters=Rural(
        voter_percent=0.55,
        voter_margin=40,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.45,
        voter_margin=-20,
        voter_margin_volatility=5
    )
)

arizona:State = State(
    name='Arizona',
    base_voters=3_000_000,
    electoral_votes=11,
    avg_margin=1,
    margin_volatility=2.5,
    voter_volatility=200_000,
    rural_voters=Rural(
        voter_percent=0.25,
        voter_margin=20,
        voter_margin_volatility=6
    ),
    urban_voters=Urban(
        voter_percent=0.75,
        voter_margin=-5,
        voter_margin_volatility=3
    )
)

arkansas:State = State(
    name='Arkansas',
    base_voters=1_000_000,
    electoral_votes=6,
    avg_margin=20,
    margin_volatility=4,
    voter_volatility=100_000,
    rural_voters=Rural(
        voter_percent=0.75,
        voter_margin=44,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.25,
        voter_margin=-20,
        voter_margin_volatility=5
    )
)

california:State = State(
    name='California',
    base_voters=15_000_000,
    electoral_votes=55,
    avg_margin=-25,
    margin_volatility=4,
    voter_volatility=1_000_000,
    rural_voters=Rural(
        voter_percent=0.12,
        voter_margin=30,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.88,
        voter_margin=-30,
        voter_margin_volatility=5
    )
)

colorado:State = State(
    name='Colorado',
    base_voters=3_000_000,
    electoral_votes=10,
    avg_margin=-12,
    margin_volatility=3,
    voter_volatility=200_000,
    rural_voters=Rural(
        voter_percent=0.28,
        voter_margin=27,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.72,
        voter_margin=-22,
        voter_margin_volatility=3
    )
)

connecticut:State = State(
    name='Connecticut',
    base_voters=1_600_000,
    electoral_votes=7,
    avg_margin=-18,
    margin_volatility=3,
    voter_volatility=150_000,
    rural_voters=Rural(
        voter_percent=0.30,
        voter_margin=14,
        voter_margin_volatility=2
    ),
    urban_voters=Urban(
        voter_percent=0.70,
        voter_margin=-25,
        voter_margin_volatility=3
    )
)

delaware:State = State(
    name='Delaware',
    base_voters=450_000,
    electoral_votes=3,
    avg_margin=-20,
    margin_volatility=3,
    voter_volatility=50_000,
    rural_voters=Rural(
        voter_percent=0.33,
        voter_margin=10,
        voter_margin_volatility=1
    ),
    urban_voters=Urban(
        voter_percent=0.67,
        voter_margin=-25,
        voter_margin_volatility=2
    )
)

florida:State = State(
    name='Florida',
    base_voters=9_000_000,
    electoral_votes=29,
    avg_margin=0,
    margin_volatility=3,
    voter_volatility=500_000,
    rural_voters=Rural(
        voter_percent=0.40,
        voter_margin=20,
        voter_margin_volatility=5
    ),
    urban_voters=Urban(
        voter_percent=0.60,
        voter_margin=-10,
        voter_margin_volatility=4
    )
)

states_data:list[State] = [alabama, alaska, arizona, arkansas, california, colorado, connecticut, delaware, florida]