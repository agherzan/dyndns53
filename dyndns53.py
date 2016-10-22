import urllib, json
import sys
import time
import signal
import os
import ConfigParser

# Create the bodo configuration out of environment variables
home = os.getenv('HOME')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
if (not aws_access_key_id) or (not aws_secret_access_key):
    print 'ERROR: AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY environment variables not defined.'
    sys.exit(1)
with open(os.path.join(home, '.bodo'),'w') as f:
    f.write('[Credentials]\naws_access_key_id = ' + aws_access_key_id + '\naws_secret_access_key = ' + aws_secret_access_key + '\n')
from area53 import route53

# Load configuration
Config = ConfigParser.ConfigParser()
try:
    Config.read(os.path.join(home, '.dyndns53'))
except:
    print 'ERROR: Failed to parse %s' % os.path.join(home, '.dyndns53')

# Time in between two updates in seconds
timeout=900

def signal_handler(signal, frame):
    print '\nSIGINT caught!'
    sys.exit(0)

def get_public_ip():
    ''' Returns the puiblic IP of '''
    data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
    return data["ip"]

signal.signal(signal.SIGINT, signal_handler)

while True:
    print "\nNew trigger: %s\n=====================================" % time.asctime(time.localtime(time.time()))
    for domain in Config.sections():
        subdomains = []
        try:
            subdomains = Config.get(domain, 'subdomains').split()
        except:
            pass
        try:
            if Config.getboolean(domain, "root"):
                subdomains.append('')
        except:
            pass
        for subdomain in subdomains:
            if subdomain:
                fqdn = '%s.%s' % (subdomain, domain)
            else:
                fqdn = '%s' % (domain)

            zone = route53.get_zone(domain)
            arec = zone.get_a(fqdn)
            new_value = get_public_ip()

            if arec:
                old_value = arec.resource_records[0]

                if old_value == new_value:
                    print '%s already has A record %s.' % (fqdn, new_value)
                    continue

                print 'Updating A for %s: %s to %s.' % (fqdn, old_value, new_value)
                zone.update_a(fqdn, new_value, timeout)
            else:
                print 'Creating A for %s: %s.' % (fqdn, new_value)
                zone.add_a(fqdn, new_value, timeout)
    print "Done. Timeout..."

    time.sleep(timeout)
