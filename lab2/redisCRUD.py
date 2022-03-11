from redis import StrictRedis
import sys
import argparse
parser=argparse.ArgumentParser(description='Press Ctrl+C to Exit.')
args=parser.parse_args()

#So not to type ip every time. It's suppossed to be the same if elastic.
hostname="44.203.88.217" 
password=input("password: \n->")


r = StrictRedis(host=hostname,port=6379,password=password,db=0)

def getPacktWelcome(key):
    #GET value stored in key
    print("Displaying current welcome message...")
    value = r.get(key)
    print("message:  " + str(value))


def setPacktWelcome(key,val):
    #SET new value key
    print("Writing",val,"to Redis...")
    r.set(key,val)

def main():
    print("Connect to a database")
    while(1):
        method=input()
        if "GET" in method:
            getPacktWelcome(input("key:\n->"))
        if "SET" in method:
            setPacktWelcome(input("key:\n->"),input("value:\n->"))
            print("->")


if __name__ == "__main__":
    main()
