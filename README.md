# song-recognizer
A small program that uses OpenAI's speech-to-text tool and Librosa's CENS chroma fingerprinting to categorize songs given recordings of various performances, such as studio version, acoustic version, rehearsal recordings etc. Created on FER as Bachelor's Thesis for Computing Bachelor programme under the tutorship of prof. dr. sc. Antonio Petošić.

This program allows users to interact via the command line to either:

- **Store** a new known recording.
- **Classify** an unknown recording by comparing it to a database.

## Usage

The current version communicates through standard input (command line). The two available operations are:

1. **`store`** – Save a known recording.
2. **`classify`** – Identify an unknown recording.

### Command-Line Arguments

| Argument             | Description                                                            |
|----------------------|------------------------------------------------------------------------|
| `-l`, `--language`    | Language of the song lyrics (ISO-639-1 format)                         |
| `-b`, `--begin-vocals`| Timestamp (in milliseconds) when vocals begin in the song             |
| `-a`, `--artist`      | Artist name                                                            |
| `-s`, `--song`        | Song name                                                              |
| `-v`, `--version`     | Version name (recording name)                                          |

---

## Examples

### Identify an unknown recording:

```bash
py main.py classify -l [language] -b [milliseconds]
```

### Store a known recording:

```bash
py main.py store -l [language] -b [milliseconds] -a [artist] -s [song] -v [version]
```

## Details

### store Operation

This operation saves a new recording into the songVersions database. Two scenarios may require user interaction:

If the song does not already exist in the database.

If the song exists, but the specified version already exists as well.

After the checks and necessary user confirmations, the metadata is stored in the songVersions table, and a copy of the recording is saved to the corresponding subdirectory under pjesme/, using a properly formatted filename.

### classify Operation

This operation extracts parameters from the given unknown recording and compares it with existing entries in the database. It returns the top 3 matching results.

The user can then select whether any of the suggested results are satisfactory. After selecting a match, the user must provide a version name under which the new recording will be saved. If the version does not already exist, the recording is saved in the same manner as in the store operation.
