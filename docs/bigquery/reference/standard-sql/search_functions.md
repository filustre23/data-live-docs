* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Search functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following search functions.

## Function list

| Name | Summary |
| --- | --- |
| [`SEARCH`](/bigquery/docs/reference/standard-sql/search_functions#search) | Checks to see whether a table or other search data contains a set of search terms. |
| [`VECTOR_SEARCH`](/bigquery/docs/reference/standard-sql/search_functions#vector_search) | Performs a vector search on embeddings to find semantically similar entities. |

## `SEARCH`

```
SEARCH(
  data_to_search, search_query
  [, json_scope => { 'JSON_VALUES' | 'JSON_KEYS' | 'JSON_KEYS_AND_VALUES' } ]
  [, analyzer => { 'LOG_ANALYZER' | 'NO_OP_ANALYZER' | 'PATTERN_ANALYZER'} ]
  [, analyzer_options => analyzer_options_values ]
)
```

**Description**

The `SEARCH` function checks to see whether a BigQuery table or other
search data contains a set of search terms (tokens). It returns `TRUE` if all
search terms appear in the data, based on the [rules for search\_query](#search_query_rules)
and text analysis described in the [text analyzer](/bigquery/docs/reference/standard-sql/text-analysis). Otherwise,
this function returns `FALSE`.

**Definitions**

* `data_to_search`: The data to search over. The value can be:

  + Any GoogleSQL data type literal
  + A list of columns
  + A table reference
  + A column of any type

  A table reference is evaluated as a `STRUCT` whose fields are the columns of
  the table. `data_to_search` can be any type, but `SEARCH` will return
  `FALSE` for all types except those listed here:

  + `ARRAY<STRING>`
  + `ARRAY<STRUCT>`
  + `JSON`
  + `STRING`
  + `STRUCT`

  You can search for string literals in columns of the preceding types.
  For additional rules, see [Search data rules](#data_to_search_rules).

* `search_query`: A `STRING` literal, or a `STRING` constant expression that
  represents the terms of the search query. If `search_query` is `NULL`, an
  error is returned. If `search_query` produces no search tokens,
  and the text analyzer is `LOG_ANALYZER` or `PATTERN_ANALYZER`, an error is
  produced.
* `json_scope`: A named argument with a `STRING` value.
  Takes one of the following values to indicate the scope of JSON data to be
  searched. It has no effect if `data_to_search` isn't a JSON value or
  doesn't contain a JSON field.

  + `'JSON_VALUES'` (default): Only the JSON values are searched. If
    `json_scope` isn't provided, this is used by default.
  + `'JSON_KEYS'`: Only the JSON keys are searched.
  + `'JSON_KEYS_AND_VALUES'`: The JSON keys and values are searched.
* `analyzer`: A named argument with a `STRING` value. Takes
  one of the following values to indicate the text analyzer to use:

  + `'LOG_ANALYZER'` (default): Breaks the input into tokens when delimiters
    are encountered and then normalizes the tokens.
    For more information, see [`LOG_ANALYZER`](/bigquery/docs/reference/standard-sql/text-analysis#log_analyzer).
  + `'NO_OP_ANALYZER'`: Extracts the text as a single token, but
    doesn't apply normalization. For more information about this analyzer,
    see [`NO_OP_ANALYZER`](/bigquery/docs/reference/standard-sql/text-analysis#no_op_analyzer).
  + `'PATTERN_ANALYZER'`: Breaks the input into tokens that match a
    regular expression. For more information, see
    [`PATTERN_ANALYZER` text analyzer](/bigquery/docs/reference/standard-sql/text-analysis#pattern_analyzer).
* `analyzer_options`: A named argument with a JSON-formatted `STRING` value.
  Takes a list of text analysis rules. For more information,
  see [Text analyzer options](/bigquery/docs/reference/standard-sql/text-analysis#text_analyzer_options).

**Details**

The `SEARCH` function is designed to work with [search indexes](/bigquery/docs/search-index) to
optimize point lookups. Although the `SEARCH` function works for
tables that aren't indexed, its performance will be greatly improved with a
search index. If both the analyzer and analyzer options match the one used
to create the index, the search index will be used.

**Rules for `search_query`**

The `'NO_OP_ANALYZER'` extracts the search query as a single token without
parsing it. The following rules apply only when using the `'LOG_ANALYZER'` or
`'PATTERN_ANALYZER'`.

A search query is a set of one or more terms that are combined
using the logical operators `AND` and `OR` along with parenthesis. Any
whitespace in the search query that is not in a *phrase* or *backtick* term is
considered an (implicit) `AND`. First, a search query is broken down into
terms using logical operators and parenthesis in the search query. Then, each
term is evaluated based on whether or not it appears in the data to search. The
final outcome of the `SEARCH` function is the result of the logical expression
represented by the search query.

The following grammar is used to transform the search query into a logical
expression of terms. The grammar is defined using the
[ANTLR meta-language](https://www.antlr2.org/doc/metalang.html):

```
query_string : expression EOF;

expression  : '(' expression  ')'
            | expression 'AND' expression
            | expression '\s' expression
            | expression 'OR' expression
            | term
            ;

term : single_term
     | phrase_term
     | backtick_term
     ;

backtick_term : '`' ( '\`' | ~[`] )+ '`';

phrase_term : '"' ( '\"' | ~["] )+ '"';

single_term : ( '\' reserved_char | ~[reserved_char] )+;
```

To evaluate each term, it is further broken down into zero or more searchable
tokens based on the text analyzer. The following section contains the rules for
how different types of terms are analyzed and evaluated.

Rules for `backtick_term` in [`search_query`](#search_query_arg):

* If the `LOG_ANALYZER` text analyzer is used, text enclosed in backticks
  forces an exact match.

  For example, `` `Hello World` happy days `` becomes `Hello World`, `happy`,
  and `days`.
* Search terms enclosed in backticks must match exactly in `data_to_search`,
  subject to the following conditions:

  + It appears at the start of `data_to_search` or is immediately preceded
    by a delimiter.
  + It appears at the end of `data_to_search` or is immediately followed by
    a delimiter.

  For example, `` SEARCH('foo.bar', '`foo.`') `` returns `FALSE` because the
  text enclosed in the backticks `foo.` is immediately followed by the
  character `b` in the search data `foo.bar`, rather than by a delimiter or
  the end of the string. However, `` SEARCH('foo..bar', '`foo.`') `` returns
  `TRUE` because `foo.` is immediately followed by the delimiter `.` in the
  search data.
* Search terms enclosed in backticks must match case exactly, regardless of
  any normalization settings in `analyzer_options`.

  For example:

  ```
  -- FALSE because backticks require an exact match, including capitalization
  SELECT
    SEARCH( 'Hello-world', '`WORLD`',
      analyzer=>'LOG_ANALYZER',
      analyzer_options=>'''
      {
        "token_filters": [
          {
            "normalizer": {"mode": "LOWER"}
          }
        ]
      }'''
    ) AS results
  ```
* The backtick itself can be escaped using a backslash,
  as in `` \`foobar\` ``.
* The following are reserved words and must be enclosed
  in backticks:

  `AND`, `NOT`, `OR`, `IN`, and `NEAR`

Rules for `reserved_char` in [`search_query`](#search_query_arg):

* Text not enclosed in backticks requires the following
  reserved characters to be escaped by a double backslash
  `\\`:

  + `[ ] < > ( ) { } | ! ' " * & ? + / : = - \ ~ ^`
  + If the quoted string is preceded by the character `r` or `R`, such as
    `r"my\+string"`, then it's treated as a raw string and only a single
    backslash is required to escape the reserved characters. For more
    information about raw strings and escape
    sequences, see [String and byte literals](/bigquery/docs/reference/standard-sql/lexical#literals).

Rules for `phrase_term` in [`search_query`](#search_query_arg):

* A phrase is a type of term. If text is enclosed in double quotes and the
  `analyzer` is `LOG_ANALYZER`, `PATTERN_ANALYZER`, or not set
  (`LOG_ANALYZER` by default), the term represents a phrase.
* When a phrase is analyzed, a subset of tokens is created for that phrase.
  For example, from the phrase `"foo baz.bar"`, the analyzer called
  `LOG_ANALYZER` generates the phrase-specific tokens `foo`, `baz`, and `bar`.
* The order of terms in a phrase matters. A match is only returned if
  the tokens that were produced for the phrase are next to each other and in
  the same order as the tokens for [`data_to_search`](#data_to_search_arg).

  For example:

  ```
  -- FALSE because 'foo' and 'bar' aren't next to each other in
  -- 'foo baz.bar'.
  SEARCH('foo baz.bar', '"foo bar"')
  ```

  ```
  -- TRUE because 'foo' and 'baz' are next to each other in
  -- 'foo baz.bar'.
  SEARCH('foo baz.bar', '"foo baz"')
  ```
* A single quote inside of the phrase is analyzed as a special character.
* An escaped double quote (double quote after a backslash) is analyzed
  as a double quote character.

**How `data_to_search` is broken into searchable tokens**

The following table shows how [`data_to_search`](#data_to_search_arg) is broken
into searchable tokens by the `LOG_ANALYZER` text analyzer. All entries are
strings.

| data\_to\_search | searchable tokens |
| --- | --- |
| 127.0.0.1 | 127   0   1   127.0.0.1  . 127.0.0   127.0   0.0   0.0.1   0.1 |
| foobar@example.com | foobar   example   com   foobar@example   example.com   foobar@example.com |
| The fox. | the   fox   The   The fox   The fox.   fox   fox. |

**How `search_query` is broken into query terms**

The following table shows how [`search_query`](#search_query_arg) is broken into
query terms by the `LOG_ANALYZER` text analyzer. All entries are strings.

| search\_query | query terms |
| --- | --- |
| 127.0.0.1 | 127   0   1 |
| `127.0.0.1` | 127.0.0.1 |
| foobar@example.com | foobar   example   com |
| `foobar@example.com` | foobar@example.com |

**Rules for `data_to_search`**

General rules for [`data_to_search`](#data_to_search_arg):

* `data_to_search` must contain all tokens produced for
  `search_query` for the function to return `TRUE`.
* To perform a cross-field search, `data_to_search` must be a `STRUCT`,
  `ARRAY`, or `JSON` data type.
* Each `STRING` field in a compound data type is individually
  searched for terms.
* If at least one field in `data_to_search` includes all search terms
  produced by `search_query`, `SEARCH` returns `TRUE`. Otherwise it has the
  following behavior:

  + If at least one `STRING` field is `NULL`, `SEARCH` returns `NULL`.
  + Otherwise, `SEARCH` returns `FALSE`.

**Return type**

`BOOL`

**Examples**

The following queries show how tokens in `search_query` are analyzed
by a `SEARCH` function call using the default analyzer, `LOG_ANALYZER`:

```
SELECT
  -- ERROR: `search_query` is NULL.
  SEARCH('foobarexample', NULL) AS a,

  -- ERROR: `search_query` contains no tokens.
  SEARCH('foobarexample', '') AS b,
```

```
SELECT
  -- TRUE: '-' and ' ' are delimiters.
  SEARCH('foobar-example', 'foobar example') AS a,

  -- TRUE: The search query is a constant expression evaluated to 'foobar'.
  SEARCH('foobar-example', CONCAT('foo', 'bar')) AS b,

  -- FALSE: The search_query isn't split.
  SEARCH('foobar-example', 'foobarexample') AS c,

  -- TRUE: The double backslash escapes the ampersand which is a delimiter.
  SEARCH('foobar-example', 'foobar\\&example') AS d,

  -- TRUE: The single backslash escapes the ampersand in a raw string.
  SEARCH('foobar-example', R'foobar\&example')AS e,

  -- FALSE: The backticks indicate that there must be an exact match for
  -- foobar&example.
  SEARCH('foobar-example', '`foobar&example`') AS f,

  -- TRUE: An exact match is found.
  SEARCH('foobar&example', '`foobar&example`') AS g

/*-------+-------+-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     | f     | g     |
 +-------+-------+-------+-------+-------+-------+-------+
 | true  | true  | false | true  | true  | false | true  |
 +-------+-------+-------+-------+-------+-------+-------*/
```

```
SELECT
  -- TRUE: The order of terms doesn't matter.
  SEARCH('foobar-example', 'example foobar') AS a,

  -- TRUE: Tokens are made lower-case.
  SEARCH('foobar-example', 'Foobar Example') AS b,

  -- TRUE: An exact match is found.
  SEARCH('foobar-example', '`foobar-example`') AS c,

  -- FALSE: Backticks preserve capitalization.
  SEARCH('foobar-example', '`Foobar`') AS d,

  -- FALSE: Backticks don't have special meaning for search_data and are
  -- not delimiters in the default LOG_ANALYZER.
  SEARCH('`foobar-example`', '`foobar-example`') AS e,

  -- TRUE: An exact match is found after the delimiter in search_data.
  SEARCH('foobar@example.com', '`example.com`') AS f,

  -- TRUE: An exact match is found between the space delimiters.
  SEARCH('a foobar-example b', '`foobar-example`') AS g;

/*-------+-------+-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     | f     | g     |
 +-------+-------+-------+-------+-------+-------+-------+
 | true  | true  | true  | false | false | true  | true  |
 +-------+-------+-------+-------+-------+-------+-------*/
```

```
SELECT
  -- FALSE: No single array entry matches all search terms.
  SEARCH(['foobar', 'example'], 'foobar example') AS a,

  -- FALSE: The search query is equivalent to foobar\\=.
  SEARCH('foobar=', '`foobar\\=`') AS b,

  -- FALSE: This is equivalent to the previous example.
  SEARCH('foobar=', R'`\foobar=`') AS c,

  -- TRUE: The equals sign is a delimiter in the data and query.
  SEARCH('foobar=', 'foobar\\=') AS d,

  -- TRUE: This is equivalent to the previous example.
  SEARCH('foobar=', R'foobar\=') AS e,

  -- TRUE: An exact match is found.
  SEARCH('foobar.example', '`foobar`') AS f,

  -- FALSE: `foobar.\` isn't analyzed because of backticks; it isn't
  -- followed by a delimiter in search_data 'foobar.example'.
  SEARCH('foobar.example', '`foobar.\`') AS g,

  -- TRUE: `foobar.` isn't analyzed because of backticks; it is
  -- followed by the delimiter '.' in search_data 'foobar..example'.
  SEARCH('foobar..example', '`foobar.`') AS h;

/*-------+-------+-------+-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     | f     | g     | h     |
 +-------+-------+-------+-------+-------+-------+-------+-------+
 | false | false | false | true  | true  | true  | false | true  |
 +-------+-------+-------+-------+-------+-------+-------+-------*/
```

The following queries show how logical expression can be used in `search_query`
to perform a `SEARCH` function call:

```
SELECT
  -- TRUE: A whitespace is an implicit AND.
  -- Both `foo` and `bar` are in `foo bar baz`.
  SEARCH(R'foo bar baz', R'foo bar') AS a,

  -- TRUE: Similar to previous case
  -- `foo` and `bar` are in `foo bar baz`.
  SEARCH(R'foo bar baz', R'foo AND bar') AS b,

  -- TRUE: Only one of `foo` or `bar` should be in `foo`.
  SEARCH(R'foo', R'foo OR bar') AS c,

  -- TRUE: `foo` and one of `bar` or `baz` should be in `foo bar`.
  SEARCH(R'foo bar', R'"foo AND (bar OR baz)"') AS d,

  -- FALSE: Neither `bar` or `baz` are in `foo`.
  SEARCH(R'foo', R'foo AND (bar OR baz)') AS c,

/*-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     |
 +-------+-------+-------+-------+-------+
 | true  | true  | true  | true  | false |
 +-------+-------+-------+-------+-------+/
```

The following queries show how phrases in `search_query` are analyzed
by a `SEARCH` function call:

```
SELECT
  -- TRUE: The phrase `foo bar` is in `foo bar baz`.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are `foo` and `bar`
  -- and because they appear in that exact order in `data_to_search`,
  -- the function returns TRUE.
  SEARCH(R'foo bar baz', R'"foo bar"') AS a,

  -- TRUE: Case is ignored.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are `foo` and `bar`
  -- and because they appear in that exact order in `data_to_search`,
  -- the function return TRUE.
  SEARCH(R'Foo bar baz', R'"foo Bar"') AS b,

  -- TRUE: Both `-` and `&` are delimiters used during tokenization.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are `foo` and `bar`
  -- and because they appear in that exact order in `data_to_search`,
  -- the function returns TRUE.
  SEARCH(R'foo-bar baz', R'"foo&bar"') AS c,

  -- FALSE: Backticks in a phrase are treated as normal characters.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are:
  -- `foo
  -- bar`
  -- Because these searchable tokens don't appear in `data_to_search`,
  -- the function returns FALSE.
  SEARCH(R'foo bar baz', R'"`foo bar`"') AS d,

  -- FALSE: `foo bar` isn't in `foo else bar`.
  -- The tokens in `data_to_search` are `foo`, `else`, and `bar`.
  -- The searchable tokens in `query_string` are `foo` and `bar`.
  -- Even though they appear in `data_to_search`, but because they
  -- don't appear in that exact order (`foo` before `bar`),
  -- the function returns FALSE.
  SEARCH(R'foo else bar', R'"foo bar"') AS e,

  -- FALSE: `foo baz` isn't in `foo bar baz`.
  -- The `search_query` produces two terms. The first term is `bar`, which
  -- matches with the similar token in `data_to_search`. However, the second
  -- term is the phrase "foo&baz" with two tokens, `foo` and `baz`. Because
  -- `foo` and `baz` don't appear next to each other in `data_to_search`
  -- (`bar` is in between), the function returns FALSE.
  SEARCH(R'foo-bar-baz', R'bar "foo&baz"') AS f;

/*-------+-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     | f     |
 +-------+-------+-------+-------+-------+-------+
 | true  | true  | false | false | false | false |
 +-------+-------+-------+-------+-------+-------*/
```

```
SELECT
  -- FALSE: Only double quotes need to be escaped in a phrase.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are `foo\` and `bar` and they
  -- must appear in that exact order in `data_to_search`, but don't.
  SEARCH(
    R'foo bar baz',
    R'"foo\ bar"',
    analyzer_options=>'{"delimiters": [" "]}') AS a,

  -- TRUE: `foo bar` is in `foo bar baz` after tokenization with the given
  -- delimiters.
  -- The tokens in `data_to_search` are `foo`, `bar`, and `baz`.
  -- The searchable tokens in `query_string` are `foo` and `bar` and they
  -- must appear in that exact order in `data_to_search`.
  SEARCH(
    R'foo bar baz',
    R'"foo? bar"',
    analyzer_options=>'{"delimiters": [" ", "?"]}') AS b,

  -- TRUE: `read book` is in `read book now` after `the` is ignored.
  -- The tokens in `data_to_search` are `read`, `book`, and `now`.
  -- The searchable tokens in `query_string` are `read` and `book` and they
  -- must appear in that exact order in `data_to_search`.
  SEARCH(
    'read the book now',
    R'"read the book"',
    analyzer_options => '{ "token_filters": [{"stop_words": ["the"]}] }') AS c,

  -- FALSE: `c d` isn't in `a`, `b`, `cd`, `e` or `f` after tokenization with
  -- the given pattern.
  -- The tokens in `data_to_search` are `a`, `b`, `cd`, `e` and `f`.
  -- The searchable tokens in `query_string` are `c` and `d` and they
  -- must appear in that exact order in `data_to_search`. `data_to_search`
  -- contains a `cd` token, but not a `c` or `d` token.
  SEARCH(
    R'abcdef',
    R'"c d"',
    analyzer=>'PATTERN_ANALYZER',
    analyzer_options=>'{"patterns": ["(?:cd)|[a-z]"]}') AS d,

  -- TRUE: `ant apple` is in `ant apple avocado` after tokenization with
  -- the given pattern.
  -- The tokens in `data_to_search` are `ant`, `apple`, and `avocado`.
  -- The searchable tokens in `query_string` are `ant` and `apple` and they
  -- must appear in that exact order in `data_to_search`.
  SEARCH(
    R'ant orange apple avocado',
    R'"ant apple"',
    analyzer=>'PATTERN_ANALYZER',
    analyzer_options=>'{"patterns": ["a[a-z]"]}') AS e;

/*-------+-------+-------+-------+-------+
 | a     | b     | c     | d     | e     |
 +-------+-------+-------+-------+-------+
 | false | true  | true  | false | true  |
 +-------+-------+-------+-------+-------*/
```

The following query shows examples of calls to the `SEARCH` function using the
`NO_OP_ANALYZER` text analyzer and reasons for various return values:

```
SELECT
  -- TRUE: exact match
  SEARCH('foobar', 'foobar', analyzer=>'NO_OP_ANALYZER') AS a,

  -- FALSE: Backticks aren't special characters for `NO_OP_ANALYZER`.
  SEARCH('foo
```