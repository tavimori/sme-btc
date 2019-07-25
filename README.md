sme-btc is a project for analyzing the transaction history of bitcoin blockchain. We use [blocksci](https://citp.github.io/BlockSci/readme.html) for processing the original chain data.


## What do we want?

The object is to retrive the transaction history of given users. The interested users are given in an `csv` files. Each user is labeled with one of his/her bitcoin address. Our program will first read in the users, then trying to find all the address hold by the same person by clustering algorithms. Finally we retrive all the transactions belonging to the same user. 

For detail, see `transaction data demostration(2).xlsx`.


## Quick Start

### Setup Blocksci

We use blocksci v0.50 for this project. Blocksci provides with two environments: 

1. [setting up blocksci on Amazon EC2](https://citp.github.io/BlockSci/readme.html#quick-setup-using-amazon-ec2) 
2. [setting up locally](https://citp.github.io/BlockSci/readme.html#setting-up-blocksci-locally)

Please choose either and setup blocksci accordingly. (We chose the second and set up blocksci on a local high-performance server on July 2019)

### Analysis

#### Potential Problems

