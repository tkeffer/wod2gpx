Convert WOD metadata to GPX format.

## Example

A typical WOD metadata record looks like:

```
#--------------------------------------------------------------------------------,,,,,
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
#--------------------------------------------------------------------------------,,,,,
```

This would get converted to a GPX record that looks like:

```aiignore
  <wpt lat="24.893" lon="-108.925">
    <name>PL 90</name>
    <time>1970-03-19T17:18:00+00:00</time>
    <desc>CAST: 595182
NODC Cruise ID: US-1908
Originators Cruise ID: 31701908
</desc>
  </wpt>
```