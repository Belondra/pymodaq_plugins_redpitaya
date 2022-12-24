pymodaq_plugins_RedPitaya
##########################################

.. the following must be adapted to your developped package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_thorlabs.svg
   :target: https://pypi.org/project/pymodaq_plugins_thorlabs/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_thorlabs/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_thorlabs
   :alt: Publication Status


The purpose of this PyMoDaq plugin is to interface between the voltage sensor on the test bench, and the user, via a display of the results and some adjustment commands. A part of the program will use the SCPI language to communicate with the CAN (redpitaya), we will find the definition of these SCPI functions in the Hardware part.

Authors
=======

* First Author  (matthieu.belondrade@free.fr , antoine.dulong1@gmail.com)
* Other author (sebastien.weber@cemes.fr)

.. if needed use this field

    Contributors
    ============

    * First Contributor : Bélondrade Matthieu, Dulong Antoine
    * Other Contributors : Weber Sébastien

Instruments
===========

Below is the list of instruments included in this plugin


Viewer1D
++++++++

* **Y**: Signal aquisition from a tension sensor (1D detector)
* **X**: Number of points of measure



Infos
=====

To use this module you first need to install PyMoDaQ.

This plugin as been created with the objective of being implemented in a plug and play spectrometer using a Raspberry Pi computer and a RedPitaya CAN.

