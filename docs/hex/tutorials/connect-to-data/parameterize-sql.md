On this page

# Parameterize SQL queries

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/1f0cfa16-cea1-428a-b950-e56379f2fdac/latest)!

One of the easiest ways to upgrade your projects is to make SQL queries dynamically react to user input or the results of a previous SQL query. We call this “parameterizing" a query.

This tutorial will walk through some quick examples of a query parameterization and touch a bit on the magic of using Jinja like a pro. Check out [the docs](/docs/explore-data/cells/using-jinja) for more information— Or this video below!

## Let's write a simple SQL query[​](#lets-write-a-simple-sql-query "Direct link to Let's write a simple SQL query")

We'll write a simple SQL query to list all the video games in a [popular video game sales dataset](https://www.kaggle.com/gregorut/videogamesales).

## Now, add some user input[​](#now-add-some-user-input "Direct link to Now, add some user input")

Cool, we've got a bunch of results.

Let's add a filter so that a user can select which genre of video game they're interested in, all without having to write SQL or even have access to the Notebook view of the app. To do this, we’ll populate a [dropdown Input parameter](/docs/explore-data/cells/input-cells/dropdown-inputs) using the unique values from the genre column in the query above. Let’s call this variable `genre_selector`.

## Finally, parameterize the SQL query with the input value[​](#finally-parameterize-the-sql-query-with-the-input-value "Direct link to Finally, parameterize the SQL query with the input value")

With the Input parameter defined, we can reference the `genre_selector` variable **in the SQL query** to dynamically insert that value into the query. We use [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) syntax to add parameters to queries.

```
SELECT *  
FROM public.vg_sales  
WHERE genre = {{genre_selector}}
```

tip

To see how Hex parses the dynamic query, click the **View compiled** button in your SQL cell.

## Arrays[​](#arrays "Direct link to Arrays")

That was a very simple example of a feature that can get very complex and powerful. In addition to inserting single variables, you can reference entire arrays using a `{{ variable | array }}` syntax in your query.

The video game dataset we’re using here includes a **lot** of different game publishers. What if we only want to see a subset of those?

Let’s define a new variable, `publishers_subset`, with a list of desired publishers (you could even use a [multi-select Input parameter](/docs/explore-data/cells/input-cells/multiselect-inputs) to make this interactive!). Instead of hard-coding that list into your where clause, you can feed it to your query as a parameter. When you pass a variable with more than one value (e.g. a list or array) to a SQL query you use the same `{{ }}` syntax with an additional flag, `| array`, so that the query knows to expect to pass through more than one value.

```
SELECT *  
FROM public.vg_sales  
WHERE genre = {{ genre_selector }}  
    AND publisher IN ({{publishers_subset | array }})
```

## The sky is the limit with Jinja[​](#the-sky-is-the-limit-with-jinja "Direct link to The sky is the limit with Jinja")

You can write some extremely flexible queries using more of the advanced options provided via Jinja templating. For example, you can run entirely different SQL statements depending on upstream logic and even create a for loop **inside your query**. Let’s walk through a quick example now.

Let’s say you want to rename the publisher ‘Sony Computer Entertainment’ to just ‘Sony’, but you can’t guarantee that Sony will always be in the subset of desired publishers. You can use a Jinja if block to test if ‘Sony Computer Entertainment’ is included in the `publishers_subset` and a CASE WHEN statement to replace that when needed!

```
SELECT  
    {% if 'Sony Computer Entertainment' in publishers_subset %}  
    CASE WHEN publisher = 'Sony Computer Entertainment' THEN 'Sony' ELSE publisher END as publisher  
		,  
    {% endif %}  
    name  
    , year  
    , genre  
FROM public.vg_sales  
WHERE genre = {{ genre_selector }}  
    AND publisher IN ({{publishers_subset | array }})
```

In another scenario, you might want a query to be filtered based on user-selected input, but want to account for the case where no input is selected. You can achieve this with a Jinja if block and a dummy `1=1` statement, where the filter is only applied if the variable holding the input parameter selection is not empty.

```
SELECT *  
FROM public.vg_sales  
WHERE 1=1  
{% if publishers_subset %}  
AND publisher in ({{publishers_subset | array}})  
{% endif %}
```

This is just the start for what you can do with parameterized SQL! Check out [the docs](/docs/explore-data/cells/using-jinja) for further details, or other gallery projects for more inspiration!

## A word about prepared statements[​](#a-word-about-prepared-statements "Direct link to A word about prepared statements")

Hex handles all parameterized SQL queries as [prepared statements](https://en.wikipedia.org/wiki/Prepared_statement) for both performance and security reasons. Prepared statements are a way to template queries and substitute values where desired during execution. Not only is there some performance benefit when using prepared statements, they are also robust against SQL injection. Read more about [prepared statements here](https://www.hackedu.com/blog/how-to-prevent-sql-injection-vulnerabilities-how-prepared-statements-work).

By default, prepared statements cannot accept query **attributes** as parameters and only allows for substituting in **values**. For example, the phrase `WHERE column = {{value}}` is allowed by default while `WHERE {{column}} = value` is not. You can force the literal parameterization of a query attribute by passing `| sqlsafe` as an additional flag with your parameter. e.g. `WHERE {{column | sqlsafe}} = value`.

With great power comes great responsibility. If you use the `sqlsafe` flag to force a parameterization, you are removing the protection that prepared statements offer against sql injection!

#### On this page

* [Let's write a simple SQL query](#lets-write-a-simple-sql-query)
* [Now, add some user input](#now-add-some-user-input)
* [Finally, parameterize the SQL query with the input value](#finally-parameterize-the-sql-query-with-the-input-value)
* [Arrays](#arrays)
* [The sky is the limit with Jinja](#the-sky-is-the-limit-with-jinja)
* [A word about prepared statements](#a-word-about-prepared-statements)