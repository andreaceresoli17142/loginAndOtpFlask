import hashlib
from random import randrange

class UsrLoginData:
    def __init__(self, username :str, email :str, password :str, pwIsHash :bool = False, salt: int = None):
        self.username = username
        self.email = email
        if salt is None:
            self.__salt = randrange( 0, 999999 )
        else:
            self.__salt = salt

        if pwIsHash:
            self.__password = password
        else:
            self.__password = self.__hash(password)

    def __hash( self, string: str):
        m = hashlib.sha256()
        m.update( bytes(self.__salt) )
        m.update( string.encode() )
        return m.hexdigest()

    def verifyPw(self, password: str):
        if self.__password == self.__hash(password):
            return True
        return False

    def newPassword(self, newPw):
        self.__password = self.__password = self.__hash(newPw)

    def toString(self):
        return self.username + "," + self.email + "," + str(self.__salt) + "," + self.__password

def main():
    loginInfo = []
    loginInfo.append( UsrLoginData( "marione", "roma@gimelli.com", "test" ) )
    print(loginInfo[0].verifyPw(input( "insert pw:" )))

if __name__ == "__main__":
    main()