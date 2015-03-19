def merge(unsort_list, n_start, n_center, n_end):
    #n1 = n_center - n_start + 1
    #n2 = n_end - n_center
    l_list = unsort_list[n_start:n_center+1]
    r_list = unsort_list[n_center+1:n_end+1]
    list_n = n_end - n_start + 1
    l_list.append(1e50)
    r_list.append(1e50)
    i = 0
    j = 0
    list_tmp = []
    for k in range(list_n):
        if l_list[i] < r_list[j]:
            list_tmp.append(l_list[i])
            i += 1
        else:
            list_tmp.append(r_list[j])
            j += 1
    unsort_list[n_start:n_end+1] = list_tmp
    return unsort_list
    
def sort2(unsort_list, n_start, n_end):
    if n_start < n_end:
        n_center = (n_start +  n_end - 1)//2
        print('n_center=%d\n' %n_center)
        unsort_list = sort2(unsort_list, n_start, n_center)
        unsort_list = sort2(unsort_list, n_center + 1, n_end)
        unsort_list = merge(unsort_list, n_start, n_center, n_end)
    return unsort_list

p = sort2([3, 2, 3, 8, 4, 6, 2],0, 6)
print(p)

            


