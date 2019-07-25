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

### Doing Clustering and Retriving the transactions

The script `analyze-sme-btc.py` is used to first clustering the user address and then retrive the address. 
The script will first read in `All_user_info_speculation_merged_all.csv` and store all the user and their given bitcoin addresses in an ordered dict. The next step is to cluster their address to acquire all the addresses belonging to the same user. Once the clustering is done, we retrive all the transactions conducted by that "cluster", aka the user.
The script will write its outputs to two files:

1. `clustering_output.csv` for the clustering result.
1. `tx_output.csv` for the transaction history of users (only successfully clustered user will be displayed here)

There are several tricks in this script:

1. some address will crash blocksci for unknown reason. There are several discussions on blocksci's official repo ([#256](https://github.com/citp/BlockSci/issues/256), for example), however I bypassed all these addresses for simplicity. (This is done by running `filter-bad.py`, which will call `analyze-sme-btc.py` multiple times and write the "bad user's id" into `bad-uids-auto.txt`, which will further read by `analyze-sme-btc.py`)
2. some address is not in the correct format. I used a strict (maybe too strict) rule to filter out invalid addresses. The regex expression I used could be found [here](http://mokagio.github.io/tech-journal/2014/11/21/regex-bitcoin.html)
3. some address will have an extremely large clustering result (more than 100,000,000 addresses). According to our disscussion, these addresses are owned by bitcoin exchange. Thus these user are also skipped.

### Analysis

On July.25th, 2019 the output statistics is:

```
proceeded user count (all user):  6564
effective user count (user clustered successfully):  1584
endless clustering user count (user with extremely large clustering result):  2833
non-exist user count (given addr does not exist in chain):  1979
max num addressed of single user:  1591
min num addressed of single user:  0
total address count:  24971
```

The output files on July.25th, 2019 could be downloaded from [here](https://www.dropbox.com/sh/z10i3xdaqgzotm2/AAAwhPxQwGLAeKdBcAkX1FnLa?dl=0)


#### Potential Problems

