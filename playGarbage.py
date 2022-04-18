
from random import randint
from string import printable

def hawkid():
    return(["nthageman"])

def createDeck(ncards=13, suits=('\u2660','\u2661','\u2662','\u2663')):
    return([(i+1, x) for x in suits for i in range(ncards)])

def scramble(D):
    for i in range(len(D)):
        swap = randint(0, len(D)-1)
        temp = D[-1-i]
        D[-1-i] = D[swap]
        D[swap] = temp
    return(D)

def dealTables(sizes, deck):
    table = []
    for i in range(len(sizes)):
        player_hand = []
        for index in range(sizes[i]):
            position = []
            position.append(False)
            position.append(deck[-1])
            deck.remove(deck[-1])
            player_hand.append(position)
        table.append(player_hand)
    return(table)

def unfilled(T):
    return(all([i for x in T for i in x if i == True or i == False]) == False)

def displayCard(c):
    return(c[-1] + str(c[-2]))

def showTable(T):
    def showEntry(E):
        if E[0] == False:
            return("[ ]")
        else:
            return("[" + displayCard(E[1]) + "]")
    return("  " + "".join([' ' + str(x+1) + showEntry(T[x]) for x in range(len(T))]))

def showScores(nplayers, S):
    return(", ".join([str(x+1) + ":" + str(S[x]) for x in range(nplayers)]))

def playTurn(c, T):
    if c[0] > len(T) or T[c[0]-1][0] == True:
        print("Discarding", c)
        print(showTable(T))
        return(c)
    else:
        print("Playing %s on location %s" % (displayCard(c), str(c[0])))
        T[c[0]-1][0] = True
        tempCard = T[c[0]-1][1]
        T[c[0]-1][1] = c
        return(playTurn(tempCard, T))
        
def drawCard(deck, discard, size, T):
    if discard == [] or discard[-1][0] > size or T[discard[-1][0]-1][0] == True:
        print("Drawing %s from deck" % displayCard(deck[-1]))
        return(deck.pop(-1))
    else:
        print("Drawing %s from discard" % displayCard(discard[-1]))
        return(discard.pop(-1))

def newGame(nplayers, nrounds):
    return({'nplayers':nplayers, 'round':1, 'scores':[0]*nplayers, 'sizes':[nrounds for x in range(nplayers)], 'suits':nplayers+2, "cardinality":nrounds+3, "current":randint(0,nplayers-1)})

def viewGame(G, i):
    print("\nPlayer" + str(i+1) + " to play (score=" + str(G['scores'][i]) + "):")
    print(showTable(G['tables'][i]))

def play(nplayers=4, nrounds=5):
    # Create and initialize the game.
    G=newGame(nplayers, nrounds)
    # Print out a banner so everyone knows which player is to begin.
    print('Player{} will start the game.\n'.format(G['current']+1))

    # This is the "outer loop." It will keep looping which there is no
    # player who has managed to work the size of their table down to
    # 0, which can only happen if they win nrounds number of
    # rounds. When a player hits 0 size for the next round, the game
    # ends, and that player is declared the winner.
    while 0 not in G['sizes']:
        # Announce the new round. Remember, rounds are 1-indexed
        # because they are just counters used to tell the world what's
        # going on. This value is never used to index another data
        # structure!
        print('Round{}:'.format(G['round']))

        # Each round also starts with an empty discard pile.
        G['discard'] = []
        # FIXME: Each round starts with a freshly scrambled
        # deck. Because the number of suits may exceed 4, you can't
        # use the default value of suits which gives the traditional
        # hearts, spades, etc. Instead, know that printable[36:52] is
        # the string 'ABCDE...Z', a portion of which will do fine as
        # artificial suits.
        G['deck'] = scramble(createDeck(5, printable[36:52])) #WAS []
        # FIXME: Each round starts with a fresh set of tables of
        # appropriate size and from the deck just created.
        G['tables'] = dealTables(G['sizes'], G['deck'])    #WAS [[]]

        # This is the "innter loop." One time through the loop
        # corresponds to an entire round. It's an infinite loop, which
        # can only be exited explicitly, which only occurs when a
        # player has filled or completed his/her table with cards
        # facing up.
        while True:
            # FIXME: print out a representation of the game from the
            # perspective of the current player.
            print(viewGame(G, G['current']))

            # Next, draw a card for the current player, play it, and
            # append the player's discarded card to the discard pile.
            card = drawCard(G['deck'], G['discard'], G['sizes'][G['current']], G['tables'][G['current']])
            G['discard'].append(playTurn(card,G['tables'][G['current']]))

            # FIXME: Check for termination conditions. The round ends
            # if the current player manages to fill their table.
            if unfilled(G['tables'][G['current']]) == False:
                # We've got a winner for this round; decrement their next table size.
                G['sizes'][G['current']] -= 1

                # Calculate score penalty for non-winners.
                for i in range(G['nplayers']):
                    if i != G['current']:
                        # Add in values of face down cards.
                        G['scores'][i] += sum([ G['tables'][i][j][1][0] for j in range(G['sizes'][i]) if not G['tables'][i][j][0] ])

                # Round is over, exit while loop to go on to next one.
                break

            # FIXME: Round still incomplete: increment the current
            # player in G and continue.
            G['current'] = (G['current']+1) % nplayers

        print("Round{} complete: player {} wins the round.".format(G['round'], G['current']+1))
        print("Current scores: {}".format(showScores(G['nplayers'], G['scores'])))
        print("=============================================")
        # Go on to next round; winning player gets to start the round.
        G['round'] = G['round'] + 1

    # Exit from while loop means that someone is a winner!
    print("The winner is Player{}, with a final score of {}.".format(G['current']+1, G['scores'][G['current']]))
play()
