# Poker Stats

Some of the definitions for the stats come from https://pokercopilot.com/userguide/6/en/topic/hud-statistics

## Poker Stars Info

### Player Actions
- Check – To check is to decline the opportunity to open the betting. Players can only check when there is no bet during the current round, and the act of checking passes the action clockwise to the next person in the hand. If all active players check, those players remain in the hand and the round is considered complete.
- Bet – Players may bet if no other players have bet during the current round. Once a bet has been made, other players must ‘call’ by matching the amount bet, in order to remain in the hand.
- Fold – Players who fold forfeit their cards and cannot win or act again during the current hand.
- Call – Players can call if other players have bet during the current round; this requires the calling player to match the highest bet made.
- Raise – Players may raise if other players have bet during the current round; this requires the raising player to match the highest bet made, and then make a greater one. All subsequent players are required to call the raise or raise again (‘re-raise’) to stay in the hand.

From my understanding bets are not considered raises in the stats.

## Stats

### Hands Played (#)
This is the total number of hands you were in. In tournaments, this number includes hands where you were sitting out, whereas these hands are not counted in ring games. In order for the statistics to be reliable, they should be based on a large number of hands. Ideally, you should play at least 10,000 hands to gain an accurate picture of your playing style.

### Big Blinds Won / 100 Hands (TBB)
Your winnings for each hand are expressed as a number of big blinds. For example, if you win $2.30 on a table where the big blind is $0.10, then your winnings for that hand are 23 big blinds. Your wins and losses as a number of big blinds are averaged and multiplied by 100. This results in a normalized value useful for comparisons, regardless of the stake level of each table.

## Preflop Statistics

### Flops Seen (FS)
This indicates in what percentage of hands you reached the flop without folding. This statistic counts every hand, regardless of whether you reached the flop without betting (for example, if you were in the big blind).

### Voluntarily Put $ in Pot (VPiP)
This measures how often you voluntarily invested money into a hand. Paying the big blind, the small blind, or the ante is not considered voluntary. Therefore this percentage indicates how often you called, bet, or raised. The lower this value, the tighter your hand selection is. The higher, the looser. Just how tight or loose depends on how many opponents you are playing against. The formula for calculating VPiP is:

`Voluntarily put $ in pot % = (times voluntarily put $ in pot) * 100 / (Hands played)`

### Preflop Raise (PFR)
The PFR statistic indicates how often you have raised before the flop is seen. A high value is an indicator of an aggressive player. A low value indicates a passive player. The formula for calculating PFR is:

`Pre-flop raise % = (times pre-flop raised) * 100 / (Hands played)`

### Called Preflop Raise (CPFR)
This is a measure of how often you called another player’s pre-flop raise, when you have the opportunity to do so. The formula for calculating CPFR is:

`Called preflop raise % = (times called preflop raise) * 100 / (number of opportunities to call preflop raise)`

### Unopened Preflop Raise (UOPFR)
This is a measure of how often you raised preflop when all players before you have called or folded. The formula for calculating UOPFR is:

`Unopened preflop raise % = (times made an unopened preflop raise) * 100 / (number of opportunities to make an unopened preflop raise)`

### Three-bet Pre-flop (3B)
This is a measure of how often you three-bet pre-flop. In pre-flop betting, to three-bet is to raise after exactly one other player has raised. The formula for calculating 3B is:

`Three-bet preflop % = (times three-bet preflop) * 100 / (number of three-bet preflop opportunities)`

**Note that any player who called the big blind or initial raise is ignored in this calculation.**

### Folded to Three-Bet Preflop (F3B)
This measures how often you folded to another player’s three-bet pre-flop, when you have the opportunity to do so. The formula for calculating F3B is:

`Folded to three-bet preflop % = (times folded to three-bet preflop) * 100 / (number of opportunities to fold to three-bet preflop)`

**Notes on fold to 3-bet:**
- You are only considered to have a “fold to 3-bet” opportunity if you made the initial raise. If player A raises, and player B reraises, and now player C has to act, only player A has a “fold to 3-bet” opportunity. Player C does not have a “fold to 3-bet” opportunity. We do this because if you have not yet made your opening action, and you are already facing two raises, you’d probably fold almost every single hand. This is not useful information to add to the “fold to 3-bet” stats. However, we are interested in knowing how people respond when their initial raise is re-raised.

### Four-bet Preflop (4B)
This is a measure of how often you four-bet pre-flop. Four-betting is similar to three- betting, except that you are re-raising after a player has already re-raised. The formula for calculating 4B is:

`Four-bet preflop % = (times Four-bet preflop) * 100 / (number of Four-bet preflop opportunities)`

**Notes on four-bet:**
- You are only considered to have a four-bet opportunity if you have already raised in the current hand.
- If two players have already raised before the action gets to you, then we don’t consider this a four-bet opportunity
- If you call the big blind, then subsequently two players raise, when the action comes back to you, we don’t consider this a four-bet opportunity
- This stat is actually four-or-higher-bet. If you make the first raise, and TWO players raise before the action comes back to you, you are now facing a five-bet. Poker Copilot considers this a four-bet opportunity.

### Folded to Four-bet Preflop (F4B)
This measures how often you folded to another player’s four-bet preflop, when you have the opportunity to do so. The formula for calculating F4B is:

`Folded to four-bet preflop % = (times folded to four-bet preflop) * 100 / (number of opportunities to fold to four-bet preflop)`

### Squeeze Bet (Sq)
This is a measure of how often a player makes a squeeze bet preflop. A squeeze bet is made by a player when all of the following occur: a) A villain raises, b) One or more players call the raise before the action comes to the hero, c) The hero re-raises the villain.
There must be at least one caller and no re-raise between villain and hero to define a squeeze.

`Squeeze bet % = (times made a squeeze bet) * 100 / (number of squeeze bet opportunities)`

## Steal Statistics

### Blind Stealing Attempts (BSA)
This indicates how often you attempt to steal the blinds when you had the opportunity to do so. Poker Copilot considers that you have a blind-stealing opportunity when you are on the button or you are the small blind (last before the blinds to make an action), and every player so far has folded. An attempt to steal the blinds is when you raised when given a blind-stealing opportunity. A good player attempts to steal the blinds often, but not always. The formula for calculating BSA is:

`Blind stealing attempts % = (times blind stealing attempted) * 100 /(number of blind stealing opportunities)`

### Folded Big Blind to Steal Attempt (FBB)
This measures how often you are facing a blind steal attempt when on the big blind and you fold. Either the button or the small blind may have made a blind steal attempt blind. Note that if the button is trying to steal but the small blind has already called the bet, then you are not facing a blind steal attempt. The formula for calculating FBB is:

`Folded big blind to steal attempt % = (times folded big blind to steal attempt) * 100 / (number of opportunities to fold the big blind to a steal attempt)`

## Postflop Statistics

### Postflop Agression Frequency (Agg)
This indicates how aggressive you are post-flop. It is calculated by counting the number of hands in which you’ve either bet or raised, then dividing this by the number of hands in which you’ve either bet, raised, called, or folded, and multiplying by 100. The higher this number, the more aggressively you are playing. Note that this measure must be interpreted in combination with Flops Seen. Players who see very few flops will naturally tend to have a higher aggression percentage because they are only playing top-quality hole cards. The formula for calculating Agg is:

`Aggression frequency % = (times bet or raised post-flop) * 100 /(times bet, raised, called, or folded post-flop)`

### Postflop Aggression Factor (AF)
This is calculated by counting the number of hands in which you’ve either bet or raised post-flop, then dividing this by the number of hands in which you’ve called post-flop. This value ranges from zero to infinity, which makes it awkward to use. Poker Copilot includes this statistic for comparisons with Poker Tracker statistics. Post-flop aggression % is a superior way of measuring aggression. The formula for calculating AF is:

`Aggression factor = (times bet or raised post-flop) / (times called post-flop)`

### Check-raised (CR)
A check-raise is when you check, let another player bet, then raise. It is a cunning play that is best used seldom. Note that due to the typically very low check-raise percentage (2% or lower) – and for the sake of meaningful comparisons – Poker Copilot shows this value to two decimal places. The formula for calculating CR is:

`Check-raise % = (times check-raised) * 100 / (number of check- raise opportunities)`

### Check-raised Flop (CR_F)
Measures the frequency you check-raised at the flop.The formula is:

`Check-raise flop % = (times check-raised on flop) * 100 / (number of check-raise on flop opportunities)`

### Check-raised Turn (CR_T)
Mesures the frequency you check-raised at the turn.The formula is:

`Check-raise turn % = (times check-raised on turn) * 100 / (number of check-raise on turn opportunities)`

### Check-raised River (CR_R)
Measures the frequency you check-raised at the river.The formula is:

`Check-raise river % = (times check-raised on river) * 100 / (number of check-raise on river opportunities)`

### Continuation Bet (CBET)
A continuation bet is when you were the last to raise preflop, and hence the aggressor, and you continued that aggression on the flop by being the first to bet. The formula for calculating CBET is:

`Continuation bet % = (times made a continuation bet on the flop)* 100 / (number of opportunities to make a continuation bet on the flop)`

### Folded to Continuation Bet (FCB)
This indicates how you respond when you are facing a continuation bet on the flop. The formula for calculating FCB is:

`Folded to continuation bet % = (times folded to continuation bet on the flop) * 100 / (number of opportunities to fold to continuation bet on the flop)`

### Continuation Bet on Turn (TCBET)
This statistic is similar to CBET, but applies when making a continuation bet on the turn. The formula for calculating TCBET is:

`Continuation bet on turn % = (times made a continuation bet on the turn) * 100 / (number of opportunities to make a continuation bet on the turn)`

### Folded to Continuation Bet on Turn (FCB_T)
This indicates how you respond when you are facing a continuation bet on the turn. The formula for calculating FCBT is:

`Folded to continuation bet on turn % = (times folded to continuation bet on the turn) * 100 / (number of opportunities to fold to continuation bet on the turn)`

### Donk Bet
Measures how often a player makes a donk bet on any street.

To make a donk bet, two things are required. You must be the caller pre-flop or on the previous street, and you must be out of position. The name comes from the fact that this is generally a play made by bad players (or “donks”). They will call a hand pre-flop, and if they like the flop, will simply bet instead of checking to the pre-flop raiser.

`Donk bet % = (times donk bet) * 100 / (number of donk bet opportunities)`

Here the donk bet stat measures all streets. The donk bet stat is further broken down by street.

### Donk Bet on Flop (DB_F)
Measures how often a player makes a donk bet on the flop. A player makes a donk bet when he was the caller pre-flop, yet opens with a bet on the flop.
An example: Player A was the last to raise pre-flop. Player B called Player A’s raise pre-flop. Now on the flop, before the action gets to Player A, Player B opened with a bet. B makes a donk bet.
The formula for calculating DB_F is:

`Donk bet on flop % = (times donk bet on flop) * 100 / (number of donk bet on flop opportunities)`

### Donk Bet on Turn (DB_T)
Measures how often a player makes a donk bet on the turn. A donk bet on the turn is made by a player when all of the following occur:
a) The player calls another player’s pre-flop raise; and then
b) The player calls the pre-flop aggressor’s continuation bet on the flop; and then
c) The player opens with a bet on the turn before the pre-flop aggressor has the chance to check or bet.
The formula for calculating DB_T is:

`Donk bet on turn % = (times donk bet on turn) * 100 / (number of donk bet on turn opportunities)`

### Donk Bet on river (DB_R)
Measures how often a player makes a donk bet on the river. A donk bet on the river is made by a player when all of the following occur:
a) The player calls another player’s pre-flop raise; and then
b) The player calls the pre-flop aggressor’s continuation bet on the flop; and then
c) The player calls the pre-flop aggressor’s continuation bet on the turn; and then
d) The player opens with a bet on the river before the pre-flop aggressor has the chance to check or bet.
The formula for calculating DB_R is:

`Donk bet on river % = (times donk bet on river) * 100 / (number of donk bet on river opportunities)`

### Went to Showdown (WtS)
This is a measure of how often you were still in the action when the hand went to showdown. Showdown occurs when the final round of betting is complete and at least two players are still in. The formula for calculating WtS is:

`Went to showdown % = (times went to showdown) * 100 / (times flop seen)`

### Won at Showdown (WaS)
This indicates how often you won a hand in a showdown. It is calculated as a percentage of all hands in which you went to showdown. The formula for calculating WaS is:

`Won at showdown % = (times won at showdown) * 100 / (times went to showdown)`

### Won Without Showdown (WwS)
This indicates how often you won a hand without going to showdown because all other players folded. It is calculated as a percentage of hands where you saw the flop. The formula for calculating WwS is:

`Won without showdown % = (times won without showdown) * 100 / (times flop seen)`

## Other Statistics

### M-ratio (M)
This measures the health of your chip stack and represents the number of passes of the dealer button (some talk of “orbits”) you can survive without winning or losing any chips. Your M-ratio is an important number to be aware of during tournament play. The formula for calculating M is:

`M-ratio = (Stack Size) / ((Small Blind) + (Big Blind) + (Total antes))`

Example # 1: 9 players table, SB = 15, BB = 30, Stack = 900 chips, M = 900/ (15+30) = 20
Example # 2: 9 players table, SB = 100, BB = 200, Ante = 20, Stack = 2880 chips, M = 2880/ (100+200+ (9 × 20)) = 6

### Big Blinds Remaining (BB)
This is a measure of the amount of money you have expressed as a number of big blinds. For example, if you have $3.00 at a table where the big blind is $0.10, then you have 30 big blinds. The big blind information is contained in your hand history files. This means we only know about a blind increase after the first hand with the increase. So for the first hand after a blind increase, we’ll show BB remaining calculation using the blind levels in the previous hand.