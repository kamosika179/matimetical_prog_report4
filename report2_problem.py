
import random

#問題3用

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

    for index in random_sequence_list:
        if items[index].weight + tmp_wight < Item.restrict:
            selected_items.append(items[index])
            tmp_wight += items[index].weight
            tmp_value += items[index].value
            items[index].is_selected = True
    
    #print(selected_items)

    return selected_items

def print_weight_and_value_sum(selected_items):
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
        weight_sum += item.weight
        value_sum += item.value
    
    print(f"重さの合計は:{weight_sum}\n価値の合計は:{value_sum}")

    return (weight_sum,value_sum)



tmp = set_items(alpha_item_info,alpha_restrict)

selec = random_first_solution(tmp)

print_weight_and_value_sum(selec)