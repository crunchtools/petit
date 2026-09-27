# Philosophy

petit is built on one idea: take out of a log everything you already know,
and what's left is what you need to read. This page is the reasoning behind
it, as Scott McCarty wrote it for the first release in 2009.

## Why

Log analysis is something that all systems administrators know they need to
do. Many of us come to this point, either because there is a problem, there
is a security requirement from the organization, or it keeps you up all
night wanting to know what is going on in all of that data.

Looking for best practices for log analysis on the Internet is difficult at
best. Many years ago, I discovered a script that hashed log files by
removing all of their numbers and replacing them with "#" characters. The
results of this simple algorithm were phenomenal, logs could be reduced by a
factor of ten. This was much more readable, yet left much of the quality
data that I needed to determine if there was a problem.

In the years since I discovered that simple algorithm, I have come to
discover many techniques on text analysis which are commonly used in
linguistics and anthropology to analyze natural languages. This has led me
to develop very simple best practices for analyzing logs.

## The Basics

1. Logs are made up of output which are programmed by human beings. There
   are no real restraints on what is output, other than, some cultural rules
   on being professional. This makes the output from programs very much a
   natural language. This also makes the output of someone's program an
   approximation of the reality of what is happening inside a program. This
   is important to remember, logs are not perfect.

2. When a systems administrator analyzes logs by changing them, they are
   creating an approximation of an approximation of reality inside a working
   program. This is not necessarily a bad thing, especially, when the
   programmer never gives you better than their approximation of reality
   anyway.

3. In practice logs are made up of certainty and uncertainty. For example, I
   know what OpenSSH puts in the log during a login, because it is common. On
   the other hand, I do not know what a Compaq DL380 G3 will put in the log
   when it has a disk controller error. This is important to remember.

4. The basic log analysis algorithm in petit works to remove certainty,
   while leaving uncertainty. Stated another way, petit quantitatively
   removes certainty, thereby leaving uncertainty, which by necessity
   requires qualitative analysis from a systems administrator.

5. After the algorithm has been applied, the output must be read by a
   systems administrator to determine if it is normal or abnormal. Then
   abnormal entries can be acted on, hopefully before there is noticeable
   impact to your system.

## Related

- [History](history.md): where the idea came from, and where petit has
  lived since
- [Hashing](hashing.md): the algorithm, as it works today
- [The Logs Are an Approximation of Reality](https://crunchtools.com/the-logs-are-an-approximation-of-reality/)
  (crunchtools.com, 2011)
