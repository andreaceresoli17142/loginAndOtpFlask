from random import randrange
import time

DELTATIME = 90

class TokenData:
    def __init__(self, email):
        self.email = email
        self.token = str(randrange( 0, 999999 )).rjust( 6, "0" )[0:6]
        self.cTime = int(time.time())
    def checkTime(self):
        if int(time.time()) + DELTATIME > self.cTime:
            return False
        return True

def main():
    test = TokenData( "mymail@gimelli.com" )
    print(test.token)

if __name__ == "__main__":
    main()