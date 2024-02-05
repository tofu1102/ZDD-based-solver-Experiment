import sys

def main(filepath):
    """
    filepathを開いて
    instance_no,result,iv_time_max,iv_time_ave,iv_time_sum,iv_memory_max,iv_memory_ave,ie_time_max,ie_time_ave,ie_time_sum,ie_memory_max,ie_mamory_ave,IS_time,IS_size,zdd_size_max,zdd_size_ave,zdd_is_num_max,zdd_is_num_ave,reconf_time_max,reconf_time_ave,Reconf_time,reconf_step,z_sol_num,z_sol_zdd
    をresult.csvに追記
    """
    with open(filepath,mode="r") as f:
        content = f.read().split("\n")

        instance_no = filepath
        result = "unsolved"
        iv_time_max = 0
        iv_count = 0
        iv_time_sum = 0
        iv_memory_max = 0
        iv_memory_sum = 0
        ie_time_max = 0
        ie_count = 0
        ie_time_sum = 0
        ie_memory_max = 0
        ie_memory_sum = 0
        IS_time = 0
        IS_size = 0
        zdd_size_max = 0
        zdd_size_sum = 0
        zdd_is_num_max = 0
        zdd_is_num_sum = 0
        reconf_time_max = 0
        Reconf_time = 0
        reconf_step = 0
        z_sol_num = 0
        z_sol_zdd = 0
        zdd_size_sq_sum = 0
        max_count = 0

    for row in content:
        row = row.split(",")
        row[0] = row[0].strip()
        if row[0] == "r":
            _, card, size, time = row
            reconf_step += 1
            zdd_is_num_max = max(zdd_is_num_max,int(card))
            zdd_is_num_sum += int(card)
            max_count = reconf_step if zdd_size_max < int(size) else max_count
            zdd_size_max = max(zdd_size_max,int(size))
            zdd_size_sum += int(size)
            zdd_size_sq_sum += int(size)**2
            reconf_time_max = max(reconf_time_max, float(time))
            Reconf_time += float(time)
            print(f'{instance_no.split("_")[1].split(".")[0]},{card},{size},{time}')


        elif row[0] == "iv":
            _, time, memory = row
            iv_count += 1
            iv_time_max = max(iv_time_max,float(time))
            iv_time_sum += float(time)
            iv_memory_max = max(iv_memory_max,int(memory))
            iv_memory_sum += int(memory)

        elif row[0] == "ie":
            _, time, memory = row
            ie_count += 1
            ie_time_max = max(ie_time_max,float(time))
            ie_time_sum += float(time)
            ie_memory_max = max(ie_memory_max,int(memory))
            ie_memory_sum += int(memory)
        elif row[0] == "IS":
            _, IS_size, __, ___ = row
            IS_size = int(IS_size)
        elif row[0] == "o":
            result = row[1]
        elif row[0] == "rsol":
            _, z_sol_num, z_sol_zdd = row
            z_sol_num, z_sol_zdd = map(int, (z_sol_num, z_sol_zdd))
        
    IS_time = iv_time_sum + ie_time_sum

    if reconf_step == 0:
        reconf_step = -1
    if ie_count == 0:
        ie_count = -1
    if iv_count == 0:
        return

    res = [instance_no.split("_")[1].split(".")[0], 
               result, 
               iv_time_max, 
               iv_time_sum/iv_count, 
               iv_time_sum, 
               iv_memory_max, 
               iv_memory_sum/iv_count, 
               ie_time_max, 
               ie_time_sum/ie_count, 
               ie_time_sum, 
               ie_memory_max, 
               ie_memory_sum/ie_count, 
               IS_time, 
               IS_size, 
               zdd_size_max, 
               zdd_size_sum/reconf_step, 
               zdd_is_num_max, 
               zdd_is_num_sum/reconf_step, 
               reconf_time_max, 
               Reconf_time/reconf_step, 
               Reconf_time, 
               reconf_step,
               z_sol_num,
               z_sol_zdd,
               (zdd_size_sq_sum/reconf_step - (zdd_size_sum/reconf_step)**2),
               max_count
               ]
    #print(",".join(map(str,res)))

if __name__ == "__main__":
    main(sys.argv[1])