import logging
from src.pipeline import Step
import uuid
import os
import time
import thre
import urllib, json
import subprocess
from multiprocessing import Process, Queue
import signal

class FrameRipper:
    def __init__(self, inputs_list, thread_count=50):
        super().__init__()
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)
        self.THREAD_COUNT = thread_count
        self.threads = []
        self.inputs_list = []

    def run_command(self, string_cmd):
        process = None
        try:
            process = subprocess.Popen(string_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data,error = process.communicate()
            code = process.returncode
            process.kill()
            if code != 0:
                raise Exception(f"Command {string_cmd} Failed: {error}")
            return data
        except Exception as e :
            print(f"Failed command: {str(process.pid)}")
            process.terminate() 
            raise e    
             
    def process_callback(self, input_url):
        outputfile = None
        try :
            print(f"Rip started: {input_url}")
            url = (self.run_command(f"youtube-dl --get-url {input_url}")).decode("utf-8") 
            time.sleep(0.5)

        except Exception as e :
            logging.error(e)
            print(input_url + " died.")

    
    def run_rip(self):
        for url in self.inputs_list:
            for i in range(self.THREAD_COUNT):
                self.threads.append(threading.Thread(target=self.process_callback(url)))
        
        while len([t for t in self.threads if t.is_alive()]) > 0:
            time.sleep(1)

def main():
    url = "" #youtube video manefest

    response = urllib.urlopen(url)

    data = list(json.loads(response.read()))

    ripper = FrameRipper(data, thread_count=10)

    ripper.run_rip()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

