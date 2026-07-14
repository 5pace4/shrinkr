# CQLSH Command Guide

This file is a practical `cqlsh` reference for monitoring and querying Cassandra from the terminal.

Project context:

- Cassandra host: `127.0.0.1`
- Cassandra port: `9043`
- Keyspace used by the app: `shrinkr`

## Connect

```bash
cqlsh 127.0.0.1 9043
```

Connect with credentials if authentication is enabled:

```bash
cqlsh 127.0.0.1 9043 -u cassandra -p cassandra
```

Connect directly to the project keyspace:

```bash
cqlsh 127.0.0.1 9043 shrinkr
```

Show help:

```bash
cqlsh --help
```

## Shell Basics

```sql
HELP;
EXIT;
QUIT;
```

Show the current consistency level:

```sql
CONSISTENCY;
```

Set a consistency level:

```sql
CONSISTENCY ONE;
CONSISTENCY QUORUM;
CONSISTENCY LOCAL_ONE;
```

Clear the screen:

```sql
CLEAR;
```

## Schema Commands

List keyspaces:

```sql
DESCRIBE KEYSPACES;
```

Show the current keyspace:

```sql
DESCRIBE KEYSPACE;
```

Use a keyspace:

```sql
USE shrinkr;
```

List tables:

```sql
DESCRIBE TABLES;
```

Show table definition:

```sql
DESCRIBE TABLE users;
DESCRIBE TABLE urls;
```

Show system metadata:

```sql
SELECT * FROM system_schema.keyspaces;
SELECT * FROM system_schema.tables;
SELECT * FROM system_schema.columns;
```

## Common Table Design Examples

Users table example:

```sql
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY,
  username text,
  email text,
  created_at timestamp
);
```

URLs table example:

```sql
CREATE TABLE IF NOT EXISTS urls (
  id uuid PRIMARY KEY,
  original_url text,
  shortened_url text,
  created_at timestamp,
  expiration_date timestamp,
  click_count int
);
```

## Insert Data

Insert a user:

```sql
INSERT INTO users (id, username, email, created_at)
VALUES (uuid(), 'user1', 'user1@test.com', toTimestamp(now()));
```

Insert a URL:

```sql
INSERT INTO urls (id, original_url, shortened_url, created_at, expiration_date, click_count)
VALUES (uuid(), 'https://example.com', 'exmpl', toTimestamp(now()), toTimestamp(now()), 0);
```

Insert with a fixed UUID:

```sql
INSERT INTO users (id, username, email, created_at)
VALUES (11111111-1111-1111-1111-111111111111, 'user2', 'user2@test.com', toTimestamp(now()));
```

## Read Data

Read all rows:

```sql
SELECT * FROM users;
```

Read selected columns:

```sql
SELECT id, username, email FROM users;
```

Read one row by primary key:

```sql
SELECT * FROM users
WHERE id = 11111111-1111-1111-1111-111111111111;
```

Limit results:

```sql
SELECT * FROM users LIMIT 10;
```

## Update Data

Update a row by primary key:

```sql
UPDATE users
SET username = 'newname'
WHERE id = 11111111-1111-1111-1111-111111111111;
```

Update multiple fields:

```sql
UPDATE urls
SET click_count = 5,
    shortened_url = 'short123'
WHERE id = 11111111-1111-1111-1111-111111111111;
```

Note: Cassandra updates behave like upserts.

## Delete Data

Delete a row:

```sql
DELETE FROM users
WHERE id = 11111111-1111-1111-1111-111111111111;
```

Delete one column:

```sql
DELETE email FROM users
WHERE id = 11111111-1111-1111-1111-111111111111;
```

Delete all rows but keep the table:

```sql
TRUNCATE users;
```

## Indexes

Create an index:

```sql
CREATE INDEX IF NOT EXISTS users_email_idx ON users (email);
```

Drop an index:

```sql
DROP INDEX users_email_idx;
```

## Batches

Group related writes:

```sql
BEGIN BATCH
  INSERT INTO users (id, username, email, created_at)
  VALUES (uuid(), 'user3', 'user3@test.com', toTimestamp(now()));

  INSERT INTO users (id, username, email, created_at)
  VALUES (uuid(), 'user4', 'user4@test.com', toTimestamp(now()));
APPLY BATCH;
```

## Monitoring and Debugging

Enable tracing for a query:

```sql
TRACING ON;
SELECT * FROM users WHERE id = 11111111-1111-1111-1111-111111111111;
TRACING OFF;
```

Explain a query:

```sql
EXPLAIN SELECT * FROM users WHERE id = 11111111-1111-1111-1111-111111111111;
```

Useful system tables:

```sql
SELECT * FROM system.local;
SELECT * FROM system.peers;
```

## Common Non-Interactive Commands

Run a query from terminal:

```bash
cqlsh 127.0.0.1 9043 -e "SELECT * FROM shrinkr.users;"
```

Run a schema script:

```bash
cqlsh 127.0.0.1 9043 -f schema.cql
```

## Common Errors

`unconfigured table`

- The table does not exist in the active keyspace
- Run `USE shrinkr;` or qualify the table name

`Cannot execute this query as it might involve data filtering`

- The query does not match the table primary key design
- Query by primary key or redesign the table

`SyntaxException`

- Check semicolons, quotes, and parentheses

`UnavailableException`

- Cassandra may not have enough replicas available
- Check the node health and consistency level

## Quick Reference

```sql
USE shrinkr;
DESCRIBE TABLES;
SELECT * FROM users;
SELECT * FROM urls;
INSERT INTO users (id, username, email, created_at) VALUES (uuid(), 'user1', 'user1@test.com', toTimestamp(now()));
UPDATE users SET username = 'newname' WHERE id = ...;
DELETE FROM users WHERE id = ...;
TRACING ON;
CONSISTENCY QUORUM;
EXIT;
```
