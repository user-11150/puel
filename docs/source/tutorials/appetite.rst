.. _tut-intro:

**********************
Whetting Your Appetite
**********************

If you do much work on computers, eventually you find that there's some task
you'd like to automate.  For example, you may wish to perform a
search-and-replace over a large number of text files, or rename and rearrange a
bunch of photo files in a complicated way. Perhaps you'd like to write a small
custom database, or a specialized GUI application, or a simple game.

If you're a professional software developer, you may have to work with several
C/C++/Java libraries but find the usual write/compile/test/re-compile cycle is
too slow.  Perhaps you're writing a test suite for such a library and find
writing the testing code a tedious task.  Or maybe you've written a program that
could use an extension language, and you don't want to design and implement a
whole new language for your application.

UEL is just the language for you.

You could write a Unix shell script or Windows batch files for some of these
tasks, but shell scripts are best at moving around files and changing text data,
not well-suited for GUI applications or games. You could write a C/C++/Java
program, but it can take a lot of development time to get even a first-draft
program.  UEL is simpler to use, available on Windows, Mac OS X, and Unix
operating systems, and will help you get the job done more quickly.

UEL is simple to use, but it is a real programming language, offering much
more structure and support for large programs than shell scripts or batch files
can offer.  On the other hand, UEL also offers much more error checking than
C, and, being a *very-high-level language*, it has high-level data types built
in, such as flexible arrays and dictionaries.  Because of its more general data
types UEL is applicable to a much larger problem domain than Awk or even
Perl, yet many things are at least as easy in UEL as in those languages.

UEL allows you to split your program into modules that can be reused in other
UEL programs.  It comes with a large collection of standard modules that you
can use as the basis of your programs --- or as examples to start learning to
program in UEL.  Some of these modules provide things like file I/O, system
calls, sockets, and even interfaces to graphical user interface toolkits like
Tk.

UEL is an interpreted language, which can save you considerable time during
program development because no compilation and linking is necessary.  The
interpreter can be used interactively, which makes it easy to experiment with
features of the language, to write throw-away programs, or to test functions
during bottom-up program development. It is also a handy desk calculator.

UEL enables programs to be written compactly and readably.  Programs written
in UEL are typically much shorter than equivalent C,  C++, or Java programs,
for several reasons:

* the high-level data types allow you to express complex operations in a single
  statement;

* no variable or argument declarations are necessary.

UEL is *extensible*: if you know how to program in C it is easy to add a new
built-in function or module to the interpreter, either to perform critical
operations at maximum speed, or to link UEL programs to libraries that may
only be available in binary form (such as a vendor-specific graphics library).
Once you are really hooked, you can link the UEL interpreter into an
application written in C and use it as an extension or command language for that
application.

Now that you are all excited about UEL, you'll want to examine it in some
more detail.  Since the best way to learn a language is to use it, the tutorial
invites you to play with the UEL interpreter as you read.

In the next chapter, the mechanics of using the interpreter are explained.  This
is rather mundane information, but essential for trying out the examples shown
later.

The rest of the tutorial introduces various features of the UEL language and
system through examples, beginning with simple expressions, statements and data
types, through functions and modules, and finally touching upon advanced
concepts like exceptions and user-defined classes.


