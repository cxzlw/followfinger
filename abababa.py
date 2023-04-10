# Read username, output from non-empty factory, drop connections

from twisted.internet import protocol, reactor
from twisted.protocols import basic


class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        self.transport.write(self.factory.getUser(user).encode() + b"\r\n")
        self.transport.loseConnection()


class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        print(user)
        return self.users.get(user.decode(), "No such user")


reactor.listenTCP(79, FingerFactory(moshez='Happy and well'))
reactor.run()
