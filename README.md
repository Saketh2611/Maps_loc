# Nearest Resident

A command-line tool that looks up nearby residential addresses using Geoapify.
Provide a latitude and longitude, and the tool prints up to four nearby
addresses, ordered from nearest to farthest.

## Requirements

- Python 3.8 or newer
- A Geoapify API key
- Internet access when running a search

## Get a Geoapify API key

Create or sign in to a Geoapify account and obtain an API key from its
dashboard. The tool sends this key to the Geoapify Places API for each search.

## Install

Open PowerShell in this project folder and create a virtual environment:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activating the environment, you can still use its
Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Otherwise, install the CLI into the active environment:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

The editable install adds the `nearest` command and installs the project
dependencies.

## Configure the API key

Choose either option below.

### Option 1: `.env` file

Create a file named `.env` in the project folder and add your key:

```text
GEOAPIFY_API_KEY=your_geoapify_api_key
```

Replace the example value with your actual key. `.env` is ignored by Git and
should not be committed or shared.

### Option 2: PowerShell environment variable

Set the key for the current PowerShell session:

```powershell
$env:GEOAPIFY_API_KEY = "your_geoapify_api_key"
```

## Run a search

Use the command followed by latitude and longitude, in that order:

```powershell
nearest resident run 17.3850 78.4867
```

Coordinates must be decimal degrees. Latitude must be from `-90` to `90`;
longitude must be from `-180` to `180`.

You can also run the script directly from the project folder without using the
installed command:

```powershell
python nearest_loc.py resident run 17.3850 78.4867
```

The tool searches for residential buildings within 2 km of the provided
coordinates and displays up to four addresses, nearest first. The exact results
depend on the address data available from Geoapify for that area. If no
addresses are found, it prints `No nearby residences found.`

## Help

Show available commands:

```powershell
nearest --help
nearest resident run --help
```

## Troubleshooting

- **`GEOAPIFY_API_KEY is not set`**: Set the key in `.env` or in the current
  shell, as described above.
- **Invalid latitude or longitude**: Use numeric decimal-degree values in the
  allowed ranges, with latitude first.
- **Request or network error**: Check your internet connection and Geoapify
  API key, then try again. API and network errors are printed to standard error.
