# Alchromy
## Introduction
Welcome to Alchromy! This package is designed to perform spectral deconvolution on waveforms obtained from UV-Vis spectrometry. It was designed for identification of different hemoglobin species in complex mixtures. It is currently in a closed beta testing phase, so expect many changes going forward.

## Dependencies
Alchromy requires Python 3 and the following packages:
 * tkinter
 * pandas
 * glob
 * io
 * scipy
 * numpy
 * matplpotlib

## Usage
Users can access the script through the command line (using *deconv.py*) or the GUI (*main_gui.py*). In either case, the following parameters should be specified:
* **Data file**: A file path, or list of file paths (directory if using GUI), in which the experimental waveforms are located.
* **Reference file**: A file path to a sheet of waveforms to be used as pure reference spectra for deconvolution. Defaults to *refspec.dat*.
* **Ignored species**: Waveforms from the reference that should not be used in curve fitting.
* **nm_min** and **nm_max**: Minimum and maximum wavelengths to consider for the curve fitting. Both experimental and reference spectra must have values continuously in this region.

## Output
At this time, Alchromy produces three types of output files:
* A text file (.txt) reporting operating parameters, fit values, and composition percentages.
* An image file (.png) graphing the experimental and fit waves.
* A spreadsheet (.xslx) of the entire fit wave used in the graph.

## To-do list
There are many changes in the works! Below is a list of features already in development.
* Better error handling.
* Improved status reporting in GUI .
* Input of multiple waves from a single file (xslx or csv format).
* Batched deconvolution from GUI, with updating progress bar.
* Input and recording of operator ID.
* More informative output file names.
