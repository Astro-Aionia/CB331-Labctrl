# Web API Servers

This directory contains all the web api servers for simplifing
control of lab instruments from different suppliers.

All of the servers are self-contained and can be used independently.

Some instruments like Topas and Zurich Instrument UHF already provides
good web APIs, however they are quite complicated for simple tasks and
may require additional authentication. For my convenience some proxy
code is written for the most used APIs so that it is tailored for our
needs.

## Port Assignments

To avoid conflict with existing APIs in our lab, different ports are assigned
to different server or proxies. If desired, the port can be changed in the
corresponding .bat files.

The "port" section in configs also needs to be changed if the server port has been altered.

By default, assigned ports start from `50001`.

### Defaults

* Linear Stages:

        CDHD2       50001

        
* TOPAS:

        Demo        50002
        T23231P     50003
        T23232P     50004
        T23233P     50005


* Detectors:

        ToupCam     50006
        PI EMCCD    50007