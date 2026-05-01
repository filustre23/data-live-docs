On this page

# Keyboard shortcuts

tip

Cmd/ctrl below indicates command on Mac and control on Windows and Linux. These instructions are for English/QWERTY keyboards.

Hex supports a number of keyboard shortcuts, most modeled after the standard Jupyter set, which make a distinction whether you are selected into a cell or not.

For a full list of supported keyboard shortcuts see the table [here](/docs/explore-data/notebook-view/keyboard-shortcuts#keyboard-shortcuts-list).

## Edit mode[​](#edit-mode "Direct link to Edit mode")

While in edit mode, you can type in a cell as with a normal text or code editor.

Press `cmd` + `enter/return` to run an individual cell

Press `option` + `enter/return` to run a cell and add a new cell after

Press `shift` + `enter/return` to run a cell and scroll to the next, or add a new cell if there isn't one immediately following

Press `escape` to enter Command mode. Users with [Vim key bindings](/docs/administration/user-settings) enabled will need to use `shift + esc`.

Press `ctrl` + `space` after a `.` to list the attributes for Python classes and objects

Press `shift` + `tab` to trigger in-line documentation for Python functions

[](/assets/medias/edit-mode-7ceafe88235e5fa5cd704548e8b04b44.mp4)

## Command mode[​](#command-mode "Direct link to Command mode")

You can enter command mode by pressing `escape`. Command mode allows you to edit a notebook without typing into individual cells.

Press `j` or `k` to navigate down or up

Press `a` to add a cell above

Press `b` to add a cell below

Press `dd` (`d` twice) to delete a cell

Press `enter/return` to select into a cell (enter Edit mode)

[](/assets/medias/command-mode-948dd68b2c86d7189f79149e5f6c8ee0.mp4)

### Select multiple cells[​](#select-multiple-cells "Direct link to Select multiple cells")

To select multiple cells, first hit `esc` to enter Command mode, and then `shift + up/down arrow` or `shift + j/k` to select additional cells. After selecting a block of cells, you can move them up/down (with the usual `j/k` or `cmd/ctrl up/down arrow`) as well as copy/cut/paste (`cmd/ctrl + c/x/v`).

## Command palette[​](#command-palette "Direct link to Command palette")

You can access the command palette by hitting `cmd+p`. From there, you can filter the available actions by typing in the search bar and press `enter`, or use the corresponding keyboard shortcut, to execute.

[](/assets/medias/command-palette-e86ca89d05380665c7000552a4cbe92a.mp4)

## Keyboard shortcuts list[​](#keyboard-shortcuts-list "Direct link to Keyboard shortcuts list")

Below are some actions we currently support with keyboard shortcuts. More complex actions (e.g. creating Input parameters, getting share links) are available via our [Command palette](/docs/explore-data/notebook-view/keyboard-shortcuts#command-palette).

| Action | Keyboard Command | Mode |
| --- | --- | --- |
| Move cell down | Cmd + J, Cmd + Down | Command |
| Move cell up | Cmd + K, Cmd + Up | Command |
| Navigate to App builder | Alt + 4 | Command, Edit |
| Navigate to Notebook view | Alt + 3 | Command, Edit |
| Restart and run all | Alt + R | Command, Edit |
| Move cursor up | Up | Edit |
| Move cursor down | Down | Edit |
| Undo | Cmd + Z | Edit |
| Redo | Ctrl + Shift + Z | Edit |
| Select All | Cmd + A | Edit |
| Dedent | Cmd + [ | Edit |
| Indent | Cmd + ] | Edit |
| Code completion or indent | Tab | Edit |
| Change the cell type to Markdown | M | Command |
| Change the cell type to Code | Y | Command |
| Open the command palette | Cmd + P | Command, Edit |
| Undo cell deletion | Z | Command |
| Delete selected cells | D + D | Command |
| Insert cell below | B | Command |
| Insert cell above | A | Command |
| Select cell below | Down, J | Command |
| Select cell above | Up, K | Command |
| Select multiple cells | Shift + Up/Down, Shift + J/K | Command |
| Copy/Cut/Paste cell | Cmd + C/X/V | Command |
| Exit Command (enter Edit ) | Enter (cell needs focus) | Command |
| Enter Command (from Edit ) | Esc (cell needs focus), Shift + Esc for Vim users | Command, Edit |
| Save checkpoint | Cmd + S | Command, Edit |
| Run selected cells | Cmd + Enter | Command, Edit |
| Run the current cell, select below | ⇧ + Enter | Command, Edit |
| Run the current cell, insert below | Option + Enter | Command, Edit |
| Open the Add Cell menu | Option + A (note: the add cell menu will display additional shortcuts to create specific cell types) | Command, Edit |

#### On this page

* [Edit mode](#edit-mode)
* [Command mode](#command-mode)
  + [Select multiple cells](#select-multiple-cells)
* [Command palette](#command-palette)
* [Keyboard shortcuts list](#keyboard-shortcuts-list)