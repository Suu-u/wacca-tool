import csv

# wacca_const.csvの読み込み
# [title, version, genre, e_const, i_const]
const_file = open('wacca_const.csv', 'r')
fc = csv.reader(const_file)
header = next(fc)
const_list = []
for row in fc:
    const_list.append(row)

# wacca_score.csvの読み込み
# [title, n_score, h_score, e_score, i_score]
score_file = open('wacca_score.csv', 'r')
fs = csv.reader(score_file)
header = next(fs)
score_list = []
for row in fs:
    score_list.append(row)

data_list = []
for const in const_list:
    is_played = False
    for score in score_list:
        if const[0] == score[0]:
            # プレイ済なので要素を追加
            is_played = True
            new_data = {}
            new_data['title'] = const[0]
            new_data['version'] = const[1]
            new_data['genre'] = const[2]
            new_data['difficulty'] = 'E'
            new_data['score'] = int(score[3])
            new_data['const'] = float(const[3])
            # （ここでレート値計算）
            data_list.append(new_data)
            if const[4] != 'NA':
                # infernoがある曲なのでさらに要素を追加
                new_data2 = {}
                new_data2['title'] = const[0]
                new_data2['version'] = const[1]
                new_data2['genre'] = const[2]
                new_data2['difficulty'] = 'I'
                new_data2['score'] = int(score[4])
                new_data2['const'] = float(const[4])
                # （ここでレート値計算）
                data_list.append(new_data2)
            score_list.remove(score)
            break
    if not is_played:
        new_data = {}
        new_data['title'] = const[0]
        new_data['version'] = const[1]
        new_data['genre'] = const[2]
        new_data['difficulty'] = 'E'
        new_data['score'] = 0
        new_data['const'] = float(const[3])

# 定数データのないスコアデータに対応
for score in score_list:
    new_data = {}
    new_data['title'] = score[0]
    new_data2['version'] = 'NA'
    new_data2['genre'] = 'NA'
    new_data2['difficulty'] = 'I'
    new_data2['score'] = int(score[3])
    new_data2['const'] = 'NA'
    data_list.append(new_data)
    if const[4] != 'NA':
        # infernoがある曲なのでさらに要素を追加
        new_data2 = {}
        new_data2['title'] = const[0]
        new_data2['version'] = const[1]
        new_data2['genre'] = const[2]
        new_data2['difficulty'] = 'I'
        new_data2['score'] = int(score[4])
        new_data2['const'] = 'NA'
        data_list.append(new_data2)

print(data_list)
