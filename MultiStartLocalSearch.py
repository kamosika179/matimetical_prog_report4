
import random
import copy

#英語=1, 数学=2, 物理=3. 化学=4
target_array = [[6,1,9,3],[2,5,7,8],[6,3,5,4],[3,5,2,1]] #各科目にかかる時間を示す、科目の十番は上と同様。1要素目Aさんのかかる時間、2要素目さん・・・といった感じ


def random_solution(target_array):
    """
    ランダムに初期解を生成する

    Parametors:
    -----------
    target_array : int[]
        各個人の所要時間、0番目の0番目がAさんの英語にかかる時間、1番目の1番目がBさんの数学にかかる時間と言った感じ。


    Returns:
    --------
    selected_num : int[]
        誰がどの科目を選択するか指定するもの。0番目がAさんのもの、1番目がBさんのもの・・・と言った感じ

    """
    row_num = len(target_array)
    col_num = len(target_array[0])

    selected_num = []
    for n in range(col_num):
        selected_num.append(n+1)
    random.shuffle(selected_num) #配列の中身をランダムに入れ替える

    return selected_num


def calc_target_func(target_array,selected_array):
    """
    初期解とtarget_arrayから合計の所要時間を計算する

    Parametors
    ----------
    target_array: int[]
        各個人の所要時間、0番目の0番目がAさんの英語にかかる時間、1番目の1番目がBさんの数学にかかる時間と言った感じ。

    selected_array : int[]
        誰がどの科目を選択するか指定するもの。0番目がAさんのもの、1番目がBさんのもの・・・と言った感じ

    Returns
    -------
    tmp_num : int
        合計所要時間
    """
    tmp_num = 0
    for num,row in enumerate(target_array):
        tmp_num += row[selected_array[num] - 1]
    
    return tmp_num


def perturbation(selected_array,point):
    """
    摂動を行う。隣同士を入れ替える。

    Parametors
    ----------
    selected_array : int[]
        誰がどの科目を選択するか指定するもの。0番目がAさんのもの、1番目がBさんのもの・・・と言った感じ
    
    point : int 
        pointは入れ替える位置を指定する際に使う。pointが0のときは0番目と1番目を入れ帰った結果を返す。

    Returns:
    --------
    tmp_array : int[]
        入れ替え済みの配列
    """

    tmp = selected_array[point]
    tmp_array = selected_array.copy()
    tmp_array[point] = tmp_array[point+1]
    tmp_array[point+1] = tmp

    return tmp_array

def local_search(target_array,selected_array):
    """
    局所探索法を行う

    Parametors:
    -----------
    selected_array: int[]
        誰がどの科目を選択するか指定するもの。0番目がAさんのもの、1番目がBさんのもの・・・と言った感じ。初期の選択もここに入る

    target_array : int[]
        各個人の所要時間、0番目の0番目がAさんの英語にかかる時間、1番目の1番目がBさんの数学にかかる時間と言った感じ。

    Returns:
    min_combination : int
        最小となる組み合わせと、その時の値を返す
    """

    neighborhoods = []
    good_neighborhoods = []
    for n in range(len(selected_array)-1):
        neighborhoods.append(perturbation(selected_array,n))

    now_solution_value = calc_target_func(target_array,selected_array)

    for num,lis in enumerate(neighborhoods):
        tmp_solution_value = calc_target_func(target_array,lis)
        if now_solution_value > tmp_solution_value: #暫定解を残す
            good_neighborhoods.append(lis)

    if len(good_neighborhoods) == 0:
        return (selected_array,now_solution_value)
    elif len(good_neighborhoods) == 1:
        return local_search(target_array,good_neighborhoods[0])
    else:
        tmp_multi_tuple = []
        for neigh in good_neighborhoods:
            tmp_multi_tuple.append(local_search(target_array,neigh))
        #tmp_multi_tupleか最小のものを探す
        return min(tmp_multi_tuple, key=lambda x: x[1])

def multi_start_local_search(target_array,first_solution_num,time):
    """
    多スタート局所探索方を行う

    Parametors:
    -----------
    target_array : int[]
        各個人の所要時間、0番目の0番目がAさんの英語にかかる時間、1番目の1番目がBさんの数学にかかる時間と言った感じ。

    first_solution_num: int
        いくつ初期解を生成するかを指定する

    time: int
        計算時間を指定する。終了条件として使う
    """
    time_limit = time #制限時間
    first_solutions = []
    for _ in range(first_solution_num):
        first_array = random_solution(target_array)
        first_solutions.append(local_search(target_array,first_array))

    print(first_solutions)
    return min(first_solutions, key=lambda x: x[1])
        

"""    
first_array = random_solution(target_array)
print(local_search(target_array,first_array))
"""

print(multi_start_local_search(target_array,3,0))

"""
for n in range(5):
    selectd_array = random_solution(target_array)
    calc_target_func(target_array,selectd_array)
    print(calc_target_func(target_array,selectd_array))
"""
    


