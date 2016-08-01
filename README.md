# Pathx

Allows for easy manipulation of %PATH% environment variable

## Usage

```
usage: pathx [-h] [-S] action pathname

positional arguments:
  action        action to preform on %PATH% (APPEND, PREPEND, REMOVE)
  pathname      pathname to add to or remove from %PATH%

optional arguments:
  -h, --help    show this help message and exit
  -S, --system  preform action on system %PATH% instead of user %PATH%
```

### Arguments

#### Positional

| Argument | Description                              | Required | Default | Choices                 |
| -------- | ---------------------------------------- | -------- | ------- | ----------------------- |
| action   | action to preform on %PATH%              | Yes      | None    | APPEND, PREPEND, REMOVE |
| pathname | pathname to add to or remove from %PATH% | Yes      | None    | N/A                     |

#### Optional

| Flag         | Description                                            | Required | Default |
| ------------ | ------------------------------------------------------ | -------- | ------- |
| -h, --help   | show this help message and exit                        | No       | False   |
| -S, --System | preform action on system %PATH% instead of user %PATH% | No       | False   |
