#!/bin/bash

gifsicle --batch --colors 255 --unoptimize -O1 $1
gifsicle --batch --resize _x240 $1
