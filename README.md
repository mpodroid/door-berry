DOOR-BERRY
==========

This project is about implementing an IP Video Door Bell and Intercom System based on Raspberry PI.

Main components are:
* Raspberry PI with Raspbian OS
* PjSIP client on Raspberry
* Smartphones/tablet  as internal station: VoIP client yet to be choosen
* Asterisk PBX: not strictly required but necessary to be able to scale system easily to multiple external and internal stations

BUILDING
========

There 3 scripts to guide you and automate the preparation and build process:
* doorberry.prepare: run it to update default image OS and firmware
* doorberry.install-dep: run it to download and build dependencies required
* doorberry.install: run it to actually install doorberry

