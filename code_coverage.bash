coverage run -m unittest discover -s ./tests
coverage report -m
coverage html
xdg-open "file:///$(pwd)/coverage_report/index.html"
