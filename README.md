# **TODL**

Todl is a simple To Do List.

It is the very first Python project I created.

Please ***shit*** on it if you can, I am more than open for possible changes.

## Commands

TODL creates a simple text file with a list of "records".

There are three main components:

### 1) -ADD

To append a new index to the list, use the "-a" flag:


> -a "Get out of here Stalker"

This will add the content to the end of the list.

Alternatively, you can add to a specific position<br>
Let's say we wanna add to the position 42:
> -a "42 Fentanyl is very tasty"

You can also run multiple "-a" flags:

> -a "I <3 vandalism" -a "1312 I hate the police"

If you want to append a number, you have to put any character in front of:

> -a ".137"

It's definitely a feature (except for one thing)

### 2) -REMOVE

There are couple of option for removing with the "-r" flag:

- **Remove the first index**

> -r f

- **Remove the last index**

> -r l

- **Remove a specific position**

> -r 137
- **Remove multiple indexes**

> -r 1,6,9
- **Remove a range of indexes**

> -r 1:7

- **Remove all indexes** (this will prompt a y/n option)

> -r a

### 3) -LIST

You can see the full list with the "-l" flag:

> -l

Nuff said

### 4) -UNDO

_______________________

## Combining flags

- You can combine flags in one command:

> -a "3 space is fake and gay" -a "also aliens" -r 6:9 -l

### HOWEVER

It is important to note couple of things:

1) You **can** have multiple **"-a"** flags, but **not** multiple **"-r"** flags<br>
The reason is, you can remove any combination of indexes with just one "-r" flag 
2) The order of execution is: <br>
- Remove <br>
- Add <br>
- List <br>
- Undo (if you add and undo in one command, guess what happens)
3) Redo function is WIP

# Epilogue

The code might be a hot mess, I will refactor it at least, if not rewrite it completely <br>
There might be inconsistent logic used for the "same" thing, I was trying out multiple approaches
The "requirements.txt" is insane, I know. I could not figure out how to make it automatically but to only include the actually necesse