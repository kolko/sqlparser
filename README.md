Simple python SQL parser based on PLY library https://github.com/dabeaz/ply/

By design, this is parser for make statistic information about SQL query,
what and from is selected. Parser may return a little bit incorrect outputs - this is ok. :)

Parser has not based on any SQL dialect (i use PostgreSQL 
and Firebird and you may think what this parser based on they).

Todo:
-Use database scheme to define aligment fields to tables.
-joins
-group by/having
-dates, float, between, etc... :(
-maybe: substrings (firebird 2.1 form)