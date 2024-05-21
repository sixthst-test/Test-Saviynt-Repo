#!/usr/bin/env bash

set -e
BUILD_NUMBER=$1
ATTEMPT_NUMBER=$2

if [[ -z $BUILD_NUMBER ]]; then
    echo Build number is blank but is required. Please provide BUILD_NUMBER as first argument.
    exit 1
fi


major_minor=$(poetry version --short | cut -d. -f1-2)

new_version="${major_minor}.${BUILD_NUMBER}"
if [[ ! -z $ATTEMPT_NUMBER ]]; then
    echo "Manual run detected. Adding dev${ATTEMPT_NUMBER} to version."
    new_version="${new_version}.dev${ATTEMPT_NUMBER}"
fi

poetry version $new_version
