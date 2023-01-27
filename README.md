# pypsu

## Installation

Use the following command to install the pypsu package with pip:

~~~sh
python -m pip install pypsu
~~~

Make sure the local bin path is in your path. If not, add it to `~/.bashrc` or `~/.zshrc`:

~~~sh
export PATH="$HOME/.local/bin:$PATH"
~~~

## Usage
~~~
usage: psu [-h] [-v] {interactive,i,list,l,ls,create,c,import,im,export,e,rename,r,delete,d,del,rm} ...

Manipulate PS2 PSU game save files.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Commands:
  {interactive,i,list,l,ls,create,c,import,im,export,e,rename,r,delete,d,del,rm}
    interactive (i)     Interactive command prompt.
    list (l, ls)        List the files and directories within the game save.
    create (c)          Create a PSU game save file.
    import (im)         Import a file from the local disk to the game save.
    export (e)          Export a file from the game save to the local disk.
    rename (r)          Rename a file within the game save.
    delete (d, del, rm)
                        Delete a file from within the game save.
~~~

### List files
~~~
└─$ psu list BASCUS-97129.psu
total 9
d Dec 23 2022  0      BASCUS-97129
d Dec 23 2022  0      .
d Dec 23 2022  0      ..
- Dec 23 2022  964    icon.sys
- Dec 23 2022  44376  bkmo1.ico
- Dec 23 2022  44376  bkmo2.ico
- Dec 23 2022  44376  bkmo3.ico
- Dec 23 2022  3460   BASCUS-97129
- Dec 23 2022  3460   bkmo0.dat
~~~

### Create PSU
~~~
└─$ psu create BASCUS-97129.psu
[+] PSU file "BASCUS-97129.psu" saved
~~~

### Import file into PSU
~~~
└─$ psu import BASCUS-97129.psu bkmo0.dat
[+] bkmo0.dat imported to bkmo0.dat
~~~

### Export file from PSU
~~~
└─$ psu export BASCUS-97129.psu bkmo0.dat
[+] bkmo0.dat exported to bkmo0.dat
~~~

### Rename file in PSU
~~~
└─$ psu rename BASCUS-97129.psu bkmo0.dat bkmo1.dat
[+] bkmo0.dat renamed to bkmo1.dat
~~~

### Delete file in PSU
~~~
└─$ psu delete BASCUS-97129.psu bkmo0.dat    
[+] bkmo0.dat deleted
~~~

### Interactive mode
~~~
└─$ psu interactive BASCUS-97129.psu
# list
total 9
d Dec 23 2022  0      BASCUS-97129
d Dec 23 2022  0      .
d Dec 23 2022  0      ..
- Dec 23 2022  964    icon.sys        
- Dec 23 2022  44376  bkmo1.ico       
- Dec 23 2022  44376  bkmo2.ico       
- Dec 23 2022  44376  bkmo3.ico       
- Dec 23 2022  3460   BASCUS-97129    
- Dec 23 2022  3460   bkmo0.dat       

# export bkmo0.dat
[+] bkmo0.dat exported to bkmo0.dat
# import bkmo1.dat
[+] bkmo1.dat imported to bkmo1.dat
# rename bkmo3.ico bkmo4.ico
[+] bkmo3.ico renamed to bkmo4.ico
# list
total 10
d Dec 23 2022  0      BASCUS-97129
d Dec 23 2022  0      .
d Dec 23 2022  0      ..
- Dec 23 2022  964    icon.sys        
- Dec 23 2022  44376  bkmo1.ico       
- Dec 23 2022  44376  bkmo2.ico       
- Dec 23 2022  44376  bkmo4.ico       
- Dec 23 2022  3460   BASCUS-97129    
- Dec 23 2022  3460   bkmo0.dat       
- Jan 27 20:26 3460   bkmo1.dat       

# exit
~~~

## API
### PSU
#### Create a new file
~~~py
psu = PSU.create('BASCUS-97129.psu')
psu.write('hello.txt', 'Hello World')
psu.save()
~~~

#### Read an existing file
~~~py
psu = PSU.load('BASCUS-97129.psu')
print(psu.read('hello.txt').decode('UTF-8'))
~~~

#### Update an existing file
~~~py
psu = PSU.load('BASCUS-97129.psu')
print(psu.read('hello.txt').decode('UTF-8'))
psu.write('hello.txt', 'Hello World New')
psu.save()
~~~

#### Import an existing file
~~~py
psu = PSU.load('BASCUS-97129.psu')
psu.copy('/tmp/hello.txt', 'hello.txt')
psu.save()
~~~

#### Export an existing file
~~~py
psu = PSU.load('BASCUS-97129.psu')
psu.export('hello.txt', '/tmp/hello.txt')
psu.save()
~~~

#### Remove an existing file
~~~py
psu = PSU.load('BASCUS-97129.psu')
psu.delete('hello.txt')
psu.save()
~~~

#### Check if an entry exists by name
~~~py
psu = PSU.load('BASCUS-97129.psu')
if psu.has('hello.txt'):
    print('hello.txt exists in BASCUS-97129.psu')
else:
    print('hello.txt does not exist in BASCUS-97129.psu')
~~~

#### Get an entry by name
~~~py
psu = PSU.load('BASCUS-97129.psu')
entry = psu.get('hello.txt')
print(entry)
~~~

#### Check if an entry is a file
~~~py
psu = PSU.load('BASCUS-97129.psu')
if psu.isFile('hello.txt'):
    print('hello.txt is a file')
else:
    print('hello.txt is not a file')
~~~

#### Check if an entry is a directory
~~~py
psu = PSU.load('BASCUS-97129.psu')
if psu.isDirectory('.'):
    print('. is a file')
else:
    print('. is not a file')
~~~

#### Get a list of files / directories
~~~py
psu = PSU.load('BASCUS-97129.psu')
for entry in psu.list():
    if entry.isFile():
        print(f'FILE: {entry.name: <16} ({entry.header.size} bytes)')
        continue
    if entry.isDirectory():
        print(f' DIR: {entry.name: <16} ({entry.header.size} entries)')
        continue
~~~

## Reference
* <https://ps2savetools.com/documents/ps2-save-game-format-for-ems-adapter-psu/>