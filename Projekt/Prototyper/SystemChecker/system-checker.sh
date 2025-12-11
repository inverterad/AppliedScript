#!/bin/bash

# Intro

actual_version=$( cat /etc/os-release | grep "VERSION" | sed "s/[0-9]//g")

echo $actual_version