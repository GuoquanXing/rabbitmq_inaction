import sys, json, httplib, urllib, base64, socket

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

conn = httplib.HTTPConnection(server, port)

path = "/api/aliveness-test/%s" % urllib.quote(vhost, safe="")
method="GET"
credentials = base64.b64encode("%s:%s" % (username, password))
try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})
except socket.error:
    print "CRITICAL: Could not connect to %s:%s!" % (server, port)
    exit(EXIT_CRITICAL)

response = conn.getresponse()

if response.status > 299:
    print "CRITICAL: Broker not alive: %s" % response.read()
    exit(EXIT_CRITICAL)
print "OK: Broker alive: %s" % response.read()
exit(EXIT_OK)