On this page

# Custom styling

Configure workspace-level custom styling options for your Hex apps.

info

* Available on the **Team** and **Enterprise** [plans](https://hex.tech/pricing/).
* Users will need the **Admin** role to configure workspace-level custom styling.

## Custom logo[​](#custom-logo "Direct link to Custom logo")

Upload your custom logo to display on all published Hex apps, in place of the standard Hex logo. Other parts of Hex, including the home page and the Notebook view of a project, will continue to use the Hex logo.

Note that when you add a custom logo, published Hex apps will still display "Powered by Hex" in the footer. Fully white-labeled branding for embedding is available as part of our [embedded analytics](/docs/share-insights/embedding/signed-embedding) add-on product.

### Add your logo[​](#add-your-logo "Direct link to Add your logo")

Head to **Settings**, then **Styling**. Under the **Custom logo** subheading, you can drag-and-drop a png or upload a file from your device.

Currently, Hex supports only one version of your logo. Be sure to preview how it looks with both the light and dark themes. You can also optionally use your logo as the favicon for published apps.

## Custom chart color palettes[​](#custom-chart-color-palettes "Direct link to Custom chart color palettes")

Standardize data visualizations colors in your workspace with custom color palettes. Head to **Settings**, then **Styling**, and add a custom palette under the **Color palette** subheading.

### Create a color palette[​](#create-a-color-palette "Direct link to Create a color palette")

Admins can create a new color palette from by clicking **+ Custom palette**.

There are a few ways to specify colors for your palette:

* Click on the color swatch to open and select a shade from the color picker.
* Enter colors as hex strings (e.g. `#F5C0C0` or `AD8EB6`)
* Enter colors as [CSS color names](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color), (e.g. `mediumpurple`)
* Paste a list of hex strings or CSS Color names, separated by commas

You can optionally name each color for easier identification. Remove colors from your palette by clicking on the trash icon.

### Set the active workspace color palette[​](#set-the-active-workspace-color-palette "Direct link to Set the active workspace color palette")

To start using your custom color palette in data visualizations throughout your workspace, click the three-dots menu next to the color palette and select **Set active**. The active color palette, will become available in all [Chart cells](/docs/explore-data/cells/visualization-cells/chart-cells).

#### Which charts will be updated when I change the active color palette?[​](#which-charts-will-be-updated-when-i-change-the-active-color-palette "Direct link to Which charts will be updated when I change the active color palette?")

Updating the active color palette will update any existing [Chart cells](/docs/explore-data/cells/visualization-cells/chart-cells). Note that changing the active color palette will **not** impact:

* Chart cells where colors have been manually customized
* Chart cells built with the legacy chart builder (deprecated as of Dec 2022)

#### When will my charts be updated when I set a new active color palette?[​](#when-will-my-charts-be-updated-when-i-set-a-new-active-color-palette "Direct link to When will my charts be updated when I set a new active color palette?")

Saved changes will be reflected in charts the next time the chart cell is run. Any apps with a [cached default state](/docs/administration/workspace_settings/docs/share-insights/apps/app-run-settings#cache-default-state) will need to have their [cache refreshed](/docs/administration/workspace_settings/docs/share-insights/apps/app-run-settings#cache-default-state) for these changes to take effect.

### Use the active workspace color palette in code[​](#use-the-active-workspace-color-palette-in-code "Direct link to Use the active workspace color palette in code")

The `hex_color_palette` [built-in variable](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables) represents the currently active color palette as an array of CSS color names, for example:

```
>>> print(hex_color_palette)  
  
['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B', '#B279A2', '#FF9DA6', '#9D755D', '#BAB0AC']
```

Using this variable can help create consistently themed visualizations when using both the native [Chart cell](/docs/explore-data/cells/visualization-cells/chart-cells) and visualizations created via Python packages. For example, this Plotly chart will use the same color palette as your workspace:

```
import plotly.express as px  
  
df = px.data.gapminder()  
fig = px.line(  
    df,  
    y="lifeExp",  
    x="year",  
    color="continent",  
    line_group="country",  
    line_shape="spline",  
    render_mode="svg",  
    color_discrete_sequence=hex_color_palette,  
)  
  
fig.show()
```

## Custom app themes[​](#custom-app-themes "Direct link to Custom app themes")

info

* **Team** customers are limited to 1 custom app theme.
* **Enterprise** customers can create up to 5 custom app themes.

Custom app themes allow Admins to select a custom font, color palette, background color and accent color that can be applied to published Apps in your workspace.

### Create a custom app theme[​](#create-a-custom-app-theme "Direct link to Create a custom app theme")

Head to **Settings**, then **Styling**, and create your custom app theme by clicking **+ Custom theme** under the **Custom theme** subheading.

#### Specify your custom font[​](#specify-your-custom-font "Direct link to Specify your custom font")

Hex currently supports [Google fonts](https://fonts.google.com/) in custom app themes. Select a preset or existing font from the drop-down menu, or select **+ Add custom font**.

To add a new [Google font](https://fonts.google.com/), first name the font, then paste the Google fonts URL, ensuring the URL starts with `https://fonts.googleapis.com/css2` and contains all desired font weights and variants.

#### Select your color palette[​](#select-your-color-palette "Direct link to Select your color palette")

Select an existing [custom chart color palette](/docs/administration/workspace_settings/workspace-custom-styling#custom-chart-color-palettes) from the drop-down menu to apply to your custom app theme.

#### Specify your custom background and accent colors[​](#specify-your-custom-background-and-accent-colors "Direct link to Specify your custom background and accent colors")

You can specify custom background and accent colors for your custom app theme by either:

* Clicking on the color swatch to open and select a shade from the color picker.
* Entering colors as hex strings (e.g. `#F5C0C0` or `AD8EB6`)
* Entering colors as [CSS color names](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color), (e.g. `mediumpurple`)

The background color will update the app background, including cell backgrounds. The accent color will update elements like tab labels and selection states within the app surface area.

### Apply custom app themes to published apps[​](#apply-custom-app-themes-to-published-apps "Direct link to Apply custom app themes to published apps")

Once you've created a custom app theme, anyone in your workspace can apply it to their projects from the **App settings** in the [app builder](/docs/share-insights/apps/app-builder).

#### On this page

* [Custom logo](#custom-logo)
  + [Add your logo](#add-your-logo)
* [Custom chart color palettes](#custom-chart-color-palettes)
  + [Create a color palette](#create-a-color-palette)
  + [Set the active workspace color palette](#set-the-active-workspace-color-palette)
  + [Use the active workspace color palette in code](#use-the-active-workspace-color-palette-in-code)
* [Custom app themes](#custom-app-themes)
  + [Create a custom app theme](#create-a-custom-app-theme)
  + [Apply custom app themes to published apps](#apply-custom-app-themes-to-published-apps)