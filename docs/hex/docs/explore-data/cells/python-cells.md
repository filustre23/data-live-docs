On this page

# Python cells

Hex’s first-class Python support unlocks a world of opportunity for data exploration.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

## Developing logic in Python cells[​](#developing-logic-in-python-cells "Direct link to Developing logic in Python cells")

Users can write, edit, and execute any valid Python in a Python cell. For inspiration, check out our [Use case library](https://hex.tech/use-cases/) to browse example Hex projects.

### Adding and editing a cell[​](#adding-and-editing-a-cell "Direct link to Adding and editing a cell")

Click the **Add cell** button and select **Python** to add a new Python cell to your project. Write your Python script in the cell and click the **Run** button to execute it.

Users can edit and execute any valid Python in a Python cell.

### Importing packages[​](#importing-packages "Direct link to Importing packages")

Hex projects come pre-installed with a number of Python packages, which you can view in the **Environment** tab of the left sidebar. Use an `import` statement to load the package into your project.

If the package you need is not already installed, add a new Python cell and use a `!uv pip install` command. Import the package as you normally would to use it in your project.

Hex frequently updates the pre-installed packages and versions. If your team requires specific package versions, [importing from GitHub](/docs/explore-data/projects/environment-configuration/using-packages#github-packages) or using [Custom images](/docs/administration/workspace_settings/custom-images) may be appropriate.

### Outputs[​](#outputs "Direct link to Outputs")

Python cells can optionally have outputs, which are visualizations of elements from the code.

If any line of a Python cell explicitly prints a value (e.g: `print("hello!")` ), that value will be included in the Output along with any other values explicitly printed by other lines.

Lines that implicitly print a value (e.g: `2+2`) are only included in output if they occur on the last line of a Python cell.

If a cell has no explicit print statements and the last line does not print a value explicitly or implicitly (e.g: `x = 5`), nothing is displayed as output. This is perfectly fine, and is often done to keep things readable while setting the stage for another cell that will display something.

## Converting cells[​](#converting-cells "Direct link to Converting cells")

You can convert a cell from a Python to a Markdown cell and vice-versa using the dropdown in the upper right.

Or use keyboard shortcuts to convert between cell types:

* Go from Python to Markdown cells with `esc + m`
* Go from Markdown to Python cells with `esc + y`

#### On this page

* [Developing logic in Python cells](#developing-logic-in-python-cells)
  + [Adding and editing a cell](#adding-and-editing-a-cell)
  + [Importing packages](#importing-packages)
  + [Outputs](#outputs)
* [Converting cells](#converting-cells)