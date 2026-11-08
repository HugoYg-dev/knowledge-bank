---
title: "Kris Shamloo"
source: "https://krisshamloo.com/blog/007"
author:
published:
created: 2026-11-08
description: "Projects by Kris Shamloo"
tags:
  - "clippings"
---
### a software engineering interview question I like: computing the median

I have a number of questions in my quiver when I'm giving technical interviews to candidates. They are all of a similar flavor. I don't ask puzzle questions, I find them low value. Instead, I ask questions that are straightforward but have a few angles with which to explore deeper topics.

Enter the humble median.

Write a function that takes an array of numbers and returns the median.

- At a minimum: this will give you a "Fizz Buzz"-like signal that the candidate can actually program. Reducing an array of values is table stakes.
- Right out the gate: the numbers must be sorted. Should the function sort them? Should the caller? If the array was passed in by reference is it ok to mutate? How does the API design influence the performance?
- It has an off-by-one trap. Mind you I don't care if anyone falls into an off-by-one trap, I fall into them all the time, but you'll often get a chance to watch someone debug a small problem.
- It has a branch: an even length array versus an odd one.
- It can lead to some discussion about statistics and why you might prefer a median to a mean in most cases.
- Gives the candidate a chance for some extra points by being so readily testable.
- Gives the candidate a chance to display some standard library knowledge via [statistics](https://docs.python.org/3/library/statistics.html#module-statistics).
- Gives the candidate a chance to teach me about a cool algorithmic trick I did not know about until writing this post with [quickselect](https://en.wikipedia.org/wiki/Quickselect).

Here's a Python implementation with discussion comments.

```
def median(numbers: list[float]) -> float:
    # What should we do if the list is empty?
    # Raise an exception? Return a sentinel value?
    if not numbers:
        raise ValueError("median called with empty list")

    # Python is pass-by-reference, what are the
    # implications of sorted() vs numbers.sort()?
    numbers = sorted(numbers)
    length = len(numbers)
    mid = length // 2

    # High-quality candidates will bravely import 1,000
    # dependencies to get an is_even library func.
    if length % 2 == 0:
        return (numbers[mid - 1] + numbers[mid]) / 2.0
    else:
        return numbers[mid]
```

复制 LaTeX 公式