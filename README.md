# j3todo
A simple command-line tool for managing tasks and creating the daily report.

## Description
### `j3todo.txt`
- A to-do list.
- Simple plain text file.
- Support nested tasks.

### `report.txt`
- A daily report.
- Completed tasks are moved from `j3todo.txt` to `report.txt` by `daily_report.sh`.

### `daily_report.sh`
- A shell script wrapping `daily_report.py`.
- Delete completed tasks from `j3todo.txt`.
- Generate a daily report from `j3todo.txt` and save it to `report.txt`.


## Usage
Create `j3todo.txt`

```
- Study Kotolin
    - Read tutorial
    - Create test app
- Study iptables
    - Experiment with hashlimit
    - Write a report
```

Change `-` mark to `x` if you did it.

```
- Study Kotolin
    x Read tutorial
    - Create test app
x Study iptables
    x Experiment hashlimit
    x Write a report
```

At the end of the day, run the following command.

```
./daily_report.sh j3todo.txt report.txt
```

Then, `report.txt` is generated.

```
# 2018-05-01 (Tue)
- Study Kotolin
    x Read tutorial
x Study iptables
    x Experiment hashlimit
    x Write a report
```

Completed tasks are deleted from `j3todo.txt`.

```
- Study Kotolin
    - Create test app
```

