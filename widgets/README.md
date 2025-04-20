# GUI widgets

This directory contains all the GUI widgets for simplifing control of lab instruments from different suppliers. Every widget can be connected to a single server deploied in `servers`.

All of the widgets can be runned as a simple application to control a single instrument.

For a complex application with GUI which needs multi-instruments, one should implement GUIs for every instrumts as a widget in this folder, and create the application in `app`, by conbining all needed widgets.