#!/bin/sh
#
echo "GET / HTTP/1.1
Host: localhost:8001
User-Agent: curl/8.4.0
Accept: */*\n\n"
curl -D - http://localhost:8001/
