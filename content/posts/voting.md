+++
date = '2025-12-12T14:05:41-08:00'
title = 'Voting in the presidential election'
+++

# EV of a presidential vote
How much is your presidential vote worth in the United States? The expected value of your vote depends on two things: the probability your vote changes the outcome of the entire election, and the value that is gained from this change in outcome. Mathematically, we have:

$$EV = P(\text{vote flips state}) \times P(\text{state flips election}) \times \Delta V$$

where \\(\Delta V\\) is the value difference between your preferred candidate winning versus losing. We'll build up each component in turn.

## Probability a single vote matters
### Normal distribution as an approximator

When we aggregate many polls, each poll is sampling from the same underlying population of voters. The Central Limit Theorem[^1] tells us that the average of these poll results will be approximately normally distributed, regardless of the underlying distribution of voter preferences.

### Splitville

Consider a small state called Splitville with:
- 100 voters (excluding you), all of whom will vote
- Two candidates: Alice and Bob
- Polls show a 50%–50% tie
- Polling error with a standard deviation of 5 percentage points

We model the number of votes for Alice as a normal distribution centered at \\(\mu = 50\\) (the polled expectation) with standard deviation \\(\sigma = 5\\) (the polling error, expressed in votes).

Your vote is decisive if Alice would otherwise receive exactly 50 votes, producing a tie. We can find this probability using the normal distribution's probability density function:

$$
\text{pdf}(x) = \frac{1}{\sigma \sqrt{2\pi}}
\exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
$$

Since vote counts are integers but the normal distribution is continuous, we apply a *continuity correction* and integrate over the interval \\([49.5, 50.5]\\):

$$
P_{\text{tie}} \approx
\int_{49.5}^{50.5}
\frac{1}{5 \sqrt{2\pi}}
\exp\left(
-\frac{(x - 50)^2}{2 \cdot 5^2}
\right)
dx
$$

This evaluates to 0.0797, or about an 8% chance of a tie in Splitville.

### Generalizing

Now let's generalize. Define:
- \\(N\\) = number of voters (excluding you)
- \\(m\\) = polling margin as a fraction (e.g., a 55%–45% lead means \\(m = 0.10\\))
- \\(r\\) = polling error as a fraction of voters

Your candidate's expected vote count is \\(N \cdot (0.5 + m/2)\\), and the standard deviation is \\(rN\\). A tie occurs at \\(N/2\\) votes for each candidate.

The probability of a tie becomes:

$$
P_{\text{tie}}(N, m, r) =
\int_{\frac{N-1}{2}}^{\frac{N+1}{2}}
\frac{1}{rN \sqrt{2\pi}}
\exp\left(
-\frac{\left(x - N(0.5 + m/2)\right)^2}{2(rN)^2}
\right)
dx
$$

For large \\(N\\), the pdf barely changes over a single-vote interval, so we can use a midpoint Riemann approximation by evaluating at the midpoint \\(x = N/2\\) and multiplying by the interval width (which is 1):

$$
P_{\text{tie}}(N, m, r) \approx
\frac{1}{rN \sqrt{2\pi}}
\exp\left(
-\frac{\left(\frac{N}{2} - N(0.5 + m/2)\right)^2}{2(rN)^2}
\right)
$$

Simplifying, we get:

$$
P_{\text{tie}}(N, m, r) \approx
\frac{1}{rN \sqrt{2\pi}}
\exp\left(
-\frac{N^2 m^2 / 4}{2 r^2 N^2}
\right)=
\frac{1}{rN \sqrt{2\pi}}
\exp\left(
-\frac{m^2}{8r^2}
\right)
$$

We still have one last wrinkle to iron out. Our formula assumes an even number of other voters, where your vote can break an exact tie. But if there's an odd number of other voters, no exact tie is possible -- instead, your vote matters only if your candidate is losing by exactly one vote and wins the resulting tiebreaker (assume a coin flip).

Let \\(p\\) be the probability density at the tie point. In both cases, we need to account for tiebreaker mechanics (assume a coin flip):
- Even \\(N\\): A tie occurs with probability \\(p\\). Without your vote, you candidate wins the tiebreaker with probability \\(0.5\\).
- Odd \\(N\\): Your candidate trails by exactly one vote with probability \\(p\\). Without your vote, they lose. With your vote, it's a tie, and they need to win the tiebreaker with probability \\(0.5\\).

In either case, the probability of your vote flipping the state election is \\(0.5p\\). Thus:

$$
P_{\text{vote flips state}}(N, m, r) \approx
\frac{0.5}{rN \sqrt{2\pi}}
\exp\left(
-\frac{m^2}{8r^2}
\right)
$$


#### Observations
- Fairly intuitively, your vote's impact is inversely proportional to \\(N\\).
- In a true toss-up, the exponential term becomes \\(e^0 = 1\\), and \\(p_{\text{vote flips state}}(N,r)\approx \frac{0.2}{rN}\\)

### Factoring in your state's decisiveness

Even if your vote decides your state, your state's electoral votes must also decide the presidential election for your vote to be truly decisive. We still need to estimate \\(P(\text{state flips election})\\).

#### Banzhaf power index
The [Banzhaf power index](https://en.wikipedia.org/wiki/Banzhaf_power_index) is meant to estimate the probability a voter (or voting bloc) is pivotal in a weighted voting system. The calculation enumerates all winning coalitions, then counts the proportion in which flipping the bloc's vote changes the outcome.

Computing this would require checking all possible combinations of state outcomes. With 51 voting blocs[^2] (50 states + DC), that's \\(2^{51}\\) combinations -- not practical to enumerate. Instead, we'll estimate via Monte Carlo simulation:
  1. For each state except yours, flip a fair coin to determine the winner
  2. Sum up your candidate's electoral votes from those other states
  3. Check if your state is pivotal: does adding its electoral votes swing the election?

Repeating this millions of times gives us a stable estimate of each state's structural power in the Electoral College.

### Limitations
Both calculations -- the state-level tie probability and the Banzhaf simulation -- treat outcomes as independent. In reality, polling errors are highly correlated across states. A national polling miss (say, systematically undersampling non-college voters) shifts all states in the same direction. If Pennsylvania's polls underestimate your candidate by 3 points, Wisconsin and Michigan probably do too. This correlation has two effects, neither or which we account for:
  1. Swing states tend to tip together, making the "tipping point state" more predictable than our model suggests
  2. Conditional on the election being close nationally, it's more likely to be close in multiple swing states simultaneously

A better approach would be to model state outcomes as draws from a multivariate normal distribution with correlations estimated from historical polling errors.

## Value of the election
The final term is \\(\Delta V\\) -- the value difference between candidates. This represents the difference in "societal good" created between the two candidates. You can think of this as the value of the donation you get to make if your vote ends up being decisive. This is the hardest to estimate: beyond monetary considerations, there are social and geopolitical factors that we cannot put a price tag on. That being said, we are after an order-of-magnitude estimate, so let the hand waving begin.

### The federal budget as a proxy
The 2024 federal budget was about $6.8T. About $1T goes to paying interest, and about $4T goes to mandatory spending, such as Social Security and Medicare. The president cannot really influence the former, and influencing the latter requires legislation. Thus to start our order-of-magnitude estimate, let's focus on discretionary spending, which is about $1.8T. Over 4 years, this amounts to $7.2T. Within the discretionary bucket, candidates don't fully differ -- both will still fund the military, run agencies, and pay benefits. So what we really care about are the marginal differences. If our preferred candidate is 10% more effective with this money, that gives us $720B. The president also influences via legislation, Supreme Court appointments, foreign policy, etc. which are hard to quantify. Together with the difference in discretionary spending, we can estimate:
$$\Delta V \approx 1T$$

### Confidence factor
Since most voters (including myself) are not 100% confident in their vote, we should also apply a confidence discount factor. Even if you are very confident in your vote, policies can have second-order effects that are hard to predict [^3], so you should still discount this number. Applying a moderate \\(c=0.5\\) gives us:
$$\Delta V \approx 500B$$

## Applying this to the 2024 US Presidential Election
Let's apply this framework to the 2024 presidential race. We used historical state-level polling margins and assumed a 5% polling error for each state and a \\(\Delta V\\) of 500B, then ran 100 million simulations[^4] to estimate \\(P(\text{state flips election})\\) for each state. Here are some sample results:
| State | Voters | Margin | P(vote flips state) | P(state flips election) | P(vote decisive) | EV |
|-------|-------:|-------:|---------------------:|------------------:|-----------------:|---------------:|
| AK | 340,981 | 8.0% | 8.50e-06 | 2.27% | 1.93e-07 | $96,579 |
| AR | 1,190,172 | 1.5% | 3.31e-06 | 4.54% | 1.50e-07 | $75,192 |
| ... | ... | ... | ...| ... | ... | ... |
| ID | 917,469 | 36.5% | 5.56e-09 | 3.02% | 1.68e-10 | $84 |
| DC | 328,871 | 83.0% | 1.33e-20 | 2.27% | 3.02e-22 | $0 |

And a graph of these (hover over states to see details):
<iframe
  src="/plots/voting_map.html"
  width="100%"
  height="420"
  frameborder="0">
</iframe>

# Analysis
## Voting EV
The EV of a vote ranges from $84 (Idaho) to $97k (Alaska). A vote in Alaska is ~1000 times more valuable than a vote in Idaho (regardless of the value one assigns to the election itself). The chance of a vote swinging the entire election ranges from ~1 in 6 billion in Idaho to ~1 in 5 million in Alaska.

Oh, and then there is DC, where a voter has an astronomically small \\(3.02\times 10^{-22}\\) chance of swinging an election. Put another way, if a DC voter had these chances and voted in a separate election for every single grain of sand on Earth, they would only have about a 0.2% chance of flipping a single election.

## What can I do in $INSERT_NONSWING_STATE?

### Political activism
Convincing an undecided person to vote for your preferred candidate in Alaska has an EV of $97k.
To put this into perspective, suppose you live in Idaho (where your vote is worth $84). Voting in your state's election is roughly equivalent to reaching out to a single person in Alaska who is currently undecided and ~brainwashing~ convincing them to vote for your candidate at a mere 1/1000 success rate.

### Vote swap
In the current equilibrium of the U.S., due to the two party system, there are only two candidates ever "worth" voting for if you think in terms of expected value. That being said, there are still some people who vote for independent candidates, knowing damn well it is 0 EV but presumably to "rage against the dying of the light" (as my friend put it), among other reasons.

This opens to the door to [vote swapping](https://en.wikipedia.org/wiki/Vote_swapping). If Dave the Democrat lives in a decided state (e.g. DC) and has a third-party friend Trent who lives in a swing state (who prefers Democrat to Republican), a swap can be arranged, where Trent votes Democrat and Dave votes third-party, and both people are happier. This is legal in the U.S., but of course requires trust to function.

### Ignore the numbers
This analysis treats voting as a means to an end in order to achieve some dollar amount of societal benefit. But there are still many reasons to vote -- self-expression, upholding civic duty, and enacting a forcing function on oneself to become more polictically informed and active -- all good things.

[^1]: [This 3Blue1Brown video](https://youtu.be/zeJD6dqJ5lo?si=7vb6GaENWJ9uYh4o) is a good explainer on the Central Limit Theorem.
[^2]: Note that we treat Maine and Nebraska as single blocs in this analysis; in reality, these states allocate electoral votes by district rather than winner-take-all.
[^3]: There are plently of examples of this -- see the [Great Hanoi Rat Massacre](https://en.wikipedia.org/wiki/Great_Hanoi_Rat_Massacre) as one of my favorites. Or consider that electing the worse candidate might be bad in the short-term but provoke reform and ends up being long-term net good.
[^4]: [Source code](https://github.com/aviguptatx/avig/tree/main/content/posts/voting/simulation.py).