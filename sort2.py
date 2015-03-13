def merge(unsort_list, n_start, n_center, n_end):
    #n1 = n_center - n_start + 1
    #n2 = n_end - n_center
    l_list = unsort_list[n_start:n_center+1]
    r_list = unsort_list[n_center+1:n_end+1]
    list_n = n_end - n_center + 1
    l_list.append(1e50)
    r_list.append(1e50)
    i = 0
    j = 0
    list_tmp = []
    for k in range(list_n):
        if l_list[i] <= r_list[j]:
            list_tmp[k] = l_list[i]
            i += 1
        else:
            list_tmp[k] = r_list[j]
            j += 1
    unsort_list[n_start:n_end+1] = list_tmp
    return unsort_list
    
def sort2(unsort_list):
    list_n = len(unsort_list)
    n_center = list_n//2
    sort2(unsort_list[:n_center+1])
    sort2(unsort_list[n_center:list_n])
    return merge(unsort_list, 0, n_center, list_n)
            


