#!/usr/bin/env python

# CONSIDER: We may want to add a helper method to the fixture in conftest.py since acquiring reputation is likely to be a pretty common operation.  It probably would be easiest to make it so`tester.k9` starts out with all of the REP in `__init__` of that fixture and then when someone needs REP, we can just transfer from them.

# CONSIDER: We may also want to move the bond-related constants to their own contract under tests/solidity_test_helpers if they will be used in other test files.

# CONSIDER: Break up test_dispute_bond_tokens() into more functions

from ethereum.tools import tester
from pytest import mark
from utils import bytesToHexString

REP_TOTAL = 11 * 10**6 # Total number of REP tokens in existence
REP_DIVISOR = 10**18 # Amount by which a single REP token can be divided

DESIGNATED_REPORTER_DISPUTE_BOND_AMOUNT = 11 * 10**20
ROUND1_REPORTERS_DISPUTE_BOND_AMOUNT = 11 * 10**21
ROUND2_REPORTERS_DISPUTE_BOND_AMOUNT = 11 * 10**22

MARKET_TYPE_CATEGORICAL = 0
MARKET_TYPE_SCALAR = 1

CATEGORICAL_OUTCOME_A = [3*10**17, 0, 0]
CATEGORICAL_OUTCOME_B = [0, 3*10**17, 0]
CATEGORICAL_OUTCOME_C = [0, 0, 3*10**17]

SCALAR_OUTCOME_A = [30*10**18, 10*10**18]
SCALAR_OUTCOME_B = [10*10**18, 30*10**18]
SCALAR_OUTCOME_C = [20*10**18, 20*10**18]

@mark.parametrize('marketType,designatedReporterAccountNum,designatedReporterOutcome,designatedReporterDisputerAccountNum,designatedReporterDisputeStakes,round1ReportersDisputerAccountNum,round1ReporterDisputeOutcome,round1ReportersDisputeStakes,round2ReportersDisputerAccountNum,round2ReportersDisputeStakes,expectedAccountBalances', [
    # CONSIDER: Create test cases where:
    # - There is no designated reporting (just first reporters & last reporters)
    # - There is a tie between 2 outcomes

    # ----- Start categorical market test cases -----
    # Test case where there is a designated reporter & no disputes
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, None, [], None, None, [], None, [], [[0, None, 1000000 * REP_DIVISOR], [1, None, 1000000 * REP_DIVISOR]]),

    # Test cases where designated reporter is disputed
    # No losing tokens; bond holder was incorrect (bond holder gets nothing back, correct token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[2, CATEGORICAL_OUTCOME_A, 1105 * REP_DIVISOR]], None, None, [], None, [], [[0,  None, 1000003987353206865401987], [1, None, 998899999999999999999999], [2, None, 1001098012646793134598014]]),
    # Some losing tokens; some winning tokens; bond holder was incorrect (bond holder gets nothing, winning token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1205 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 1001302000000000000000001], [1, None, 998799999999999999999999], [2, None, 999900000000000000000000]]),
    # Small amount of losing tokens; some winning tokens; bond holder was correct (bond holder gets less than 2x, winning token holders get no bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 100 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 105 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 999900000000000000000000], [1, None, 1000202000000000000000000], [2, None, 999900000000000000000000]]),
    # Large amount of losing tokens; some winning tokens; bond holder was correct (bond holder gets 2x, winning token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 2500 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 1500 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_B, 1500 * REP_DIVISOR], [3, CATEGORICAL_OUTCOME_C, 1500 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 997500000000000000000000], [1, None, 1002551000000000000000000], [2, None, 1001451000000000000000000], [3, None, 998500000000000000000000]]),
    # No losing tokens; bond holder was right (bond holder gets 1x back, winning tokens get no bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[1, CATEGORICAL_OUTCOME_B, 200 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR]], None, None, [], None, [], [[0,  None, 1000000000000000000000000], [1, None, 1000002000000000000000000], [2, None, 1000000000000000000000000]]),

    # Test cases where designated reporter & first reporters are disputed
    # No losing tokens; bond holder was incorrect (bond holder gets nothing back, correct token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1105 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_B, [[3, CATEGORICAL_OUTCOME_A, 11050 * REP_DIVISOR]], None, [], [[0, None, 1001103809656987743686764], [1, None, 998899999999999999999999], [2, None, 989000000000000000000000], [3, None, 1010998190343012256313237]]),
    # Some losing tokens; some winning tokens; bond holders were incorrect (bond holders get nothing, winning token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1305 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_B, [[3, CATEGORICAL_OUTCOME_A, 11005 * REP_DIVISOR]], None, [], [[0, None, 1001307726120857699805068], [1, None, 998799999999999999999999], [2, None, 988900000000000000000000], [3, None, 1010994273879142300194933]]),
    # Small amount of losing tokens; some winning tokens; bond holders were correct (bond holders get less than 2x, winning token holders get no bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1305 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_B, [[3, CATEGORICAL_OUTCOME_B, 150 * REP_DIVISOR]], None, [], [[0, None, 998695000000000000000000], [1, None, 1001100000000000000000000], [2, None, 1000207000000000000000000], [3, None, 1000000000000000000000000]]),
    # Large amount of losing tokens; some winning tokens; bond holders were correct (bond holders get 2x, winning token holders get bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 25000 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 105 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], 1, CATEGORICAL_OUTCOME_B, [[3, CATEGORICAL_OUTCOME_B, 25000 * REP_DIVISOR]], None, [], [[0, None, 975000000000000000000000], [1, None, 1012154380003983270264887], [2, None, 999900000000000000000000], [3, None, 1012947619996016729735113]]),
    # No losing tokens; first bond holder was right (first bond holder get 1x back, winning tokens get no bonus)
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[2, CATEGORICAL_OUTCOME_B, 105 * REP_DIVISOR]], 0, CATEGORICAL_OUTCOME_C, [[3, CATEGORICAL_OUTCOME_B, 11150 * REP_DIVISOR]], None, [], [[0, None, 988999999999999999999999], [1, None, 1000002000000000000000001], [2, None, 1000102621057307863171923], [3, None, 1010897378942692136828077]]),
    # Some losing tokens; some winning tokens; bond holders were correct; No reporting during the last reporting phase
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[1, CATEGORICAL_OUTCOME_B, 2000 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 50 * REP_DIVISOR]], 2, None, [], None, [], [[0, None, 1000000000000000000000000], [1, None, 999099999999999999999999], [2, None, 1000902000000000000000001], [3, None, 1000000000000000000000000]]),
    # Some losing tokens; some winning tokens; bond holders were incorrect; No reporting during the last reporting phase
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 12200 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 50 * REP_DIVISOR]], 2, None, [], None, [], [[0, None, 1012152000000000000000001], [1, None, 998849999999999999999999], [2, None, 989000000000000000000000], [3, None, 1000000000000000000000000]]),

    # Test cases where designated reporter, first reporters, & last reporters are disputed.  (Users should always end up with roughly the same amount of REP they started with, since there is no REP redistribution in the event of a fork)
    (MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1105 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_B, [[3, CATEGORICAL_OUTCOME_A, 11050 * REP_DIVISOR]], 1, [[0, CATEGORICAL_OUTCOME_A], [1, CATEGORICAL_OUTCOME_B], [2, CATEGORICAL_OUTCOME_B], [3, CATEGORICAL_OUTCOME_A], [4, CATEGORICAL_OUTCOME_A]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [0, CATEGORICAL_OUTCOME_A, 1000002000000000000000000], [1, CATEGORICAL_OUTCOME_A, 0], [2, CATEGORICAL_OUTCOME_A, 0], [3, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [4, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [0, CATEGORICAL_OUTCOME_B, 0], [1, CATEGORICAL_OUTCOME_B, 999999999999999999999999], [2, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [3, CATEGORICAL_OUTCOME_B, 0], [4, CATEGORICAL_OUTCOME_B, 0], [0, CATEGORICAL_OUTCOME_C, 0], [1, CATEGORICAL_OUTCOME_C, 0], [2, CATEGORICAL_OUTCOME_C, 0], [3, CATEGORICAL_OUTCOME_C, 0], [4, CATEGORICAL_OUTCOME_C, 0]]),
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1205 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_A, [[3, CATEGORICAL_OUTCOME_A, 11150 * REP_DIVISOR]], 4, [[0, CATEGORICAL_OUTCOME_A], [1, CATEGORICAL_OUTCOME_B], [2, CATEGORICAL_OUTCOME_B], [3, CATEGORICAL_OUTCOME_A], [4, CATEGORICAL_OUTCOME_B], [5, CATEGORICAL_OUTCOME_A], [6, CATEGORICAL_OUTCOME_A]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, CATEGORICAL_OUTCOME_A, 1000002000000000000000000], [1, CATEGORICAL_OUTCOME_A, 0], [2, CATEGORICAL_OUTCOME_A, 0], [3, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [4, CATEGORICAL_OUTCOME_A, 0], [5, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [6, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [0, CATEGORICAL_OUTCOME_B, 0], [1, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [2, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [3, CATEGORICAL_OUTCOME_B, 0], [4, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [5, CATEGORICAL_OUTCOME_B, 0], [6, CATEGORICAL_OUTCOME_B, 0], [0, CATEGORICAL_OUTCOME_C, 0], [1, CATEGORICAL_OUTCOME_C, 0], [2, CATEGORICAL_OUTCOME_C, 0], [3, CATEGORICAL_OUTCOME_C, 0], [4, CATEGORICAL_OUTCOME_C, 0], [5, CATEGORICAL_OUTCOME_C, 0], [6, CATEGORICAL_OUTCOME_C, 0]]),
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 1205 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100 * REP_DIVISOR], [2, CATEGORICAL_OUTCOME_C, 100 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_C, [[3, CATEGORICAL_OUTCOME_B, 150 * REP_DIVISOR]], 4, [[0, CATEGORICAL_OUTCOME_A], [1, CATEGORICAL_OUTCOME_B], [2, CATEGORICAL_OUTCOME_C], [3, CATEGORICAL_OUTCOME_B], [4, CATEGORICAL_OUTCOME_A], [5, CATEGORICAL_OUTCOME_B], [6, CATEGORICAL_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, CATEGORICAL_OUTCOME_A, 1000002000000000000000000], [1, CATEGORICAL_OUTCOME_A, 0], [2, CATEGORICAL_OUTCOME_A, 0], [3, CATEGORICAL_OUTCOME_A, 0], [4, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [5, CATEGORICAL_OUTCOME_A, 0], [6, CATEGORICAL_OUTCOME_A, 0], [0, CATEGORICAL_OUTCOME_B, 0], [1, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [2, CATEGORICAL_OUTCOME_B, 0], [3, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [4, CATEGORICAL_OUTCOME_B, 0], [5, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [6, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [0, CATEGORICAL_OUTCOME_C, 0], [1, CATEGORICAL_OUTCOME_C, 0], [2, CATEGORICAL_OUTCOME_C, 1000000000000000000000000], [3, CATEGORICAL_OUTCOME_C, 0], [4, CATEGORICAL_OUTCOME_C, 0], [5, CATEGORICAL_OUTCOME_C, 0], [6, CATEGORICAL_OUTCOME_C, 0]]),
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[0, CATEGORICAL_OUTCOME_A, 150000 * REP_DIVISOR], [1, CATEGORICAL_OUTCOME_B, 100000 * REP_DIVISOR]], 2, CATEGORICAL_OUTCOME_C, [[2, CATEGORICAL_OUTCOME_B, 200000 * REP_DIVISOR], [3, CATEGORICAL_OUTCOME_A, 100000 * REP_DIVISOR]], 4, [[0, CATEGORICAL_OUTCOME_A], [1, CATEGORICAL_OUTCOME_B], [2, CATEGORICAL_OUTCOME_B], [3, CATEGORICAL_OUTCOME_A], [4, CATEGORICAL_OUTCOME_B], [5, CATEGORICAL_OUTCOME_B], [6, CATEGORICAL_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, CATEGORICAL_OUTCOME_A, 1000002000000000000000000], [1, CATEGORICAL_OUTCOME_A, 0], [2, CATEGORICAL_OUTCOME_A, 0], [3, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [4, CATEGORICAL_OUTCOME_A, 0], [5, CATEGORICAL_OUTCOME_A, 0], [6, CATEGORICAL_OUTCOME_A, 0], [0, CATEGORICAL_OUTCOME_B, 0], [1, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [2, CATEGORICAL_OUTCOME_B, 999999999999999999999999], [3, CATEGORICAL_OUTCOME_B, 0], [4, CATEGORICAL_OUTCOME_B, 890000000000000000000000], [5, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [6, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [0, CATEGORICAL_OUTCOME_C, 0], [1, CATEGORICAL_OUTCOME_C, 0], [2, CATEGORICAL_OUTCOME_C, 0], [3, CATEGORICAL_OUTCOME_C, 0], [4, CATEGORICAL_OUTCOME_C, 0], [5, CATEGORICAL_OUTCOME_C, 0], [6, CATEGORICAL_OUTCOME_C, 0]]),
    #(MARKET_TYPE_CATEGORICAL, 0, CATEGORICAL_OUTCOME_A, 1, [[2, CATEGORICAL_OUTCOME_B, 105 * REP_DIVISOR]], 0, CATEGORICAL_OUTCOME_C, [[3, CATEGORICAL_OUTCOME_B, 11050 * REP_DIVISOR]], 4, [[0, CATEGORICAL_OUTCOME_A], [1, CATEGORICAL_OUTCOME_B], [2, CATEGORICAL_OUTCOME_B], [3, CATEGORICAL_OUTCOME_B], [4, CATEGORICAL_OUTCOME_A], [5, CATEGORICAL_OUTCOME_B], [6, CATEGORICAL_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, CATEGORICAL_OUTCOME_A, 999999999999999999999999], [1, CATEGORICAL_OUTCOME_A, 0], [2, CATEGORICAL_OUTCOME_A, 0], [3, CATEGORICAL_OUTCOME_A, 0], [4, CATEGORICAL_OUTCOME_A, 1000000000000000000000000], [5, CATEGORICAL_OUTCOME_A, 0], [6, CATEGORICAL_OUTCOME_A, 0], [0, CATEGORICAL_OUTCOME_B, 0], [1, CATEGORICAL_OUTCOME_B, 999999999999999999999999], [2, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [3, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [4, CATEGORICAL_OUTCOME_B, 0], [5, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [6, CATEGORICAL_OUTCOME_B, 1000000000000000000000000], [0, CATEGORICAL_OUTCOME_C, 0], [1, CATEGORICAL_OUTCOME_C, 0], [2, CATEGORICAL_OUTCOME_C, 0], [3, CATEGORICAL_OUTCOME_C, 0], [4, CATEGORICAL_OUTCOME_C, 0], [5, CATEGORICAL_OUTCOME_C, 0], [6, CATEGORICAL_OUTCOME_C, 0]]),
    # ----- End categorical market test cases -----

    # ----- Start scalar market test cases -----
    # Test case where there is a designated reporter & no disputes
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, None, [], None, None, [], None, [], [[0, None, 1000000 * REP_DIVISOR], [1, None, 1000000 * REP_DIVISOR]]),

    # Test cases where designated reporter is disputed
    # No losing tokens; bond holder was incorrect (bond holder gets nothing back, correct token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[2, SCALAR_OUTCOME_A, 1105 * REP_DIVISOR]], None, None, [], None, [], [[0,  None, 1000003987353206865401987], [1, None, 998899999999999999999999], [2, None, 1001098012646793134598014]]),
    # Some losing tokens; some winning tokens; bond holder was incorrect (bond holder gets nothing, winning token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1205 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 1001302000000000000000001], [1, None, 998799999999999999999999], [2, None, 999900000000000000000000]]),
    # Small amount of losing tokens; some winning tokens; bond holder was correct (bond holder gets less than 2x, winning token holders get no bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 100 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 105 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 999900000000000000000000], [1, None, 1000202000000000000000000], [2, None, 999900000000000000000000]]),
    # Large amount of losing tokens; some winning tokens; bond holder was correct (bond holder gets 2x, winning token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 2500 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 1500 * REP_DIVISOR], [2, SCALAR_OUTCOME_B, 1500 * REP_DIVISOR], [3, SCALAR_OUTCOME_C, 1500 * REP_DIVISOR]], None, None, [], None, [], [[0, None, 997500000000000000000000], [1, None, 1002551000000000000000000], [2, None, 1001451000000000000000000], [3, None, 998500000000000000000000]]),
    # No losing tokens; bond holder was right (bond holder gets 1x back, winning tokens get no bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[1, SCALAR_OUTCOME_B, 200 * REP_DIVISOR], [2, SCALAR_OUTCOME_B, 100 * REP_DIVISOR]], None, None, [], None, [], [[0,  None, 1000000000000000000000000], [1, None, 1000002000000000000000000], [2, None, 1000000000000000000000000]]),

    # Test cases where designated reporter & first reporters are disputed
    # No losing tokens; bond holder was incorrect (bond holder gets nothing back, correct token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1105 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_A, 11050 * REP_DIVISOR]], None, [], [[0, None, 1001103809656987743686764], [1, None, 998899999999999999999999], [2, None, 989000000000000000000000], [3, None, 1010998190343012256313237]]),
    # Some losing tokens; some winning tokens; bond holders were incorrect (bond holders get nothing, winning token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1305 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_A, 11005 * REP_DIVISOR]], None, [], [[0, None, 1001307726120857699805068], [1, None, 998799999999999999999999], [2, None, 988900000000000000000000], [3, None, 1010994273879142300194933]]),
    # Small amount of losing tokens; some winning tokens; bond holders were correct (bond holders get less than 2x, winning token holders get no bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1305 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_B, 150 * REP_DIVISOR]], None, [], [[0, None, 998695000000000000000000], [1, None, 1001100000000000000000000], [2, None, 1000207000000000000000000], [3, None, 1000000000000000000000000]]),
    # Large amount of losing tokens; some winning tokens; bond holders were correct (bond holders get 2x, winning token holders get bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 25000 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 105 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], 1, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_B, 25000 * REP_DIVISOR]], None, [], [[0, None, 975000000000000000000000], [1, None, 1012154380003983270264887], [2, None, 999900000000000000000000], [3, None, 1012947619996016729735113]]),
    # No losing tokens; first bond holder was right (first bond holder get 1x back, winning tokens get no bonus)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[2, SCALAR_OUTCOME_B, 105 * REP_DIVISOR]], 0, SCALAR_OUTCOME_C, [[3, SCALAR_OUTCOME_B, 11150 * REP_DIVISOR]], None, [], [[0, None, 988999999999999999999999], [1, None, 1000002000000000000000001], [2, None, 1000102621057307863171923], [3, None, 1010897378942692136828077]]),
    # Some losing tokens; some winning tokens; bond holders were correct; No reporting during the last reporting phase
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[1, SCALAR_OUTCOME_B, 2000 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 50 * REP_DIVISOR]], 2, None, [], None, [], [[0, None, 1000000000000000000000000], [1, None, 999099999999999999999999], [2, None, 1000902000000000000000001], [3, None, 1000000000000000000000000]]),
    # Some losing tokens; some winning tokens; bond holders were incorrect; No reporting during the last reporting phase
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 12200 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 50 * REP_DIVISOR]], 2, None, [], None, [], [[0, None, 1012152000000000000000001], [1, None, 998849999999999999999999], [2, None, 989000000000000000000000], [3, None, 1000000000000000000000000]]),

    # Test cases where designated reporter, first reporters, & last reporters are disputed.  (Users should always end up with roughly the same amount of REP they started with, since there is no REP redistribution in the event of a fork)
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1105 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_A, 11050 * REP_DIVISOR]], 1, [[0, SCALAR_OUTCOME_A], [1, SCALAR_OUTCOME_B], [2, SCALAR_OUTCOME_B], [3, SCALAR_OUTCOME_A], [4, SCALAR_OUTCOME_A]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [0, SCALAR_OUTCOME_A, 1000002000000000000000000], [1, SCALAR_OUTCOME_A, 0], [2, SCALAR_OUTCOME_A, 0], [3, SCALAR_OUTCOME_A, 1000000000000000000000000], [4, SCALAR_OUTCOME_A, 1000000000000000000000000], [0, SCALAR_OUTCOME_B, 0], [1, SCALAR_OUTCOME_B, 999999999999999999999999], [2, SCALAR_OUTCOME_B, 1000000000000000000000000], [3, SCALAR_OUTCOME_B, 0], [4, SCALAR_OUTCOME_B, 0], [0, SCALAR_OUTCOME_C, 0], [1, SCALAR_OUTCOME_C, 0], [2, SCALAR_OUTCOME_C, 0], [3, SCALAR_OUTCOME_C, 0], [4, SCALAR_OUTCOME_C, 0]]),
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1205 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_A, 11150 * REP_DIVISOR]], 4, [[0, SCALAR_OUTCOME_A], [1, SCALAR_OUTCOME_B], [2, SCALAR_OUTCOME_B], [3, SCALAR_OUTCOME_A], [4, SCALAR_OUTCOME_B], [5, SCALAR_OUTCOME_A], [6, SCALAR_OUTCOME_A]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, SCALAR_OUTCOME_A, 1000002000000000000000000], [1, SCALAR_OUTCOME_A, 0], [2, SCALAR_OUTCOME_A, 0], [3, SCALAR_OUTCOME_A, 1000000000000000000000000], [4, SCALAR_OUTCOME_A, 0], [5, SCALAR_OUTCOME_A, 1000000000000000000000000], [6, SCALAR_OUTCOME_A, 1000000000000000000000000], [0, SCALAR_OUTCOME_B, 0], [1, SCALAR_OUTCOME_B, 1000000000000000000000000], [2, SCALAR_OUTCOME_B, 1000000000000000000000000], [3, SCALAR_OUTCOME_B, 0], [4, SCALAR_OUTCOME_B, 1000000000000000000000000], [5, SCALAR_OUTCOME_B, 0], [6, SCALAR_OUTCOME_B, 0], [0, SCALAR_OUTCOME_C, 0], [1, SCALAR_OUTCOME_C, 0], [2, SCALAR_OUTCOME_C, 0], [3, SCALAR_OUTCOME_C, 0], [4, SCALAR_OUTCOME_C, 0], [5, SCALAR_OUTCOME_C, 0], [6, SCALAR_OUTCOME_C, 0]]),
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 1205 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100 * REP_DIVISOR], [2, SCALAR_OUTCOME_C, 100 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[3, SCALAR_OUTCOME_B, 150 * REP_DIVISOR]], 4, [[0, SCALAR_OUTCOME_A], [1, SCALAR_OUTCOME_B], [2, SCALAR_OUTCOME_C], [3, SCALAR_OUTCOME_B], [4, SCALAR_OUTCOME_A], [5, SCALAR_OUTCOME_B], [6, SCALAR_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, SCALAR_OUTCOME_A, 1000002000000000000000000], [1, SCALAR_OUTCOME_A, 0], [2, SCALAR_OUTCOME_A, 0], [3, SCALAR_OUTCOME_A, 0], [4, SCALAR_OUTCOME_A, 1000000000000000000000000], [5, SCALAR_OUTCOME_A, 0], [6, SCALAR_OUTCOME_A, 0], [0, SCALAR_OUTCOME_B, 0], [1, SCALAR_OUTCOME_B, 1000000000000000000000000], [2, SCALAR_OUTCOME_B, 0], [3, SCALAR_OUTCOME_B, 1000000000000000000000000], [4, SCALAR_OUTCOME_B, 0], [5, SCALAR_OUTCOME_B, 1000000000000000000000000], [6, SCALAR_OUTCOME_B, 1000000000000000000000000], [0, SCALAR_OUTCOME_C, 0], [1, SCALAR_OUTCOME_C, 0], [2, SCALAR_OUTCOME_C, 1000000000000000000000000], [3, SCALAR_OUTCOME_C, 0], [4, SCALAR_OUTCOME_C, 0], [5, SCALAR_OUTCOME_C, 0], [6, SCALAR_OUTCOME_C, 0]]),
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[0, SCALAR_OUTCOME_A, 150000 * REP_DIVISOR], [1, SCALAR_OUTCOME_B, 100000 * REP_DIVISOR]], 2, SCALAR_OUTCOME_B, [[2, SCALAR_OUTCOME_B, 200000 * REP_DIVISOR], [3, SCALAR_OUTCOME_A, 100000 * REP_DIVISOR]], 4, [[0, SCALAR_OUTCOME_A], [1, SCALAR_OUTCOME_B], [2, SCALAR_OUTCOME_B], [3, SCALAR_OUTCOME_A], [4, SCALAR_OUTCOME_B], [5, SCALAR_OUTCOME_B], [6, SCALAR_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, SCALAR_OUTCOME_A, 1000002000000000000000000], [1, SCALAR_OUTCOME_A, 0], [2, SCALAR_OUTCOME_A, 0], [3, SCALAR_OUTCOME_A, 1000000000000000000000000], [4, SCALAR_OUTCOME_A, 0], [5, SCALAR_OUTCOME_A, 0], [6, SCALAR_OUTCOME_A, 0], [0, SCALAR_OUTCOME_B, 0], [1, SCALAR_OUTCOME_B, 1000000000000000000000000], [2, SCALAR_OUTCOME_B, 1000000000000000000000000], [3, SCALAR_OUTCOME_B, 0], [4, SCALAR_OUTCOME_B, 890000000000000000000000], [5, SCALAR_OUTCOME_B, 1000000000000000000000000], [6, SCALAR_OUTCOME_B, 1000000000000000000000000], [0, SCALAR_OUTCOME_C, 0], [1, SCALAR_OUTCOME_C, 0], [2, SCALAR_OUTCOME_C, 0], [3, SCALAR_OUTCOME_C, 0], [4, SCALAR_OUTCOME_C, 0], [5, SCALAR_OUTCOME_C, 0], [6, SCALAR_OUTCOME_C, 0]]),
    #(MARKET_TYPE_SCALAR, 0, SCALAR_OUTCOME_A, 1, [[2, SCALAR_OUTCOME_B, 105 * REP_DIVISOR]], 0, SCALAR_OUTCOME_A, [[3, SCALAR_OUTCOME_B, 11050 * REP_DIVISOR]], 4, [[0, SCALAR_OUTCOME_A], [1, SCALAR_OUTCOME_B], [2, SCALAR_OUTCOME_B], [3, SCALAR_OUTCOME_B], [4, SCALAR_OUTCOME_A], [5, SCALAR_OUTCOME_B], [6, SCALAR_OUTCOME_B]], [[0, None, 0], [1, None, 0], [2, None, 0], [3, None, 0], [4, None, 0], [5, None, 0], [6, None, 0], [0, SCALAR_OUTCOME_A, 998901999999999999999999], [1, SCALAR_OUTCOME_A, 0], [2, SCALAR_OUTCOME_A, 0], [3, SCALAR_OUTCOME_A, 0], [4, SCALAR_OUTCOME_A, 1000000000000000000000000], [5, SCALAR_OUTCOME_A, 0], [6, SCALAR_OUTCOME_A, 0], [0, SCALAR_OUTCOME_B, 0], [1, SCALAR_OUTCOME_B, 999999999999999999999999], [2, SCALAR_OUTCOME_B, 1000000000000000000000000], [3, SCALAR_OUTCOME_B, 1000000000000000000000000], [4, SCALAR_OUTCOME_B, 0], [5, SCALAR_OUTCOME_B, 1000000000000000000000000], [6, SCALAR_OUTCOME_B, 1000000000000000000000000], [0, SCALAR_OUTCOME_C, 0], [1, SCALAR_OUTCOME_C, 0], [2, SCALAR_OUTCOME_C, 0], [3, SCALAR_OUTCOME_C, 0], [4, SCALAR_OUTCOME_C, 0], [5, SCALAR_OUTCOME_C, 0], [6, SCALAR_OUTCOME_C, 0]]),
    # ----- End scalar market test cases -----
])
def test_dispute_bond_tokens(marketType, designatedReporterAccountNum, designatedReporterOutcome, designatedReporterDisputerAccountNum, designatedReporterDisputeStakes, round1ReportersDisputerAccountNum, round1ReporterDisputeOutcome, round1ReportersDisputeStakes, round2ReportersDisputerAccountNum, round2ReportersDisputeStakes, expectedAccountBalances, contractsFixture, universe, binaryMarket, categoricalMarket, scalarMarket):
    if (marketType == MARKET_TYPE_CATEGORICAL):
        market = categoricalMarket
        otherMarket = scalarMarket
        otherOutcome = SCALAR_OUTCOME_A
        OUTCOME_A = CATEGORICAL_OUTCOME_A
        OUTCOME_B = CATEGORICAL_OUTCOME_B
        OUTCOME_C = CATEGORICAL_OUTCOME_C
    elif (marketType == MARKET_TYPE_SCALAR):
        market = scalarMarket
        otherMarket = categoricalMarket
        otherOutcome = CATEGORICAL_OUTCOME_A
        OUTCOME_A = SCALAR_OUTCOME_A
        OUTCOME_B = SCALAR_OUTCOME_B
        OUTCOME_C = SCALAR_OUTCOME_C
    stakeTokenA = contractsFixture.getStakeToken(market, OUTCOME_A, False)
    stakeTokenB = contractsFixture.getStakeToken(market, OUTCOME_B, False)
    stakeTokenC = contractsFixture.getStakeToken(market, OUTCOME_C, False)
    reportingWindow = contractsFixture.applySignature('ReportingWindow', market.getReportingWindow())
    aUniverseReputationToken = None
    bUniverseReputationToken = None
    cUniverseReputationToken = None
    aUniverse = None
    bUniverse = None
    cUniverse = None
    winningStakeToken = None
    designatedReporterStake = universe.getDesignatedReportStake()
    stakeDelta = 0

    designatedReporterDisputeBondToken = None
    round1ReportersDisputeBondToken = None
    round2ReportersDisputeBondToken = None

    # Seed legacy REP contract with 11 million reputation tokens
    legacyRepContract = contractsFixture.contracts['LegacyRepContract']
    legacyRepContract.faucet(long(REP_TOTAL * REP_DIVISOR))

    # Get the reputation token for this universe and migrate legacy REP to it
    reputationToken = contractsFixture.applySignature('ReputationToken', universe.getReputationToken())
    legacyRepContract.approve(reputationToken.address, REP_TOTAL * REP_DIVISOR)
    reputationToken.migrateFromLegacyRepContract()

    initializeTestAccountBalances(reputationToken)

    # Fast forward to one second after the next reporting window
    contractsFixture.chain.head_state.timestamp = market.getEndTime() + 1

    # Perform designated reports on the other markets so they can finalize and we can redeemWinningTokens later
    assert contractsFixture.designatedReport(otherMarket, otherOutcome, tester.k0)
    assert contractsFixture.designatedReport(binaryMarket, [10**18,0], tester.k0)

    # Perform designated report (if there is one)
    if (len(designatedReporterOutcome) > 0):
        contractsFixture.designatedReport(market, designatedReporterOutcome, getattr(tester, 'k' + str(designatedReporterAccountNum)))

        # If someone disputes the designated reporter outcome
        if (designatedReporterDisputerAccountNum != None):
            # Fast forward to one second after dispute start time
            contractsFixture.chain.head_state.timestamp = market.getDesignatedReportDueTimestamp() + 1

            print "a" + str(designatedReporterDisputerAccountNum) + " is disputing designated reporter outcome"

            # Dispute the designated reporter outcome
            disputerAccountBalance = reputationToken.balanceOf(getattr(tester, 'a' + str(designatedReporterDisputerAccountNum)))
            market.disputeDesignatedReport(OUTCOME_B, 1, False, sender=getattr(tester, 'k' + str(designatedReporterDisputerAccountNum)))
            designatedReporterDisputeBondToken = contractsFixture.applySignature('DisputeBondToken', market.getDesignatedReporterDisputeBondToken())
            assert designatedReporterDisputeBondToken.getMarket() == market.address

            # Ensure correct bond amount was sent to dispute bond token
            assert reputationToken.balanceOf(getattr(tester, 'a' + str(designatedReporterDisputerAccountNum))) == disputerAccountBalance - DESIGNATED_REPORTER_DISPUTE_BOND_AMOUNT - 1
            assert reputationToken.balanceOf(designatedReporterDisputeBondToken.address) == DESIGNATED_REPORTER_DISPUTE_BOND_AMOUNT
            assert designatedReporterDisputeBondToken.getBondRemainingToBePaidOut() == DESIGNATED_REPORTER_DISPUTE_BOND_AMOUNT * 2

            # CONSIDER: Are these asserts required when disputing designated reporter
            # outcome like they are when disputing first/last rerporters outcomes?
            # assert not reportingWindow.isContainerForMarket(market.address)
            # assert universe.isContainerForMarket(market.address)
            # reportingWindow = contractsFixture.applySignature('ReportingWindow', market.getReportingWindow())
            # assert reportingWindow.isContainerForMarket(market.address)

            # Fast forward to reporting start time
            contractsFixture.chain.head_state.timestamp = reportingWindow.getReportingStartTime() + 1

            # Have test accounts report on the outcome
            buyStakeTokens(marketType, designatedReporterDisputeStakes, reputationToken, stakeTokenA, stakeTokenB, stakeTokenC)

            # Fast forward to one second after dispute end time
            contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeEndTime() + 1

    if (round1ReportersDisputerAccountNum != None):
        # Fast forward to one second after dispute start time
        contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeStartTime() + 1

        print "a" + str(designatedReporterDisputerAccountNum) + " is disputing first reporters outcome"

        # Dispute the first reporters result
        disputerAccountBalance = reputationToken.balanceOf(getattr(tester, 'a' + str(round1ReportersDisputerAccountNum)))
        if (round1ReporterDisputeOutcome != None):
            round1ReporterDisputeOutcomePayoutHash = market.derivePayoutDistributionHash(round1ReporterDisputeOutcome, False)
            stakeDelta = contractsFixture.contracts["MarketExtensions"].getPayoutDistributionHashStake(market.address, round1ReporterDisputeOutcomePayoutHash)
            stakeDelta = 1 - stakeDelta
            if stakeDelta < 0:
                stakeDelta = 0
        else:
            round1ReporterDisputeOutcome = []
            stakeDelta = 0
        market.disputeRound1Reporters(round1ReporterDisputeOutcome, stakeDelta, False, sender=getattr(tester, 'k' + str(round1ReportersDisputerAccountNum)))
        round1ReportersDisputeBondToken = contractsFixture.applySignature('DisputeBondToken', market.getRound1ReportersDisputeBondToken())
        assert round1ReportersDisputeBondToken.getMarket() == market.address

        # Ensure correct bond amount was sent to dispute bond token
        assert reputationToken.balanceOf(getattr(tester, 'a' + str(round1ReportersDisputerAccountNum))) == disputerAccountBalance - ROUND1_REPORTERS_DISPUTE_BOND_AMOUNT - stakeDelta
        assert reputationToken.balanceOf(round1ReportersDisputeBondToken.address) == ROUND1_REPORTERS_DISPUTE_BOND_AMOUNT

        assert not reportingWindow.isContainerForMarket(market.address)
        assert universe.isContainerForMarket(market.address)
        assert universe.isContainerForDisputeBondToken(round1ReportersDisputeBondToken.address)
        reportingWindow = contractsFixture.applySignature('ReportingWindow', market.getReportingWindow())
        assert reportingWindow.isContainerForMarket(market.address)

        # Fast forward to reporting start time
        contractsFixture.chain.head_state.timestamp = reportingWindow.getReportingStartTime() + 1

        # Have test accounts report on the outcome
        buyStakeTokens(marketType, round1ReportersDisputeStakes, reputationToken, stakeTokenA, stakeTokenB, stakeTokenC)

        # Fast forward to one second after dispute end time
        contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeEndTime() + 1

    if (round2ReportersDisputerAccountNum != None):
        # Fast forward to one second after dispute start time
        contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeStartTime() + 1

        # Have test account dispute the first reporting result
        print "a" + str(designatedReporterDisputerAccountNum) + " is disputing last reporters outcome (and forking)"

        # Dispute the last reporters result
        disputerAccountBalance = reputationToken.balanceOf(getattr(tester, 'a' + str(round2ReportersDisputerAccountNum)))
        market.disputeRound2Reporters(sender=getattr(tester, 'k' + str(round2ReportersDisputerAccountNum)))
        round2ReportersDisputeBondToken = contractsFixture.applySignature('DisputeBondToken', market.getRound2ReportersDisputeBondToken())
        assert round2ReportersDisputeBondToken.getMarket() == market.address

        # Ensure correct bond amount was sent to dispute bond token
        assert reputationToken.balanceOf(getattr(tester, 'a' + str(round2ReportersDisputerAccountNum))) == disputerAccountBalance - ROUND2_REPORTERS_DISPUTE_BOND_AMOUNT
        assert reputationToken.balanceOf(round2ReportersDisputeBondToken.address) == ROUND2_REPORTERS_DISPUTE_BOND_AMOUNT

        assert not reportingWindow.isContainerForMarket(market.address)
        assert universe.isContainerForMarket(market.address)
        reportingWindow = contractsFixture.applySignature('ReportingWindow', market.getReportingWindow())
        assert reportingWindow.isContainerForMarket(market.address)

        aUniverse = contractsFixture.getOrCreateChildUniverse(universe, market, OUTCOME_A)
        aUniverseReputationToken = contractsFixture.applySignature('ReputationToken', aUniverse.getReputationToken())
        assert aUniverse.address != universe.address
        bUniverse = contractsFixture.getOrCreateChildUniverse(universe, market, OUTCOME_B)
        bUniverseReputationToken = contractsFixture.applySignature('ReputationToken', bUniverse.getReputationToken())
        assert bUniverse.address != universe.address
        cUniverse = contractsFixture.getOrCreateChildUniverse(universe, market, OUTCOME_C)
        cUniverseReputationToken = contractsFixture.applySignature('ReputationToken', cUniverse.getReputationToken())
        assert bUniverse.address != universe.address
        assert aUniverse.address != bUniverse.address
        assert aUniverse.address != cUniverse.address
        assert bUniverse.address != cUniverse.address

        # Participate in the fork by moving REP
        for row in round2ReportersDisputeStakes:
            if (row[1] == OUTCOME_A):
                destinationUniverseReputationToken = aUniverseReputationToken
            elif (row[1] == OUTCOME_B):
                destinationUniverseReputationToken = bUniverseReputationToken
            elif (row[1] == OUTCOME_C):
                destinationUniverseReputationToken = cUniverseReputationToken
            accountBalance = reputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
            reputationToken.migrateOut(destinationUniverseReputationToken.address, getattr(tester, 'a' + str(row[0])), reputationToken.balanceOf(getattr(tester, 'a' + str(row[0]))), sender=getattr(tester, 'k' + str(row[0])))
            assert not reputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
            assert destinationUniverseReputationToken.balanceOf(getattr(tester, 'a' + str(row[0]))) == accountBalance

        # Fast forward to one second after dispute end time
        contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeEndTime() + 1

    if (designatedReporterDisputerAccountNum == None and round1ReportersDisputerAccountNum == None and round2ReportersDisputerAccountNum == None):
        contractsFixture.chain.head_state.timestamp = reportingWindow.getDisputeEndTime() + 1

    tentativeWinningStakeTokenAddress = market.getStakeTokenOrZeroByPayoutDistributionHash(market.getTentativeWinningPayoutDistributionHash())
    tentativeWinningStakeTokenBalance = reputationToken.balanceOf(tentativeWinningStakeTokenAddress)

    totalLosingDisputeBondTokens = calculateTotalLosingDisputeBondTokens(designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, market.getTentativeWinningPayoutDistributionHash())

    # Finalize market (i.e., transfer losing dispute bond tokens to winning stake token)
    print "\nFinalizing markets\n"
    assert market.tryFinalize()
    if (round2ReportersDisputerAccountNum == None):
        assert otherMarket.tryFinalize()
        assert binaryMarket.tryFinalize()
        assert otherMarket.getReportingState() == contractsFixture.contracts['Constants'].FINALIZED()
        assert binaryMarket.getReportingState() == contractsFixture.contracts['Constants'].FINALIZED()

    assert market.getReportingState() == contractsFixture.contracts['Constants'].FINALIZED()
    if (round2ReportersDisputerAccountNum):
        print "Original universe test accounts"
        printTestAccountBalances(reputationToken, False)
        print "A universe test accounts"
        printTestAccountBalances(aUniverseReputationToken, False)
        print "B universe test accounts"
        printTestAccountBalances(bUniverseReputationToken, False)
        print "C universe test accounts"
        printTestAccountBalances(cUniverseReputationToken, False)
    else:
        printTestAccountBalances(reputationToken, False)

    printStakeTokenBalances(reputationToken, stakeTokenA, stakeTokenB, stakeTokenC, False)
    printDisputeBondTokenBalances(reputationToken, designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, round2ReportersDisputeBondToken, False)

    # Verify that losing dispute bonds went to the winning stake token
    if (round2ReportersDisputerAccountNum == None):
        winningStakeToken = contractsFixture.applySignature('StakeToken', market.getFinalWinningStakeToken())
        winningStakeTokenBalance = reputationToken.balanceOf(winningStakeToken.address)

        if (designatedReporterDisputeBondToken and designatedReporterDisputeBondToken.getDisputedPayoutDistributionHash() == market.getTentativeWinningPayoutDistributionHash()):
            assert reputationToken.balanceOf(designatedReporterDisputeBondToken.address) == 0
        if (round1ReportersDisputeBondToken and round1ReportersDisputeBondToken.getDisputedPayoutDistributionHash() == market.getTentativeWinningPayoutDistributionHash()):
            assert reputationToken.balanceOf(round1ReportersDisputeBondToken.address) == 0
        assert winningStakeTokenBalance == tentativeWinningStakeTokenBalance + totalLosingDisputeBondTokens

        print "-------------------------------------------------------"
        print "Winning stake token balance before market finalization: " + str(tentativeWinningStakeTokenBalance / REP_DIVISOR)
        print "Total losing dispute bond tokens: " + str(totalLosingDisputeBondTokens / REP_DIVISOR)
        print "Winning stake token balance after market finalization: " + str(winningStakeTokenBalance / REP_DIVISOR) + "\n"

    if (designatedReporterDisputerAccountNum != None or round1ReportersDisputerAccountNum != None):
        # Migrate losing stake tokens (if no fork occurred)
        if (round2ReportersDisputerAccountNum == None):
            winningStakeTokenBalanceBeforeMigration = reputationToken.balanceOf(winningStakeToken.address)

            # Calculate total losing stake tokens
            totalLosingStakeTokens = 0
            if (market.getFinalPayoutDistributionHash() == stakeTokenA.getPayoutDistributionHash()):
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenB.address)
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenC.address)
            elif (market.getFinalPayoutDistributionHash() == stakeTokenB.getPayoutDistributionHash()):
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenA.address)
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenC.address)
            elif (market.getFinalPayoutDistributionHash() == stakeTokenC.getPayoutDistributionHash()):
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenA.address)
                totalLosingStakeTokens += reputationToken.balanceOf(stakeTokenB.address)

            amountSentToDesignatedReporterDisputeBondToken = 0
            amountSentToRound1ReportersDisputeBondToken = 0
            amountSentToRound2ReportersDisputeBondToken = 0
            # Calculate how many losing tokens should be sent to each winning dispute bond token
            if (designatedReporterDisputeBondToken and designatedReporterDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                designatedReporterDisputeBondTokenBalanceBeforeMigration = reputationToken.balanceOf(designatedReporterDisputeBondToken.address)
                amountNeeded = designatedReporterDisputeBondToken.getBondRemainingToBePaidOut() - designatedReporterDisputeBondTokenBalanceBeforeMigration
                amountSentToDesignatedReporterDisputeBondToken = min(amountNeeded, totalLosingStakeTokens)
            if (round1ReportersDisputeBondToken and round1ReportersDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                round1ReportersDisputeBondTokenBalanceBeforeMigration = reputationToken.balanceOf(round1ReportersDisputeBondToken.address)
                amountNeeded = round1ReportersDisputeBondToken.getBondRemainingToBePaidOut() - round1ReportersDisputeBondTokenBalanceBeforeMigration
                amountSentToRound1ReportersDisputeBondToken = min(amountNeeded, totalLosingStakeTokens - amountSentToDesignatedReporterDisputeBondToken)
            if (round2ReportersDisputeBondToken and round2ReportersDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                round2ReportersDisputeBondTokenBalanceBeforeMigration = reputationToken.balanceOf(round2ReportersDisputeBondToken.address)
                amountNeeded = round2ReportersDisputeBondToken.getBondRemainingToBePaidOut() - round2ReportersDisputeBondTokenBalanceBeforeMigration
                amountSentToRound2ReportersDisputeBondToken = min(amountNeeded, totalLosingStakeTokens - amountSentToRound1ReportersDisputeBondToken - amountSentToDesignatedReporterDisputeBondToken)
            # Calculate remaining losing tokens to be sent to winning stake token
            amountSentToWinningStakeToken = totalLosingStakeTokens - amountSentToRound2ReportersDisputeBondToken - amountSentToRound1ReportersDisputeBondToken - amountSentToDesignatedReporterDisputeBondToken

            print "Migrating losing stake tokens"
            if (market.getFinalPayoutDistributionHash() == stakeTokenA.getPayoutDistributionHash()):
                stakeTokenB.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenB.address) == 0
                stakeTokenC.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenC.address) == 0
            elif (market.getFinalPayoutDistributionHash() == stakeTokenB.getPayoutDistributionHash()):
                stakeTokenA.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenA.address) == 0
                stakeTokenC.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenC.address) == 0
            elif (market.getFinalPayoutDistributionHash() == stakeTokenC.getPayoutDistributionHash()):
                stakeTokenA.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenA.address) == 0
                stakeTokenB.migrateLosingTokens()
                assert reputationToken.balanceOf(stakeTokenB.address) == 0

            if (designatedReporterDisputeBondToken and designatedReporterDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                assert reputationToken.balanceOf(designatedReporterDisputeBondToken.address) == designatedReporterDisputeBondTokenBalanceBeforeMigration + amountSentToDesignatedReporterDisputeBondToken
            if (round1ReportersDisputeBondToken and round1ReportersDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                assert reputationToken.balanceOf(round1ReportersDisputeBondToken.address) == round1ReportersDisputeBondTokenBalanceBeforeMigration + amountSentToRound1ReportersDisputeBondToken
            if (round2ReportersDisputeBondToken and round2ReportersDisputeBondToken.getDisputedPayoutDistributionHash() != market.getFinalPayoutDistributionHash()):
                assert reputationToken.balanceOf(round2ReportersDisputeBondToken.address) == round2ReportersDisputeBondTokenBalanceBeforeMigration + amountSentToRound2ReportersDisputeBondToken
            assert reputationToken.balanceOf(winningStakeToken.address) == winningStakeTokenBalanceBeforeMigration + amountSentToWinningStakeToken

            winningStakeTokenBalance = reputationToken.balanceOf(winningStakeToken.address)

            print "Total losing stake tokens: " + str(totalLosingStakeTokens)
            print "Amount sent to designated reporter dispute bond token: " + str(amountSentToDesignatedReporterDisputeBondToken)
            print "Amount sent to first reporters dispute bond token: " + str(amountSentToRound1ReportersDisputeBondToken)
            print "Amount sent to last reporters dispute bond token: " + str(amountSentToRound2ReportersDisputeBondToken)
            print "Amount sent to winning stake token: : " + str(amountSentToWinningStakeToken)
            print "Winning stake token balance before migration: " + str(winningStakeTokenBalanceBeforeMigration / REP_DIVISOR)
            print "Winning stake token balance after migration: " + str(winningStakeTokenBalance / REP_DIVISOR) + "\n"
            printDisputeBondTokenBalances(reputationToken, designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, round2ReportersDisputeBondToken, False)

        winningOutcome = OUTCOME_A
        if (market.getFinalPayoutDistributionHash() == stakeTokenB.getPayoutDistributionHash()):
            winningOutcome = OUTCOME_B
        elif (market.getFinalPayoutDistributionHash() == stakeTokenC.getPayoutDistributionHash()):
            winningOutcome = OUTCOME_C

        # Redeem winning/forked stake tokens
        handleStakeTokens(market, designatedReporterAccountNum, designatedReporterDisputerAccountNum, round1ReportersDisputerAccountNum, round1ReporterDisputeOutcome, stakeDelta, round2ReportersDisputerAccountNum, designatedReporterDisputeStakes, round1ReportersDisputeStakes, round2ReportersDisputeStakes, reputationToken, stakeTokenA, stakeTokenB, stakeTokenC, aUniverseReputationToken, bUniverseReputationToken, cUniverseReputationToken, winningStakeToken, OUTCOME_A, OUTCOME_B, OUTCOME_C, designatedReporterStake, winningOutcome)

        contractsFixture.chain.head_state.timestamp = reportingWindow.getEndTime() + 1

        # Have correct dispute bond holders withdraw from dispute token
        withdrawBondsFromDisputeTokens(market, round2ReportersDisputeStakes, designatedReporterDisputerAccountNum, round1ReportersDisputerAccountNum, round2ReportersDisputerAccountNum, designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, round2ReportersDisputeBondToken, reputationToken, winningStakeToken, aUniverse, bUniverse, cUniverse, aUniverseReputationToken, bUniverseReputationToken, cUniverseReputationToken, OUTCOME_A, OUTCOME_B, OUTCOME_C)

    print "Final test account balances"
    if (round2ReportersDisputerAccountNum):
        print "Original universe test accounts"
        printTestAccountBalances(reputationToken, True)
        print "A universe test accounts"
        printTestAccountBalances(aUniverseReputationToken, True)
        print "B universe test accounts"
        printTestAccountBalances(bUniverseReputationToken, True)
        print "C universe test accounts"
        printTestAccountBalances(cUniverseReputationToken, True)
    else:
        printTestAccountBalances(reputationToken, True)

    for row in expectedAccountBalances:
        if (row[1] == OUTCOME_A):
            assert row[2] == aUniverseReputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
        elif (row[1] == OUTCOME_B):
            assert row[2] == bUniverseReputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
        elif (row[1] == OUTCOME_C):
            assert row[2] == cUniverseReputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
        elif (row[1] == None):
            assert row[2] == reputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))

def handleStakeTokens(market, designatedReporterAccountNum, designatedReporterDisputerAccountNum, round1ReportersDisputerAccountNum, round1ReporterDisputeOutcome, stakeDelta, round2ReportersDisputerAccountNum, designatedReporterDisputeStakes, round1ReportersDisputeStakes, round2ReportersDisputeStakes, reputationToken, stakeTokenA, stakeTokenB, stakeTokenC, aUniverseReputationToken, bUniverseReputationToken, cUniverseReputationToken, winningStakeToken, OUTCOME_A, OUTCOME_B, OUTCOME_C, designatedReportStake, winningOutcome):
    if (round2ReportersDisputerAccountNum):
        # Reputation staked on a particular outcome must be redeemed only on the universe for that outcome.
        # Reputation held in a dispute bond against a particular outcome must be redeemed on a universe other than the disputed outcome.
        migrators = {}
        for row in round2ReportersDisputeStakes:
            migrators[row[0]] = row[1]

        print 'Migrators array:'
        print str(migrators) + "\n"

        for row in designatedReporterDisputeStakes:
            destinationReputationToken = None
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_A):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe A"
                stakeToken = stakeTokenA
                destinationReputationToken = aUniverseReputationToken
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_B):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe B"
                stakeToken = stakeTokenB
                destinationReputationToken = bUniverseReputationToken
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_C):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe C"
                stakeToken = stakeTokenC
                destinationReputationToken = cUniverseReputationToken
            if (destinationReputationToken):
                accountBalanceBeforeRedemption = destinationReputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
                stake = row[2]
                if row[0] == designatedReporterAccountNum:
                    stake += designatedReportStake
                if (designatedReporterDisputerAccountNum == row[0] and migrators[row[0]] == OUTCOME_B):
                    stake += 1
                if (round1ReportersDisputerAccountNum == row[0] and migrators[row[0]] == round1ReporterDisputeOutcome):
                    stake += stakeDelta
                expectedWinnings = reputationToken.balanceOf(stakeToken.address) * stake / stakeToken.totalSupply()
                print "accountBalanceBeforeRedemption: " + str(accountBalanceBeforeRedemption)
                print "expectedWinnings: " + str(expectedWinnings)
                stakeToken.redeemForkedTokens(sender=getattr(tester, 'k' + str(row[0])))
                assert destinationReputationToken.balanceOf(getattr(tester, 'a' + str(row[0]))) == accountBalanceBeforeRedemption + expectedWinnings
                print "Transferred " + str(expectedWinnings) + " to account a" + str(row[0]) + "\n"

        for row in round1ReportersDisputeStakes:
            destinationReputationToken = None
            print row
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_A):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe A"
                stakeToken = stakeTokenA
                destinationReputationToken = aUniverseReputationToken
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_B):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe B"
                stakeToken = stakeTokenB
                destinationReputationToken = bUniverseReputationToken
            if (migrators[row[0]] and migrators[row[0]] == OUTCOME_C):
                print "Redeeming forked stake tokens for tester.a" + str(row[0]) + " on universe C"
                stakeToken = stakeTokenC
                destinationReputationToken = cUniverseReputationToken
            if (destinationReputationToken):
                accountBalanceBeforeRedemption = destinationReputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
                stake = row[2]
                if row[0] == designatedReporterAccountNum:
                    stake += designatedReportStake
                if (designatedReporterDisputerAccountNum == row[0] and migrators[row[0]] == OUTCOME_B):
                    stake += 1
                if (round1ReportersDisputerAccountNum == row[0] and migrators[row[0]] == round1ReporterDisputeOutcome):
                    stake += stakeDelta
                expectedWinnings = reputationToken.balanceOf(stakeToken.address) * stake / stakeToken.totalSupply()
                print "accountBalanceBeforeRedemption: " + str(accountBalanceBeforeRedemption)
                print "expectedWinnings: " + str(expectedWinnings)
                stakeToken.redeemForkedTokens(sender=getattr(tester, 'k' + str(row[0])))
                assert destinationReputationToken.balanceOf(getattr(tester, 'a' + str(row[0]))) == accountBalanceBeforeRedemption + expectedWinnings
                print "Transferred " + str(expectedWinnings) + " to account a" + str(row[0]) + "\n"

        print "Original universe test accounts"
        printTestAccountBalances(reputationToken, False)
        print "A universe test accounts"
        printTestAccountBalances(aUniverseReputationToken, False)
        print "B universe test accounts"
        printTestAccountBalances(bUniverseReputationToken, False)
        print "C universe test accounts"
        printTestAccountBalances(cUniverseReputationToken, False)
    else:
        # Calculate total stake tokens staked on winning outcome
        totalStakedOnWinningOutcome = 0
        winningOutcomeStakes = {}
        if (winningStakeToken.getPayoutDistributionHash() == market.getDesignatedReportPayoutHash()):
            winningOutcomeStakes[designatedReporterAccountNum] = designatedReportStake
        if (designatedReporterDisputerAccountNum != None and winningOutcome == OUTCOME_B):
            winningOutcomeStakes[designatedReporterDisputerAccountNum] = 1
        if (round1ReportersDisputerAccountNum != None and winningOutcome == round1ReporterDisputeOutcome):
            if (round1ReportersDisputerAccountNum not in winningOutcomeStakes):
                winningOutcomeStakes[round1ReportersDisputerAccountNum] = 0
            winningOutcomeStakes[round1ReportersDisputerAccountNum] += stakeDelta
        for row in designatedReporterDisputeStakes:
            if (market.derivePayoutDistributionHash(row[1], False) == winningStakeToken.getPayoutDistributionHash()):
                totalStakedOnWinningOutcome += row[2]
                if (row[0] in winningOutcomeStakes):
                    winningOutcomeStakes[row[0]] += row[2]
                else:
                    winningOutcomeStakes.update({row[0]: row[2]})
        for row in round1ReportersDisputeStakes:
            if (market.derivePayoutDistributionHash(row[1], False) == winningStakeToken.getPayoutDistributionHash()):
                totalStakedOnWinningOutcome += row[2]
                if (row[0] in winningOutcomeStakes):
                    winningOutcomeStakes[row[0]] += row[2]
                else:
                    winningOutcomeStakes.update({row[0]: row[2]})

        print "Total stake tokens staked on winning outcome: " + str(totalStakedOnWinningOutcome)
        print winningOutcomeStakes
        print ""

        print "Redeeming winning stake tokens"


        for key in winningOutcomeStakes:
            accountBalanceBeforeRedemption = reputationToken.balanceOf(getattr(tester, 'a' + str(key)))
            expectedWinnings = reputationToken.balanceOf(winningStakeToken.address) * winningOutcomeStakes[key] / winningStakeToken.totalSupply()
            winningStakeToken.redeemWinningTokens(sender=getattr(tester, 'k' + str(key)))
            assert reputationToken.balanceOf(getattr(tester, 'a' + str(key))) == accountBalanceBeforeRedemption + expectedWinnings
            print "Transferred " + str(expectedWinnings) + " to account a" + str(key)
        printTestAccountBalances(reputationToken, False)

def withdrawBondsFromDisputeTokens(market, round2ReportersDisputeStakes, designatedReporterDisputerAccountNum, round1ReportersDisputerAccountNum, round2ReportersDisputerAccountNum, designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, round2ReportersDisputeBondToken, reputationToken, winningStakeToken, aUniverse, bUniverse, cUniverse, aUniverseReputationToken, bUniverseReputationToken, cUniverseReputationToken, OUTCOME_A, OUTCOME_B, OUTCOME_C):
    if (round2ReportersDisputerAccountNum == None):
        if (designatedReporterDisputeBondToken and market.getFinalPayoutDistributionHash() != designatedReporterDisputeBondToken.getDisputedPayoutDistributionHash()):
            print "Withdrawing designated reporter dispute bond tokens"
            accountBalanceBeforeWithdrawl = reputationToken.balanceOf(designatedReporterDisputeBondToken.getBondHolder())
            disputeBondTokenBalanceBeforeWithdrawl = reputationToken.balanceOf(designatedReporterDisputeBondToken.address)
            designatedReporterDisputeBondToken.withdraw(sender=getattr(tester, 'k' + str(designatedReporterDisputerAccountNum)))
            assert reputationToken.balanceOf(designatedReporterDisputeBondToken.address) == 0
            assert reputationToken.balanceOf(designatedReporterDisputeBondToken.getBondHolder()) == accountBalanceBeforeWithdrawl + disputeBondTokenBalanceBeforeWithdrawl
        if (round1ReportersDisputeBondToken and market.getFinalPayoutDistributionHash() != round1ReportersDisputeBondToken.getDisputedPayoutDistributionHash()):
            print "Withdrawing first reporters dispute bond tokens"
            accountBalanceBeforeWithdrawl = reputationToken.balanceOf(round1ReportersDisputeBondToken.getBondHolder())
            disputeBondTokenBalanceBeforeWithdrawl = reputationToken.balanceOf(round1ReportersDisputeBondToken.address)
            round1ReportersDisputeBondToken.withdraw(sender=getattr(tester, 'k' + str(round1ReportersDisputerAccountNum)))
            assert reputationToken.balanceOf(round1ReportersDisputeBondToken.address) == 0
            assert reputationToken.balanceOf(round1ReportersDisputeBondToken.getBondHolder()) == accountBalanceBeforeWithdrawl + disputeBondTokenBalanceBeforeWithdrawl
    else:
        # Withdraw dispute bond tokens to the universe the disputers migrated to
        print "All reporters dispute stakes:"
        for row in round2ReportersDisputeStakes:
            disputeAccountNum = None
            disputeBondToken = None
            print str(row) + "\n"
            if (row[0] == designatedReporterDisputerAccountNum):
                disputeAccountNum = designatedReporterDisputerAccountNum
                disputeBondToken = designatedReporterDisputeBondToken
                disputeBondTokenBalanceBeforeWithdrawl = reputationToken.balanceOf(disputeBondToken.address)
                destinationUniverse = None
                destinationUniverseReputationToken = None
                #print "disputedPayoutDistributionHash:" + str(disputeBondToken.getDisputedPayoutDistributionHash())
                #print "market.derivePayoutDistributionHash(row[1], False): " + str(market.derivePayoutDistributionHash(row[1], False))
                if (disputeBondToken.getDisputedPayoutDistributionHash() != market.derivePayoutDistributionHash(row[1], False)):
                    if (row[1] == OUTCOME_A):
                        destinationUniverse = aUniverse
                        destinationUniverseReputationToken = aUniverseReputationToken
                        print "Withdrawing designated reporter dispute bond tokens for a" + str(row[0]) + " to universe A"
                    elif (row[1] == OUTCOME_B):
                        destinationUniverse = bUniverse
                        destinationUniverseReputationToken = bUniverseReputationToken
                        print "Withdrawing designated reporter dispute bond tokens for a" + str(row[0]) + " to universe B"
                    elif (row[1] == OUTCOME_C):
                        destinationUniverse = cUniverse
                        destinationUniverseReputationToken = cUniverseReputationToken
                        print "Withdrawing designated reporter dispute bond tokens for a" + str(row[0]) + " to universe C"
                    if (destinationUniverse and destinationUniverseReputationToken):
                        accountBalanceBeforeWithdrawl = destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder())
                        disputeBondToken.withdrawToUniverse(destinationUniverse.address, sender=getattr(tester, 'k' + str(disputeAccountNum)))
                        assert reputationToken.balanceOf(disputeBondToken.address) == 0
                        assert destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder()) == accountBalanceBeforeWithdrawl + disputeBondTokenBalanceBeforeWithdrawl
                        printTestAccountBalances(destinationUniverseReputationToken, True)
            if (row[0] == round1ReportersDisputerAccountNum):
                disputeAccountNum = round1ReportersDisputerAccountNum
                disputeBondToken = round1ReportersDisputeBondToken
                disputeBondTokenBalanceBeforeWithdrawl = reputationToken.balanceOf(disputeBondToken.address)
                destinationUniverse = None
                destinationUniverseReputationToken = None
                #print "disputedPayoutDistributionHash:" + str(disputeBondToken.getDisputedPayoutDistributionHash())
                #print "market.derivePayoutDistributionHash(row[1]): " + str(market.derivePayoutDistributionHash(row[1]))
                if (disputeBondToken.getDisputedPayoutDistributionHash() != market.derivePayoutDistributionHash(row[1])):
                    if (row[1] == OUTCOME_A):
                        destinationUniverse = aUniverse
                        destinationUniverseReputationToken = aUniverseReputationToken
                        print "Withdrawing first reporters dispute bond tokens for a" + str(row[0]) + " to universe A"
                    elif (row[1] == OUTCOME_B):
                        destinationUniverse = bUniverse
                        destinationUniverseReputationToken = bUniverseReputationToken
                        print "Withdrawing first reporters dispute bond tokens for a" + str(row[0]) + " to universe B"
                    elif (row[1] == OUTCOME_C):
                        destinationUniverse = cUniverse
                        destinationUniverseReputationToken = cUniverseReputationToken
                        print "Withdrawing first reporters dispute bond tokens for a" + str(row[0]) + " to universe C"
                    if (destinationUniverse and destinationUniverseReputationToken):
                        accountBalanceBeforeWithdrawl = destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder())
                        disputeBondToken.withdrawToUniverse(destinationUniverse.address, sender=getattr(tester, 'k' + str(disputeAccountNum)))
                        assert reputationToken.balanceOf(disputeBondToken.address) == 0
                        assert destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder()) == accountBalanceBeforeWithdrawl + disputeBondTokenBalanceBeforeWithdrawl
                        printTestAccountBalances(destinationUniverseReputationToken, True)
            if (row[0] == round2ReportersDisputerAccountNum):
                disputeAccountNum = round2ReportersDisputerAccountNum
                disputeBondToken = round2ReportersDisputeBondToken
                disputeBondTokenBalanceBeforeWithdrawl = reputationToken.balanceOf(disputeBondToken.address)
                destinationUniverse = None
                destinationUniverseReputationToken = None
                #print "disputedPayoutDistributionHash:" + str(disputeBondToken.getDisputedPayoutDistributionHash())
                #print "market.derivePayoutDistributionHash(row[1], False): " + str(market.derivePayoutDistributionHash(row[1], False))
                if (disputeBondToken.getDisputedPayoutDistributionHash() != market.derivePayoutDistributionHash(row[1], False)):
                    if (row[1] == OUTCOME_A):
                        destinationUniverse = aUniverse
                        destinationUniverseReputationToken = aUniverseReputationToken
                        print "Withdrawing last reporters dispute bond tokens for a" + str(row[0]) + " to universe A"
                    elif (row[1] == OUTCOME_B):
                        destinationUniverse = bUniverse
                        destinationUniverseReputationToken = bUniverseReputationToken
                        print "Withdrawing last reporters dispute bond tokens for a" + str(row[0]) + " to universe B"
                    elif (row[1] == OUTCOME_C):
                        destinationUniverse = cUniverse
                        destinationUniverseReputationToken = cUniverseReputationToken
                        print "Withdrawing last reporters dispute bond tokens for a" + str(row[0]) + " to universe C"
                    if (destinationUniverse and destinationUniverseReputationToken):
                        accountBalanceBeforeWithdrawl = destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder())
                        disputeBondToken.withdrawToUniverse(destinationUniverse.address, sender=getattr(tester, 'k' + str(disputeAccountNum)))
                        assert reputationToken.balanceOf(disputeBondToken.address) == 0
                        assert destinationUniverseReputationToken.balanceOf(disputeBondToken.getBondHolder()) == accountBalanceBeforeWithdrawl + disputeBondTokenBalanceBeforeWithdrawl
                        printTestAccountBalances(destinationUniverseReputationToken, True)

def printTestAccountBalances(reputationToken, showRepFractions):
    divisor = REP_DIVISOR
    if (showRepFractions):
        divisor = 1
    for accountNum in xrange(0, 10):
        print "a" + str(accountNum) + ": " + bytesToHexString(getattr(tester, 'a' + str(accountNum))) + " | " + str(reputationToken.balanceOf(getattr(tester, 'a' + str(accountNum))) / divisor)
    print ""

def printStakeTokenBalances(reputationToken, stakeTokenA, stakeTokenB, stakeTokenC, showRepFractions):
    divisor = REP_DIVISOR
    if (showRepFractions):
        divisor = 1
    print "----- REPORTING TOKEN BALANCES -----"
    print str(reputationToken.balanceOf(stakeTokenA.address) / divisor)
    print str(reputationToken.balanceOf(stakeTokenB.address) / divisor)
    print str(reputationToken.balanceOf(stakeTokenC.address) /divisor) + "\n"

def printDisputeBondTokenBalances(reputationToken, designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, round2ReportersDisputeBondToken, showRepFractions):
    divisor = REP_DIVISOR
    if (showRepFractions):
        divisor = 1
    print "----- DISPUTE BOND TOKEN BALANCES -----"
    if (designatedReporterDisputeBondToken):
        print "designatedReporterDisputeBondToken balance: " + str(reputationToken.balanceOf(designatedReporterDisputeBondToken.address) / divisor)
    if (round1ReportersDisputeBondToken):
        print "round1ReportersDisputeBondToken balance: " + str(reputationToken.balanceOf(round1ReportersDisputeBondToken.address) / divisor)
    if (round2ReportersDisputeBondToken):
        print "round2ReportersDisputeBondToken balance: " + str(reputationToken.balanceOf(round2ReportersDisputeBondToken.address) / divisor)
    print ""

# Put 1 million REP tokens in tester.a0-tester.a8 and the remainder in tester.a9
def initializeTestAccountBalances(reputationToken):
    print "Initializing test account balances"
    originalAccountBalance = 1 * 10**6 * REP_DIVISOR
    numOfTesterAccounts = 10
    for accountNum in xrange(0, numOfTesterAccounts-1):
        reputationToken.transfer(getattr(tester, 'a' + str(accountNum)), originalAccountBalance)
    reputationToken.transfer(tester.a9, reputationToken.balanceOf(tester.a0) - originalAccountBalance)
    print ""

def buyStakeTokens(marketType, disputeStakes, reputationToken, stakeTokenA, stakeTokenB, stakeTokenC):
    print "Buying stake tokens"
    for row in disputeStakes:
        accountBalance = reputationToken.balanceOf(getattr(tester, 'a' + str(row[0])))
        if (marketType == MARKET_TYPE_CATEGORICAL):
            if (row[1] == CATEGORICAL_OUTCOME_A):
                stakeToken = stakeTokenA
            elif (row[1] == CATEGORICAL_OUTCOME_B):
                stakeToken = stakeTokenB
            elif (row[1] == CATEGORICAL_OUTCOME_C):
                stakeToken = stakeTokenC
        elif (marketType == MARKET_TYPE_SCALAR):
            if (row[1] == SCALAR_OUTCOME_A):
                stakeToken = stakeTokenA
            elif (row[1] == SCALAR_OUTCOME_B):
                stakeToken = stakeTokenB
            elif (row[1] == SCALAR_OUTCOME_C):
                stakeToken = stakeTokenC
        accountStakeTokenBalance = stakeToken.balanceOf(getattr(tester, 'a' + str(row[0])))
        stakeToken.buy(row[2], sender=getattr(tester, 'k' + str(row[0])))
        assert stakeToken.balanceOf(getattr(tester, 'a' + str(row[0]))) == accountStakeTokenBalance + row[2]
        assert reputationToken.balanceOf(getattr(tester, 'a' + str(row[0]))) == accountBalance - row[2]
    print ""

def calculateTotalLosingDisputeBondTokens(designatedReporterDisputeBondToken, round1ReportersDisputeBondToken, tentativeWinningPayoutDistributionHash):
    totalLosingDisputeBondTokens = 0
    if (designatedReporterDisputeBondToken and designatedReporterDisputeBondToken.getDisputedPayoutDistributionHash() == tentativeWinningPayoutDistributionHash):
        totalLosingDisputeBondTokens += DESIGNATED_REPORTER_DISPUTE_BOND_AMOUNT
    if (round1ReportersDisputeBondToken and round1ReportersDisputeBondToken.getDisputedPayoutDistributionHash() == tentativeWinningPayoutDistributionHash):
        totalLosingDisputeBondTokens += ROUND1_REPORTERS_DISPUTE_BOND_AMOUNT
    return totalLosingDisputeBondTokens
