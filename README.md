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

### 4) -KROSS

You can cross any indexes you want using the same combination as in *remove*. <br>
The flag for crossing is "-k" or "-d" (for "done"):

> -k l <br> ^ crosses the Last index <br> <br> -k 1,3,7 <br> ^ crosses indexes 1, 3 and 7
<br> <br> -k a <br>^ crosses everything

Currently, the only way to "uncross" is to either undo your last action (if possible), or use "-kd":

> -k d <br> ^this will clear all the past crossings

### 5) -UNDO / -REDO

You can *undo* your last action by using the "-u" flag:
> -u

Might add multiple undies soon

You can also *redo* your last undo, by using "-ree" or "-m":

> -ree <br>
> -m

### 6) -EXPORT

The list gets automatically stored in the "data" folder as "tdl.txt". <br>
You can save your current list anywhere, under a different name, with the flag "-x":

> -x /home/rq137/Documents/bruuuh

This will save your current list in the "Documents" directory under the name "bruuuh". <br>
Alternatively you can save it as any other file format if you append it (idk like ".pron" or ".cia").


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
3) Not properly tested with other commands

# Epilogue

The code might be a hot mess, I will refactor it at least, if not rewrite it completely <br>
There might be inconsistent logic used for the "same" thing, I was trying out multiple approaches
The "requirements.txt" is insane, I know. I could not figure out how to make it automatically but to only include the actually necesse