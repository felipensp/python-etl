# regex-etl
ETL tool written in Python using Regex rules as DSL to generate python parsing scripts.

## DSL

```
/(pattern)/ {
    // Python code to run when pattern matches
    // We can use $1, $2, $N to refer to the matching group
}

or

<csv> {
    // Python code to run on every csv row
    // We can use $0, $1, $N to refer to csv column index
}
```

# Examples

#### ETL file

```
result = []
/(?m:^)(\d{3})-([a-z]+)/ {
    result.append({"number": int($1), "description": 'good' if $2 == 'foo' else 'bad'})
}
/(\d+)/ {
    result.append({"number": int($1)})
}
print(result)
```

### Using stdin in command-line

```
>python regex-etl.py test.etl
123
^Z
[{'number': 123}]
```

```
>python regex-etl.py test.etl
123-foo
^Z
[{'number': 123, 'description': 'good'}, {'number': 123}]
```

### Using payload input file

```
>type test\payload | python regex-etl.py test.etl
[{'number': 123, 'description': 'good'}, {'number': 1337}, {'number': 123}, {'number': 456}, {'number': 777}]
```

## Processing CSV file

#### ETL file
```
<csv> {
   print($1)
}
```

### Testing in command line

```
> python regex-etl.py csv.etl
id,name
1,felipe
^Z
name
felipe
```