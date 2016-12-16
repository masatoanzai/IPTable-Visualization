#Masato Anzai
#Final Project
#Digital Forensics: NYU
import SimpleHTTPServer
import SocketServer
import os.path
import os
import sys
import argparse
import webbrowser
import re
import fileinput
import json

##UI for the Application
def parse_func():
    parser = argparse.ArgumentParser(description='IPTable Visualizer, Please Specify File Name to Start')
    parser.add_argument("-i","--in_file",metavar="log",type=str,help="Specify name of log file")
    args = parser.parse_args()

    if not args.in_file:
        print "Specify Name of log file with -i, --in_file. -h For more help."
    return args

## Server is enabled
def serverStart(port=8000):
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", port), handler)
	print "****** Starting WebApp on http://127.0.0.1:" + str(port) + "/ ******"
	webbrowser.open("http://127.0.0.1:" + str(port) + "/")
	httpd.serve_forever()

## Log file is parsed using re
def logParse(name):
    fileinput = open(name,'r')
    pair_re = re.compile('([^ ]+)=([^ ]+)')
    wanted_keys = {"SRC","DST"}
    removeKeys = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    with open('result.txt', 'w') as fp:
        for line in fileinput:
            line = line.rstrip()
            data = dict(pair_re.findall(line))
            data = removeKeys(data,wanted_keys)
            for x in data:
                json.dump(data[x], fp)
                fp.write(',')
## Main
def main():
    args = parse_func()
    if args.in_file:
        logParse(args.in_file)
        port = raw_input('Please input port number: ')
        serverStart(int(port))


if __name__ == "__main__":
	main()
