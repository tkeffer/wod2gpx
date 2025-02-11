import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def parse_file(infile):
    """
    Parse a WOD metadata file.

    Args:
        infile(file): An open file-like object.

    Returns:
        list of dict: A list of dictionaries. Each dictionary represents a record.
    """
    # Initialize variables
    data = []
    record = {}

    # Read file line by line
    for line in infile:
        # Skip the section separator
        if line.startswith("#--------------------------------------------------------------------------------"):
            if record:  # Save the current record if it's not empty
                data.append(record)
                record = {}  # Reset for the next record
            continue

        # Use regex to match data lines (e.g., Latitude,,value,,units,,)
        match = re.match(r"(.*?),(.*?),(.*?),(.*)", line.strip())
        if match:
            key = match.group(1).strip()
            value = match.group(3).strip()
            if key and value:  # Avoid storing empty keys or values
                record[key] = value

    # Add the last record if it exists
    if record:
        data.append(record)

    return data


def create_gpx(records, output_file, symbol="Symbol-X-Small-Red"):
    """
    Create a GPX file from a list of parsed records.

    Args:
    records (list of dict): List of records with 'Latitude', 'Longitude', 'Time', etc.
    output_file (file): An open file-like object to write the GPX data to.
    symbol (str): The symbol to use for the mark. Default is a small red x.
    """
    root = ET.Element("gpx", version="1.1", creator="Python GPX Generator", xmlns="http://www.topografix.com/GPX/1/1")

    for record in records:
        # Ensure required fields exist
        latitude = record.get("Latitude")
        longitude = record.get("Longitude")
        if latitude and longitude:
            # Create a waypoint element
            wpt = ET.SubElement(root, "wpt", lat=latitude, lon=longitude)

            # Use the original station ID as the name
            name = record.get("Originators Station ID", "N/A")
            ET.SubElement(wpt, "name").text = name

            # Set the 'desc' field as a string with other metadata
            cast = record.get("CAST", "N/A")
            nodc_cruise_id = record.get("NODC Cruise ID", "N/A")
            originators_cruise_id = record.get("Originators Cruise ID", "N/A")
            ET.SubElement(wpt, "desc").text = (f"CAST: {cast}\n"
                                               f"NODC Cruise ID: {nodc_cruise_id}\n"
                                               f"Originators Cruise ID: {originators_cruise_id}")

            year = record.get("Year")
            month = record.get("Month")
            day = record.get("Day")
            time = record.get("Time", 0.0)
            if year and month and day:
                ET.SubElement(wpt, "time").text = convert_to_iso(year, month, day, time)

            ET.SubElement(wpt, "sym").text = symbol

    tree = ET.ElementTree(root)

    # Pretty indent the results:
    ET.indent(tree, space="  ", level=0)

    # Use tostring to obtain the XML as a string
    xml_data = ET.tostring(root, encoding="unicode", method="xml")

    # Include the XML declaration manually
    output_file.write('<?xml version="1.0" encoding="utf-8"?>\n')

    # Write the XML string
    output_file.write(xml_data)


def convert_to_iso(year, month, day, decimal_time):
    """
    Convert year, month, day, and decimal-time-of-day to ISO 8601 datetime format.

    Args:
    year (str or int): Year (e.g., "1970").
    month (str or int): Month (e.g., "3").
    day (str or int): Day (e.g., "19").
    decimal_time (str or float): Time in decimal hours (e.g., "17.3").

    Returns:
    str: ISO 8601 datetime string (e.g., "1970-03-19T17:18:00+00:00").
    """
    # Convert to integers
    year = int(year)
    month = int(month)
    day = int(day)
    decimal_time = float(decimal_time)

    # Extract hours and minutes from decimal time
    hours = int(decimal_time)
    minutes = int((decimal_time - hours) * 60)
    seconds = int((((decimal_time - hours) * 60) - minutes) * 60)

    # Create a datetime object
    iso_datetime = datetime(year, month, day, hours, minutes, seconds, tzinfo=timezone.utc)

    # Return in ISO 8601 format
    return iso_datetime.isoformat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='wod2gpx',
        description='Convert WOD metadata to GPX format.')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="File to process. Use '-' for stdin.")
    parser.add_argument('outfile', nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="File to write GPX data to. Use '-' for stdout.")
    parser.add_argument('--symbol',
                        default="Symbol-X-Small-Red",
                        help="Symbol to use. Default is a small red x.")
    args = parser.parse_args()

    # Parse input data
    parsed_records = parse_file(args.infile)

    # Create GPX file
    create_gpx(parsed_records, args.outfile, symbol=args.symbol)
