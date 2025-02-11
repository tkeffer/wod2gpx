Convert WOD metadata to GPX format.

For a description of the WOD "CSV" format, see
https://www.ncei.noaa.gov/access/world-ocean-database-select/csv_info.html.
Unfortunately, it cannot be read using Excel. The purpose of this program is to
read the format, then translate it into GPX, which can be readily injested into
any number of plotting programs.

## Usage

```aiignore
usage: wod2gpx [-h] [--comment COMMENT] [--symbol SYMBOL] [infile] [outfile]

Convert WOD metadata to GPX format.

positional arguments:
  infile             File to process. Use '-' for stdin.
  outfile            File to write GPX data to. Use '-' for stdout.

optional arguments:
  -h, --help         show this help message and exit
  --comment COMMENT  Comment to be added to the GPX 'desc' field.
  --symbol SYMBOL    Symbol to use. Default is a small red x.
```

## Example

Here is a typical WOD CSV record. 

```
#--------------------------------------------------------------------------------
CAST                        ,,595182,WOD Unique Cast Number,WOD code,
NODC Cruise ID              ,,US-1908        ,,,
Originators Station ID      ,,PL 90             ,,,alpha
Originators Cruise ID       ,,31701908,,,
Latitude                    ,,24.893,decimal degrees,,
Longitude                   ,,-108.925,decimal degrees,,
Year                        ,,1970,,,
Month                       ,,3,,,
Day                         ,,19,,,
Time                        ,,17.3,decimal hours (UT),,
#--------------------------------------------------------------------------------
```

Assuming it is in a file `input_file.csv`, to convert it to GPX:
```aiignore
wod2gpx.py input_file.csv output_file.gpx --comment="Example"
```

This would result in the file `output_file.gpx` with a single `<wpt>` record:

```aiignore
<?xml version="1.0" encoding="utf-8"?>
<gpx version="1.1" creator="Python GPX Generator" xmlns="http://www.topografix.com/GPX/1/1">
  <wpt lat="24.893" lon="-108.925">
    <name>PL 90</name>
    <desc>Example
CAST: 595182
NODC Cruise ID: US-1908
Originators Cruise ID: 31701908</desc>
    <time>1970-03-19T17:18:00+00:00</time>
    <sym>Symbol-X-Small-Red</sym>
  </wpt>
</gpx>
```