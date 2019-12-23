#!/bin/bash

yarn install
for file in quagga.js quagga.min.js; do
    cp node_modules/@ericblade/quagga2/dist/$file interface/static/js/
    dos2unix interface/static/js/$file
    git add interface/static/js/$file
done
