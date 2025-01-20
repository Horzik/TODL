# **TODL**

Todl is a simple To Do List.

## Commands

TODL creates a simple text file with a list of "records".

Here are the possible functions:

### 1) -ADD

To append a new index to the list, use the "-a" flag:


> -a "Get out of here Stalker"

This will add the content to the end of the list.

Alternatively, you can add to a specific position.<br>
Let's say we wanna add to the position 42:
> -a "42 Fentanyl is very tasty"

You can also run multiple "-a" flags:

> -a "I <3 vandalism" -a "1312 I hate the police"

If you want to append a number, you have to put a character in front of the number:

> -a ".137"

It's definitely a feature (except for one thing)

### 2) -REMOVE

There are couple options for removing with the "-r" flag:

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

You can cross any position you want using the same combination as in *remove*. <br>
The flag for crossing is "-k" or "-d" (for "done"):

> -k l <br> ^ crosses the Last index <br> <br> -k 1,3,7 <br> ^ crosses indexes 1, 3 and 7
<br> <br> -k a <br>^ crosses everything


> -k a <br> ^this will clear all the past crossings

### 5) -CLEAN

This function will clean the desired index from being crossed over.
Flag is "-c" and the position is again defined same as with *remove* or *kross*.

> -c 3:7 <br> ^ this will clean the records number 3 through 7

### 6) -UNDO / -REDO

You can *undo* your last action by using the "-u" flag:
> -u

Might add multiple undies soon

You can also *redo* your last undo, by using "-ree" or "-m":

> -ree <br>
> -m

The maximum history for both undo and redo stacks is currently 5.

### 7) -EXPORT

The list gets automatically stored in the "data" folder as "tdl.txt". <br>
You can save your current list anywhere, under a different name, with the flag "-x":

> -x newCopy

This will save the file in the current directory under the name "newCopy"

> -x /home/rq137/Documents/bruuuh

This will save your current list in the "Documents" directory under the name "bruuuh". <br>
Alternatively you can save it as any other file format if you append it (idk like ".pron" or ".cia").


## EDITOR

Additionally, there is a simple CLI text editor included. To run it, you can use the flag "-e"<br>
It is basic but should work sufficiently, there are couple shortcuts:

### -EXIT

*"ctrl + e"*<br>

You can use this to exit the editor gracefully.<br>
If any changes were done to the list, the *exit* will prompt the user if they want to save them.

### -SAVE/WRITE

*"ctrl + w"*<br>

This will save the file with any changes done while in the editor.

### -KROSS

*"ctrl + k"*<br>

Sane as with the krosser before, this will kross the current line.

### -CLEAN

*"ctrl + l"*<br>

Guess what this does (yes). 
_______________________

## Combining flags

- You can combine flags in one command:

> -a "3 space is fake and gay" -a "also aliens" -r 6:9 -l

### HOWEVER

It is important to note couple things:

1) You **can** have multiple **"-a"** flags, but **not** multiple **"-r"** flags<br>
The reason is, you can remove any combination of indexes with just one "-r" flag 
2) The order of execution is: <br>
- Remove <br>
- Add <br>

# Epilogue

This is the first Python project I have started.<br>
Any feedback for improvement is more than welcomed.