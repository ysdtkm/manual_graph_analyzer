# Semi-manual graph analyzer
This CGI script analyzes any graph by breadth-first order.

<img src="document/anime.gif">

### The CGI script does
* Memorization of already visited nodes
* Breadth-first suggestion of next step
* Visualization

### We need to
* Parse programs and input dependencies

### Objective
* Universal applicability by using human as a parser
* Help us organizing search and code analysis

# Usage
```
sh start.sh
# Access localhost:8000/cgi-bin/server.py
```

# Dependency
* Python3.6
* graphviz
