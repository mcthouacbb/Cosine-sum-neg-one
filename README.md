# Sums of cosines <= 1

Let's say you have a function $g(\theta) = \sum_{k \in B} \cos(k\theta)$, where B is a multiset of positive integers.

It is always possible to find a value $\theta$ such that $g(\theta) = -1$.

However, it is quite tricky to show this is the case. This repository contains a python script which implements an algorithm to always find a value of $\theta$ such that $g(\theta) <= -1$. Since $g(0) \geq 1$, by the intermediate value theorem, such a value of $\theta$ always exists.

## Usage

Python 3 and pip are required. The tabulate package is required in order to format the output.
Run `pip install -r requirements.txt` to install all dependencies

Run `python main.py --numbers <space-separated integers here>` in order to print human readable table of the result.
Run `python main.py --numbers <numbers> --latex` in order to print a latex formatted table of the result.
