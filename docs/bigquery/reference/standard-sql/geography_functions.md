* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Geography functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports geography functions.
Geography functions operate on or generate GoogleSQL
`GEOGRAPHY` values. The signature of most geography
functions starts with `ST_`. GoogleSQL for BigQuery supports the following functions
that can be used to analyze geographical data, determine spatial relationships
between geographical features, and construct or manipulate
`GEOGRAPHY`s.

All GoogleSQL geography functions return `NULL` if any input argument
is `NULL`.

## Categories

The geography functions are grouped into the following categories based on their
behavior:

| Category | Functions | Description |
| --- | --- | --- |
| Constructors | [`ST_GEOGPOINT`](#st_geogpoint)  [`ST_MAKELINE`](#st_makeline)  [`ST_MAKEPOLYGON`](#st_makepolygon)  [`ST_MAKEPOLYGONORIENTED`](#st_makepolygonoriented) | Functions that build new geography values from coordinates or existing geographies. |
| Parsers | [`ST_GEOGFROM`](#st_geogfrom)  [`ST_GEOGFROMGEOJSON`](#st_geogfromgeojson)  [`ST_GEOGFROMTEXT`](#st_geogfromtext)  [`ST_GEOGFROMWKB`](#st_geogfromwkb)  [`ST_GEOGPOINTFROMGEOHASH`](#st_geogpointfromgeohash) | Functions that create geographies from an external format such as [WKT](https://en.wikipedia.org/wiki/Well-known_text) and [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON). |
| Formatters | [`ST_ASBINARY`](#st_asbinary)  [`ST_ASGEOJSON`](#st_asgeojson)  [`ST_ASTEXT`](#st_astext)  [`ST_GEOHASH`](#st_geohash) | Functions that export geographies to an external format such as WKT. |
| Transformations | [`ST_BOUNDARY`](#st_boundary)  [`ST_BUFFER`](#st_buffer)  [`ST_BUFFERWITHTOLERANCE`](#st_bufferwithtolerance)  [`ST_CENTROID`](#st_centroid)  [`ST_CENTROID_AGG`](#st_centroid_agg) (Aggregate)  [`ST_CLOSESTPOINT`](#st_closestpoint)  [`ST_CONVEXHULL`](#st_convexhull)  [`ST_DIFFERENCE`](#st_difference)  [`ST_EXTERIORRING`](#st_exteriorring)  [`ST_INTERIORRINGS`](#st_interiorrings)  [`ST_INTERSECTION`](#st_intersection)  [`ST_LINEINTERPOLATEPOINT`](#st_lineinterpolatepoint)  [`ST_LINESUBSTRING`](#st_linesubstring)  [`ST_SIMPLIFY`](#st_simplify)  [`ST_SNAPTOGRID`](#st_snaptogrid)  [`ST_UNION`](#st_union)  [`ST_UNION_AGG`](#st_union_agg) (Aggregate) | Functions that generate a new geography based on input. |
| Accessors | [`ST_DIMENSION`](#st_dimension)  [`ST_DUMP`](#st_dump)  [`ST_ENDPOINT`](#st_endpoint)  [`ST_GEOMETRYTYPE`](#st_geometrytype)  [`ST_ISCLOSED`](#st_isclosed)  [`ST_ISCOLLECTION`](#st_iscollection)  [`ST_ISEMPTY`](#st_isempty)  [`ST_ISRING`](#st_isring)  [`ST_NPOINTS`](#st_npoints)  [`ST_NUMGEOMETRIES`](#st_numgeometries)  [`ST_NUMPOINTS`](#st_numpoints)  [`ST_POINTN`](#st_pointn)  [`ST_STARTPOINT`](#st_startpoint)  [`ST_X`](#st_x)  [`ST_Y`](#st_y) | Functions that provide access to properties of a geography without side-effects. |
| Predicates | [`ST_CONTAINS`](#st_contains)  [`ST_COVEREDBY`](#st_coveredby)  [`ST_COVERS`](#st_covers)  [`ST_DISJOINT`](#st_disjoint)  [`ST_DWITHIN`](#st_dwithin)  [`ST_EQUALS`](#st_equals)  [`ST_HAUSDORFFDWITHIN`](#st_hausdorffdwithin)  [`ST_INTERSECTS`](#st_intersects)  [`ST_INTERSECTSBOX`](#st_intersectsbox)  [`ST_TOUCHES`](#st_touches)  [`ST_WITHIN`](#st_within) | Functions that return `TRUE` or `FALSE` for some spatial relationship between two geographies or some property of a geography. These functions are commonly used in filter clauses. |
| Measures | [`ST_ANGLE`](#st_angle)  [`ST_AREA`](#st_area)  [`ST_AZIMUTH`](#st_azimuth)  [`ST_BOUNDINGBOX`](#st_boundingbox)  [`ST_DISTANCE`](#st_distance)  [`ST_EXTENT`](#st_extent) (Aggregate)  [`ST_HAUSDORFFDISTANCE`](#st_hausdorffdistance)  [`ST_LINELOCATEPOINT`](#st_linelocatepoint)  [`ST_LENGTH`](#st_length)  [`ST_MAXDISTANCE`](#st_maxdistance)  [`ST_PERIMETER`](#st_perimeter) | Functions that compute measurements of one or more geographies. |
| Clustering | [`ST_CLUSTERDBSCAN`](#st_clusterdbscan) | Functions that perform clustering on geographies. |
| S2 functions | [`S2_CELLIDFROMPOINT`](#s2_cellidfrompoint)  [`S2_COVERINGCELLIDS`](#s2_coveringcellids) | Functions for working with S2 cell coverings of GEOGRAPHY. |
| Raster functions | [`ST_REGIONSTATS`](#st_regionstats) | Functions for analyzing geospatial rasters using geographies. |

## Function list

| Name | Summary |
| --- | --- |
| [`S2_CELLIDFROMPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#s2_cellidfrompoint) | Gets the S2 cell ID covering a point `GEOGRAPHY` value. |
| [`S2_COVERINGCELLIDS`](/bigquery/docs/reference/standard-sql/geography_functions#s2_coveringcellids) | Gets an array of S2 cell IDs that cover a `GEOGRAPHY` value. |
| [`ST_ANGLE`](/bigquery/docs/reference/standard-sql/geography_functions#st_angle) | Takes three point `GEOGRAPHY` values, which represent two intersecting lines, and returns the angle between these lines. |
| [`ST_AREA`](/bigquery/docs/reference/standard-sql/geography_functions#st_area) | Gets the area covered by the polygons in a `GEOGRAPHY` value. |
| [`ST_ASBINARY`](/bigquery/docs/reference/standard-sql/geography_functions#st_asbinary) | Converts a `GEOGRAPHY` value to a `BYTES` WKB geography value. |
| [`ST_ASGEOJSON`](/bigquery/docs/reference/standard-sql/geography_functions#st_asgeojson) | Converts a `GEOGRAPHY` value to a `STRING` GeoJSON geography value. |
| [`ST_ASTEXT`](/bigquery/docs/reference/standard-sql/geography_functions#st_astext) | Converts a `GEOGRAPHY` value to a `STRING` WKT geography value. |
| [`ST_AZIMUTH`](/bigquery/docs/reference/standard-sql/geography_functions#st_azimuth) | Gets the azimuth of a line segment formed by two point `GEOGRAPHY` values. |
| [`ST_BOUNDARY`](/bigquery/docs/reference/standard-sql/geography_functions#st_boundary) | Gets the union of component boundaries in a `GEOGRAPHY` value. |
| [`ST_BOUNDINGBOX`](/bigquery/docs/reference/standard-sql/geography_functions#st_boundingbox) | Gets the bounding box for a `GEOGRAPHY` value. |
| [`ST_BUFFER`](/bigquery/docs/reference/standard-sql/geography_functions#st_buffer) | Gets the buffer around a `GEOGRAPHY` value, using a specific number of segments. |
| [`ST_BUFFERWITHTOLERANCE`](/bigquery/docs/reference/standard-sql/geography_functions#st_bufferwithtolerance) | Gets the buffer around a `GEOGRAPHY` value, using tolerance. |
| [`ST_CENTROID`](/bigquery/docs/reference/standard-sql/geography_functions#st_centroid) | Gets the centroid of a `GEOGRAPHY` value. |
| [`ST_CENTROID_AGG`](/bigquery/docs/reference/standard-sql/geography_functions#st_centroid_agg) | Gets the centroid of a set of `GEOGRAPHY` values. |
| [`ST_CLOSESTPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_closestpoint) | Gets the point on a `GEOGRAPHY` value which is closest to any point in a second `GEOGRAPHY` value. |
| [`ST_CLUSTERDBSCAN`](/bigquery/docs/reference/standard-sql/geography_functions#st_clusterdbscan) | Performs DBSCAN clustering on a group of `GEOGRAPHY` values and produces a 0-based cluster number for this row. |
| [`ST_CONTAINS`](/bigquery/docs/reference/standard-sql/geography_functions#st_contains) | Checks if one `GEOGRAPHY` value contains another `GEOGRAPHY` value. |
| [`ST_CONVEXHULL`](/bigquery/docs/reference/standard-sql/geography_functions#st_convexhull) | Returns the convex hull for a `GEOGRAPHY` value. |
| [`ST_COVEREDBY`](/bigquery/docs/reference/standard-sql/geography_functions#st_coveredby) | Checks if all points of a `GEOGRAPHY` value are on the boundary or interior of another `GEOGRAPHY` value. |
| [`ST_COVERS`](/bigquery/docs/reference/standard-sql/geography_functions#st_covers) | Checks if all points of a `GEOGRAPHY` value are on the boundary or interior of another `GEOGRAPHY` value. |
| [`ST_DIFFERENCE`](/bigquery/docs/reference/standard-sql/geography_functions#st_difference) | Gets the point set difference between two `GEOGRAPHY` values. |
| [`ST_DIMENSION`](/bigquery/docs/reference/standard-sql/geography_functions#st_dimension) | Gets the dimension of the highest-dimensional element in a `GEOGRAPHY` value. |
| [`ST_DISJOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_disjoint) | Checks if two `GEOGRAPHY` values are disjoint (don't intersect). |
| [`ST_DISTANCE`](/bigquery/docs/reference/standard-sql/geography_functions#st_distance) | Gets the shortest distance in meters between two `GEOGRAPHY` values. |
| [`ST_DUMP`](/bigquery/docs/reference/standard-sql/geography_functions#st_dump) | Returns an array of simple `GEOGRAPHY` components in a `GEOGRAPHY` value. |
| [`ST_DWITHIN`](/bigquery/docs/reference/standard-sql/geography_functions#st_dwithin) | Checks if any points in two `GEOGRAPHY` values are within a given distance. |
| [`ST_ENDPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_endpoint) | Gets the last point of a linestring `GEOGRAPHY` value. |
| [`ST_EQUALS`](/bigquery/docs/reference/standard-sql/geography_functions#st_equals) | Checks if two `GEOGRAPHY` values represent the same `GEOGRAPHY` value. |
| [`ST_EXTENT`](/bigquery/docs/reference/standard-sql/geography_functions#st_extent) | Gets the bounding box for a group of `GEOGRAPHY` values. |
| [`ST_EXTERIORRING`](/bigquery/docs/reference/standard-sql/geography_functions#st_exteriorring) | Returns a linestring `GEOGRAPHY` value that corresponds to the outermost ring of a polygon `GEOGRAPHY` value. |
| [`ST_GEOGFROM`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogfrom) | Converts a `STRING` or `BYTES` value into a `GEOGRAPHY` value. |
| [`ST_GEOGFROMGEOJSON`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromgeojson) | Converts a `STRING` GeoJSON geometry value into a `GEOGRAPHY` value. |
| [`ST_GEOGFROMTEXT`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromtext) | Converts a `STRING` WKT geometry value into a `GEOGRAPHY` value. |
| [`ST_GEOGFROMWKB`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogfromwkb) | Converts a `BYTES` or hexadecimal-text `STRING` WKT geometry value into a `GEOGRAPHY` value. |
| [`ST_GEOGPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogpoint) | Creates a point `GEOGRAPHY` value for a given longitude and latitude. |
| [`ST_GEOGPOINTFROMGEOHASH`](/bigquery/docs/reference/standard-sql/geography_functions#st_geogpointfromgeohash) | Gets a point `GEOGRAPHY` value that's in the middle of a bounding box defined in a `STRING` GeoHash value. |
| [`ST_GEOHASH`](/bigquery/docs/reference/standard-sql/geography_functions#st_geohash) | Converts a point `GEOGRAPHY` value to a `STRING` GeoHash value. |
| [`ST_GEOMETRYTYPE`](/bigquery/docs/reference/standard-sql/geography_functions#st_geometrytype) | Gets the Open Geospatial Consortium (OGC) geometry type for a `GEOGRAPHY` value. |
| [`ST_HAUSDORFFDISTANCE`](/bigquery/docs/reference/standard-sql/geography_functions#st_hausdorffdistance) | Gets the discrete Hausdorff distance between two geometries. |
| [`ST_HAUSDORFFDWITHIN`](/bigquery/docs/reference/standard-sql/geography_functions#st_hausdorffdwithin) | Checks if the Hausdorff distance between two `GEOGRAPHY` values is within a given distance. |
| [`ST_INTERIORRINGS`](/bigquery/docs/reference/standard-sql/geography_functions#st_interiorrings) | Gets the interior rings of a polygon `GEOGRAPHY` value. |
| [`ST_INTERSECTION`](/bigquery/docs/reference/standard-sql/geography_functions#st_intersection) | Gets the point set intersection of two `GEOGRAPHY` values. |
| [`ST_INTERSECTS`](/bigquery/docs/reference/standard-sql/geography_functions#st_intersects) | Checks if at least one point appears in two `GEOGRAPHY` values. |
| [`ST_INTERSECTSBOX`](/bigquery/docs/reference/standard-sql/geography_functions#st_intersectsbox) | Checks if a `GEOGRAPHY` value intersects a rectangle. |
| [`ST_ISCLOSED`](/bigquery/docs/reference/standard-sql/geography_functions#st_isclosed) | Checks if all components in a `GEOGRAPHY` value are closed. |
| [`ST_ISCOLLECTION`](/bigquery/docs/reference/standard-sql/geography_functions#st_iscollection) | Checks if the total number of points, linestrings, and polygons is greater than one in a `GEOGRAPHY` value. |
| [`ST_ISEMPTY`](/bigquery/docs/reference/standard-sql/geography_functions#st_isempty) | Checks if a `GEOGRAPHY` value is empty. |
| [`ST_ISRING`](/bigquery/docs/reference/standard-sql/geography_functions#st_isring) | Checks if a `GEOGRAPHY` value is a closed, simple linestring. |
| [`ST_LENGTH`](/bigquery/docs/reference/standard-sql/geography_functions#st_length) | Gets the total length of lines in a `GEOGRAPHY` value. |
| [`ST_LINEINTERPOLATEPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_lineinterpolatepoint) | Gets a point at a specific fraction in a linestring `GEOGRAPHY` value. |
| [`ST_LINELOCATEPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_linelocatepoint) | Gets a section of a linestring `GEOGRAPHY` value between the start point and a point `GEOGRAPHY` value. |
| [`ST_LINESUBSTRING`](/bigquery/docs/reference/standard-sql/geography_functions#st_linesubstring) | Gets a segment of a single linestring at a specific starting and ending fraction. |
| [`ST_MAKELINE`](/bigquery/docs/reference/standard-sql/geography_functions#st_makeline) | Creates a linestring `GEOGRAPHY` value by concatenating the point and linestring vertices of `GEOGRAPHY` values. |
| [`ST_MAKEPOLYGON`](/bigquery/docs/reference/standard-sql/geography_functions#st_makepolygon) | Constructs a polygon `GEOGRAPHY` value by combining a polygon shell with polygon holes. |
| [`ST_MAKEPOLYGONORIENTED`](/bigquery/docs/reference/standard-sql/geography_functions#st_makepolygonoriented) | Constructs a polygon `GEOGRAPHY` value, using an array of linestring `GEOGRAPHY` values. The vertex ordering of each linestring determines the orientation of each polygon ring. |
| [`ST_MAXDISTANCE`](/bigquery/docs/reference/standard-sql/geography_functions#st_maxdistance) | Gets the longest distance between two non-empty `GEOGRAPHY` values. |
| [`ST_NPOINTS`](/bigquery/docs/reference/standard-sql/geography_functions#st_npoints) | An alias of `ST_NUMPOINTS`. |
| [`ST_NUMGEOMETRIES`](/bigquery/docs/reference/standard-sql/geography_functions#st_numgeometries) | Gets the number of geometries in a `GEOGRAPHY` value. |
| [`ST_NUMPOINTS`](/bigquery/docs/reference/standard-sql/geography_functions#st_numpoints) | Gets the number of vertices in the a `GEOGRAPHY` value. |
| [`ST_PERIMETER`](/bigquery/docs/reference/standard-sql/geography_functions#st_perimeter) | Gets the length of the boundary of the polygons in a `GEOGRAPHY` value. |
| [`ST_POINTN`](/bigquery/docs/reference/standard-sql/geography_functions#st_pointn) | Gets the point at a specific index of a linestring `GEOGRAPHY` value. |
| [`ST_REGIONSTATS`](/bigquery/docs/reference/standard-sql/geography_functions#st_regionstats) | Computes statistics describing the pixels in a geospatial raster image that intersect a `GEOGRAPHY` value. |
| [`ST_SIMPLIFY`](/bigquery/docs/reference/standard-sql/geography_functions#st_simplify) | Converts a `GEOGRAPHY` value into a simplified `GEOGRAPHY` value, using tolerance. |
| [`ST_SNAPTOGRID`](/bigquery/docs/reference/standard-sql/geography_functions#st_snaptogrid) | Produces a `GEOGRAPHY` value, where each vertex has been snapped to a longitude/latitude grid. |
| [`ST_STARTPOINT`](/bigquery/docs/reference/standard-sql/geography_functions#st_startpoint) | Gets the first point of a linestring `GEOGRAPHY` value. |
| [`ST_TOUCHES`](/bigquery/docs/reference/standard-sql/geography_functions#st_touches) | Checks if two `GEOGRAPHY` values intersect and their interiors have no elements in common. |
| [`ST_UNION`](/bigquery/docs/reference/standard-sql/geography_functions#st_union) | Gets the point set union of multiple `GEOGRAPHY` values. |
| [`ST_UNION_AGG`](/bigquery/docs/reference/standard-sql/geography_functions#st_union_agg) | Aggregates over `GEOGRAPHY` values and gets their point set union. |
| [`ST_WITHIN`](/bigquery/docs/reference/standard-sql/geography_functions#st_within) | Checks if one `GEOGRAPHY` value contains another `GEOGRAPHY` value. |
| [`ST_X`](/bigquery/docs/reference/standard-sql/geography_functions#st_x) | Gets the longitude from a point `GEOGRAPHY` value. |
| [`ST_Y`](/bigquery/docs/reference/standard-sql/geography_functions#st_y) | Gets the latitude from a point `GEOGRAPHY` value. |

## `S2_CELLIDFROMPOINT`

```
S2_CELLIDFROMPOINT(point_geography[, level => cell_level])
```

**Description**

Returns the [S2 cell ID](https://s2geometry.io/devguide/s2cell_hierarchy) covering a point `GEOGRAPHY`.

* The optional `INT64` parameter `level` specifies the S2 cell level for the
  returned cell. Naming this argument is optional.

This is advanced functionality for interoperability with systems utilizing the
[S2 Geometry Library](https://s2geometry.io/).

**Constraints**

* Returns the cell ID as a signed `INT64` bit-equivalent to
  [unsigned 64-bit integer representation](https://s2geometry.io/devguide/s2cell_hierarchy).
* Can return negative cell IDs.
* Valid S2 cell levels are 0 to 30.
* `level` defaults to 30 if not explicitly specified.
* The function only supports a single point GEOGRAPHY. Use the `SAFE` prefix if
  the input can be multipoint, linestring, polygon, or an empty `GEOGRAPHY`.
* To compute the covering of a complex `GEOGRAPHY`, use
  [S2\_COVERINGCELLIDS](#s2_coveringcellids).

**Return type**

`INT64`

**Example**

```
WITH data AS (
  SELECT 1 AS id, ST_GEOGPOINT(-122, 47) AS geo
  UNION ALL
  -- empty geography isn't supported
  SELECT 2 AS id, ST_GEOGFROMTEXT('POINT EMPTY') AS geo
  UNION ALL
  -- only points are supported
  SELECT 3 AS id, ST_GEOGFROMTEXT('LINESTRING(1 2, 3 4)') AS geo
)
SELECT id,
       SAFE.S2_CELLIDFROMPOINT(geo) cell30,
       SAFE.S2_CELLIDFROMPOINT(geo, level => 10) cell10
FROM data;

/*----+---------------------+---------------------+
 | id | cell30              | cell10              |
 +----+---------------------+---------------------+
 | 1  | 6093613931972369317 | 6093613287902019584 |
 | 2  | NULL                | NULL                |
 | 3  | NULL                | NULL                |
 +----+---------------------+---------------------*/
```

## `S2_COVERINGCELLIDS`

```
S2_COVERINGCELLIDS(
    geography
    [, min_level => cell_level]
    [, max_level => cell_level]
    [, max_cells => max_cells]
    [, buffer => buffer])
```

**Description**

Returns an array of [S2 cell IDs](https://s2geometry.io/devguide/s2cell_hierarchy) that cover the input
`GEOGRAPHY`. The function returns at most `max_cells` cells. The optional
arguments `min_level` and `max_level` specify minimum and maximum levels for
returned S2 cells. The array size is limited by the optional `max_cells`
argument. The optional `buffer` argument specifies a buffering factor in
meters; the region being covered is expanded from the extent of the
input geography by this amount.

This is advanced functionality for interoperability with systems utilizing the
[S2 Geometry Library](https://s2geometry.io/).

**Constraints**

* Returns the cell ID as a signed `INT64` bit-equivalent to
  [unsigned 64-bit integer representation](https://s2geometry.io/devguide/s2cell_hierarchy).
* Can return negative cell IDs.
* Valid S2 cell levels are 0 to 30.
* `max_cells` defaults to 8 if not explicitly specified.
* `buffer` should be nonnegative. It defaults to 0.0 meters if not explicitly
  specified.

**Return type**

`ARRAY<INT64>`

**Example**

```
WITH data AS (
  SELECT 1 AS id, ST_GEOGPOINT(-122, 47) AS geo
  UNION ALL
  SELECT 2 AS id, ST_GEOGFROMTEXT('POINT EMPTY') AS geo
  UNION ALL
  SELECT 3 AS id, ST_GEOGFROMTEXT('LINESTRING(-122.12 47.67, -122.19 47.69)') AS geo
)
SELECT id, S2_COVERINGCELLIDS(geo, min_level => 12) cells
FROM data;

/*----+--------------------------------------------------------------------------------------+
 | id | cells                                                                                |
 +----+--------------------------------------------------------------------------------------+
 | 1  | [6093613931972369317]                                                                |
 | 2  | []                                                                                   |
 | 3  | [6093384954555662336, 6093390709811838976, 6093390735581642752, 6093390740145045504, |
 |    |  6093390791416217600, 6093390812891054080, 6093390817187069952, 6093496378892222464] |
 +----+--------------------------------------------------------------------------------------*/
```

## `ST_ANGLE`

```
ST_ANGLE(point_geography_1, point_geography_2, point_geography_3)
```

**Description**

Takes three point `GEOGRAPHY` values, which represent two intersecting lines.
Returns the angle between these lines. Point 2 and point 1 represent the first
line and point 2 and point 3 represent the second line. The angle between
these lines is in radians, in the range `[0, 2pi)`. The angle is measured
clockwise from the first line to the second line.

`ST_ANGLE` has the following edge cases:

* If points 2 and 3 are the same, returns `NULL`.
* If points 2 and 1 are the same, returns `NULL`.
* If points 2 and 3 are exactly antipodal, returns `NULL`.
* If points 2 and 1 are exactly antipodal, returns `NULL`.
* If any of the input geographies aren't single points or are the empty
  geography, then throws an error.

**Return type**

`FLOAT64`

**Example**

```
WITH geos AS (
  SELECT 1 id, ST_GEOGPOINT(1, 0) geo1, ST_GEOGPOINT(0, 0) geo2, ST_GEOGPOINT(0, 1) geo3 UNION ALL
  SELECT 2 id, ST_GEOGPOINT(0, 0), ST_GEOGPOINT(1, 0), ST_GEOGPOINT(0, 1) UNION ALL
  SELECT 3 id, ST_GEOGPOINT(1, 0), ST_GEOGPOINT(0, 0), ST_GEOGPOINT(1, 0) UNION ALL
  SELECT 4 id, ST_GEOGPOINT(1, 0) geo1, ST_GEOGPOINT(0, 0) geo2, ST_GEOGPOINT(0, 0) geo3 UNION ALL
  SELECT 5 id, ST_GEOGPOINT(0, 0), ST_GEOGPOINT(-30, 0), ST_GEOGPOINT(150, 0) UNION ALL
  SELECT 6 id, ST_GEOGPOINT(0, 0), NULL, NULL UNION ALL
  SELECT 7 id, NULL, ST_GEOGPOINT(0, 0), NULL UNION ALL
  SELECT 8 id, NULL, NULL, ST_GEOGPOINT(0, 0))
SELECT ST_ANGLE(geo1,geo2,geo3) AS angle FROM geos ORDER BY id;

/*---------------------+
 | angle               |
 +---------------------+
 | 4.71238898038469    |
 | 0.78547432161873854 |
 | 0                   |
 | NULL                |
 | NULL                |
 | NULL                |
 | NULL                |
 | NULL                |
 +---------------------*/
```

## `ST_AREA`

```
ST_AREA(geography_expression[, use_spheroid])
```

**Description**

Returns the area in square meters covered by the polygons in the input
`GEOGRAPHY`.

If `geography_expression` is a point or a line, returns zero. If
`geography_expression` is a collection, returns the area of the polygons in the
collection; if the collection doesn't contain polygons, returns zero.

The optional `use_spheroid` parameter determines how this function measures
distance. If `use_spheroid` is `FALSE`, the function measures distance on the
surface of a perfect sphere.

The `use_spheroid` parameter currently only supports
the value `FALSE`. The default value of `use_spheroid` is `FALSE`.

**Return type**

`FLOAT64`

## `ST_ASBINARY`

```
ST_ASBINARY(geography_expression)
```

**Description**

Returns the [WKB](https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary) representation of an input
`GEOGRAPHY`.

See [`ST_GEOGFROMWKB`](#st_geogfromwkb) to construct a
`GEOGRAPHY` from WKB.

**Return type**

`BYTES`

## `ST_ASGEOJSON`

```
ST_ASGEOJSON(geography_expression)
```

**Description**

Returns the [RFC 7946](https://tools.ietf.org/html/rfc7946) compliant [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON)
representation of the input `GEOGRAPHY`.

A GoogleSQL `GEOGRAPHY` has spherical
geodesic edges, whereas a GeoJSON `Geometry` object explicitly has planar edges.
To convert between these two types of edges, GoogleSQL adds additional
points to the line where necessary so that the resulting sequence of edges
remains within 10 meters of the original edge.

See [`ST_GEOGFROMGEOJSON`](#st_geogfromgeojson) to construct a
`GEOGRAPHY` from GeoJSON.

**Return type**

`STRING`

## `ST_ASTEXT`

```
ST_ASTEXT(geography_expression)
```

**Description**

Returns the [WKT](https://en.wikipedia.org/wiki/Well-known_text) representation of an input
`GEOGRAPHY`.

See [`ST_GEOGFROMTEXT`](#st_geogfromtext) to construct a
`GEOGRAPHY` from WKT.

**Return type**

`STRING`

## `ST_AZIMUTH`