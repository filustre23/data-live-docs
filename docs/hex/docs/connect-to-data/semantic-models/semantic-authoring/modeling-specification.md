On this page

# YAML specification

Reference documentation for writing semantic resources in Hex.

info

Authoring semantic models within Hex is in **beta**.  
Minor changes may be made to the following formats during the beta period.

## Resources[​](#resources "Direct link to Resources")

Each YAML document represents a single semantic resource.

* **Models** declare reusable definitions for tables, measures, dimensions, and relationships in a data warehouse.
* **Views** are optionally declared on top of models and provide fit-for-purpose entrypoints for users to conduct self-serve analysis.

## Model specification[​](#model-specification "Direct link to Model specification")

Models declare a reusable definition for a data table alongside its measures, dimensions, and relationships. Models act as the core building blocks for all analytical logic within the semantic project. Data models typically correspond closely to tables in your database.

```
id: users  
type: model  
base_sql_table: public.users  
dimensions:  
  - id: email  
    type: string  
    unique: true  
measures:  
  - id: total_users  
    func: count  
relations:  
  - id: organizations  
    type: many_to_one  
    join_sql: org_id = ${organizations}.id
```

\*id:[ID](#id)

The unique identifier for this model.

This identifier is used as its reference across all models and must be unique across the semantic project. Changing this identifier may invalidate existing references.

type:"model"

The string **"model"** to discern this resource as a data model.

One of **base\_sql\_table** or **base\_sql\_query** is required to specify the data for this model:

\*base\_sql\_table:string

A table or SQL view in the data connection.

```
id: customers  
base_sql_table: public.customers
```

\*base\_sql\_query:string

A SQL query that produces a table.

```
id: subscribers  
base_sql_query: |  
  SELECT * FROM public.customers  
  WHERE tier IN ('PREMIUM', 'Plus');
```

name:string

The user-facing display name for this model.

If omitted, defaults to the sentence-case value of **id**.

description:string

The user-facing description for this model.

visibility:[Visibility](#visibility)

The visibility of this model.

Defining a model as **internal** or **private** will prevent it from appearing within the data browser as an explore entrypoint for users, which can be helpful to hide models which are more clearly exposed with a view.

Defaults to **public**.

measures:[Measure[]](#measures)

List of measures for this model.

dimensions:[Dimension[]](#dimensions)

List of dimensions for this model.

relations:[Relation[]](#relations)

List of relations for this model.

### Dimensions[​](#dimensions "Direct link to Dimensions")

A dimension is a field backed by a physical column, a SQL expression, or a formula based expression. Dimensions are used to filter, group by, and inspect the details of analysis.

\*id:[ID](#id)

The unique identifier for this dimension.

This identifier is used as its reference and must be unique across all dimensions, measures and relations in this model. Changing this identifier may invalidate existing references.

One of **expr\_sql** or **expr\_calc** can be used to specify the logic for selecting this dimension.

If both **expr\_sql** and **expr\_calc** are omitted, then **expr\_sql** is defaulted to the value of **id**.

expr\_sql:string

A SQL column expression that produces a value for each row.

Often this is simply a column name.

```
id: sku  
type: string  
expr_sql: stock_keeping_unit
```

Or a more complex SQL expression:

```
id: subscription_attribution_quarter  
type: datetime_tz  
expr_sql: DATE_TRUNC(subscribed_at, 'quarter')
```

expr\_calc:string

A [Hex calculation formula](/docs/explore-data/cells/calculations#formulas) that produces a value for each row.

```
id: full_name  
type: string  
expr_calc: CONCAT(first_name, ' ', last_name)
```

\*type:[DataType](#data-type)

The data type of this dimension.

unique:boolean

If true, this dimension is unique across all rows in the model, such as for a primary key column.

At least one `unique: true` dimension is required on each model. This is used to properly aggregate measures across relationships without double counting.

name:string

The user-facing display name for this dimension.

If omitted, defaults to the sentence-case value of **id**.

description:string

The user-facing description for this dimension.

visibility:[Visibility](#visibility)

The visibility of this dimension.

Defaults to **public**.

### Measures[​](#measures "Direct link to Measures")

A measure defines an aggregation which derives a single value from a group of records. Measures are used to quantify large amounts of data into meaningful values.

\*id:[ID](#id)

The unique identifier for this measure.

This identifier is used as its reference and must be unique across all dimensions, measures and relations in this model. Changing this identifier may invalidate existing references.

One of **func**, **func\_sql** or **func\_calc** is required to specify the aggregation logic for a measure.

\*func:string

A standard aggregation function over a provided dimension.

* **count:** Count of records. If **of** is specified (optional in this case), then only non-null values for that dimension will be calculated.
* **count\_distinct:** Count of unique values over the dimension.
* **sum, avg, median, min, max, stddev, stddev\_pop, variance**, and **variance\_pop:**  
  Standard mathematical functions over a number dimension.

of:string

The dimension over which the aggregation is applied.

> A dimension id can be used to reference an existing dimension, or a new dimension can be specified inline.

filters:[Dimension[]](#dimensions)

List of boolean dimensions which must be true for a row to be included in the measure’s aggregation.

> A dimension id can be used to reference an existing dimension, or a new dimension can be specified inline.

```
id: total_sales  
func: count
```

```
id: revenue  
func: sum  
of: price
```

```
id: revenue_from_us_deliveries  
func: sum  
of: price  
filters:  
  - is_delivery  
  - expr_sql: region = 'US'
```

\*func\_sql:string

An aggregating SQL select expression that produces a single value over a set of rows.

```
id: adjusted_revenue  
func_sql: SUM(price) * 0.9
```

\*func\_calc:string

An aggregating
[Hex calculation formula](/docs/explore-data/cells/calculations#formulas)
that produces a single value over a set of rows.

```
id: profits  
func_calc: revenue - costs
```

type:[DataType](#data-type)

The data type of this measure.

If omitted, defaults to **number**.

name:string

The user-facing display name for this measure.

If omitted, defaults to the sentence-case value of **id**.

description:string

The user-facing description for this measure.

visibility:[Visibility](#visibility)

The visibility of this measure.

Defaults to **public**.

semi\_additive:object

The semi-additive behavior of this measure when aggregated over specific dimensions.

\*over:object[]

A list of dimensions that determine row selection for aggregation. Rows are selected using a hierarchical approach where dimensions are evaluated for the representative value (minimum or maximum) in the order they are specified.

> Currently limited to a single dimension.

\*dimension:[Dimension](#dimension)

The dimension to use for row selection.

> A dimension id can be used to reference an existing dimension.

pick:min | max

Whether to select rows with the minimum or maximum dimension value.

If omitted, defaults to **max**.

groupings:[Dimension[]](#dimensions)

A list of dimensions to group by when determining minimum or maximum values. A representative value will be selected from each group.

#### Semi-additive[​](#semi-additive "Direct link to Semi-additive")

A measure is semi-additive when it cannot be added together when aggregating over some dimension(s). Instead, a representative value should be determined and all rows matching that value should be aggregated.

Semi-additive measures are useful on snapshot tables where values should not be added together when aggregating over time. In the following example, the total of all account balances is the sum of balances only on the latest date.

```
id: total  
func_sql: SUM(balance)  
semi_additive:  
  over:  
    - dimension: date
```

If the data is such that the accounts do not have a row for every date, then **groupings** defines how to slice the data to pick the latest balance for each account. (This requires that the snapshot reflects when an account balance goes to 0, otherwise the last valid balance for an account will be included, which could include closed accounts.)

```
id: total  
func_sql: SUM(balance)  
semi_additive:  
  over:  
    - dimension: date  
  groupings:  
    - account_id
```

### Relations[​](#relations "Direct link to Relations")

A relation defines how two models connect to each other, allowing you to analyze data across multiple tables. For example, you might connect a sales model to a customers model to analyze sales by customer characteristics.

```
id: owner  
target: users  
type: many_to_one  
join_sql: owner_id = ${owner}.id
```

\*id:[ID](#id)

The unique identifier for this relation. Typically, this is the id of the model being joined to.

This identifier is used as its reference and must be unique across all dimensions, measures and relations in this model. Changing this identifier may invalidate existing references.

target:[ID](#id)

The target model this relation joins to.

If omitted, defaults to the value of **id**.

\*join\_sql:string

The SQL condition to join the base model to a target.

Join conditions are typically of the form `foreign_key = ${relation_id}.primary_key`.

\*type:string

The cardinality of the join, from the base model to the target.

One of the following values:

* **many\_to\_one**
* **one\_to\_many**
* **one\_to\_one**

visibility:[Visibility](#visibility)

The visibility of this relation.

Defaults to **public**.

## View specification[​](#view-specification "Direct link to View specification")

Views are declared on top of models and provide fit-for-purpose entrypoints for users to conduct self-serve analysis.

Views can rename and reorganize the dimensions, measures, and relations of models for clarity and readability. Using this feature can help simplify complex join trees or flatten relations to simpler concepts for your users.

> Views are an optional feature. Models and views share all analytical capabilities in Hex. Views can be incrementally introduced to build a cleaner facade over your data models as it becomes more complex.

```
id: revenue  
type: view  
base: order_items  
contents:  
  - measures:  
      - revenue  
    dimensions:  
      - timestamp  
      - orders.is_delivery  
  - relation: orders.customers  
    dimensions: ...
```

\*id:[ID](#id)

The unique identifier for this view.

This identifier is used as its reference across all resources and must be unique across the semantic project. Changing this identifier may invalidate existing references.

\*type:"view"

The string **"view"** to discern this resource as a view.

\*base:string

The data model to use as the grain for this view.

\*contents:[Group[]](#groups)

The contents for this view.

### Groups[​](#groups "Direct link to Groups")

A group is a set of dimensions and measures to display to the end user in the UI. Groups are displayed as folders in Hex UIs. The layout of groups only affects the visual organization of dimensions and measures, and has no effects on query logic.

The most common practice is to create one group per related entity you want to expose as part of the view.

relation:string

Dot-separated relation path for this group, relative to the parent (**base** for top-level groups). Sets the default model for declarations within this group.

If omitted, defaults to the **base** model.

name:string

The user-facing display name for this group.

If omitted, defaults to the name of the group's **relation**.

description:string

The user-facing description for this group.

If omitted, defaults to the description of the group's **relation**.

dimensions:string[]

List of dimensions to include in this group, relative to the group's **relation**.

measures:string[]

List of measures to include in this group, relative to the group's **relation**.

contents:[Group[]](#groups)

Nested groups to be displayed as an inner tree.

Using nested groups can be useful to explicitly surface a hierarchical relationships between entities. However, for the simplest experience for end-users, consider hoisting up nested relations to a single flat list of uniquely named groups.

#### Wildcard Inclusions[​](#wildcard-inclusions "Direct link to Wildcard Inclusions")

To include all dimensions or measures from the group's relation, you may use the `...` shorthand in place of a list of items:

```
- relation: orders.customers  
  dimensions: ...
```

To omit some items from the `...` list, you may specify it as part of a list with excluded items prefixed with `~`:

```
- relation: orders.customers  
  dimensions:  
    - ...  
    - ~phone_number # not relevant for revenue analytics
```

#### Overriding names and descriptions[​](#overriding-names-and-descriptions "Direct link to Overriding names and descriptions")

To include an item but under a different name or with a different description, specify an object instead of a string, and provide **name** or **description** to override the item's fields:

```
- relation: orders.customers  
  dimensions:  
    - dimension: is_subscriber  
      name: Ordered by subscriber  
  measures:  
    - measure: count  
      description: Unique count of users contributing to revenue
```

## Shared types[​](#shared-types "Direct link to Shared types")

### ID[​](#id "Direct link to ID")

An ID is a string that conforms to the following rules:

* Begins with a lowercase letter or an underscore
* Only contains lowercase letters, underscores, and numbers
* Between 2 and 128 characters long (inclusive)

The following IDs are reserved by the system and cannot be used:

```
this, self, dataset, model, view, metric, env, _hex*
```

### DataType[​](#datatype "Direct link to DataType")

Data types are abstract. You do not need to specify the exact subtype of number (int64, unsigned int, double, float, etc), instead you can just specify "number".

* **number:** Includes INT, BIGINT, FLOAT, DECIMAL, DOUBLE, REAL, etc.
* **string:** Includes CHAR, VARCHAR, TEXT, etc.
* **timestamp\_tz:** Timezone-aware.
* **timestamp\_naive:** Without timezone information.
* **date:** The date portion of a timestamp; always without a timezone.
* **boolean:** True or false.
* **other:** Any other type without special support in Hex.

### Visibility[​](#visibility "Direct link to Visibility")

The **visibility** key controls where a resource can be used and who can see it. Hex supports three built-in values:

* **public:** Can be viewed and used by everyone.
* **internal:** Can be referenced by other resources in the semantic project, but will be hidden from users.
* **private:** Can only be used within the current resource. Hidden from users.

The **visibility** key should not be relied on as a security control and is only used to visually hide content in the UI. For the strongest security guarantees, configure OAuth or role-based access within your database.

## SQL interpolation[​](#sql-interpolation "Direct link to SQL interpolation")

Any key containing **sql** will be treated as SQL to execute in your database. To reference semantic entities within these SQL snippets, you may use interpolation within `${}`.

Interpolations can reference all the dimensions, measures, and relations within the current model by their **id**.

Specifying a **dimension id** inside of a `${}` will interpolate a column expression which produces the value for the referenced dimension. This can be used to create derived dimensions, aggregates on top of dimensions, or for the join condition of relations.

```
dimensions:  
  - id: customer_tier  
    type: string  
  - id: is_premium_tier  
    func_sql: ${customer_tier} IN ('Premium', 'Plus')
```

Specifying a **measure id** inside of a `${}` will interpolate an aggregating expression which produces the value for the referenced measure. This is only valid inside of aggregating contexts, such as another measure.

```
measures:  
  - id: revenue  
    func: sum  
    of: price  
  - id: costs  
    func: sum  
    of: cost_of_goods  
  - id: profit  
    func_sql: ${revenue} - ${costs}
```

Specifying a **relation id** inside of a `${}` will interpolate the alias name for the joined table, which may differ from the id of the relation.
Using dot-notation inside of the interpolation will allow accessing the measures and dimensions inside of the joined model.

```
relations:  
  - id: customers  
    type: many_to_one  
    # reference the join alias  
    join_sql: customer_id = ${customers}.id  
  
measures:  
  - id: adjusted_revenue  
    # reference a dimension on `customers`  
    # let's assume premium tier users get a 10% discount  
    func_sql: SUM(IF(${customers.is_premium_tier}, price * 0.9, price))
```

Note the distinction between referencing a dimension on a relation versus referencing the relation's table and then accessing a SQL column:

* `${customers.full_name}` accesses the **full\_name** dimension on the **customers** model
* `${customers}.first_name` accesses the underlying **first\_name** column on the **customers** model's underlying table.

## Calculation formulas[​](#calculation-formulas "Direct link to Calculation formulas")

Any key containing **calc** will be treated as a [Hex calculation formula](/docs/explore-data/cells/calculations#formulas).

Calculation formulas can reference all the dimensions, measures, and relations within the current model by their **id**. SQL columns which are not included as dimensions are not in scope and cannot be referenced.

## File and directories[​](#file-and-directories "Direct link to File and directories")

The Hex semantic specification currently infers no behavior from the names or locations of YAML files. A file can be named anything so long as it ends with a valid YAML extension (`.yaml` or `.yml`).

[Multi-document YAML](https://yaml.irz.fr/multiples-documents.html) is fully supported. Two or more semantic resources can be specified in the same file when separated by a `---` divider.

## Examples[​](#examples "Direct link to Examples")

* Basic
* Sales

This example builds a simple AAR measure between a **users** and **organizations** model, without defining anything else. It demonstrates the basic approach when authoring models.

```
id: organizations  
type: model  
base_sql_table: public.organizations  
  
measures:  
  - id: arr  
    name: Annual reoccurring revenue  
    func: sum  
    of: users.annual_seat_price  
  
dimensions:  
  - id: organization_id  
    type: string  
    unique: true  
  
relations:  
  - id: users  
    type: one_to_many  
    join_sql: id = ${users}.org_id
```

```
id: users  
type: model  
base_sql_table: public.users  
  
dimensions:  
  - id: annual_seat_price  
    type: number  
    expr_sql: IF(seat_type = 'VIEW_ONLY', 20, 60)
```

This example models data for a hypothetical pizza shop which utilizes more features, joins between fact and dimensional tables, includes more dimensions and measures that users could slice and dice around, and then exposes a revenue view.

```
id: order_items  
type: model  
base_sql_table: public.order_items  
description: Fact table of line items on a given order.  
visibility: internal  
  
measures:  
  - id: revenue  
    func: sum  
    of: value  
    description: |  
      The total sales of pizza.  
      synonyms: sales, top line revenue  
  - id: number_of_customers  
    func: count_distinct  
    of: customer_id  
  - id: number_of_orders  
    func: count_distinct  
    of: order_id  
  - id: revenue_per_customer  
    func_calc: revenue / number_of_customers  
  - id: revenue_per_order  
    func_calc: revenue / number_of_orders  
  - id: avg_unit_price  
    func_calc: SUM(value) / SUM(quantity)  
  - id: orders_per_customer  
    func_calc: number_of_orders / number_of_customers  
  - id: revenue_adjusted_for_delivery_cost  
    func: sum  
    of:  
      expr_sql: ${value} * IF(${orders.is_delivery}, 0.8, 1)  
  - id: revenue_from_custom_delivery_pizza  
    func: sum  
    of: value  
    filters:  
      - orders.is_delivery  
      - expr_sql: ${products.pizza_type} = 'Custom'  
  
dimensions:  
  # facts  
  - id: value  
    type: number  
    expr_sql: item_price * quantity  
    description: The total price paid for the sale.  
  - id: item_price  
    type: number  
  - id: quantity  
    type: number  
  - id: timestamp  
    type: timestamp_tz  
  # keys  
  - id: id  
    type: string  
    unique: true  
    visibility: internal  
  - id: item_id  
    type: number  
    visibility: internal  
  - id: customer_id  
    type: string  
    visibility: internal  
  - id: order_id  
    type: number  
    visibility: internal  
  - id: product_id  
    type: string  
    visibility: internal  
  
relations:  
  - id: customers  
    join_sql: ${customer_id} = ${customers.id}  
    type: many_to_one  
  - id: orders  
    join_sql: ${order_id} = ${orders.id}  
    type: many_to_one  
  - id: products  
    join_sql: ${product_id} = ${products.id}  
    type: many_to_one
```

```
id: orders  
type: model  
base_sql_table: public.orders  
description: Fact table of order information.  
  
measures:  
  - id: count  
    name: Number of orders  
    func: count  
  - id: total_order_value  
    func: sum  
    of: order_value  
  
dimensions:  
  # facts  
  - id: timestamp  
    type: timestamp_naive  
  - id: payment_method  
    type: string  
  - id: is_delivery  
    type: boolean  
    expr_sql: delivery = 'Yes'  
  - id: type  
    type: string  
  - id: order_value  
    type: number  
  - id: discount_code  
    type: string  
  - id: feedback_rating  
    type: number  
  - id: delivery_time  
    type: number  
  - id: preparation_time  
    type: number  
  - id: special_request  
    type: string  
  - id: referral_source  
    type: string  
  # ids  
  - id: id  
    type: number  
    visibility: internal  
    unique: true  
  - id: customer_id  
    type: string  
    visibility: internal  
  - id: cook_id  
    type: string  
    visibility: internal  
  - id: location_id  
    type: string  
    visibility: internal  
  
relations:  
  - id: customers  
    join_sql: ${customer_id} = ${customers.id}  
    type: many_to_one  
  - id: order_items  
    join_sql: ${id} = ${order_items.order_id}  
    type: one_to_many
```

```
id: products  
type: model  
base_sql_table: public.products  
description: Dimensional table of product information.  
dimensions:  
  - id: id  
    type: string  
    visibility: internal  
    unique: true  
  - id: name  
    type: string  
  - id: pizza_size  
    type: string  
  - id: pizza_shape  
    type: string  
  - id: pizza_type  
    type: string  
  - id: price  
    type: number
```

```
id: customers  
type: model  
name: Valued customers  
base_sql_table: public.users  
description: Dimensional table of customer information.  
measures:  
  - id: count  
    func: count  
dimensions:  
  - id: id  
    type: string  
    visibility: internal  
    unique: true  
  - id: name  
    type: string  
  - id: address  
    type: string  
  - id: phone_number  
    type: string
```

```
id: revenue  
type: view  
description: View over relevant information for revenue tracking.  
base: order_items  
contents:  
  - name: Sale  
    measures:  
      - revenue  
      - revenue_per_customer  
      - revenue_per_order  
    dimensions:  
      - timestamp  
      - orders.is_delivery  
      - orders.payment_method  
  - relation: products  
    dimensions: ...  
  - relation: orders.customers  
    measures:  
      - measure: count  
        name: Unique customers  
    dimensions:  
      - ...  
      - ~phone_number
```

#### On this page

* [Resources](#resources)
* [Model specification](#model-specification)
  + [Dimensions](#dimensions)
  + [Measures](#measures)
  + [Relations](#relations)
* [View specification](#view-specification)
  + [Groups](#groups)
* [Shared types](#shared-types)
  + [ID](#id)
  + [DataType](#datatype)
  + [Visibility](#visibility)
* [SQL interpolation](#sql-interpolation)
* [Calculation formulas](#calculation-formulas)
* [File and directories](#file-and-directories)
* [Examples](#examples)