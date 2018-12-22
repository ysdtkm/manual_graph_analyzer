<kbd><img src="document/anime.gif"></kbd>

# Semi-manual graph analyzer
This CGI script analyzes any graph by breadth-first order.

### The CGI script
* Memorizes already visited nodes
* Suggest next step with breadth-first order
* Visualizes the structure

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
