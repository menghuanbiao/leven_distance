#encoding:utf-8
import math
import xlrd
import xlwt



def leven_distance(search, dist_str):
    m, n = len(search), len(dist_str)
    if m == 1:
        return not search in dist_str
    if not n:
        return m
    row1 = [0] * (n+1)
    for i in range(0,m):
        row2 = [i+1]
        for j in range(0,n):
            cost = ( search[i] != dist_str[j] )
            row2.append(min(row1[j+1]+1,
                              row2[j]+1,
                              row1[j]+cost)
                          )
        row1 = row2
    len_search = len(search)
    len_dist_str = len(dist_str)
    score = 1-float(min(row1))/float(max(len_search,len_dist_str))

    #score = 1/(1+pow(math.e,-min(row1)))
    return score

def getGongshangData(path='./data_src/工商表.xls'):
    if not path:
        return []
    gongshang_data = xlrd.open_workbook(path)
    table = gongshang_data.sheets()[0]
    nrows = table.nrows
    arr_gongshang_data = []
    for i in range(nrows):
        if i == 0:
            continue
        v = table.row_values(i)
        item = (v[0], v[1], int(v[2]))
        arr_gongshang_data.append(item)
    return arr_gongshang_data

def getYongdian(path='./data_src/用电表.xls'):
    if not path:
        return []
    gongshang_data = xlrd.open_workbook(path)
    table = gongshang_data.sheets()[0]
    nrows = table.nrows
    arr_gongshang_data = []
    for i in range(nrows):
        if i == 0:
            continue
        v = table.row_values(i)
        item = (v[0], int(v[1]))
        arr_gongshang_data.append(item)
    return arr_gongshang_data

def getSearchData(search,list):
    item_list = []
    for l in list:
        record = leven_distance(search, l)
        item_list.append((record, l))
    sort_res = sorted(item_list, reverse=True)
    result = []
    for r in sort_res:
        if r[0] >= 0.6:
            result.append(r)
    return result

# if __name__ == '__main__':
#     search = '南京大学'
#     list = ['北大','中华人民共和国','南京','南京师范大学','中国教育部','清华大学']
#     print getSearchData(search,list)[0]

def write_match_xls(list_data=[]):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    row_num = 0
    for row in list_data:
        col_num = 0
        for col in row:
            sheet1.write(row_num, col_num, col)
            col_num += 1
        row_num += 1
    workbook.save('./data_dst/result.xls')

if __name__ == '__main__':
    arr_gongshang_data = getGongshangData()
    arr_yongdian_data = getYongdian()
    arr_yongdian_hash = {}
    yongdian_list = []
    for yongdian in arr_yongdian_data:
        arr_yongdian_hash[yongdian[0]] =yongdian
        yongdian_list.append(yongdian[0])
    match_result = []
    for gongshang in arr_gongshang_data:
        search_res = getSearchData(gongshang[0],yongdian_list)
        if search_res:
            match_word = search_res[0][1]
            match_result.append((gongshang[0],gongshang[1],gongshang[2],match_word,arr_yongdian_hash[match_word][1],search_res[0][0]))
    write_match_xls(match_result)








