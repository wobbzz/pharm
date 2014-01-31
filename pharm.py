#!/usr/bin/env python3
# kow pharmer v0.1
# Created by: Wobbzz
# Contributors: tr0gd0r
# BTC: 17EZkVxpNmPB1Rwges8g8VAz3T4NRfudCS
# DGC: DKGT5gcQdr8nQsaqLiszR71kMYLjAuCt6F

import socket
import json
import pickle
import os

# Config area
apiport = 4028
pooldb = os.getcwd() + '/pools.dat'  # Pool stored here
workerpw = 'password'

# List of kows (miners). Comment out to remove from script.
# Again, this script is designed so that miners and worker user names can be identified by their last octet #.
# Be mindful of this.

kows = ['192.168.1.100',
        '192.168.1.101',
#        '192.168.1.102',
        '192.168.1.103']


# Objectifies the kows. A lot of these are unused, but here for later use.
class Kowz:
    def __init__(self, host, port=apiport):
        self.__splt = host.split('.')
        self.num = self.__splt[3]
        self.name = 'ScryptKow' + self.num  # Not used, but might utilize it later.
        self.host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _moo(self, cmd):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.host, self._port))
        except:
            print('Unable to connect to host %s' % self.host)
            return None
        self._sock.send(json.dumps(cmd).encode())
        self._resp = b''
        while 1:
            self._buf = self._sock.recv(4096)
            if self._buf:
                self._resp += self._buf
            else:
                break

        # print('%s' % self._resp)  # debugging, shows cgminer response from api

        self._values = json.loads(self._resp[:-1].decode())
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        return self._values

    def summary(self):
        return self._moo({'command': 'summary'})

    def pools(self):
        return self._moo({'command': 'pools'})

    def devDetails(self):
        return self._moo({'command': 'devdetails'})

    def stats(self):
        return self._moo({'command': 'stats'})

    def coin(self):
        return self._moo({'command': 'coin'})

    def notify(self):
        return self._moo({'command': 'notify'})

    def quit(self):
        return self._moo({'command': 'quit'})

    def switchpool(self, n):
        return self._moo({'command': 'switchpool', 'parameter': n})

    def enablepool(self, n):
        return self._moo({'command': 'enablepool', 'parameter': n})

    def disablepool(self, n):
        return self._moo({'command': 'disablepool', 'parameter': n})

    def poolpriority(self, n):
        """Priority (n) should be provided in string format eg. '2,1,3'. """
        return self._moo({'command': 'enablepool', 'parameter': n})

    def addpool(self, pool):
        """Pool credentials should be provided in the format 'URL,USR,PASS'."""
        return self._moo({'command': 'addpool', 'parameter': pool})

    def removepool(self, n):
        return self._moo({'command': 'removepool', 'parameter': n})


# Brand all of our kows.
# This creates all of the miner objects.
herd = [Kowz(i) for i in kows]


# Returns the pool you want to use and manages some db additions.
def selectpool(firstuse=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    if firstuse:
        pools = {}
    else:
        pools = pickle.load(open(pooldb, 'rb'))  # load addresses from file

    correctpool = False
    while not correctpool:
        print("The following coins are available:")
        for coin in pools:
            print(coin)
        coinchoice = input("Enter the coin you want ('n' for new coin): ").lower()  # Use of .lower may not be proper.
                                                                                    # But hey, it works jack.
        if coinchoice == 'n':
            correct = False
            while not correct:
                newcoin = input("Enter the coin abbreviation (BTC/DGC/LTC, etc.): ").lower()
                newpoolnick = input("Enter a nickname for the pool (i.e. cryptopools-a, multipool-all): ").lower()
                newpoolurl = input("Enter the url. (i.e. http://multipool.us:1234): ").lower()
                newpooltype = input("Is this a (w)orker or an (a)ddress based pool? ").lower()
                if newpooltype == 'w':
                    newpoolusr = input("Enter user prefix (i.e. kowpharm. or kowpharm_): ")
                elif newpooltype == 'a':
                    newpoolusr = input("Enter the payment address: ")
                else:
                    break

                os.system('cls' if os.name == 'nt' else 'clear')
                print("Coin: %s\nNickname: %s\nURL: %s\nUser: %s\n" %
                     (newcoin, newpoolnick, newpoolurl, newpoolusr))
                poolconfirm = input("Do you want to add the above (y/n)?").lower()

                if poolconfirm == 'y':  # Add coin/pool to dictionary.
                    pools[newcoin] = {}
                    pools[newcoin][newpoolnick] = {}
                    pools[newcoin][newpoolnick]['url'] = newpoolurl
                    pools[newcoin][newpoolnick]['type'] = newpooltype
                    pools[newcoin][newpoolnick]['usr'] = newpoolusr
                    pools[newcoin][newpoolnick]['pass'] = workerpw
                    pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
                    if firstuse:
                        return
                    else:
                        return pools[newcoin][newpoolnick]  # Only return if this isn't our first time.
                elif input("You didn't confirm. (e)xit or enter to try again.").lower() == 'e':
                    return
                else:
                    break

        if coinchoice in pools:
            correct = False
            while not correct:
                os.system('cls' if os.name == 'nt' else 'clear')
                for nickname, v in pools[coinchoice].items():
                    print(nickname, v)
                nickchoice = input("Enter the nickname of the pool you want to use ('n' for new pool): ").lower()
                if nickchoice == 'n':
                    correct = False
                    while not correct:
                        newpoolnick = input("Enter a nickname for the pool: ").lower()
                        newpoolurl = input("Enter the url. (i.e. http://multipool.us:1234): ").lower()
                        newpooltype = input("Is this a (w)orker or an (a)ddress based pool? ").lower()
                        if newpooltype == 'w':
                            newpoolusr = input("Enter user prefix (i.e. kowpharm. or kowpharm_): ")
                        elif newpooltype == 'a':
                            newpoolusr = input("Enter the payment address: ")
                        else:
                            break

                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Coin: %s\nNickname: %s\nURL: %s\nUser: %s\n" %
                             (coinchoice, newpoolnick, newpoolurl, newpoolusr))
                        poolconfirm = input("Do you want to add the above (y/n)?").lower()

                        if poolconfirm == 'y':  # Add pool to coin dictionary.
                            pools[coinchoice][newpoolnick] = {}
                            pools[coinchoice][newpoolnick]['url'] = newpoolurl
                            pools[coinchoice][newpoolnick]['type'] = newpooltype
                            pools[coinchoice][newpoolnick]['usr'] = newpoolusr
                            pools[coinchoice][newpoolnick]['pass'] = workerpw
                            pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
                            input("Since we added a new pool we need to re-prioritize. Enter to continue.")
                            poolprio(mod=coinchoice)  # Keyword arg lets us skip some unnecessary prompting.
                            return pools[coinchoice][newpoolnick]
                        elif input("You didn't confirm. (e)xit or enter to try again: ").lower() == 'e':
                            return
                        else:
                            break
                elif nickchoice in pools[coinchoice]:
                    return pools[coinchoice][nickchoice]
                elif input("I couldn't find that nickname in the db. (e)xit or enter to try again: ").lower() == 'e':
                    return
                else:
                    pass
        elif input("I couldn't find that nickname in the database. (e)xit or enter to try again: ").lower() == 'e':
            return
        else:
            pass


# Prompts for kow selection and returns appropriate values to build command later.
def selectkow():
    os.system('cls' if os.name == 'nt' else 'clear')
    correct = False
    while not correct:
        choice = input("Enter #'s for the kows you want to manage. (i.e. '1,4,19,31' or 'all'): ").lower()
        if choice == 'all':
            selection = []
            for i in range(1, 32):
                selection.append(str(i))
            print("Setting all kows to stun.\n")
            input('Enter to continue.')
            return selection
        else:
            selection = choice.split(',')
            print("You chose the following kows:")
            for i in selection:
                print(i)
            if input("Is that correct? ").lower() == 'y':
                return selection


# Handles command construction based on pool worker type. Sends addpool() command to single kow.
def addpool(kow, pool):
    status = []
    if pool['type'] == 'a':
        command = pool['url'] + ',' + pool['usr'] + ',' + pool['pass']
        status.append(kow.addpool(command)['STATUS'])
        return status
    elif pool['type'] == 'w':
        command = pool['url'] + ',' + pool['usr'] + str(kow.num) + ',' + pool['pass']
        status.append(kow.addpool(command)['STATUS'])
        return status
    else:
        return 'There was some sort of error with addpool(). Investigate this.'


# Handles removal of coins/pools from db.
def removepool():
    os.system('cls' if os.name == 'nt' else 'clear')
    pools = pickle.load(open(pooldb, 'rb'))  # load addresses from file
    for coin in pools:
        print(coin)
    coinchoice = input("Enter the coin you want to modify: ").lower()
    os.system('cls' if os.name == 'nt' else 'clear')
    if coinchoice in pools:
        if len(pools[coinchoice]) == 1:
            print(pools[coinchoice])
            if input("You only have one pool for this coin. Do you want to delete it (y/n)?").lower() == 'y':
                pools.pop(coinchoice, None)
                pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
                return
        else:
            for pool, v in pools[coinchoice].items():
                print(pool, v)
            poolchoice = input("Enter the pool nickname you want to remove. ('ALL' to delete them all): ")

            if poolchoice == 'ALL':
                pools.pop(coinchoice, None)
                pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
                return
            elif poolchoice.lower() in pools[coinchoice]:
                pools[coinchoice].pop(poolchoice, None)
                pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
                input("Since we removed a pool we need to re-prioritize. Enter to continue.")
                poolprio(mod=coinchoice)
                return
            else:
                input("I didn't find that option in the db. Enter to continue.")
                return
    else:
        return


# Sets the priority of each pool. Priority will be used by multipharm()
def poolprio(mod=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    pools = pickle.load(open(pooldb, 'rb'))  # load addresses from file
    if not mod:
        for coin in pools:
            print(coin)
        coinchoice = input("Enter the coin you want to modify: ").lower()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Here are the pools you have to choose from: \n")
        for pool, v in pools[coinchoice].items():
            print(pool, v)

        count = 0
        total = len(pools[coinchoice])
        accounted = []
    else:
        coinchoice = mod
        count = 0
        total = len(pools[coinchoice])
        accounted = []
        print("Here are the pools you have to choose from: \n")
        for pool, v in pools[coinchoice].items():
            print(pool, v)

    print("\nAll pool nicknames for this coin are required to end this function.\n"
          "Enter them in priority from highest to lowest. ('Q' to quit)")
    while count < total:
        curr = input("pool > ")
        if curr.lower() in pools[coinchoice]:
            if curr.lower() not in accounted:
                pools[coinchoice][curr.lower()]['prio'] = count
                count += 1
                accounted.append(curr.lower())
            else:
                print("You've already entered that pool.")
        elif curr == 'E':
            return
        elif curr.lower() not in pools[coinchoice]:
            input("Couldn't find that choice. Enter to try again.")
        else:
            pass
    pickle.dump(pools, open(pooldb, 'wb'))  # write pool list back to a file
    return


# Switches pools on the kows. If the pool isn't on the kow already, calls addpool() to make it so.
def switchpool(kow, pool):
    poolid = None
    kowstatus = []
    kowpools = kow.pools()['POOLS']  # get the list of pools this kow has
    for p in kowpools:  # iterate through his pools so we can find the his poolid for the pool we chose
        if pool['url'] in p['URL']:
            poolid = int(p['POOL'])
            print(kow.num, poolid)
            kowstatus.append(kow.switchpool(poolid))

    if not poolid:  # If for some reason he doesn't have that pool in the list we'll add it for him
        kowstatus.append(addpool(kow, pool))
        kowpools = kow.pools()['POOLS']  # get the list of pools this kow has again to make sure it stuck :)
        for p in kowpools:  # iterate through his pools so we can find the his poolid for the pool we chose
            if pool['url'] in p['URL']:
                poolid = int(p['POOL'])
                kowstatus.append(kow.switchpool(poolid))
    print(kowstatus)
    return kowstatus


# Handles the menu presented to the user.
def interactiveops():
    done = False
    while not done:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Here's what we can do:\n"
              " (a)dd a pool to the db\n"
              " (r)emove a pool from the db\n"
              " set pool (p)riority in the db\n"
              " (s)witch pools on the kows\n"
              " (m)ultipharm - coming soon\n"
              " (q)uit")
        choice = input("Enter a selection: ").lower()

        if choice == 'a':
            selectpool()
            input("Enter to continue.")
        elif choice == 'r':
            removepool()
        elif choice == 'p':
            poolprio()
        elif choice == 's':
            kowselection = selectkow()
            poolselection = selectpool()
            for kow in herd:
                if kow.num in kowselection:
                    switchpool(kow, poolselection)
            input("pause")
        elif choice == 'm':
            print("Coming soon to a pharm near you.")
            input("Enter to continue.")
        elif choice == 'q':
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        else:
            input("I don't recognize that option. Enter to continue.")


def main():
    # For first time use, create the pool db with at least one pool
    try:
        with open(pooldb):
            pass
    except IOError:
        input("Since this is your first time using this script, let's add at least one pool. Enter to continue.")
        selectpool(firstuse=True)

    interactiveops()

    # cmdops() coming soon for run-once command line based options


if __name__ == '__main__':
    main()