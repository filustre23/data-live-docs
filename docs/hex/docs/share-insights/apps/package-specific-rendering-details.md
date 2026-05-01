On this page

# Package-specific rendering details

Hex is able to handle elements rendered by specific packages in flexible ways.

## Matplotlib, Seaborn, and other image-based renderers[​](#matplotlib-seaborn-and-other-image-based-renderers "Direct link to Matplotlib, Seaborn, and other image-based renderers")

Elements from packages which generate static images (e.g., matplotlib and related libraries) will be scaled linearly in the App builder. This can cause blurriness at larger sizes, so it's recommended to adjust the size directly using the [figure parameter](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure).

You can read more about matplotlib and its usage [here](https://jakevdp.github.io/PythonDataScienceHandbook/04.00-introduction-to-matplotlib.html).

## Plotly[​](#plotly "Direct link to Plotly")

Plotly outputs rescale dynamically in the App builder.

## Styled Dataframes[​](#styled-dataframes "Direct link to Styled Dataframes")

DataFrames generated using [the Pandas style API](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html) are rendered with default styles, as opposed to un-styled DataFrames which have some Hex-specific styling applied.

#### On this page

* [Matplotlib, Seaborn, and other image-based renderers](#matplotlib-seaborn-and-other-image-based-renderers)
* [Plotly](#plotly)
* [Styled Dataframes](#styled-dataframes)