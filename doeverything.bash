#!/bin/bash

git pull

python get_external.py

git add systems_*/*
git commit -a -m "Automatic update"
git push
