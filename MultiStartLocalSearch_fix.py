
import random
import time


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
    min_combination : (int[],int)
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

def multi_start_local_search(target_array,first_solution_num,time_limit):
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

    start_time = time.perf_counter()

    first_solutions = [] #初期解が入る
    solutions = [] #各々、局所探索法をした結果が入る
    for _ in range(first_solution_num):
        first_array = random_solution(target_array)
        first_solutions.append(first_array)
        solutions.append(local_search(target_array,first_array))

        now_time = time.perf_counter()
        if (now_time-start_time) > time_limit:
            break

    print("初期解の中で最良の解と、最悪の解")
    first_solution_values =[]
    for sol in first_solutions:
        tmp_val = calc_target_func(target_array,sol)
        first_solution_values.append(tmp_val)
    
    bad_solution_value = max(first_solution_values)
    bad_solution_index =  first_solution_values.index(bad_solution_value)
    good_solution_value = min(first_solution_values)
    good_solution_index = first_solution_values.index(good_solution_value)

    print("最悪の解、その時の値")
    print(first_solutions[bad_solution_index])
    print(bad_solution_value)

    print("最良の解、その時の値")
    print(first_solutions[good_solution_index])
    print(good_solution_value)

    print("------------")

    if len(solutions) == 0:
        print("時間が短すぎます")
    else:
        print("最終解の中での最良の解と、最悪の解")
        print("最悪の解、その時の値")
        tmp_max = max(solutions, key=lambda x: x[1])
        print(tmp_max[0])
        print(tmp_max[1])

        print("最良の解、その時の値")
        tmp_mix = min(solutions, key=lambda x: x[1])
        print(tmp_mix[0])
        print(tmp_mix[1])
        

multi_start_local_search(target_array,5,10)
