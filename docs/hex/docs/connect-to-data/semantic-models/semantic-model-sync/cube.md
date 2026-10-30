On this page

# Syncing from Cube

Cube is an open-source semantic model that can be used to centralize business logic across your data stack and accelerate query performance. For more information, see [the documentation](https://cube.dev/docs/product/introduction).

## Concepts[​](#concepts "Direct link to Concepts")

To effectively leverage your Cube models within Hex, check how key concepts translate between the two platforms.

| Cube | Hex |
| --- | --- |
| data model | semantic project |
| cube | model |
| dimension | dimension |
| measure | measure |
| join | join |
| view | view |
| segment | n/a |

## Supported Features[​](#supported-features "Direct link to Supported Features")

Not all Cube features translate directly in Hex; check the following table to see what is supported.

| Feature | Supported |
| --- | --- |
| **Dimension features** |  |
| Time, String, Number, Boolean | ✅ |
| Dimensions with case, sub\_query | ❌ |
| **Measure features** |  |
| Count, Count distinct, Sum, Average, Min, Max, String, Time, Boolean | ✅ |
| Approximate count distinct, | ❌ |
| Granularities | ❌ |
| propagate\_filters\_to\_sub\_query | ❌ |
| Measure filters | ✅ |
| drill\_members | ❌ |
| Rolling window | ❌ |
| **Join features** |  |
| many\_to\_one, one\_to\_many, one\_to\_one | ✅ |
| **View features** |  |
| Explicit join\_paths with included/excluded items | ✅ |
| Folders | ❌ |
| **Other features** |  |
| Pre-aggregations | ❌ |
| Hierarchies | ❌ |
| Calculated measures that reference measures across models | ❌ |

#### On this page

* [Concepts](#concepts)
* [Supported Features](#supported-features)