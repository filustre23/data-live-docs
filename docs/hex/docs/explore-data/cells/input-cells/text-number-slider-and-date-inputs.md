On this page

# Text, Number, Slider, Date, & Checkbox inputs

Add inputs for text strings, numbers, dates or date ranges, and boolean checkboxes or toggles.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

## Text[​](#text "Direct link to Text")

Simple text input that returns a string.

## Number[​](#number "Direct link to Number")

Similar to text, but returns a numeric. Users can set an increment size, which dictates how much the value changes when the up and down arrows are used.
Optionally add numeric formatting with the **Format** dropdown (choose between Number, Percentage, or Currency) and the **Thousands** toggle (which adds thousands separators). The applied formatting will not affect the returned variable; the resulting python variable will remain an unformatted number variable.

## Slider[​](#slider "Direct link to Slider")

Numeric input with configurable minimum, maximum, and step size.

## Date / Time[​](#date--time "Direct link to Date / Time")

A calendar-based date picker that allows selection of dates and, optionally, times.

For the ability to use non-fixed dates, toggle on **Show relative dates**.
Use the relative dates tab to select fixed time intervals relative to the current date.

[](/assets/medias/relative-date-input-8f76a289afc346e40b7f7577cb3bc395.mp4)

Inputs are stored as `datetime.datetime` objects and can be accessed as they would be normally ([see Python documentation here](https://docs.python.org/3/library/datetime.html)).

## Checkbox[​](#checkbox "Direct link to Checkbox")

Boolean input (True/False). Optionally, can be configured as a toggle.

#### On this page

* [Text](#text)
* [Number](#number)
* [Slider](#slider)
* [Date / Time](#date--time)
* [Checkbox](#checkbox)