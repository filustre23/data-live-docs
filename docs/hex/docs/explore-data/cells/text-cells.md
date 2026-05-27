On this page

# Text and Markdown cells

Add narrative to your Hex project with Text or Markdown cells.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

Text and Markdown cells let you add narrative, explanations, and context to your data project.

Text cells provide a WYSIWIG (what you see is what you get) editor that accepts both markdown shortcuts for text formatting as well as UI-driven formatting. Markdown cells provide a familiar UI for Markdown writers, which render as cell output.

* Markdown cell
* Text cell

tip

Both Markdown and Text cells allow you to mix variables with your text through use of the Jinja templating language, like so: `Today we sold {{ n_widgets }} widgets`

Check out the section on [dynamic text](#dynamic-text) for more tips.

## Markdown and Text cell features[​](#markdown-and-text-cell-features "Direct link to Markdown and Text cell features")

tip

We plan to combine these cells into two modes of the same cell. For now, there are slight differences in the functionality of each cell type.

| Feature | Markdown cell | Text cell |
| --- | --- | --- |
| [Formatting](#formatting) | ✅ | ✅¹ |
| [Dynamic text](#dynamic-text) | ✅ | 🟡² |
| [User mentions](#user-mentions) | ❌ | ✅ |
| [Image support](#image-support) | ✅ | ✅ |
| [Emoji picker](#emoji-picker) | ✅ | ❌ |
| [LaTeX formulas](#latex-formulas) | ✅ | ❌ |

¹Currently, code blocks are not supported in Text cells (i.e. code blocks with three backticks). Code snippets (single backticks) are supported. All other formatting options (headings, bold, italics, hyperlinks, lists, and quotes) are supported in Text cells.

²Jinja support in Text Cells is only for Jinja variables (i.e. code within `{{ }}`). At present, code blocks (within `{% %}`), like `if` statements and `for` loops are not supported).

## Formatting[​](#formatting "Direct link to Formatting")

### Headings[​](#headings "Direct link to Headings")

* Markdown cell
* Text cell

To add a heading, use the `#` symbol followed by the heading text. You can add up to 6 `#` and the size of the heading will decrease with each one added.

[](/assets/medias/Markdown-Headings-0b8aceaf592841eb48d9b0f721347a8f.mp4)

To add a heading, select the text that you want to format and right click. The options menu will appear over the selected text from which you can choose your heading size. You can also use the `#` symbol in the same way you would with a markdown heading.

[](/assets/medias/Text-cell-heading-1c58e32133d9b0ae4837504e658cd45d.mp4)

### Lists[​](#lists "Direct link to Lists")

* Markdown cell
* Text cell

To create unordered lists in markdown, use either the `*` or `-` symbols. To create an ordered list, use the `)` or `.` symbols preceded by a number.

[](/assets/medias/Markdown-lists-f08e3bf232be044a5dadd12c1b975ea2.mp4)

To create an ordered or unordered list, select the list formatting option on the far right of the menu.

[](/assets/medias/Text-cell-list-b62e442573fd4c2aa8aed8b9ac47d1bc.mp4)

### Links[​](#links "Direct link to Links")

* Markdown cell
* Text cell

To add a link to a markdown cell, you can wrap your text in square brackets `[]` followed by the URL wrapped in parenthesis `()`.

[](/assets/medias/MD-links-d781fedc358959a0e8d062c5f8833367.mp4)

To add links to a Text cell, select the part of your text where the link will go and select the link formatting option. Press enter once the link has been pasted to commit your changes. You can also add links by pasting the link over the text you wish to format

[](/assets/medias/Text-cell-link-menu-c8f0d7fa703e1cd448aac7038fa239cc.mp4)

### Code formatting[​](#code-formatting "Direct link to Code formatting")

* Markdown cell
* Text cell

You can highlight variables in your text by wrapping your text in backticks (``), or you can use 3 backticks before and after your text to create a code block.

You can highlight variables within a Text cell using the code formatting option.

[](/assets/medias/Text-cell-code-formatting-fdac7226f1d544870cbe49231c395a06.mp4)

tip

Code blocks are not yet supported in Text cells.

### Quotes[​](#quotes "Direct link to Quotes")

* Markdown cell
* Text cell

To create a blockquote, start a line with a `>` followed by the quote.

You can add a quote to a Text cell by selecting the blockquote option in the formatting menu.

[](/assets/medias/text-cell-blockquotes-43510df2f00dc0a678334c6236c2f14f.mp4)

## Dynamic text[​](#dynamic-text "Direct link to Dynamic text")

* Markdown cell
* Text cell

You can also insert Python variables directly into Markdown cells. Type your text as usual but in place of hard-coding the value you want, wrap the variable name in `{{ }}` braces to dynamically update your Markdown text. See the screenshot below for an example.

Text cells support variable substitution using the usual double curly braces, `{{}}`, of [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) syntax. In order to render values, you'll need to run the cell.

[](/assets/medias/Text-cell-jinja-syntax-e71b066f45aab28ee266e244e21e596c.mp4)

info

Complex logic such as if statements and for loops are not yet supported.

## User mentions[​](#user-mentions "Direct link to User mentions")

* Markdown cell
* Text cell

info

Markdown cells do not currently support user mentions

You can ping other members of your workspace by mentioning them in a Text cell. When mentioning a user, they will receive a notification by email or slack.

[](/assets/medias/Text-cell-mentions-2-87c917471f95a595adb01cb685071562.mp4)

## Image support[​](#image-support "Direct link to Image support")

You can render images in Markdown and Text cells by dragging a file from your computer and dropping it in the cell. The image is uploaded as a file and can be referenced again in any other cell.

* Markdown cell
* Text cell

[](/assets/medias/markdown-text-image-1bcd6eda576dba739fba4bb656958bc3.mp4)

[](/assets/medias/Tex-cell-image-b1a7199cd1958b8e62ad69b30b64044f.mp4)

## Emoji picker[​](#emoji-picker "Direct link to Emoji picker")

* Markdown cell
* Text cell

To add an emoji to your markdown, start by adding a colon (`:`) which will prompt you to select an emoji from the list of available emojis.

[](/assets/medias/emojis-8dd0e031a1571b43de47af89d669f8f7.mp4)

info

The emoji picker has not yet been implemented for text cells

## LaTeX formulas[​](#latex-formulas "Direct link to LaTeX formulas")

* Markdown cell
* Text cell

You can use the `$$` delimiters in Markdown to insert math expressions in LaTeX style syntax.

info

LaTeX formulas are not yet supported in Text cells.

#### On this page

* [Markdown and Text cell features](#markdown-and-text-cell-features)
* [Formatting](#formatting)
  + [Headings](#headings)
  + [Lists](#lists)
  + [Links](#links)
  + [Code formatting](#code-formatting)
  + [Quotes](#quotes)
* [Dynamic text](#dynamic-text)
* [User mentions](#user-mentions)
* [Image support](#image-support)
* [Emoji picker](#emoji-picker)
* [LaTeX formulas](#latex-formulas)