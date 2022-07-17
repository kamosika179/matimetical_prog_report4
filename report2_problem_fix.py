
import random
import copy


#問題4用 改良版

alpha_item_info = [[3,7],[6,12],[5,9],[4,7],[8,13],[5,8],[3,4],[4,5]]
alpha_restrict = 25

beta_item_info = [[3,7],[6,12],[5,9],[4,7],[8,13],[5,8],[3,4],[4,5],[3,3],[5,10],[6,7],[4,5],[8,6],[7,14],[11,5],[8,9],[14,6],[6,12],[12,5],[4,9]]
beta_restrict = 55

class Item:
    
    restrict = 0#重さの制限
    is_selected = False #選択されたかどうか
    def __init__(self,name,weight,value):
        self.name = name #荷物の番号
        self.weight = weight #荷物の重さ
        self.value = value #荷物の価格
    
def set_items(item_info,item_restrict):
    '''
    Itemオブジェクトのリストを作成し、返す

    Parameter:
    ------------
    item_info
            アイテムの情報をリストで表したもの、0番目に重さ、1番目に価値を持つリストの集合
    item_restrict
            重さの制限を指定する
    Return:
    -----------
    items
        itemオブジェクトのリスト
    '''
    items = []

    for num,i in enumerate(item_info):
        items.append(Item(name=num+1,weight=i[0],value=i[1]))

    Item.restrict = item_restrict
    return items

def random_first_solution(items):
    '''
    ランダムに初期解を生成する

    Parameter:
    ----------
    items: 
        Itemオブジェクトのリスト

    Return:
    ---------
    first_solution:
        ランダムな初期解
    '''
    random_sequence_list = list(range(len(items)))
    random.shuffle(random_sequence_list)

    tmp_value = 0
    tmp_wight = 0
    selected_items = []

    new_list = copy.deepcopy(items)
    for index in random_sequence_list:
        if new_list[index].weight + tmp_wight <= Item.restrict:
            tmp_wight += items[index].weight
            tmp_value += items[index].value
            new_list[index].is_selected = True
    
    #print(selected_items)

    return new_list

def calc_weight_and_value_sum(selected_items):
    '''
    アイテムの重さと価値の合計値を返す

    Parameter:
        selected_items: List<Item>
            アイテムのリスト
    
    Return:
        weight_and_value_sum: tuple
            重さと価値のタプル
    '''

    weight_sum = 0
    value_sum = 0
    for item in selected_items:
        if item.is_selected == True:
            weight_sum += item.weight
            value_sum += item.value
    
    #print(f"重さの合計は:{weight_sum}\n価値の合計は:{value_sum}")

    return (weight_sum,value_sum)

def perturbation(selected_list,change_num):
    '''
    摂動を行う。
    左から順番に一つずつ選択するアイテムを変更していく(n回,合計n通りの選択が作られる)
    このときにすでに選択したアイテムを選択しないように注意する

    Parameter:
        selected_list: List<Item>
            選択されたアイテムのリスト
        change_num: Int
            変更するアイテムの数（作成する通りの数）
    Return :
        return_list: List<Item>
            摂動によって得られて一番良い組み合わせ
    '''
    
    new_lists = []
    return_list = copy.deepcopy(selected_list) #戻り値、最も価値の大きかった組み合わせが入る
    for _ in range(change_num):
        new_lists.append(copy.deepcopy(selected_list))

    now_weight,now_value = calc_weight_and_value_sum(selected_list) #現在の重さ
    afford_weight = Item.restrict - now_weight #残り入る量

    #順番に選択するアイテムを変更する
    for order,now_list in enumerate(new_lists):
        selected_items = [x for x in now_list if x.is_selected == True]  #選択されたアイテムを取りだす
        selected_item_name = selected_items[order].name #取り出すアイテム名を探す
        afford_weight += selected_items[order].weight

        unselected_items = [x for x in now_list if x.is_selected == False and x.weight <= afford_weight] #選択されなかった要素を取り出す
        
        unselected_items = sorted(unselected_items,key=lambda x:x.value,reverse=True) #fix 価値の高い順に並び替える
        
        #新しく入れるアイテムを探す
        if len(unselected_items) == 0:
            get_item_name = None
        else:
            get_item_name = unselected_items[0].name #入れるアイテムを選択する

        #is_selectedを変更する
        if get_item_name != None:
            for item in now_list:
                if item.name == selected_item_name:
                    item.is_selected = False
                if item.name == get_item_name:
                    item.is_selected = True

            tmp_value = 0
            tmp_weight = 0
            for item in now_list:  
                if item.is_selected == True:
                    tmp_value += item.value
                    tmp_weight += item.weight
            #価値を更新しているか調べる
            if tmp_value > now_value:
                now_value = tmp_value
                return_list = copy.deepcopy(now_list)
        afford_weight = Item.restrict - now_weight

    return return_list
    calc_weight_and_value_sum(return_list)
        
def multi_local_search(item_info,item_restrict,count):
    """
    局所探索を行う
    Parametor:
    item_info
        アイテムの情報をリストで表したもの、0番目に重さ、1番目に価値を持つリストの集合
    item_restrict
        重さの制限を指定する
    count
        初期解の数
    """
    first_solutions_weight_and_value = []
    result_local_search_weight_and_value = []
    change_num = 3
    for order in range(count):
        tmp_items = set_items(alpha_item_info,alpha_restrict)
        random_items = random_first_solution(tmp_items)
        now_weight = calc_weight_and_value_sum(random_items)[0]
        now_value = calc_weight_and_value_sum(random_items)[1]
        first_solutions_weight_and_value.append((now_weight,now_value))

        tmp_list = copy.deepcopy(random_items)
        is_finish = False
        while(is_finish == False):
            #すべての値を入れ替えるようにする
            change_num = 0 
            for t in tmp_list:
                if t.is_selected == True:
                    change_num += 1
            tmp_list = perturbation(tmp_list,change_num)
            tmp_weight,tmp_value = calc_weight_and_value_sum(tmp_list)
            if tmp_value <= now_value:
                is_finish = True
                result_local_search_weight_and_value.append((tmp_weight,tmp_value))
            else:
                now_value = tmp_value
        

    #first_solutions_weight_and_values,result_local_search_weight_and_valueをまとめる
    first_solutions_weight_and_value = sorted(first_solutions_weight_and_value, key=lambda x: x[1])
    print(f"初期解の中で最良の価値と、最悪の価値\n最悪の価値:{first_solutions_weight_and_value[0][1]}\n最良の価値:{first_solutions_weight_and_value[-1][1]}")
    result_local_search_weight_and_value = sorted(result_local_search_weight_and_value,key=lambda x:x[1])
    print(f"最終解の中で最良の価値と、最悪の価値\n最悪の価値:{result_local_search_weight_and_value[0][1]}\n最良の価値:{result_local_search_weight_and_value[-1][1]}")


counts = [5,10,20]

print("αの問題を解く")
for c in counts:
    print(f"初期解の数:{c}")
    multi_local_search(alpha_item_info,alpha_restrict,c)
    print("\n")


print("\n")
print("βの問題を解く")
for c in counts:
    print(f"初期解の数:{c}")
    multi_local_search(beta_item_info,beta_restrict,c)
    print("\n")