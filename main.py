import re
import sys
import time
import requests

from threading import Thread

API_URL = "http://192.168.122.1:8080/sony/camera"


def info(text):
    """Pretty-print information to the console."""
    print("[info]", text)


def setup_camera():
    """Setup the camera for taking photos."""
    requests.post(API_URL, json={
    	"method": "startRecMode",
    	"params": [],
    	"id": 1,
    	"version": "1.0"
    })


def take_photo():
    """Take a picture with the camera. Returns the photo's URL."""
    print("Taking picture")
    response = requests.post(API_URL, json={
    	"method": "actTakePicture",
    	"params": [],
    	"id": 1,
    	"version": "1.0"
    })
    return response.json()["result"][0][0]


def nonblocking(fn):
    """Run an I/O bound task in a non-blocking fashion using threads."""
    Thread(target=fn).start()


def save_photo(url):
    """Save a photo to the current directory."""
    import os
    filename = re.search("(DSC.*)\.JPG", url).group(1)
    os.system("wget -q --content-disposition {} -O {}.jpg".format(url, filename))
    

def take_and_save_photo():
    """Atomic wrapper function to allow parallelising these two operations."""
    url = take_photo()
    save_photo(url)

    
def timelapse(interval, number_photos):
    """Take a timelapse with `interval` seconds between photos."""
    info("Setting up camera...")
    setup_camera()
    info("Done!")
    for _ in range(number_photos):
        nonblocking(take_and_save_photo)
        time.sleep(interval)
    
    
if __name__ == "__main__":
    try:
        timelapse(float(sys.argv[1]), int(sys.argv[2]))
    except (ValueError, IndexError):
        print("Usage:\n\ttimelapse <interval> <count>")