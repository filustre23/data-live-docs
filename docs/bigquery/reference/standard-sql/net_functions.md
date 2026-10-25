* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Net functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following Net functions.

## Function list

| Name | Summary |
| --- | --- |
| [`NET.HOST`](/bigquery/docs/reference/standard-sql/net_functions#nethost) | Gets the hostname from a URL. |
| [`NET.IP_FROM_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netip_from_string) | Converts an IPv4 or IPv6 address from a `STRING` value to a `BYTES` value in network byte order. |
| [`NET.IP_NET_MASK`](/bigquery/docs/reference/standard-sql/net_functions#netip_net_mask) | Gets a network mask. |
| [`NET.IP_TO_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netip_to_string) | Converts an IPv4 or IPv6 address from a `BYTES` value in network byte order to a `STRING` value. |
| [`NET.IP_TRUNC`](/bigquery/docs/reference/standard-sql/net_functions#netip_trunc) | Converts a `BYTES` IPv4 or IPv6 address in network byte order to a `BYTES` subnet address. |
| [`NET.IPV4_FROM_INT64`](/bigquery/docs/reference/standard-sql/net_functions#netipv4_from_int64) | Converts an IPv4 address from an `INT64` value to a `BYTES` value in network byte order. |
| [`NET.IPV4_TO_INT64`](/bigquery/docs/reference/standard-sql/net_functions#netipv4_to_int64) | Converts an IPv4 address from a `BYTES` value in network byte order to an `INT64` value. |
| [`NET.PUBLIC_SUFFIX`](/bigquery/docs/reference/standard-sql/net_functions#netpublic_suffix) | Gets the public suffix from a URL. |
| [`NET.REG_DOMAIN`](/bigquery/docs/reference/standard-sql/net_functions#netreg_domain) | Gets the registered or registrable domain from a URL. |
| [`NET.SAFE_IP_FROM_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netsafe_ip_from_string) | Similar to the `NET.IP_FROM_STRING`, but returns `NULL` instead of producing an error if the input is invalid. |

## `NET.HOST`

```
NET.HOST(url)
```

**Description**

Takes a URL as a `STRING` value and returns the host. For best results, URL
values should comply with the format as defined by
[RFC 3986](https://tools.ietf.org/html/rfc3986#appendix-A). If the URL value doesn't comply
with RFC 3986 formatting, this function makes a best effort to parse the input
and return a relevant result. If the function can't parse the input, it
returns `NULL`.

**Note:** The function doesn't perform any normalization.

**Return Data Type**

`STRING`

**Example**

```
SELECT
  FORMAT("%T", input) AS input,
  description,
  FORMAT("%T", NET.HOST(input)) AS host,
  FORMAT("%T", NET.PUBLIC_SUFFIX(input)) AS suffix,
  FORMAT("%T", NET.REG_DOMAIN(input)) AS domain
FROM (
  SELECT "" AS input, "invalid input" AS description
  UNION ALL SELECT "http://abc.xyz", "standard URL"
  UNION ALL SELECT "//user:password@a.b:80/path?query",
                   "standard URL with relative scheme, port, path and query, but no public suffix"
  UNION ALL SELECT "https://[::1]:80", "standard URL with IPv6 host"
  UNION ALL SELECT "http://例子.卷筒纸.中国", "standard URL with internationalized domain name"
  UNION ALL SELECT "    www.Example.Co.UK    ",
                   "non-standard URL with spaces, upper case letters, and without scheme"
  UNION ALL SELECT "mailto:?to=&subject=&body=", "URI rather than URL--unsupported"
);
```

| input | description | host | suffix | domain |
| --- | --- | --- | --- | --- |
| "" | invalid input | NULL | NULL | NULL |
| "http://abc.xyz" | standard URL | "abc.xyz" | "xyz" | "abc.xyz" |
| "//user:password@a.b:80/path?query" | standard URL with relative scheme, port, path and query, but no public suffix | "a.b" | NULL | NULL |
| "https://[::1]:80" | standard URL with IPv6 host | "[::1]" | NULL | NULL |
| "http://例子.卷筒纸.中国" | standard URL with internationalized domain name | "例子.卷筒纸.中国" | "中国" | "卷筒纸.中国" |
| "    www.Example.Co.UK    " | non-standard URL with spaces, upper case letters, and without scheme | "www.Example.Co.UK" | "Co.UK" | "Example.Co.UK" |
| "mailto:?to=&subject=&body=" | URI rather than URL--unsupported | "mailto" | NULL | NULL |

## `NET.IP_FROM_STRING`

```
NET.IP_FROM_STRING(addr_str)
```

**Description**

Converts an IPv4 or IPv6 address from text (STRING) format to binary (BYTES)
format in network byte order.

This function supports the following formats for `addr_str`:

* IPv4: Dotted-quad format. For example, `10.1.2.3`.
* IPv6: Colon-separated format. For example,
  `1234:5678:90ab:cdef:1234:5678:90ab:cdef`. For more examples, see the
  [IP Version 6 Addressing Architecture](http://www.ietf.org/rfc/rfc2373.txt).

This function doesn't support [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing), such as `10.1.2.3/32`.

If this function receives a `NULL` input, it returns `NULL`. If the input is
considered invalid, an `OUT_OF_RANGE` error occurs.

**Return Data Type**

BYTES

**Example**

```
SELECT
  addr_str, FORMAT("%T", NET.IP_FROM_STRING(addr_str)) AS ip_from_string
FROM UNNEST([
  '48.49.50.51',
  '::1',
  '3031:3233:3435:3637:3839:4041:4243:4445',
  '::ffff:192.0.2.128'
]) AS addr_str;

/*---------------------------------------------------------------------------------------------------------------+
 | addr_str                                | ip_from_string                                                      |
 +---------------------------------------------------------------------------------------------------------------+
 | 48.49.50.51                             | b"0123"                                                             |
 | ::1                                     | b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01" |
 | 3031:3233:3435:3637:3839:4041:4243:4445 | b"0123456789@ABCDE"                                                 |
 | ::ffff:192.0.2.128                      | b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xc0\x00\x02\x80" |
 +---------------------------------------------------------------------------------------------------------------*/
```

## `NET.IP_NET_MASK`

```
NET.IP_NET_MASK(num_output_bytes, prefix_length)
```

**Description**

Returns a network mask: a byte sequence with length equal to `num_output_bytes`,
where the first `prefix_length` bits are set to 1 and the other bits are set to
0. `num_output_bytes` and `prefix_length` are INT64.
This function throws an error if `num_output_bytes` isn't 4 (for IPv4) or 16
(for IPv6). It also throws an error if `prefix_length` is negative or greater
than `8 * num_output_bytes`.

**Return Data Type**

BYTES

**Example**

```
SELECT x, y, FORMAT("%T", NET.IP_NET_MASK(x, y)) AS ip_net_mask
FROM UNNEST([
  STRUCT(4 as x, 0 as y),
  (4, 20),
  (4, 32),
  (16, 0),
  (16, 1),
  (16, 128)
]);

/*--------------------------------------------------------------------------------+
 | x  | y   | ip_net_mask                                                         |
 +--------------------------------------------------------------------------------+
 | 4  | 0   | b"\x00\x00\x00\x00"                                                 |
 | 4  | 20  | b"\xff\xff\xf0\x00"                                                 |
 | 4  | 32  | b"\xff\xff\xff\xff"                                                 |
 | 16 | 0   | b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" |
 | 16 | 1   | b"\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" |
 | 16 | 128 | b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff" |
 +--------------------------------------------------------------------------------*/
```

## `NET.IP_TO_STRING`

```
NET.IP_TO_STRING(addr_bin)
```

**Description**
Converts an IPv4 or IPv6 address from binary (BYTES) format in network byte
order to text (STRING) format.

If the input is 4 bytes, this function returns an IPv4 address as a STRING. If
the input is 16 bytes, it returns an IPv6 address as a STRING.

If this function receives a `NULL` input, it returns `NULL`. If the input has
a length different from 4 or 16, an `OUT_OF_RANGE` error occurs.

**Return Data Type**

STRING

**Example**

```
SELECT FORMAT("%T", x) AS addr_bin, NET.IP_TO_STRING(x) AS ip_to_string
FROM UNNEST([
  b"0123",
  b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01",
  b"0123456789@ABCDE",
  b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xc0\x00\x02\x80"
]) AS x;

/*---------------------------------------------------------------------------------------------------------------+
 | addr_bin                                                            | ip_to_string                            |
 +---------------------------------------------------------------------------------------------------------------+
 | b"0123"                                                             | 48.49.50.51                             |
 | b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01" | ::1                                     |
 | b"0123456789@ABCDE"                                                 | 3031:3233:3435:3637:3839:4041:4243:4445 |
 | b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xc0\x00\x02\x80" | ::ffff:192.0.2.128                      |
 +---------------------------------------------------------------------------------------------------------------*/
```

## `NET.IP_TRUNC`

```
NET.IP_TRUNC(addr_bin, prefix_length)
```

**Description**
Takes `addr_bin`, an IPv4 or IPv6 address in binary (BYTES) format in network
byte order, and returns a subnet address in the same format. The result has the
same length as `addr_bin`, where the first `prefix_length` bits are equal to
those in `addr_bin` and the remaining bits are 0.

This function throws an error if `LENGTH(addr_bin)` isn't 4 or 16, or if
`prefix_len` is negative or greater than `LENGTH(addr_bin) * 8`.

**Return Data Type**

BYTES

**Example**

```
SELECT
  FORMAT("%T", x) as addr_bin, prefix_length,
  FORMAT("%T", NET.IP_TRUNC(x, prefix_length)) AS ip_trunc
FROM UNNEST([
  STRUCT(b"\xAA\xBB\xCC\xDD" as x, 0 as prefix_length),
  (b"\xAA\xBB\xCC\xDD", 11), (b"\xAA\xBB\xCC\xDD", 12),
  (b"\xAA\xBB\xCC\xDD", 24), (b"\xAA\xBB\xCC\xDD", 32),
  (b'0123456789@ABCDE', 80)
]);

/*--------------------------------------------------------
```