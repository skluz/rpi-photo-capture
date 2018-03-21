import sys, os, datetime, time, logging
import requests, json

def main():
    SERVER_URL = os.getenv('SERVER_URL', "http://localhost:5000")
    logging.basicConfig(format = '%(asctime)s %(message)s', level = logging.INFO)
    while True:
        try:
            start = datetime.datetime.now()
            stateResponse = requests.get(url = SERVER_URL + "/state")
            if(stateResponse.ok):
                stateData = stateResponse.json()
                if(stateData['state'] == 'requested'):
                    file = open('test.png', 'rb')
                    files = {'file': file}
                    uploadResponse = requests.post(url = SERVER_URL + "/upload", files = files)
                    stop = datetime.datetime.now()
                    if(uploadResponse.ok):
                        logging.info("Photo uploaded in: " + str(stop - start))
                    else:
                        logging.warn("Cannot upload image due too: " + uploadResponse.status_code)
            else:
                logging.warn("State not available")
        except Exception as e:
            logging.error("Cannot upload captured photo: " + str(e))
        time.sleep(2)

if __name__ == '__main__':
    sys.exit(main())        
    