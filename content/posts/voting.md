+++
date = '2025-12-22T14:05:41-08:00'
title = 'The value of voting in the U.S.'
+++

I like to think I'm principled in my approach to life. I don't play the lottery. I buy the cheapest apartment insurance possible. I've run the numbers. 

So why the hell do I vote?

By a back-of-the-envelope estimate, future me will waste about ten hours of my life voting in federal elections. Ten hours for something I’m pretty sure is useless. This is deeply unsettling, so naturally, I sat down and spent far more than ten hours proving whether those ten hours were, in fact, going to be wasted.

# Formulation
The expected value of your vote depends on two things: the chance your vote changes the election outcome, and the altruistic value of your preferred candidate winning the election. Mathematically, we have:

<div class="small-equation-mobile">

$$EV = \underbrace{P(\text{vote flips state}) \times P(\text{state flips election})}_{\text{chance vote flips election}} \times \underbrace{\Delta V}_{\text{altruistic value of election}}$$

</div>

### A note on \(\Delta V\): why altruistic value?
We use \(\Delta V\) to represent the *altruistic* value difference between two candidates -- not the personal gain. Why?

Voting for personal gain simply doesn't make sense. Even if you somehow valued the election at $1 million for yourself, the probability terms are so small that your EV would be ~$0. No rational self-interested actor should vote.

The only lens under which voting makes mathematical sense is the altruistic one: the aggregate value created for society if your preferred candidate wins. So that's what we'll estimate.

Let's calculate each component, starting with the probability your vote flips your state.

## P(vote flips state)
### Normal distribution as an approximator

When we aggregate many polls, the Central Limit Theorem[^1] tells us their average will be approximately normally distributed, regardless of the underlying distribution of voter preferences.

### Splitville

Consider a small state called Splitville with:
- 100 voters (excluding you), all of whom will vote
- Two candidates: Alice and Bob
- Polls show a 50%–50% tie
- Polling error with a standard deviation of 5 percentage points

We model the number of votes for Alice as a normal distribution centered at \(\mu = 50\) (the polled expectation) with standard deviation \(\sigma = 5\) (the polling error, expressed in votes).

Your vote is decisive if Alice would otherwise receive exactly 50 votes. We can find this probability using the normal distribution's probability density function:

$$
\text{pdf}(x) = \frac{1}{\sigma \sqrt{2\pi}}
\exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
$$

Since vote counts are integers but the normal distribution is continuous, we apply a *continuity correction* and integrate over the interval \([49.5, 50.5]\):

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

Generalizing, define:
- \(N\) = number of voters (excluding you)
- \(m\) = polling margin as a fraction (e.g., a 55%–45% lead means \(m = 0.10\))
- \(r\) = polling error as a fraction of voters, \(r \neq 0\)[^2]

Your candidate's expected vote count is \(N \cdot (0.5 + m/2)\), and the standard deviation is \(rN\). A tie occurs at \(N/2\) votes for each candidate.

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

For large \(N\), the pdf barely changes over a single-vote interval, so we can use a midpoint Riemann approximation by evaluating at the midpoint \(x = N/2\) and multiplying by the interval width (which is 1):

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

Finally, we have to multiply by a factor of 0.5 to account for tiebreaker mechanics[^3], which we must factor in for both even and odd \(N\):

$$
P_{\text{vote flips state}}(N, m, r) \approx
\frac{0.5}{rN \sqrt{2\pi}}
\exp\left(
-\frac{m^2}{8r^2}
\right)
$$


#### Observations
- Your vote's impact is inversely proportional to \(N\).
- In a true toss-up (\(m=0\)), the exponential term becomes \(e^0 = 1\), and \(p_{\text{vote flips state}}(N,r)\approx \frac{0.2}{rN}\)

## P(state flips election)
We now know the probability of a vote flipping your state, but we still need to determine the probability that this event flips the entire election result.

The [Banzhaf power index](https://en.wikipedia.org/wiki/Banzhaf_power_index) measures exactly this: the probability that a voting bloc is pivotal in a weighted voting system. The calculation enumerates all possible voter coalitions, then counts the proportion of these in which flipping the bloc's vote changes the outcome.

Computing this would require checking all possible combinations of state outcomes. With 51 voting blocs[^4] (50 states + DC), that's \(2^{51}\) combinations -- not practical to enumerate. 

### Monte Carlo simulation
Instead, we'll estimate via Monte Carlo simulation. The algorithm:
1. Generate a randomized election: for each state, flip a fair coin to determine the winner
2. Sum electoral votes for candidate A, call this \(E_A\)
3. Check pivotality for each state \(s\):
   - Let \(V_s\) represent the number of electoral votes that state \(s\) is worth
   - If candidate A won state \(s\):
     - Is \(E_A \geq 270\) but \(E_A - \text{V}_s < 270\)?
   - If candidate A lost state \(s\):
     - Is \(E_A < 270\) but \(E_A + \text{V}_s \geq 270\)?
   - If either condition holds, state \(s\) is pivotal in this simulation

For each state, \(P(\text{state flips election})\) evaluates to the proportion of simulations in which the state was pivotal. Repeating this simulation millions of times gives us an estimate of each state's structural power in the Electoral College.

## Limitations
Both calculations -- the state-level tie probability and the Banzhaf simulation -- treat outcomes as independent. In reality, polling errors are correlated across states. A national polling miss (say, systematically undersampling non-college voters) shifts all states in the same direction. In 2024, the seven main swing states (PA, MI, WI, GA, NC, AZ, NV) all moved in the same direction. This correlation has two effects, neither of which we account for:
  1. Swing states tend to tip together, making the "tipping point state" more predictable than our model suggests
  2. Conditional on the election being close nationally, it's more likely to be close in multiple swing states simultaneously

A better approach would be to model state outcomes as draws from a multivariate normal distribution with multi-state correlations estimated from historical polling errors, but we leave this as an exercise to the reader :)

## Value of the election
Now for the hard part: estimating \(\Delta V\). Beyond monetary considerations, there are social and geopolitical factors we can't put a price tag on. That being said, we're after an order-of-magnitude estimate, so let the hand-waving begin.

### The federal budget as a proxy
The 2024 federal budget was about $6.8T. About $1T goes to paying interest, and about $4T goes to mandatory spending, such as Social Security and Medicare. The president can't influence the former, and influencing the latter requires legislation. So let's focus on discretionary spending, which is about $1.8T. Over 4 years, this amounts to $7.2T. Within the discretionary bucket, candidates don't fully differ -- both will still fund the military, run agencies, and pay benefits. So what we care about are the marginal differences. If our preferred candidate is 10% more effective with this money, that gives us $720B.

The president also influences via legislation, Supreme Court appointments, foreign policy, etc. which are hard to quantify. Let's conveniently estimate the impact of these over 4 years at $280B, bringing our total to:
$$\Delta V \approx 1T$$

### Confidence factor
Since most voters aren't 100% confident in their vote, we should also apply a confidence discount factor. Even if you do feel 100% confident in your vote, policies can have second-order effects that are hard to predict [^5], so you should still discount this number. Applying a moderate \(c=0.5\) gives us:
$$\Delta V \approx 500B$$

## Applying this to the 2024 US Presidential Election
Let's apply this framework to the 2024 presidential race. We used historical state-level polling margins and assumed a 5% polling error for each state and a \(\Delta V\) of 500B, then ran 100 million simulations[^6] to estimate \(P(\text{state flips election})\) for each state. Here are the results:
{{< darklight light="/plots/voting_map_light_mode.png" dark="/plots/voting_map_dark_mode.png" alt="Voting Map" >}}
<div class="giant-table">
<table>

| State | P(vote flips state) | P(state flips election) | EV |
|-------|--------------------:|------------------------:|---:|
| AK | 8.50e-06 | 2.27% | $96,427 |
| AR | 3.31e-06 | 4.54% | $75,241 |
| NM | 3.59e-06 | 3.78% | $67,925 |
| NH | 4.23e-06 | 3.03% | $64,067 |
| NV | 2.68e-06 | 4.54% | $60,750 |
| KS | 2.62e-06 | 4.54% | $59,493 |
| ME | 3.27e-06 | 3.03% | $49,531 |
| IA | 2.13e-06 | 4.54% | $48,422 |
| AZ | 1.15e-06 | 8.35% | $47,869 |
| GA | 7.48e-07 | 12.19% | $45,587 |
| WI | 1.15e-06 | 7.58% | $43,745 |
| RI | 2.86e-06 | 3.03% | $43,300 |
| TX | 2.66e-07 | 31.75% | $42,247 |
| NC | 6.91e-07 | 12.19% | $42,121 |
| PA | 5.64e-07 | 14.52% | $40,927 |
| MI | 6.88e-07 | 11.41% | $39,250 |
| MN | 1.01e-06 | 7.58% | $38,128 |
| VA | 7.43e-07 | 9.87% | $36,685 |
| FL | 2.99e-07 | 23.30% | $34,854 |
| OH | 5.07e-07 | 12.96% | $32,839 |
| IL | 4.24e-07 | 14.51% | $30,780 |
| CO | 7.47e-07 | 7.58% | $28,291 |
| SC | 7.84e-07 | 6.82% | $26,731 |
| OR | 8.41e-07 | 6.06% | $25,485 |
| NE | 1.34e-06 | 3.78% | $25,377 |
| MT | 1.29e-06 | 3.03% | $19,505 |
| OK | 7.04e-07 | 5.30% | $18,654 |
| CT | 6.20e-07 | 5.30% | $16,440 |
| MO | 4.32e-07 | 7.58% | $16,364 |
| DE | 1.39e-06 | 2.27% | $15,776 |
| IN | 3.44e-07 | 8.35% | $14,335 |
| NJ | 2.41e-07 | 10.64% | $12,802 |
| NY | 1.01e-07 | 21.66% | $10,955 |
| HI | 5.42e-07 | 3.03% | $8,204 |
| WA | 1.56e-07 | 9.11% | $7,125 |
| MS | 2.84e-07 | 4.54% | $6,442 |
| TN | 1.43e-07 | 8.34% | $5,958 |
| LA | 1.76e-07 | 6.06% | $5,318 |
| ND | 2.80e-07 | 2.27% | $3,177 |
| SD | 2.73e-07 | 2.27% | $3,094 |
| CA | 1.14e-08 | 46.08% | $2,630 |
| UT | 1.01e-07 | 4.54% | $2,298 |
| WV | 1.35e-07 | 3.02% | $2,045 |
| MD | 3.22e-08 | 7.59% | $1,222 |
| MA | 2.45e-08 | 8.35% | $1,022 |
| VT | 6.39e-08 | 2.27% | $725 |
| AL | 1.95e-08 | 6.82% | $666 |
| KY | 2.12e-08 | 6.06% | $641 |
| WY | 8.89e-09 | 2.27% | $101 |
| ID | 5.56e-09 | 3.03% | $84 |
| DC | 1.33e-20 | 2.27% | $0 |

</table>
</div>

# Analysis
## Voting EV
The EV of a vote ranges from $84 (Idaho) to $96k (Alaska). A vote in Alaska is ~1000 times more valuable than a vote in Idaho (regardless of the value one assigns to the election itself). The chance of a vote swinging the entire election ranges from ~1 in 6 billion in Idaho to ~1 in 5 million in Alaska.

Oh, and then there is DC, where a voter has an astronomically small \(3.02\times 10^{-22}\) chance of swinging an election. If a DC voter had these chances and voted in a separate election for every single grain of sand on Earth, they would only have about a 0.2% chance of flipping a single election.

## What can I do in $NONSWING_STATE?

### Political activism
Convincing an undecided voter in Alaska to vote for your preferred candidate has an EV of $96k.
To put this into perspective, suppose you live in Idaho (where your vote is worth $84). Voting in your state is roughly equivalent to reaching out to a single undecided Alaskan voter and ~brainwashing~ convincing them to vote for your candidate at a 0.1% success rate.

### Vote swap
In the current equilibrium of the U.S., due to the two party system, there are only two candidates ever "worth" voting for if you think in terms of expected value. That being said, there are still some people who vote for independent candidates, knowing damn well it is futile but presumably to "rage against the dying of the light", as my friend put it.

This opens the door to [vote swapping](https://en.wikipedia.org/wiki/Vote_swapping). If Dave the Democrat lives in a decided state (e.g. DC) and has a third-party friend Trent in a swing state (who prefers Democrat to Republican), they can arrange a swap: Trent votes Democrat and Dave votes third-party, both are happier. This is legal in the U.S., but requires trust to function.

# Conclusion

This entire analysis is an elaborate rationalization for something I was probably going to do anyway. And it treats voting as a means to an end, a pure mathematical decision.

But there are plenty of reasons to ignore the numbers and vote: self-expression, civic duty, or simply using Election Day as a forcing function to stay politically informed. All valid.

But now when someone claims my vote is worthless, or that the Electoral College is a good thing, I can pull out probability density functions and Banzhaf simulations and end the conversation immediately. Not because I've won, but because literally no one cares.

{{< separator >}}

*Thanks to draft readers Varun and Michael.*

[^1]: [This](https://youtu.be/zeJD6dqJ5lo?si=7vb6GaENWJ9uYh4o) 3Blue1Brown video is a good explainer on the Central Limit Theorem.
[^2]: If \(r=0\), we simply have 100% probability if \(m=0\) and 0% probability otherwise.
[^3]: Assume the tiebreaker is a coin toss. For even \(N\), without your vote, your candidate wins the tiebreaker with probability \(0.5\). For odd \(N\), with your vote, your candidate wins the tiebreaker with probability \(0.5\). Thus in either case, your vote only changes the outcome half the time.
[^4]: Note that we treat Maine and Nebraska as single blocs in this analysis; in reality, these states allocate electoral votes by district rather than winner-take-all.
[^5]: There are plenty of examples of this -- see the [Great Hanoi Rat Massacre](https://en.wikipedia.org/wiki/Great_Hanoi_Rat_Massacre) as one of my favorites. Or consider that electing the worse candidate might be bad in the short-term but provoke reform and ends up being long-term net good.
[^6]: Source code [here](https://github.com/aviguptatx/avig/tree/main/content/posts/voting/simulation.py). You can run the code with your own parameters and get a table and annotated map like the ones in this post.
