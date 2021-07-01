## About

This package is designed to perform spectral deconvolution on waveforms obtained from UV-Vis spectrometry. It was designed for identification of different hemoglobin species in complex mixtures, but may be used on any absorbance-based data.


## Usage

Users can access the script through the command line (using *deconv_multi.py*) or the GUI (*main_gui.py*). In either case, the following parameters should be specified:
- **Data file**: A file path, or list of file paths (directory if using GUI), in which the experimental waveforms are located.
- **Reference file**: A file path to a sheet of waveforms to be used as pure reference spectra for deconvolution. Defaults to *refspec.dat*.
- **Ignored species**: Waveforms from the reference that should not be used in curve fitting.
- **nm_min** and **nm_max**: Minimum and maximum wavelengths to consider for the curve fitting. Both experimental and reference spectra must have values continuously in this region.
- **Kinetic** *vs* **Replicate**: If more than one column of data is present, specify whether it should be treated as kinetic data collected over time, or replicates of the same sample (where the spectra will be averaged).
- **Normalize**: Adjusts the input waves such that the lowest value becomes 0. Potentially helpful for solutions with known baseline offset from light scattering, use with caution otherwise.
- **File note** (optional): A short string that will be appended to the file name and included in the text report. Useful for reporting concentration, operator ID, additional sample information, etc.
- **Verbose Output**: If enabled, will print frequent status updates to your Python console.
- **Graph, Report,** and **Spectra**: Boolean values that determine whether .png, .txt, and .xlsx files (respectively) are produced.

### File input format
The file input methods of Alchromy are being expanded, but are currently limited to a narrow specification. Reference files should contain multiple columns beginning with wavelength. Subsequent columns should be named for the species they contain. Experimental data files should have a list of wavelengths as the first column. Each subsequent column will be treated as either replicates of the same sample, or different time points (see *kinetic vs replicate*). Files may be in tab delimited format with the extension *.dat, .txt* or *.csv* or a single Excel sheet in a *.xls* or *.xlsx* file.

### Output
At this time, Alchromy produces three types of output files:
- A text file (.txt) reporting operating parameters, fit values, and composition percentages.
- An image file (.png) graphing the experimental and fit waves.
- A spreadsheet (.xslx) of the entire fit wave used in the graph.

