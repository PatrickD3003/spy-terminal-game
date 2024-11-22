import random
from map_data import raw_maps
from gameclear import gameclear
from gameover import gameover


WALK_PATH = 0
WALL = 1
DOOR = 2
BOX = 3
PLAYER = 4
ENEMY = 5
AROMA = 6
SHOES = 7
TRAP = 8
NOISE_METER = 0
MAX_NOISE = 20
STEP_COUNT = 0
GOAL_MONEY = 20000
GOAL_MONEY_FLAG = False



class Player:
    """
    プレイヤーを表すクラス。
    このクラスの必要な情報：
    ・現在いる全体マップの情報
    ・現在いる探索マップの情報(x,y)
    ・現在所持しているアイテム
    ・現在の歩数
    ・現在の所持金額
    """
    def __init__(self):
        self.my_item = {AROMA:0, SHOES:0}  # 所持しているアイテム
        self.step_cnt = 0  # 歩数
        self.money = 0  # 所持金額
        self.y_pos, self.x_pos = 1, 1
        self.y_room_pos, self.x_room_pos = 0, 0
        self.shoes_flag = 0

    def get_step_count(self):
        return self.step_cnt

    def get_current_pos(self): 
        """
        担当者：パトリック
        """
        return [[self.y_pos, self.x_pos], [self.y_room_pos, self.x_room_pos]]
    
    def update_player_pos(self, y_pos, x_pos):
        self.y_pos = y_pos
        self.x_pos = x_pos

    def add_step_cnt(self):
        self.step_cnt += 1
        
    def get_shoes_flag(self):
        return self.shoes_flag    

    def increase_shoes_flag(self):
        self.shoes_flag += 1
    
    def reset_shoes_flag(self):
        self.shoes_flag = 0
    
    def can_enter(self, room_map, input_y, input_x):
        exit_room = [[2,2],[3,1]]
        # 脱出部屋
        if input_y == len(room_map)-1 or input_x == len(room_map[input_y])-1:
            if GOAL_MONEY_FLAG == False and [self.y_room_pos, self.x_room_pos] in exit_room:
                print(f"金額が足りないため、脱出部屋ご利用できない。")
                return False
            else:
                return True

        return True
    
    def update_room(self, room_map, input_y, input_x): 
        # 上の部屋に移動する処理
        if input_y == 0:
            self.y_room_pos -= 1
            self.y_pos = len(room_map)-2
        # 下の部屋に移動する処理
        if input_y == len(room_map)-1:
            self.y_room_pos += 1
            self.y_pos = 1
        # 右の部屋に移動する処理
        if input_x == len(room_map[input_y])-1:
            self.x_room_pos += 1
            self.x_pos = 1
        # 左の部屋に移動する処理
        if input_x == 0:
            self.x_room_pos -= 1
            self.x_pos = len(room_map[input_y])-2
        # 歩数リセット
        self.step_cnt = 0

    def get_my_item(self):
        """
        担当者：パト
        """
        return self.my_item
    
    def get_current_money(self):
        """
        担当者：パトリック
        """
        return self.money
    
    def get_player_key(self):
        player_input_key = input("\nキーを半角小文字で入力してください\n(移動:[上:w,下:s,左:a,右:d] m:マップ i:アイテムを使う r:ルールを再表示)\n =>")
        return player_input_key
    
    def get_next_move(self, move_key):
        """
        担当者：町田
        プレイヤーの次の移動位置を返す関数
        現在地をコピーして、移動キーに応じて次の移動位置を返す
        引数：プレイヤーが入力した移動キー
        戻り値：次の移動位置
        """
        move_dict = {"w":[-1, 0], "s":[1, 0], "a":[0, -1], "d":[0, 1]}  # valuesは[y, x]
        temp_y_pos = self.y_pos
        temp_x_pos = self.x_pos

        temp_y_pos += move_dict[move_key][0]
        temp_x_pos += move_dict[move_key][1]
        
        return [temp_y_pos, temp_x_pos]

    def add_item(self, type):
        self.my_item[type] += 1
    
    def print_my_item(self):
        print(f"所持しているアイテム(アロマ:{self.my_item[AROMA]}個 靴:{self.my_item[SHOES]}個)")
        

    def use_item(self, room_class):
        """
        担当者：町田
        アイテムを使用する関数。
        この関数は、プレイヤーがIを入力するたびに呼び出される。
        アイテムの数を取得して使えるアイテムがあるか確認する。（アイテムがない場合はないことを表示して終了）
        ↓
        アイテムがある場合、どのアイテムを使うか選択する。
        ↓
        使用したアイテムの効果を処理する。
        ↓
        使ったアイテムの数を減らす。
        ↓
        終了

        """
        global NOISE_METER
        my_item = self.get_my_item()
        if my_item[AROMA] == 0 and my_item[SHOES] == 0:
            print("アイテムがありません。")
            print("終了します。")
            return
        
        while True:
            print(f"所持しているアイテム(アロマ:{my_item[AROMA]}個 靴:{my_item[SHOES]}個)")
            print("使うアイテムまたは終了を選択してください。")
            print("半角数字で入力してください 1:アロマ 2:靴 3:終了")
            Player_input = input()

            if Player_input == "1":
                if my_item[AROMA] == 0:
                    print("使用できるアロマがありません。")
                else:
                    print("アロマを使いました。騒音メーターが4減ります")
                    NOISE_METER -= 4      # ノイズメーターを4減らす
                    if NOISE_METER < 0:   # ノイズメーターが0未満になった場合は0にする  
                        NOISE_METER = 0
                    my_item[AROMA] -= 1   # アロマの数を1減らす
                    print_meter(NOISE_METER, MAX_NOISE)

            elif Player_input == "2":
                if my_item[SHOES] == 0:
                    print("使用できる靴がありません。")
                else:
                    print("靴を使いました。この部屋の歩数制限が5増えます")
                    room_class.increase_step_limit(5)
                    self.increase_shoes_flag()
                    # step_limit += 10 # 歩数制限を10増やす
                    my_item[SHOES] -= 1
            elif Player_input == "3":
                print("終了します。")
                return
            
            else:
                print("正しい数字を入力してください。")
                continue

    
class Building:
    """
    担当者：パトリック
    マップの全体を表すクラス。
    プレイヤーがどの部屋にいるかを記録
    部屋移動の処理
    プレイヤー移動処理
    """
    def __init__(self, player, maps):
        self.player = player
        self.maps = maps
    
    def show_current_loc(self, player_pos):
        """
        担当者：パトリック
        プレイヤーの最新位置を表示する
        """
        room_y = player_pos[1][0]
        room_x = player_pos[1][1]

        current_room = self.maps[room_y][room_x]
        # current_room.insert_player(player_y, player_x)
        current_room.print_room()

    def get_current_room(self, player_pos):
        room_y, room_x = player_pos[1]
        return self.maps[room_y][room_x]

    def check_termination(self, player_pos, room_class):
        """
        担当者：パトリック
        終了条件の確認
        """
        step_cnt = self.player.get_step_count() 
        step_limit = room_class.get_step_limit()
        
        if player_pos[1] == [3, 2]:  # 脱出部屋の場合
            print(f"脱出成功しました！おめでとうございます")
            print("")
            gameclear()
            print("")
            print("="*70)
            print(f"あなたが取り返した金額は : {self.player.get_current_money()}")
            print("="*70)
            print("")
            return True
        
        if step_cnt > step_limit:
            print(f"歩数制限を超えてしまった。。")
            print(f"GAME OVER (*_*) ")
            gameover()
            return True
        
        if NOISE_METER >= MAX_NOISE:
            print(f"うるさすぎて、敵にバレてしまった")
            print(f"GAME OVER (*_*) ")
            gameover()
            return True
        else:
            return False

        
    def process_player_key(self, input_key, money_list):
        """   
        担当者：米山、パトリック
        プレイヤーの入力を処理する関数
        """
        legal_movement = ["w", "a", "s", "d", "m", "i", "r"]
        movement_key = ["w", "a", "s", "d"]
        view_map_key = "m"
        use_item_key = "i"
        print_rule_key = "r"
        player_pos = self.player.get_current_pos()
        room_class = self.get_current_room(player_pos)

        if input_key not in legal_movement:
            print("受け付けられないキーです。再度入力してください")
        else: 
            if input_key in movement_key:  
                input_y, input_x = self.player.get_next_move(input_key)
                self.process_player_movement(player_pos, room_class, input_y, input_x, money_list)

            elif input_key == view_map_key:  # マップ表示のキー
                my_money = self.player.get_current_money()
                print_overall_map(money_list, my_money)
                
            elif input_key == use_item_key: # アイテムを使うキー
                self.player.use_item(room_class)

            elif input_key == print_rule_key: # ルールを表示するキー
                print_rule()

    def process_player_movement(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG

        process_movement_dict = {
            "no pass": self.no_pass,
            "walk": self.move_player,
            "door": self.change_room,
            "aroma": self.use_aroma_item,
            "shoes": self.use_shoes_item,
            "box": self.get_money,
            "trap": self.activate_trap
        }
        collision_check = self.collision_check(player_pos, input_y, input_x)
        process_movement_dict[collision_check](player_pos, room_class, input_y, input_x, money_list)

    def no_pass(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        print(f"障害物があるため進めない")
    
    def move_player(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        self.player.update_player_pos(input_y, input_x)
        self.around_enemy_search(self.player, room_class)
        self.player.add_step_cnt()
    
    def change_room(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        room_data = room_class.get_room_map()
        flag = self.player.get_shoes_flag()
        room_class.increase_step_limit(flag*(-10))
        self.player.reset_shoes_flag()
        can_enter = self.player.can_enter(room_data, input_y, input_x)
        if can_enter:
            room_class.delete_random_trap() # トラップを消す
            self.player.update_room(room_data, input_y, input_x)
            room_class = self.get_current_room(self.player.get_current_pos())
            room_class.generate_random_trap()
            room_class.loc_random_trap()
            NOISE_METER += 1 
        else:
            print(f"cannot enter")
    
    def use_aroma_item(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        self.player.add_item(AROMA)
        self.player.update_player_pos(input_y, input_x)
        self.around_enemy_search(self.player, room_class)
        self.player.add_step_cnt()
    
    def use_shoes_item(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        self.player.add_item(SHOES)
        self.player.update_player_pos(input_y, input_x)
        self.around_enemy_search(self.player, room_class)
        self.player.add_step_cnt()
    
    def get_money(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        y, x = self.player.get_current_pos()[1]
        print(f"{money_list[y][x]}獲得しました")
        self.player.money += money_list[y][x]
        self.player.update_player_pos(input_y, input_x)
        self.around_enemy_search(self.player, room_class)
        self.player.add_step_cnt()
        if self.player.money >= GOAL_MONEY:
            GOAL_MONEY_FLAG = True

    def activate_trap(self, player_pos, room_class, input_y, input_x, money_list):
        global NOISE_METER, GOAL_MONEY_FLAG
        # ※トラップを踏んだ際に消えてしまっているので、トラップの位置を表示する処理を追加する必要があるかも！！
        self.player.update_player_pos(input_y, input_x)
        self.around_enemy_search(self.player, room_class)
        trap_event()
        self.player.add_step_cnt()
            
    def collision_check(self, player_pos, input_y, input_x):
        """
        担当者：町田
        改良：パト
        プレイヤーが入力した方向に進めるか判断する関数
        引数：プレイヤーが次に進む座標
        判定: 壁（Wall）かどうか 敵（Enemy）かどうか
        """
        room_map = self.get_current_room(player_pos).get_room_map()
        collision_dict = {
            WALK_PATH : "walk",
            DOOR : "door",
            SHOES : "shoes",
            AROMA : "aroma",
            BOX : "box",
            TRAP : "trap"
        }

        if room_map[input_y][input_x] in [WALL, ENEMY]:
            print("壁です。進めません。")
            return "no pass"
        else:
            return collision_dict.get(room_map[input_y][input_x], "no pass")        

    def around_enemy_search(self, player, room_class):
        """
        担当者：米山
        プレイヤーの周りに敵がいるかを探し、いたら騒音メーターを上昇させる関数
        この関数は、プレイヤーが移動した後に呼び出される
        引数： room_map=マップ情報
        """
        global NOISE_METER
        room_map = room_class.get_room_map()
        current_pos = player.get_current_pos()
        current_y = current_pos[0][0]
        current_x = current_pos[0][1]
        move_list = [[current_y-1,current_x-1],[current_y-1,current_x],
                     [current_y-1,current_x+1],[current_y,current_x-1],
                     [current_y,current_x+1],[current_y+1,current_x],
                     [current_y+1,current_x-1],[current_y+1,current_x+1]]
        
        for i in range(len(move_list)):
            y = move_list[i][0]
            x = move_list[i][1]
            if room_map[y][x] == ENEMY:
                NOISE_METER += 1

class Room:
    """
    各部屋を表すクラス。
    このクラスの必要な情報：
    ・部屋の探索マップの情報(２次元配列)
    ・部屋の番号
    ・部屋の歩数制限
    ・ドア位置をキーとし、移動先の位置と部屋番号を値とする辞書
    ・ランダムトラップの数
    ・金庫の金額
    """
    def __init__(self, room_map, step_limit, random_trap_num):
        self.room_map = room_map
        self.step_limit = step_limit
        self.random_trap_num = random_trap_num
        self.random_trap_array = []
        self.pasty = None
        self.pastx = None

    def get_room_map(self):
        """
        担当者：パトリック
        部屋の２次元リストを返す関数
        """
        return self.room_map

    def increase_step_limit(self, amount):
        self.step_limit += amount

    def get_step_limit(self):
        return self.step_limit

    def insert_player(self, player_y, player_x):
        """
        担当者：パトリック
        プレイヤーをマップの中に入れる
        """
        if (self.pasty is not None) and (self.pastx is not None):
            if (self.pasty != player_y) or (self.pastx != player_x):
                self.room_map[self.pasty][self.pastx] = WALK_PATH
        if self.room_map != "脱出部屋":
            self.room_map[player_y][player_x] = PLAYER
        self.pasty = player_y
        self.pastx = player_x

    def print_room(self):
        """
        マップを画面にプリントする関数
        """
        symbols = {WALL: "# ", WALK_PATH: "  ", AROMA: "A ", 
                SHOES: "S ", DOOR: "D ", PLAYER: "P ", 
                BOX: "B ", ENEMY: "E ", TRAP: "T "}

        print("\n現在の部屋：")
        len_row = len(self.room_map)
        len_column = len(self.room_map[0])

        for i in range(len_row):
            row = [
                self.colorize_symbol(symbols.get(self.room_map[i][j], " ")) 
                for j in range(len_column)
            ]
            print("".join(row))

    def colorize_symbol(self, symbol):
        """
        テキスト出力を色つける
        """
        symbol_color_dict = {"P ": f"\x1b[38;5;158m{symbol}\033[0m",  # 黄緑
                             "A ": f"\033[1;34m{symbol}\033[0m",  # 青
                             "S ": f"\033[1;34m{symbol}\033[0m",  # 青
                             "B ": f"\033[1;33m{symbol}\x1b[0m",  # 黄色
                             "E ": f"\033[1;31m{symbol}\033[0m" ,  # 赤
                             "T ": f"\x1b[38;5;208m{symbol}\033[0m",  # オレンジ
                             "D ": f"\033[1;32m{symbol}\033[0m",  # 茶色
                             "# ": f"\x1b[38;5;15m{symbol}\033[0m"}  # グレー
        
        if symbol in symbol_color_dict.keys():
            return symbol_color_dict[symbol]
        else:
            return symbol 
        
    def generate_random_trap(self):
        trap = self.random_trap_num
        room_map = self.room_map
        can_walk = []
        if trap>0:
            for y in range(len(room_map)):
                for x in range(len(room_map[0])):
                    if room_map[y][x] == WALK_PATH:
                        can_walk.append((y,x))
            self.random_trap_array = random.sample(can_walk,k=trap)
        else:
            self.random_trap_array = []
    
    def loc_random_trap(self):
        random_trap_array = self.random_trap_array
        room_map = self.room_map
        if random_trap_array:
            for i in range(len(random_trap_array)):
                room_map[random_trap_array[i][0]][random_trap_array[i][1]] = TRAP

    def delete_random_trap(self):
        room_map = self.room_map
        random_trap_pos_array = self.random_trap_array
        if random_trap_pos_array:
            for i in range(len(random_trap_pos_array)):
                x = random_trap_pos_array[i][1]
                y = random_trap_pos_array[i][0]
                room_map[y][x] = WALK_PATH


def process_raw_map(raw_data):
    """
    担当者：パトリック
    map_dataファイルから輸入したraw_maps変数を加工して、
    部屋のクラスの２次元リストに変換する関数。
    """
    processed_map = []
    for row in range(len(raw_data)):
        col_lst = []
        for column in raw_data[row]:
            room_map, step_limit, random_trap_num = column
            room = Room(room_map, step_limit, random_trap_num)
            col_lst.append(room)
        processed_map.append(col_lst)

    return processed_map

def print_overall_map(money_list,curent_get_money):
    """
    担当者：町田
    全体マップを表示する関数。
    この関数は、プレイヤーがMを入力するたびに呼び出される。
    引数でdivided_money関数で作成したroom_money_listを受け取る。
    また、プレイヤーが現在所持している金額を受け取る。
    """
    print("~全体(金額)マップ~")
    print("----------------")
    print(f"|{money_list[0][0]}|{money_list[0][1]}|{money_list[0][2]}|")
    print("----------------")
    print(f"|{money_list[1][0]}|{money_list[1][1]}|{money_list[1][2]}|")
    print("----------------")
    print(f"|{money_list[2][0]}|{money_list[2][1]}|{money_list[2][2]}|")
    print("----------------")
    print(f"|{money_list[3][0]}|{money_list[3][1]}|\x1b[32mgoal\033[0m|")
    print("----------------")
    print(f"目標金額：{GOAL_MONEY}")
    print(f"所持金額：{curent_get_money}")

def print_meter(current, limit):
    """
    担当者：町田
    ノイズメーターを表示する関数。
    この関数は、プレイヤーが移動するたびに呼び出される。
    現在のマップの上に表示される。
    引数でプレイヤーのノイズメーターの値を受け取る。
    """
    current_cpy = current
    for i in range(1,limit + 1):
        if current > 0:
            print(color_meter("■", current_cpy, limit), end="")
            current -= 1
        else:
            print("□", end="")
        if i % 5 == 0:
            if i != 0:
                print("|", end="")  # 5個ごとに区切り線を表示

def color_meter(symbol, current, limit):
    """
    騒音メーターがMAX_NOISEの5割以下なら、緑になり、
    ５割以上、7割以下なら、黄色になり、
    それ以上は赤になる。
    """
    if current <= limit * 0.5:
        return f"\033[32m{symbol}\033[0m"
    elif 0.5 <= current <= limit * 0.7:
        return f"\x1b[33m{symbol}\033[0m"
    else:
        return f"\033[31m{symbol}\033[0m"

def divide_money():
    """
    担当者：町田
    各部屋の金庫にランダムに金額を振り分ける関数。
    この関数は、ゲーム開始時に呼び出される。
    """
    money_list = [1500, 1500, 2000, 2000, 2500, 3000, 3000, 3000, 4000, 5000, 5000]
    random.shuffle(money_list)
    room_money_list = [[],[],[],[]]
    j = 0
    for i in range(11):
        if i == 3 or i == 6 or i == 9:
            j += 1
        room_money_list[j].append(money_list[i])
    # print(room_money_list)  # 動作確認

    return room_money_list

def print_rule():
    
    print("""
---ゲーム説明---
[ストーリー]
プレイヤーはスパイとなり、組織に奪われたお金を回収するためにアジトに潜入します
目標金額を集め,脱出を目指します
お金は金庫(B)を踏むことで入手できます

\033[32m[勝利条件](どちらも満たす)\033[0m
1. 目標金額を集める
2. 脱出部屋に到着する

\033[31m[敗北条件](どちらかを満たす)\033[0m
1. 部屋ごとの歩数制限を超える
2. 騒音メーターが20に達する

[騒音メーターの上がり方]
1. トラップ(T)のマスで騒音メーターがランダムに上昇します(0~5)
2. 敵(E)の周囲1マスを通るごとに騒音メーターが1上昇します
3. ドア(D)に到達し別の部屋に移動すると騒音メーターが1上昇します

[歩数制限]
1. 1マス進むごとに+1されます
2. 部屋ごとに歩数制限の値は異なります
3. 部屋を移動すると現在の歩数はリセットされます

[アイテム]
シューズ(S)：歩数制限を5増加
アロマ(A)：騒音メーターを4減少

[注意事項]
・左上の部屋からのスタートです
・アイテム、金庫は1度入手するとマップから消えます
・壁(#)や敵(E)のマスは通れません
・現在いるマップ番号は知ることができないので覚えてください
・騒音メーターは0以下になりません
""")


def print_map_info():
    """
    担当者：町田
    マップの情報を表示する関数
    """
    print("\n")

    print("オブジェクトの説明 (\x1b[38;5;15m#\033[0m:壁 \033[1;34mA\033[0m:アロマ \033[1;34mS\033[0m:靴 \033[1;32mD\033[0m:ドア \033[1;33mB\x1b[0m:金庫 \033[1;31mE\033[0m:敵 \x1b[38;5;208mT\033[0m:トラップ \x1b[38;5;158mP\033[0m:プレイヤー)")

def trap_event():
    """
    担当者：米山
    トラップを踏んだ時に呼び出される関数
    ランダムで騒音メーターが上昇する
    """
    global NOISE_METER
    add = random.randint(0,5)
    print(f"{add}増加した")
    NOISE_METER += add

def play_game():
    """
    担当者：パトリック
    """
    # 色々初期化
    maps = process_raw_map(raw_maps)  # 全体マップの初期化
    player = Player()  # プレイヤークラスの初期化
    building = Building(player, maps)

    # ルールの表示
    print_rule()
    # 金額の割り振る
    money_list = divide_money()
    my_money = player.get_current_money()
     # 全体マップの表示
    print_overall_map(money_list, my_money)

    # 最初のゲーム表示
    player_pos = player.get_current_pos()
    current_room_class = building.get_current_room(player_pos)
    current_room_class.generate_random_trap()
    current_room_class.loc_random_trap()
    current_room_class.insert_player(player_pos[0][0], player_pos[0][1])
    building.show_current_loc(player_pos)
    print_map_info()

    while True:
        # プレイヤーの入力を求める
        player_key = player.get_player_key() 

        flag = building.process_player_key(player_key, money_list)
        if flag == True:
            continue
        player_pos = player.get_current_pos()
        current_room_class = building.get_current_room(player_pos)
        
        # 勝利条件の初期化
        if building.check_termination(player_pos, current_room_class):
            break
        
        # マップを更新と表示
        current_room_class.insert_player(player_pos[0][0], player_pos[0][1])  # プレイヤーをマップの中に入れる
        building.show_current_loc(player_pos) 

        # 騒音メーター処理
        # building.around_enemy_search(player, current_room_class)
        current_noise = NOISE_METER
        max_noise = MAX_NOISE
        print_map_info()
        print_meter(current_noise, max_noise)
        print("")  
        print(f"騒音メーター：{NOISE_METER}/{MAX_NOISE}")


        # 歩数制限の表示(仮)担当：町田
        step_cnt = player.get_step_count()
        step_limit = building.get_current_room(player_pos).get_step_limit()
        print_meter(step_cnt, step_limit)
        print("")
        print(f"歩数制限：{step_cnt}/{step_limit}")
        print("")
        print(f"所持金額:{player.get_current_money()}")

if __name__ == "__main__":
    play_game()