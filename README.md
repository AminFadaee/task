# Task
A simple cli to-do list. Created using python and click library.
## How to
Create a task belonging to a group:
```bash
~ task add Movies John Wick 2
```

Edit a task (partial match available):
```bash
~ task edit Movies John
Enter the new name for John Wick 2 [John Wick 2]: John Wick: Chapter 2
```

Finish a task (partial match available):
```bash
~ task finish Movies John
```

List tasks:
```bash
~ task list Movies
    Movies
================================
[ ] The Irishman
[x] John Wick 2
[x] Toy Story 4
[ ] One Upon a Time in Hollywood
[x] Avengers: End Game
================================
```

Export the tasks to `.txt` file:
```bash
~ task export Movies path/to/save
```

or to `.pdf`:
```bash
~ task export Movies path/to/save --pdf
```

![](assets/samples/pdf.png)

## Future
I try to add sorting feature for list and exports, also I might try
to add attributes to each task (due date, urgency, ...).

The big next feature would be syncing the tasks in the cloud so
you could access your tasks anywhere.

## Author
Amin Fadaee

Checkout my channel: [BackendLife](https://t.me/backendlife)