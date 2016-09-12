# dyndns53

Tool for updating your Amazon Route53 DNS A records to the current external IP of a running machine.

## Configuration

There are two configurations that are needed for this tool to work properly:
+ AWS credentials which need to be provided via environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. Make sure that you have access to modify the DNS records.
+ A tool's configuration text file which needs to reside in ~/.dyndns53

## ~/.dyndns53 configuration file

The configuration file should contain blocks of the following format:
```
[bar.com]
subdomains: foo
root: True
```

Each section is a domain. `subdomains` option need to include all the subdomains for which this tool will update the A record. The `root` option needs to be boolean and will determine if the tool will update the record for the root domain too.

Example:
```
[bar.com]
subdomains: foo www
root: True

[test.com]
root: True
```

The above configuration will update the A record of the following fully qualified domain names to the current external IP address:
+ foo.bar.com
+ www.bar.com
+ bar.com
+ test.com

## Running the container
docker run -v /where/i/put/my/files/.dyndns53:/root/.dyndns53:ro -e AWS_ACCESS_KEY_ID=XXX -e AWS_SECRET_ACCESS_KEY=YYY alephan/dyndns53
