
import random


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
        Itemオブジェクトの集合

    Return:
    ---------
    first_solution:
        ランダムな初期解
    '''
    random_sequience_list = list(range(len(items)))
    random.shuffle(random_sequience_list)

    tmp_value = 0
    tmp_wight = 0
    selected_items = []

    for index in random_sequience_list:
        if items[index].weight + tmp_wight < Item.restrict:
            selected_items.append(items[index])
            tmp_wight += items[index].weight
            tmp_value += items[index].value
            items[index].is_selected = True
    
    print(selected_items)


tmp = set_items(alpha_item_info,alpha_restrict)
random_first_solution(tmp)