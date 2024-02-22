#!/bin/bash

cut -f2 courses.txt | sort | uniq > course_names.txt
echo "wrote course_names.txt"
cat course_names.txt
