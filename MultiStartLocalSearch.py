
import random

#英語=1, 数学=2, 物理=3. 化学=4
target_array = [[6,1,9,3],[2,5,7,8],[6,3,5,4],[3,5,2,1]] #各科目にかかる時間を示す、科目の十番は上と同様。1要素目Aさんのかかる時間、2要素目さん・・・といった感じ

#ランダムに初期解を生成する
def random_solution(target_array):
    row_num = len(target_array)
    col_num = len(target_array[0])

    selected_num = []
    for n in range(col_num):
        selected_num.append(n+1)
    random.shuffle(selected_num) #配列の中身をランダムに入れ替える

    return selected_num

#初期解とtarget_arrayから合計の所要時間を計算する
def calc_target_func(target_array,selected_array):
    tmp_num = 0
    for num,row in enumerate(target_array):
        tmp_num += row[selected_array[num] - 1]
    
    return tmp_num

for n in range(5):
    selectd_array = random_solution(target_array)
    calc_target_func(target_array,selectd_array)
    print(calc_target_func(target_array,selectd_array))

    


