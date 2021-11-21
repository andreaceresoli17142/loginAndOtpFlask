import smtplib
from userLoginData import UsrLoginData
from tokenData import TokenData
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import platform

if platform == "linux" or platform == "linux2":
    dataPath = "data//usr.dat"
elif platform == "win32":
    dataPath = "data\\usr.dat"

class LoginManager:
    loginInfo = {}
    pwReset = {}
    otpInfo = {}

    def __init__(self):
        self.__loadUsers()

    def __loadUsers(self):

        with open(dataPath) as usrDataFile:
            for line in usrDataFile:
                splitted = line.split(',')
                self.loginInfo.update({splitted[1]: UsrLoginData( splitted[0], splitted[1], splitted[3], True, int(splitted[2]))})

    def addUser(self, username, email, password):
        if not self.userExists(email):
            self.loginInfo.update({email: UsrLoginData(username, email, password)})
            with open(dataPath, 'a') as usrDataFile:
                usrDataFile.write("\n"+self.loginInfo[email].toString())
            return True
        return False

    def login(self, email, password ):
        if email in self.loginInfo:
            if self.loginInfo[email].verifyPw( password ):
                return True
        return False

    def userExists(self, email):
        if email in self.loginInfo:
            return True
        return False

    def sendResetPwRequest(self, email):
        if self.userExists(email):
            pwResetObj = TokenData(email)
            self.pwReset.update( {email:pwResetObj} )

            msg = MIMEMultipart()
            msg['From'] = 'noReplyMail@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'password reset mail'
            message = "password reset code is: " + str(pwResetObj.token)
            msg.attach(MIMEText(message))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("noreply.64189489@gmail.com", "noreply566778908987967")
            server.sendmail(
            "noreply.64189489@gmail.com",
            email,
            msg=msg.as_string())
            server.quit()

    def resetPwRequest(self, email, token, newPw):
        if email in self.pwReset:
            if self.pwReset[email].checkTime():
                if self.pwReset[email].resetToken == token:
                    if self.userExists(email):
                        self.loginInfo[email].newPassword( newPw )
                        self.pwReset.pop(email)
                        return True
                self.pwReset.pop(email)
        return False

    def requestOtp(self, email):
        if self.userExists(email) and not email in self.otpInfo:
            otpTokenData = TokenData(email)
            self.otpInfo.update({email : otpTokenData})

            msg = MIMEMultipart()
            msg['From'] = 'noReplyMail@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'otp verification mail'
            message = "otp verification code is: " + str(otpTokenData.token)
            msg.attach(MIMEText(message))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("noreply.64189489@gmail.com", "noreply566778908987967")
            server.sendmail(
            "noreply.64189489@gmail.com",
            email,
            msg=msg.as_string())
            server.quit()
        print( self.otpInfo )

    def verifyOtp(self, email, token):
        if email in self.otpInfo:
            if self.otpInfo[email].checkTime():
                if self.otpInfo[email].token == token:
                    self.otpInfo.pop(email)
                    return True
            self.otpInfo.pop(email)
        return False

def main():
    manager = LoginManager()
    manager.requestOtp( "andrea.ceresoli03@gmail.com" )
    print(manager.verifyOtp( "andrea.ceresoli03@gmail.com", input( "insertToken: ") ))
    # manager.sendResetPwRequest( "andrea.ceresoli03@gmail.com" )
    # print(manager.resetPwRequest( "andrea.ceresoli03@gmail.com", input( "insertToken: " ), "test1" ))

if __name__ == "__main__":
    main( )
