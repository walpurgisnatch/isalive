import requests
import re
import argparse
import time
import threading

from queue import Queue

alive = 0
threads = 32
queue = Queue()

def get_args():
    global threads
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="urls", help="Target urls")
    parser.add_argument("-o", dest="output", help="Output file for urls with status 200")
    parser.add_argument("-f", dest="forbidden", help="Output file for urls with status 403")
    parser.add_argument("-t", dest="threads", type=int, help="Threads")
    arguments = parser.parse_args()

    if not arguments.urls:
        parser.error("[-] Error: null target")

    if arguments.threads:
        threads = arguments.threads
    
    return arguments

args = get_args()

def set_url(url):
    try:
        test = httplib.HTTPSConnection(url)
        test.request("GET", "/")
        response = test.getresponse()
        if (response.status == 200) | (response.status == 302):
            url = "https://www." + str(url)
        else:
            url = "http://www." + str(url)
    except:
        url = "http://" + str(url)
    return url

def print_result():
    print("[{}] urls alive\n".format(alive))

def get_last(url):
    url = re.search('^[^?]+', url)
    return url.group(0)

def write_line(fname, data):
    with open(fname, 'a') as f:
        f.write(data + '\n')

def threader():
    while True:
        url = queue.get()
        check_url(url)
        queue.task_done()

def walk_through():
    for x in range(threads):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    f = open(args.urls, "r")
    for line in f:
        try:
            queue.put(line.strip())
        except:
            pass
    f.close()

    queue.join()
    

def check_url(url):
    global alive
    try:
        response = requests.get(url, timeout=10)
        if get_last(response.url) == get_last(url):
            if response.status_code == 200:
                write_line(args.output, url)
                print(url + "\n")
                alive += 1
            if response.status_code == 403 and args.forbidden:
                write_line(args.forbidden, url)
                alive += 1
    except Exception as e:
        return   


def main():
    try:
        walk_through()
        print("Done\n")
        print_result()
    except KeyboardInterrupt:
        print_result()
        print("\nAborted\n")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main() 
