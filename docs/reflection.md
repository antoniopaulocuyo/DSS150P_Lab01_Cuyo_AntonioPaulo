# Reflection

**1. Which source would be easiest to integrate into a future pipeline, and why?**

`products.parquet` would be the easiest to integrate. It arrived with zero nulls and
zero duplicate rows. In addition, Parquet embeds its own schema
directly in the file, so a pipeline can read it without guessing at types or writing
custom parsing logic. By contrast, the CSV and JSON sources both required extra work.
`customers.csv` needed explicit date parsing since `signup_date` was stored as plain
text, and `orders.json` needed a nested-object flattening step before basic
operations like duplicate detection would even run.

**2. Which source presents the greatest schema or data-quality risk, and what
evidence supports your answer?**

`orders.json` presents the greatest risk. First, its `shipping` field is a nested dictionary, which caused `df.duplicated()`
to fail outright with a `TypeError` rather than silently returning a wrong count. Second,
`order_timestamp` is stored as a string and required explicit coercion with
`pd.to_datetime()` before min/max values could be computed.

**3. What could go wrong if a pipeline is built before the source schema and
contract are understood?**

Without understanding the schema in advance, a pipeline could silently load bad data
rather than fail. For example, if `customer_id` had been assumed unique and
used directly as a database primary key without profiling first, the pipeline would
have crashed on load the moment it hit one of the 3 duplicate values discovered
during profiling. Similarly, treating `orders.json`'s
`shipping` field as flat instead of nested could cause a naive pipeline to either
drop the field entirely or throw unclear errors deep in the process, rather than
handling it deliberately at ingestion time.

**4. How do Git, virtual environments, containers, and documentation improve
reproducibility for a data-engineering team?**

Git ensures every change to scripts, schemas, and documentation is tracked and
recoverable. This allows a team can see exactly what changed and when, and roll back a bad
change safely. Virtual environments pin the exact Python dependencies a project
needs. This prevents the "it works on my machine" failures caused by mismatched library
versions. Containers (Docker) go a step further by isolating not just Python
dependencies but the entire runtime environment. Any team member can spin up an identical database with one command rather than
manually installing and configuring Postgres. Documentation 
captures why decisions were made so future team members don't have to rediscover the same risks through trial and
error.