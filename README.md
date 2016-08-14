# Scratching Forth
## The elegance of Forth, with the awesomeness of Scratch
---

## What is Scratching Forth?
Scratching Forth is a compiler from Forth to Scratch .sb2 files.
It is written in Python, and released under the MIT license.

## How to install
1. Make sure you have Python 3.5 installed.
2. Clone this repo to your computer with `git clone https://github.com/BookOwl/scratching-forth`

## How to run
Cd into the cloned repo, and run `python3 main.py source.fs`.
To see all the options, run `python3 main.py -h`

## I found a bug or I have a great idea!
Great! Please make an issue with your bug report or suggestion. PRs are welcomed.

## What words does Scratching Forth support?
Scratching Forth currently support the following words:
* +
* -
* *
* /
* DUP
* DROP
* MOD
* /MOD
* SWAP
* ROT
* OVER
* .
* CR
* =
* IF ... [ELSE ...] THEN

Scratching Forth does _not_ have support for the return stack (yet).

## License
The MIT License (MIT)
Copyright (c) 2016 Matthew (@BookOwl)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
