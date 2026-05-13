* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# AEAD encryption functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following AEAD encryption functions.
For a description of how the AEAD encryption
functions work, see [AEAD encryption concepts](/bigquery/docs/aead-encryption-concepts).

## Function list

| Name | Summary |
| --- | --- |
| [`AEAD.DECRYPT_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeaddecrypt_bytes) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext. |
| [`AEAD.DECRYPT_STRING`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeaddecrypt_string) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext into a `STRING` plaintext. |
| [`AEAD.ENCRYPT`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeadencrypt) | Encrypts `STRING` plaintext, using the primary cryptographic key in a keyset. |
| [`DETERMINISTIC_DECRYPT_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_decrypt_bytes) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext, using deterministic AEAD. |
| [`DETERMINISTIC_DECRYPT_STRING`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_decrypt_string) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext into a `STRING` plaintext, using deterministic AEAD. |
| [`DETERMINISTIC_ENCRYPT`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_encrypt) | Encrypts `STRING` plaintext, using the primary cryptographic key in a keyset, using deterministic AEAD encryption. |
| [`KEYS.ADD_KEY_FROM_RAW_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysadd_key_from_raw_bytes) | Adds a key to a keyset, and return the new keyset as a serialized `BYTES` value. |
| [`KEYS.KEYSET_CHAIN`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_chain) | Produces a Tink keyset that's encrypted with a Cloud KMS key. |
| [`KEYS.KEYSET_FROM_JSON`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_from_json) | Converts a `STRING` JSON keyset to a serialized `BYTES` value. |
| [`KEYS.KEYSET_LENGTH`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_length) | Gets the number of keys in the provided keyset. |
| [`KEYS.KEYSET_TO_JSON`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_to_json) | Gets a JSON `STRING` representation of a keyset. |
| [`KEYS.NEW_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysnew_keyset) | Gets a serialized keyset containing a new key based on the key type. |
| [`KEYS.NEW_WRAPPED_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysnew_wrapped_keyset) | Creates a new keyset and encrypts it with a Cloud KMS key. |
| [`KEYS.REWRAP_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrewrap_keyset) | Re-encrypts a wrapped keyset with a new Cloud KMS key. |
| [`KEYS.ROTATE_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrotate_keyset) | Adds a new primary cryptographic key to a keyset, based on the key type. |
| [`KEYS.ROTATE_WRAPPED_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrotate_wrapped_keyset) | Rewraps a keyset and rotates it. |

## `AEAD.DECRYPT_BYTES`

```
AEAD.DECRYPT_BYTES(keyset, ciphertext, additional_data)
```

**Description**

Uses the matching key from `keyset` to decrypt `ciphertext` and verifies the
integrity of the data using `additional_data`. Returns an error if decryption or
verification fails.

`keyset` is a serialized `BYTES` value returned by one of the
`KEYS` functions or a `STRUCT` returned by
`KEYS.KEYSET_CHAIN`. `keyset` must contain the key that was used to
encrypt `ciphertext`, and the key must be in an `'ENABLED'` state, or else the
function returns an error. `AEAD.DECRYPT_BYTES` identifies the matching key
in `keyset` by finding the key with the key ID that matches the one encrypted in
`ciphertext`.

`ciphertext` is a `BYTES` value that's the result of
a call to `AEAD.ENCRYPT` where the input `plaintext` was of type
`BYTES`.

If `ciphertext` includes an initialization vector (IV),
it should be the first bytes of `ciphertext`. If `ciphertext` includes an
authentication tag, it should be the last bytes of `ciphertext`. If the
IV and authentic tag are one (SIV), it should be the first bytes of
`ciphertext`. The IV and authentication tag commonly require 16 bytes, but may
vary in size.

`additional_data` is a `STRING` or `BYTES` value that binds the ciphertext to
its context. This forces the ciphertext to be decrypted in the same context in
which it was encrypted. This function casts any
`STRING` value to `BYTES`.
This must be the same as the `additional_data` provided to `AEAD.ENCRYPT` to
encrypt `ciphertext`, ignoring its type, or else the function returns an error.

**Return Data Type**

`BYTES`

**Example**

This example creates a table of unique IDs with associated plaintext values and
keysets. Then it uses these keysets to encrypt the plaintext values as
`BYTES` and store them in a new table. Finally, it
uses `AEAD.DECRYPT_BYTES` to decrypt the encrypted values and display them as
plaintext.

The following statement creates a table `CustomerKeysets` containing a column of
unique IDs, a column of `AEAD_AES_GCM_256` keysets, and a column of favorite
animals.

```
CREATE TABLE aead.CustomerKeysets AS
SELECT
  1 AS customer_id,
  KEYS.NEW_KEYSET('AEAD_AES_GCM_256') AS keyset,
  b'jaguar' AS favorite_animal
UNION ALL
SELECT
  2 AS customer_id,
  KEYS.NEW_KEYSET('AEAD_AES_GCM_256') AS keyset,
  b'zebra' AS favorite_animal
UNION ALL
SELECT
  3 AS customer_id,
  KEYS.NEW_KEYSET('AEAD_AES_GCM_256') AS keyset,
  b'nautilus' AS favorite_animal;
```

The following statement creates a table `EncryptedCustomerData` containing a
column of unique IDs and a column of ciphertext. The statement encrypts the
plaintext `favorite_animal` using the keyset value from `CustomerKeysets`
corresponding to each unique ID.

```
CREATE TABLE aead.EncryptedCustomerData AS
SELECT
  customer_id,
  AEAD.ENCRYPT(keyset, favorite_animal, CAST(CAST(customer_id AS STRING) AS BYTES))
   AS encrypted_animal
FROM
  aead.CustomerKeysets AS ck;
```

The following query uses the keysets in the `CustomerKeysets` table to decrypt
data in the `EncryptedCustomerData` table.

```
SELECT
  ecd.customer_id,
  AEAD.DECRYPT_BYTES(
    (SELECT ck.keyset
     FROM aead.CustomerKeysets AS ck
     WHERE ecd.customer_id = ck.customer_id),
    ecd.encrypted_animal,
    CAST(CAST(customer_id AS STRING) AS BYTES)
  ) AS favorite_animal
FROM aead.EncryptedCustomerData AS ecd;
```

## `AEAD.DECRYPT_STRING`

```
AEAD.DECRYPT_STRING(keyset, ciphertext, additional_data)
```

**Description**

Like [`AEAD.DECRYPT_BYTES`](#aeaddecrypt_bytes), but where `additional_data` is
of type `STRING`.

**Return Data Type**

`STRING`

## `AEAD.ENCRYPT`

```
AEAD.ENCRYPT(keyset, plaintext, additional_data)
```

**Description**

Encrypts `plaintext` using the primary cryptographic key in `keyset`. The
algorithm of the primary key must be `AEAD_AES_GCM_256`. Binds the ciphertext to
the context defined by `additional_data`. Returns `NULL` if any input is `NULL`.

`keyset` is a serialized `BYTES` value returned by one of the
`KEYS` functions or a `STRUCT` returned by
`KEYS.KEYSET_CHAIN`.

`plaintext` is the `STRING` or
`BYTES` value to be encrypted.

`additional_data` is a `STRING` or `BYTES` value that binds the ciphertext to
its context. This forces the ciphertext to be decrypted in the same context in
which it was encrypted. `plaintext` and `additional_data` must be of the same
type. `AEAD.ENCRYPT(keyset, string1, string2)` is equivalent to
`AEAD.ENCRYPT(keyset, CAST(string1 AS BYTES), CAST(string2 AS BYTES))`.

The output is ciphertext `BYTES`. The ciphertext contains a
[Tink-specific](https://github.com/google/tink/blob/master/docs/KEY-MANAGEMENT.md) prefix indicating the key used to perform the encryption.

**Return Data Type**

`BYTES`

**Example**

The following query uses the keysets for each `customer_id` in the
`CustomerKeysets` table to encrypt the value of the plaintext `favorite_animal`
in the `PlaintextCustomerData` table corresponding to that `customer_id`. The
output contains a column of `customer_id` values and a column of
corresponding ciphertext output as `BYTES`.

```
WITH CustomerKeysets AS (
  SELECT 1 AS customer_id, KEYS.NEW_KEYSET('AEAD_AES_GCM_256') AS keyset UNION ALL
  SELECT 2, KEYS.NEW_KEYSET('AEAD_AES_GCM_256') UNION ALL
  SELECT 3, KEYS.NEW_KEYSET('AEAD_AES_GCM_256')
), PlaintextCustomerData AS (
  SELECT 1 AS customer_id, 'elephant' AS favorite_animal UNION ALL
  SELECT 2, 'walrus' UNION ALL
  SELECT 3, 'leopard'
)
SELECT
  pcd.customer_id,
  AEAD.ENCRYPT(
    (SELECT keyset
     FROM CustomerKeysets AS ck
     WHERE ck.customer_id = pcd.customer_id),
    pcd.favorite_animal,
    CAST(pcd.customer_id AS STRING)
  ) AS encrypted_animal
FROM PlaintextCustomerData AS pcd;
```

## `DETERMINISTIC_DECRYPT_BYTES`

```
DETERMINISTIC_DECRYPT_BYTES(keyset, ciphertext, additional_data)
```

**Description**

Uses the matching key from `keyset` to decrypt `ciphertext` and verifies the
integrity of the data using `additional_data`. Returns an error if decryption
fails.

`keyset` is a serialized `BYTES` value or a `STRUCT`
value returned by one of the `KEYS` functions. `keyset` must contain
the key that was used to encrypt `ciphertext`, the key must be in an `'ENABLED'`
state, and the key must be of type `DETERMINISTIC_AEAD_AES_SIV_CMAC_256`, or
else the function returns an error. `DETERMINISTIC_DECRYPT_BYTES` identifies the
matching key in `keyset` by finding the key with the key ID that matches the one
encrypted in `ciphertext`.

`ciphertext` is a `BYTES` value that's the result of a call to
`DETERMINISTIC_ENCRYPT` where the input `plaintext` was of type `BYTES`.

The ciphertext must follow Tink's [wire format](https://developers.google.com/tink/wire-format#deterministic_aead). The first
byte of `ciphertext` should contain a Tink key version followed by a 4 byte key
hint. If `ciphertext` includes an initialization vector (IV), it should be the
next bytes of `ciphertext`. If `ciphertext` includes an authentication tag, it
should be the last bytes of `ciphertext`. If the IV and authentic tag are one
(SIV), it should be the first bytes of `ciphertext`. The IV and authentication
tag commonly require 16 bytes, but may vary in size.

`additional_data` is a `STRING` or `BYTES` value that binds the ciphertext to
its context. This forces the ciphertext to be decrypted in the same context in
which it was encrypted. This function casts any `STRING` value to `BYTES`. This
must be the same as the `additional_data` provided to `DETERMINISTIC_ENCRYPT` to
encrypt `ciphertext`, ignoring its type, or else the function returns an error.

**Return Data Type**

`BYTES`

**Example**

This example creates a table of unique IDs with associated plaintext values and
keysets. Then it uses these keysets to encrypt the plaintext values as `BYTES`
and store them in a new table. Finally, it uses `DETERMINISTIC_DECRYPT_BYTES` to
decrypt the encrypted values and display them as plaintext.

The following statement creates a table `CustomerKeysets` containing a column of
unique IDs, a column of `DETERMINISTIC_AEAD_AES_SIV_CMAC_256` keysets, and a
column of favorite animals.

```
CREATE TABLE deterministic.CustomerKeysets AS
SELECT
  1 AS customer_id,
  KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') AS keyset,
  b'jaguar' AS favorite_animal
UNION ALL
SELECT
  2 AS customer_id,
  KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') AS keyset,
  b'zebra' AS favorite_animal
UNION ALL
SELECT
  3 AS customer_id,
  KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') AS keyset,
  b'nautilus' AS favorite_animal;
```

The following statement creates a table `EncryptedCustomerData` containing a
column of unique IDs and a column of ciphertext. The statement encrypts the
plaintext `favorite_animal` using the keyset value from `CustomerKeysets`
corresponding to each unique ID.

```
CREATE TABLE deterministic.EncryptedCustomerData AS
SELECT
  customer_id,
  DETERMINISTIC_ENCRYPT(ck.keyset, favorite_animal, CAST(CAST(customer_id AS STRING) AS BYTES))
   AS encrypted_animal
FROM
  deterministic.CustomerKeysets AS ck;
```

The following query uses the keysets in the `CustomerKeysets` table to decrypt
data in the `EncryptedCustomerData` table.

```
SELECT
  ecd.customer_id,
  DETERMINISTIC_DECRYPT_BYTES(
    (SELECT ck.keyset
     FROM deterministic.CustomerKeysets AS ck
     WHERE ecd.customer_id = ck.customer_id),
    ecd.encrypted_animal,
    CAST(CAST(ecd.customer_id AS STRING) AS BYTES)
  ) AS favorite_animal
FROM deterministic.EncryptedCustomerData AS ecd;
```

## `DETERMINISTIC_DECRYPT_STRING`

```
DETERMINISTIC_DECRYPT_STRING(keyset, ciphertext, additional_data)
```

**Description**

Like [`DETERMINISTIC_DECRYPT_BYTES`](#deterministic_decrypt_bytes), but where
`plaintext` is of type `STRING`.

**Return Data Type**

`STRING`

## `DETERMINISTIC_ENCRYPT`

```
DETERMINISTIC_ENCRYPT(keyset, plaintext, additional_data)
```

**Description**

Encrypts `plaintext` using the primary cryptographic key in `keyset` using
[deterministic AEAD](https://developers.google.com/tink/deterministic-aead). The algorithm of the primary key must
be `DETERMINISTIC_AEAD_AES_SIV_CMAC_256`. Binds the ciphertext to the context
defined by `additional_data`. Returns `NULL` if any input is `NULL`.

`keyset` is a serialized `BYTES` value or a `STRUCT`
value returned by one of the `KEYS` functions.

`plaintext` is the `STRING` or `BYTES` value to be encrypted.

`additional_data` is a `STRING` or `BYTES` value that binds the ciphertext to
its context. This forces the ciphertext to be decrypted in the same context in
which it was encrypted. `plaintext` and `additional_data` must be of the same
type. `DETERMINISTIC_ENCRYPT(keyset, string1, string2)` is equivalent to
`DETERMINISTIC_ENCRYPT(keyset, CAST(string1 AS BYTES), CAST(string2 AS BYTES))`.

The output is ciphertext `BYTES`. The ciphertext contains a
[Tink-specific](https://github.com/google/tink/blob/master/docs/KEY-MANAGEMENT.md) prefix indicating the key used to perform the encryption.
Given an identical `keyset` and `plaintext`, this function returns the same
ciphertext each time it's invoked (including across queries).

**Return Data Type**

`BYTES`

**Example**

The following query uses the keysets for each `customer_id` in the
`CustomerKeysets` table to encrypt the value of the plaintext `favorite_animal`
in the `PlaintextCustomerData` table corresponding to that `customer_id`. The
output contains a column of `customer_id` values and a column of corresponding
ciphertext output as `BYTES`.

```
WITH CustomerKeysets AS (
  SELECT 1 AS customer_id,
  KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') AS keyset UNION ALL
  SELECT 2, KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') UNION ALL
  SELECT 3, KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256')
), PlaintextCustomerData AS (
  SELECT 1 AS customer_id, 'elephant' AS favorite_animal UNION ALL
  SELECT 2, 'walrus' UNION ALL
  SELECT 3, 'leopard'
)
SELECT
  pcd.customer_id,
  DETERMINISTIC_ENCRYPT(
    (SELECT keyset
     FROM CustomerKeysets AS ck
     WHERE ck.customer_id = pcd.customer_id),
    pcd.favorite_animal,
    CAST(pcd.customer_id AS STRING)
  ) AS encrypted_animal
FROM PlaintextCustomerData AS pcd;
```

## `KEYS.ADD_KEY_FROM_RAW_BYTES`

```
KEYS.ADD_KEY_FROM_RAW_BYTES(keyset, key_type, raw_key_bytes)
```

**Description**

Returns a serialized keyset as `BYTES` with the
addition of a key to `keyset` based on `key_type` and `raw_key_bytes`.

The primary cryptographic key remains the same as in `keyset`. The expected
length of `raw_key_bytes` depends on the value of `key_type`. The following are
supported `key_types`:

* `'AES_CBC_PKCS'`: Creates a key for AES decryption using cipher block chaining
  and PKCS padding. `raw_key_bytes` is expected to be a raw key
  `BYTES` value of length 16, 24, or 32; these
  lengths have sizes of 128, 192, and 256 bits, respectively. GoogleSQL
  AEAD functions don't support keys of these types for encryption; instead,
  prefer `'AEAD_AES_GCM_256'` or `'AES_GCM'` keys.
* `'AES_GCM'`: Creates a key for AES decryption or encryption using
  [Galois/Counter Mode](https://en.wikipedia.org/wiki/Galois/Counter_Mode).
  `raw_key_bytes` must be a raw key `BYTES`
  value of length 16 or 32; these lengths have sizes of 128 and 256 bits,
  respectively. When keys of this type are inputs to `AEAD.ENCRYPT`, the output
  ciphertext doesn't have a Tink-specific prefix indicating which key was
  used as input.

**Return Data Type**

`BYTES`

**Example**

The following query creates a table of customer IDs along with raw key bytes,
called `CustomerRawKeys`, and a table of unique IDs, called `CustomerIds`. It
creates a new `'AEAD_AES_GCM_256'` keyset for each `customer_id`; then it adds a
new key to each keyset, using the `raw_key_bytes` value corresponding to that
`customer_id`. The output is a table where each row contains a `customer_id` and
a keyset in `BYTES`, which contains the raw key added
using KEYS.ADD\_KEY\_FROM\_RAW\_BYTES.

```
WITH CustomerRawKeys AS (
  SELECT 1 AS customer_id, b'0123456789012345' AS raw_key_bytes UNION ALL
  SELECT 2, b'9876543210543210' UNION ALL
  SELECT 3, b'0123012301230123'
), CustomerIds AS (
  SELECT 1 AS customer_id UNION ALL
  SELECT 2 UNION ALL
  SELECT 3
)
SELECT
  ci.customer_id,
  KEYS.ADD_KEY_FROM_RAW_BYTES(
    KEYS.NEW_KEYSET('AEAD_AES_GCM_256'),
    'AES_CBC_PKCS',
    (SELECT raw_key_bytes FROM CustomerRawKeys AS crk
     WHERE crk.customer_id = ci.customer_id)
  ) AS keyset
FROM CustomerIds AS ci;
```