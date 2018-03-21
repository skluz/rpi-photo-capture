import time, os

class Server:
    claiming = False
    filePath = None

    @staticmethod
    def uploadImage(file):
        UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', "./uploads")
        if file.filename == '':
            raise Exception("file not provided")
        if file and Server.allowed_file(file.filename):
            filename = time.strftime("%Y%m%d-%H%M%S") + ".png"
            filePath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filePath)
            Server.filePath = filePath
            return os.path.getsize(filePath)
        else:
            raise Exception("Cannot upload image")

    @staticmethod
    def claimImage():
        if not Server.claiming:
            Server.claiming = True
            finishAt = time.time() + os.getenv('TIMEOUT', 30)
            while True:
                if Server.filePath != None:
                    newImage = Server.filePath
                    Server.filePath = None
                    Server.claiming = False
                    return newImage
                if time.time() > finishAt:
                    Server.claiming = False
                    raise Exception("Image not ready")
                time.sleep(.1)
        else:
            raise Exception("Cannot request image due to illegal phase: " + Server.claiming)
    
    @staticmethod
    def getState():
        return Server.claiming

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = set(['png'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS        
