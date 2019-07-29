#!/usr/bin/env python3

import csv
import blocksci
import re
from collections import OrderedDict
import sys

chain = blocksci.Blockchain("/mnt/licheng-sme/bitcoin-data")

# use this for the first time to create a new clustering
# cm = blocksci.cluster.ClusterManager.create_clustering("/mnt/licheng-sme/bitcoin-data/clusters-jul6", chain, should_overwrite=True)
# use this if clustering has already been done once (and no modification is made)
cm = blocksci.cluster.ClusterManager("/mnt/licheng-sme/bitcoin-data/clusters-jul6", chain)


user_dict = dict()

bad_uids = set()

if len(sys.argv) == 2:
    offset = int(sys.argv[1])
    print("offset set to {}".format(offset))
else:
    offset = 0

with open("bad-uids-auto.txt") as uid_file:
    for uid_str in uid_file:
        bad_uids.add(uid_str.strip())

with open("All_user_info_speculation_merged_all.csv") as user_file:
    # with open("")
    user_reader = csv.reader(user_file)
    next(user_reader) # bypass the header
    count = 0
    btc_addr_pattern =  re.compile("^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")

    for row in user_reader:
        # if row[6].strip() == "":
        #     continue # no bitcoin addr provided for this user
        addr = row[24].strip()
        uid = row[20]
        if addr == "":
            continue
        if not btc_addr_pattern.match(addr):
            # print("uid: {}, not valid btc addr {}".format(row[20], addr))
            continue
        # print("id: {} \tuid: {} \tbit addr: {}".format(count, row[20], addr))
        count += 1
        user_dict[uid] = addr
        #print(row[2])
        #addr = chain.address_from_string(row[2])
        #if addr is None:
        #    print("None ADDR")
        #    continue
        #cluster = cm.cluster_with_address(addr)
        #for ins in cluster.ins():
        #    print("  on{}: -{}".format(ins.block.height,ins.value/1e8))
        #for outs in cluster.outs():
        #    print("  on{}: +{}".format(outs.block.height,outs.value/1e8))
#             cluster = cm.cluster_with_address(addr)
#             for i, clu_addr in enumerate(cluster.addresses):
#                 print("  subad{}: ".format(i))
#                 for tx in clu_addr.in_txes():
#                     print("      {}".format(tx.block_height))
        # count +=1
        # if count > 100:
            # break

user_dict_orded = OrderedDict(sorted(user_dict.items(), key=lambda t: int(t[0])))


print("loaded user addresses")

addr_count = 0
proceeded_user_count = 0
nonexist_user_count = 0
effective_user_count = 0
endless_cluster_user_count = 0
top_num_clu_addrs = 0
bottom_num_clu_addrs = 10086 # just a big number

# skip first several items
it = iter(user_dict_orded.items())

# first_uid, _ = next(it)
# print("largest uid is {}", first_uid)

if offset:
    for i in range(offset):
        next(it)

with open("clustering_output.csv", "w") as clustering_output_file:

    header = ["id", "uid", "addr","is_original","is_valid","comments", "ins_count", "outs_count"]
    csv_writer = csv.DictWriter(clustering_output_file, fieldnames=header)
    csv_writer.writeheader()

    with open("tx_output.csv", "w") as tx_output_file:
        header = ["date", "uid", "tid", "action", "is_mining"]
        tx_writer = csv.DictWriter(tx_output_file, fieldnames=header)
        tx_writer.writeheader()

        for uid, addr_str in it:
        # for uid, addr_str in user_dict_orded.items():

            # print("id: {} uid: {}".format(count, uid))
            print("id: {} \t".format(count), end="")
            addr_count += 1
            proceeded_user_count += 1
            
            if count > 20000000: # to prevent the endless loop, one may tune this value to limit the size of the problem
                break

            print("uid: {} \t".format(uid), end="")

            if uid in bad_uids:
                print("bad user, skip")
                csv_writer.writerow({"id": count, "uid": uid, "addr": addr_str, "is_original": 1, "is_valid": 0, "comments": "this addr causes bug in blocksci 0.5"})
                continue

            addr = chain.address_from_string(addr_str)
            if addr is None:
                print("addr not exist")
                csv_writer.writerow({"id": count, "uid": uid, "addr": addr_str, "is_original": 1, "is_valid": 0, "comments": "this addr does not exist in chain"})
                nonexist_user_count += 1
                continue
            print("addr constructed ({})\t".format(addr_str), end="")
            
            
            
            
            clu = cm.cluster_with_address(addr)
            clu_addrs = clu.addresses

            check = True

            # count_clu_addr = 0

            # sometimes the clustering result may contains extremely many addresses (perhaps they belongs to an exchange centor)
            # we filter out such "exchange centor addr" here
            user_addr_count = 0
            for i,addr in enumerate(clu_addrs):
                # print("\t\t{}: \t type: {}".format(i, addr.type))

                # based on our experience, if there is a "nonstandard" addr in cluster, it is likely the cluster belongs to an exchange centor
                # thus we filter it out 
                if addr.type == blocksci.address_type.nonstandard:
                    check = False
                    reason = "non standard address"
                    csv_writer.writerow({"id": count, "uid": uid, "addr": addr_str, "is_original": 1, "is_valid": 1, "comments": "this addr causes bug when clustering (non-standard) endless clustering"})
                    endless_cluster_user_count += 1
                    break

                # user_addr_count += 1
                # if user_addr_count > 10000:
                #     check = False
                #     reason = "too large clustering result address"
                #     csv_writer.writerow({"id": count, "uid": uid, "addr": addr_str, "is_original": 1, "is_valid": 1, "comments": "this addr may result in endless clustering"})
                #     endless_cluster_user_count += 1
                #     break



            if not check: 
                print("check fail".format(uid))
                continue
        
            sys.stdout.flush() # we flush the buffer before potential segmentation fault
            # because of unknown reason, the following line may cause segmentation fault
            clu_addrs_count = len(list(clu_addrs))
            if clu_addrs_count > top_num_clu_addrs:
                top_num_clu_addrs = clu_addrs_count
            if clu_addrs_count < bottom_num_clu_addrs:
                bottom_num_clu_addrs = clu_addrs_count
            print("clu_addrs_count: {}".format(clu_addrs_count))


            csv_writer.writerow({"id": count, "uid": uid, "addr": addr_str, "is_original": 1, "is_valid": 1, "comments": "", "ins_count": len(list(clu.ins())), "outs_count": len(list(clu.outs()))})
            effective_user_count += 1

            # write transactions
            for tx_in in clu.ins():
                tx_writer.writerow({"date": tx_in.tx.block.time, "uid": uid, "tid": tx_in.tx.hash, "action": tx_in.value/1e8, "is_mining": 0})

            for tx_out in clu.outs():
                # tx_writer.writerow({"date": tx_out.tx.block.time, "uid": uid, "tid": tx_out.tx.hash, "action": -tx_out.value/1e8})
                if int(tx_out.tx.input_value) == 0:
                    tx_writer.writerow({"date": tx_out.block.time, "uid": uid, "tid": tx_out.tx.hash, "action": -tx_out.value/1e8, "is_mining": 1})
                else:
                    tx_writer.writerow({"date": tx_out.block.time, "uid": uid, "tid": tx_out.tx.hash, "action": -tx_out.value/1e8, "is_mining": 0})


            for clu_addr in clu_addrs:
                addr_count += 1
                if (clu_addr.type == blocksci.address_type.pubkeyhash) \
                or (clu_addr.type == blocksci.address_type.scripthash) \
                or (clu_addr.type == blocksci.address_type.pubkey) \
                or (clu_addr.type == blocksci.address_type.witness_pubkeyhash):
                    if clu_addr.address_string == addr_str:
                        # the same as original addr, skip
                        addr_count -=1
                        continue
                    csv_writer.writerow({"id": count, "uid": uid, "addr": clu_addr.address_string, "is_original": 0, "is_valid": 1, "comments": ""})
                else:
                    print("error: invalid_addr_type: {}".format(clu_addr.type))
            # except Exception:
            #     print("fail")


print("proceeded user count (all user): ", proceeded_user_count)
print("effective user count (user clustered successfully): ", effective_user_count)
print("endless clustering user count (user with extremely large clustering result): ", endless_cluster_user_count)
print("non-exist user count (given addr does not exist in chain): ", nonexist_user_count)
print("max num addressed of single user: ", top_num_clu_addrs)
print("min num addressed of single user: ", bottom_num_clu_addrs)
print("total address count: ", addr_count)