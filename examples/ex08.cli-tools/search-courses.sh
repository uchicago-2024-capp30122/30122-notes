#!/bin/sh
#
grep Online courses.txt | cut -f2,3 | grep Programming > my-courses.txt
cat courses.txt
