# excel-validator-app

## Project Tasks

- Environment Setup

    - [x] Create a dev container
    - [x] Install dependencies via pip install -r requirements.txt
    - [x] Configure .gitignore

- Core Logic Development

    - [ ] Define validation rules
    - [x] Develop an expandable validation pipeline
    - [ ] Develop validation reporting logic (Pass/Fail criteria)

- UI Implementation

    - [x] Design main window layout (PyQt6)
    - [x] Build file processing progress bar
    - [ ] Create results table with error highlighting

- Testing & Distribution

    - [ ] Run unit tests for Excel validation
    - [ ] Package application using PyInstaller
    - [ ] Conduct end-to-end test with a sample Google Drive folder

## Validation Roadmap

- [x] Verify input format
- [ ] Verify file location
- [ ] Validate that `Sum(E:G)` for each record matches the total in `Column H`
- [ ] Ensure the combined sum of `Columns H + I` matches the constant value assigned to the user's role
- [ ] Flag any data records containing timestamps or dates falling on Saturdays or Sundays
- [ ] Validate that the total cumulative time does not exceed the maximum threshold defined by the user's role

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
