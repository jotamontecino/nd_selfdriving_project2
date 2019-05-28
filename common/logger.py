class Logger:
    __instance = None
    __env = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self, env):
        """ Virtually private constructor. """
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self
            Logger.__instance.__env = env

    def info(self, txt):
        if(self.__instance.__env != "production" ):
            output = "INFO: %s"%(txt)
            print(output)
    def warning(self, txt):
        output = "WARNING: %s"%(txt)
        print(output)
