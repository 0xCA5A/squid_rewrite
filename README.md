# squid_rewrite
Example how to modify data from HTTP pages on the proxy using squid and its redirectors.

## How to build and run a squid_rewrite docker container

### Build and run a container
```
$ ./build_and_run.sh $(pwd)/squid_rewrite.conf 
```

## Demo pages
 * http://www.columbia.edu/~fdc/sample.html
 * http://www.euro.who.int/en/home
 * http://bluecare.ch

### Follow the data
Who connects?
```
$ docker exec -it squid_rewrite tail -f /var/log/squid/access.log
```
```
$ docker exec -it squid_rewrite tail -f /var/log/squid/cache.log
```
What is changed by us?
```
$ docker exec -it squid_rewrite tail -f /var/log/squid/rewrite.log
```

## Testing
```
$ curl -x http://localhost:3128 -I https://www.bluecare.ch
```
```
$ opera --proxy-server="127.0.0.1:3128"
```

## Doc
* https://wiki.squid-cache.org/Features/Redirectors
