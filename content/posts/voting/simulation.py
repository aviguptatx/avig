import random
from collections import defaultdict
import math
import plotly.graph_objects as go

ELECTORAL_VOTES = {
    "Alabama": 9,
    "Alaska": 3,
    "Arizona": 11,
    "Arkansas": 6,
    "California": 54,
    "Colorado": 10,
    "Connecticut": 7,
    "Delaware": 3,
    "District of Columbia": 3,
    "Florida": 30,
    "Georgia": 16,
    "Hawaii": 4,
    "Idaho": 4,
    "Illinois": 19,
    "Indiana": 11,
    "Iowa": 6,
    "Kansas": 6,
    "Kentucky": 8,
    "Louisiana": 8,
    "Maine": 4,
    "Maryland": 10,
    "Massachusetts": 11,
    "Michigan": 15,
    "Minnesota": 10,
    "Mississippi": 6,
    "Missouri": 10,
    "Montana": 4,
    "Nebraska": 5,
    "Nevada": 6,
    "New Hampshire": 4,
    "New Jersey": 14,
    "New Mexico": 5,
    "New York": 28,
    "North Carolina": 16,
    "North Dakota": 3,
    "Ohio": 17,
    "Oklahoma": 7,
    "Oregon": 8,
    "Pennsylvania": 19,
    "Rhode Island": 4,
    "South Carolina": 9,
    "South Dakota": 3,
    "Tennessee": 11,
    "Texas": 40,
    "Utah": 6,
    "Vermont": 3,
    "Virginia": 13,
    "Washington": 12,
    "West Virginia": 4,
    "Wisconsin": 10,
    "Wyoming": 3,
}

STATE_CODES = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

STATE_CENTROIDS = {
    "Alabama": (32.7, -86.7),
    "Alaska": (64.0, -153.0),
    "Arizona": (34.2, -111.6),
    "Arkansas": (34.8, -92.4),
    "California": (37.2, -119.4),
    "Colorado": (39.0, -105.5),
    "Connecticut": (40.8, -72.7),
    "Delaware": (39.0, -75.5),
    "District of Columbia": (38.9, -77.0),
    "Florida": (28.6, -82.4),
    "Georgia": (32.6, -83.4),
    "Hawaii": (20.8, -156.3),
    "Idaho": (44.4, -114.6),
    "Illinois": (40.0, -89.2),
    "Indiana": (39.9, -86.3),
    "Iowa": (42.0, -93.5),
    "Kansas": (38.5, -98.4),
    "Kentucky": (37.5, -85.3),
    "Louisiana": (31.0, -92.0),
    "Maine": (45.4, -69.2),
    "Maryland": (38.2, -76.8),
    "Massachusetts": (42.3, -71.8),
    "Michigan": (43.3, -84.4),
    "Minnesota": (46.3, -94.3),
    "Mississippi": (32.7, -89.7),
    "Missouri": (38.3, -92.4),
    "Montana": (47.0, -109.6),
    "Nebraska": (41.5, -99.8),
    "Nevada": (39.3, -116.6),
    "New Hampshire": (43.2, -71.5),
    "New Jersey": (40.2, -74.7),
    "New Mexico": (34.4, -106.1),
    "New York": (42.9, -75.5),
    "North Carolina": (35.5, -79.8),
    "North Dakota": (47.4, -100.3),
    "Ohio": (40.4, -82.8),
    "Oklahoma": (35.6, -97.5),
    "Oregon": (43.9, -120.6),
    "Pennsylvania": (40.9, -77.8),
    "Rhode Island": (41.5, -70.5),
    "South Carolina": (33.9, -80.9),
    "South Dakota": (44.4, -100.2),
    "Tennessee": (35.8, -86.3),
    "Texas": (31.5, -99.4),
    "Utah": (39.3, -111.7),
    "Vermont": (44.5, -72.7),
    "Virginia": (37.5, -78.8),
    "Washington": (47.4, -120.5),
    "West Virginia": (38.9, -80.4),
    "Wisconsin": (44.6, -89.7),
    "Wyoming": (43.0, -107.5),
}

# State data: (voters, margin, polling_error)
# - voters: number of voters in state
#   - data from https://election.lab.ufl.edu
# - margin: polling margin as fraction (e.g., 0.10 for 55%-45% race)
#   - data from https://www.270towin.com/2024-presidential-election-polls/
#   - except for Alabama, District of Columbia, Hawaii, Idaho, Illinois, Kentucky, Louisiana, Mississippi
#     where we just use the actual results as a proxy (source of these: Wikipedia)
STATE_DATA = {
    "Alabama":              (2270000, .30),
    "Alaska":               (340981, .08),
    "Arizona":              (3428011, .017),
    "Arkansas":             (1190172, .015),
    "California":           (16140044, .248),
    "Colorado":             (3241120, .10),
    "Connecticut":          (1788981, .16),
    "Delaware":             (518330, .185),
    "District of Columbia": (328871, .83),
    "Florida":              (11004209, .062),
    "Georgia":              (5297264, .012),
    "Hawaii":               (522236, .23),
    "Idaho":                (917469, .365),
    "Illinois":             (5705246, .10),
    "Indiana":              (2976581, .165),
    "Iowa":                 (1674011, .047),
    "Kansas":               (1344147, .05),
    "Kentucky":             (2092872, .30),
    "Louisiana":            (2021164, .22),
    "Maine":                (842447, .086),
    "Maryland":             (3062527, .272),
    "Massachusetts":        (3512930, .277),
    "Michigan":             (5706503, .018),
    "Minnesota":            (3272414, .062),
    "Mississippi":          (1250000, .22),
    "Missouri":             (3000000, .15),
    "Montana":              (612423, .18),
    "Nebraska":             (965236, .15),
    "Nevada":               (1487887, .006),
    "New Hampshire":        (831467, .05),
    "New Jersey":           (4321921, .164),
    "New Mexico":           (928290, .06),
    "New York":             (8381429, .176),
    "North Carolina":       (5723987, .013),
    "North Dakota":         (371975, .27),
    "Ohio":                 (5851387, .077),
    "Oklahoma":             (1575000, .16),
    "Oregon":               (2308256, .12),
    "Pennsylvania":         (7075000, 0),
    "Rhode Island":         (523402, .14),
    "South Carolina":       (2566404, .117),
    "South Dakota":         (436478, .265),
    "Tennessee":            (3080000, .21),
    "Texas":                (11400000, .074),
    "Utah":                 (1525885, .255),
    "Vermont":              (372885, .32),
    "Virginia":             (4537976, .058),
    "Washington":           (3961569, .193),
    "West Virginia":        (770587, .27),
    "Wisconsin":            (3437142, .011),
    "Wyoming":              (271123, .385),
}


def p_decisive_in_state(n_voters, margin, polling_error):
    r = polling_error
    m = margin
    n = n_voters
    
    coefficient = 0.5 / (r * n * math.sqrt(2 * math.pi))
    exponent = -m**2 / (8 * r**2)
    
    return coefficient * math.exp(exponent)


def simulate_banzhaf(num_simulations):
    states = list(ELECTORAL_VOTES.keys())
    pivotal_counts = defaultdict(int)

    winning_threshold = 270

    for _ in range(num_simulations):
        outcomes = {state: random.random() < 0.5 for state in states}

        candidate_a_evs = sum(
            ELECTORAL_VOTES[state] for state, won in outcomes.items() if won
        )

        for state in states:
            state_evs = ELECTORAL_VOTES[state]

            if outcomes[state]:
                evs_without = candidate_a_evs - state_evs
                if candidate_a_evs >= winning_threshold and evs_without < winning_threshold:
                    pivotal_counts[state] += 1
            else:
                evs_with = candidate_a_evs + state_evs
                if candidate_a_evs < winning_threshold and evs_with >= winning_threshold:
                    pivotal_counts[state] += 1

    return {
        state: count / num_simulations
        for state, count in pivotal_counts.items()
    }


def format_ev(value):
    if value >= 1000:
        return f"${value/1000:.1f}k"
    elif value >= 1:
        return f"${value:.0f}"
    else:
        return ""


def create_map(results):
    locations = [STATE_CODES[r["state"]] for r in results]
    values = [r["p_vote_decisive"] * 500e9 if r["p_vote_decisive"] else 0 for r in results]

    fig = go.Figure(data=go.Choropleth(
        locations=locations,
        z=values,
        locationmode='USA-states',
        hoverinfo='skip',
        colorscale=[
            [0, '#f7fcf5'],
            [0.15, '#e5f5e0'],
            [0.3, '#c7e9c0'],
            [0.45, '#a1d99b'],
            [0.6, '#74c476'],
            [0.75, '#41ab5d'],
            [0.9, '#238b45'],
            [1, '#1a7838']
        ],
        colorbar=dict(
            title="EV ($)",
            thickness=20,
            len=0.6,
            y=0.5,
            yanchor='middle',
            tickformat='$,.0f'
        ),
        marker=dict(
            line=dict(
                color='white',
                width=1.5
            )
        )
    ))

    lats = [STATE_CENTROIDS[r["state"]][0] for r in results]
    lons = [STATE_CENTROIDS[r["state"]][1] for r in results]
    labels = [format_ev(r["p_vote_decisive"] * 500e9) if r["p_vote_decisive"] else "" for r in results]

    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lat=lats,
        lon=lons,
        text=labels,
        mode='text',
        textfont=dict(
            size=8,
            color='black'
        ),
        hoverinfo='skip'
    ))

    fig.update_layout(
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            bgcolor='rgba(0,0,0,0)',
            showland=False,
            showcountries=False,
            showcoastlines=False,
            showframe=False
        ),
        height=400,
        margin=dict(t=0, b=0, l=0, r=60),
        paper_bgcolor='white',
        plot_bgcolor='white',
        dragmode=False,
        showlegend=False
    )

    return fig


if __name__ == "__main__":
    banzhaf_results = simulate_banzhaf(10_000_000)
    
    results = []
    for state in ELECTORAL_VOTES:
        voters, margin = STATE_DATA[state]
        
        p_state = p_decisive_in_state(voters, margin, polling_error=.05)
        p_vote = p_state * banzhaf_results[state]
        
        results.append({
            "state": state,
            "evs": ELECTORAL_VOTES[state],
            "voters": voters,
            "margin": margin,
            "p_decisive_state": p_state,
            "p_state_decisive": banzhaf_results[state],
            "p_vote_decisive": p_vote,
        })
    
    results.sort(key=lambda x: (x["p_vote_decisive"] is None, -(x["p_vote_decisive"] or 0)))
    
    print("\n| State | P(vote flips state) | P(state flips election) | EV |")
    print("|-------|--------------------:|------------------------:|---:|")
    for r in results:
        state_code = STATE_CODES[r['state']]
        p_decisive_state_str = f"{r['p_decisive_state']:.2e}" if r['p_decisive_state'] else "—"
        p_state_decisive_str = f"{r['p_state_decisive']:.2%}" if r['p_state_decisive'] else "—"
        expected_value = r['p_vote_decisive'] * 500e9 if r['p_vote_decisive'] else 0
        ev_str = f"${expected_value:,.0f}" if expected_value else "—"

        print(f"| {state_code} | {p_decisive_state_str} | {p_state_decisive_str} | {ev_str} |")
    
    fig = create_map(results)
    
    fig.show()
    
    fig.write_html(
        "voting_map.html",
        config={
            "scrollZoom": False,
            "displayModeBar": False,
            "doubleClick": False,
            "staticPlot": False
        }
    )
