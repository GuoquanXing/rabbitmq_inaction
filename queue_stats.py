import sys, json, httplib, urllib, base64

if len(sys.argv) < 6:
    print "USAGE: queue_stats.py server_name:port auth_user " + \
        "auth_pass VHOST QUEUE_NAME"
    sys.exit(1)

server, port = sys.argv[1].split(":")
username = sys.argv[2]
password = sys.argv[3]
vhost = sys.argv[4]
queue_name = sys.argv[5]

# Build API path for queue operation
vhost = urllib.quote(vhost, safe='')
queue_name = urllib.quote(queue_name, safe='')
path = "/api/queues/%s/%s" % (vhost, queue_name)
method = "GET"

 # issue API request to get queue stats
conn = httplib.HTTPConnection(server, port)
credentials = base64.b64encode("%s:%s" % (username, password))
headers = {"Content-Type" : "application/json",
           "Authorization" : "Basic " + credentials}
conn.request(method, path, "", headers)
response = conn.getresponse()
if response.status > 299:
    print "Error executing API call (%d): %s" % (response.status,
                                                 response.read())
    sys.exit(2)
 
# Parse and dislay queue stats from response
payload = json.loads(response.read())
print "\tMemory Used (bytes): " + str(payload["memory"])
print "\tConsumer Count: " + str(payload["consumers"])
print "\tMessages:"
print "\t\tUnack'd: " + str(payload["messages_unacknowledged"])
print "\t\tReady: " + str(payload["messages_ready"])
print "\t\tTotal: " + str(payload["messages"])
sys.exit(0)