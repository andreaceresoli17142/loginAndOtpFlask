import smtplib
from userLoginData import UsrLoginData
from tokenData import TokenData
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class LoginManager:
    loginInfo = []
    pwReset = []
    otpInfo = []

    def __init__(self):
        self.__loadUsers()

    def __loadUsers(self):

        with open("data\\usr.dat") as usrDataFile:
            for line in usrDataFile:
                splitted = line.split(',')
                self.loginInfo.append(UsrLoginData( splitted[0], splitted[1], splitted[3], True, int(splitted[2]) ))

    def addUser(self, username, email, password):
        #! check if valid
        if True:
            self.loginInfo.append(UsrLoginData(username, email, password))
            with open('data\\usr.dat', 'a') as usrDataFile:
                usrDataFile.write("\n"+self.loginInfo[-1].toString())
            return True

    def login(self, email, password ):
        for user in self.loginInfo:
            if user.email == email:
                if user.verifyPw( password ):
                    return True
                return False

    def userExists(self, email):
        for user in self.loginInfo:
            if user.email == email:
                return True
        return False

    def sendResetPwRequest(self, email):
        if self.userExists(email):
            pwResetObj = TokenData(email)
            self.pwReset.append( pwResetObj )

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
        for resObj in self.pwReset:
            if resObj.email == email:
                if resObj.checkTime():
                    if resObj.resetToken == token:
                        for user in self.loginInfo:
                            if user.email == email:
                                #! need to update usr.dat file with new password
                                user.newPassword( newPw )
                        return True
                self.pwReset.remove(resObj)
        #* since two tokens might be equal we have to search through all the token objects
        return False

    def requestOtp(self, email):
        if self.userExists(email):
            otpTokenData = TokenData(email)
            self.otpInfo.append( otpTokenData )

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

    def verifyOtp(self, email, token):
        for otpToken in self.otpInfo:
            if otpToken.email == email:
                if otpToken.checkTime():
                    if otpToken.token == token:
                        return True
                self.otpInfo.remove(otpToken)
        #* since two tokens might be equal we have to search through all the token objects
        return False

def main():
    manager = LoginManager()
    # manager.sendResetPwRequest( "andrea.ceresoli03@gmail.com" )
    # print(manager.resetPwRequest( "andrea.ceresoli03@gmail.com", input( "insertToken: " ), "test1" ))
    manager.requestOtp( "andrea.ceresoli03@gmail.com" )
    print(manager.verifyOtp( "andrea.ceresoli03@gmail.com", input( "insertToken: ") ))

if __name__ == "__main__":
    main( )
