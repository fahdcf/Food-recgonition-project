# Application data

The SQLite meal log/goal database is created locally by the existing `init_db()`
startup routine. No populated user database is distributed in the repository.
Run the application normally to initialize a fresh database; do not copy another
user's meal logs, timestamps or notes into a public fixture.

Python caches, local databases, environment files and training logs are ignored.
The image datasets, model artifacts and project documentation were preserved.
Historical commits can still contain previously tracked data; current-tree
cleanup does not erase those copies.
