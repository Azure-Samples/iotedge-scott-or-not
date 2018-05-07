import io
import time

def capture(output, format):
    try:
        f = open("/home/pi/image/picture.jpg", "rb")
        output.write(f.read())
        f.close()
        time.sleep(1)
    except Exception as e:
        print(e)