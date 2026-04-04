# excel-validator-app

[![Build Windows EXE](https://github.com/pasztork/excel-validator-app/actions/workflows/build-windows-exe.yml/badge.svg)](https://github.com/pasztork/excel-validator-app/actions/workflows/build-windows-exe.yml)

## Project Tasks

- Environment Setup

    - [x] Create a dev container
    - [x] Install dependencies via pip install -r requirements.txt
    - [x] Configure .gitignore

- Core Logic Development

    - [x] Define validation rules
    - [x] Develop an expandable validation pipeline
    - [x] Develop validation reporting logic (Pass/Fail criteria)

- UI Implementation

    - [x] Design main window layout (PyQt6)
    - [x] Build file processing progress bar
    - [x] Create results table with error highlighting

- Testing & Distribution

    - [x] Run unit tests for Excel validation
    - [x] Package application using PyInstaller
    - [x] Conduct end-to-end test with a sample Google Drive folder

## Validation Roadmap

- [x] Verify input format
- [x] Verify file location
- [x] Validate that `Sum(E:G)` for each record matches the total in `Column H`
- [x] Ensure the combined sum of `Columns H + I` matches the constant value assigned to the user's role
- [x] Flag any data records containing data falling on Saturdays or Sundays
- [x] Validate that the total cumulative time does not exceed the maximum threshold defined by the user's role

## Validation Constants

The app enforces role-specific rules to ensure data integrity.
These constants define the "Ground Truth" for each user role and are used to flag discrepancies.

| User Role | Max Daily Hours | Monthly Project Target | Column I Requirement |
| :--- | :---: | :---: | :---: |
| **Consilier scolar** | 4h | 21h | **Must be Empty** |
| **Mentor** | 12h | 21h | **Required** |
| **Profesor limba romana** | 4h | 40h | **Must be Empty** |
| **Asistent grup tinta** | 4h | 21h | **Must be Empty** |
| **Responsabil grup tinta** | 12h | 84h | **Required** |
| **Consilier CEOC** | 4h | 42h | **Must be Empty** |
| **Asistent UCP** | 12h | 84h | **Required** |
