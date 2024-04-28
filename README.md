# Project Mole

## Overview
This Python script, `app.py`, is designed to scan all the files in the repository (excluding directories, 
markdown files, the script itself, and hidden files) and generate a JSON object that includes the path and content of 
each file. This JSON object is useful for creating project documentation or summaries, such as automatically 
generating a README file for the project.

## Features
- Scans all files in the project directory recursively.
- Filters out directories, markdown (.md) files, the script file itself, and hidden files.
- Outputs the paths and contents of the scanned files in a structured JSON format.

## Usage
To use this script, run it with an argument specifying the output file path for the JSON. The command to run the script 
would look like this:

```bash
python app.py <output_file_path>
```

For example, to generate a project context file named project_context.json, you would run:

```bash
python app.py project_context.json
```

This command will create a context.json file that contains the path and content of each file in the project directory, 
structured as a JSON array of objects.

## Contributing
Contributions to enhance the functionality of this script are welcome. Please ensure any pull requests are 
well-documented and include updates to this README if necessary.

## License
This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for more details.
