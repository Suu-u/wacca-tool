import csv


# listに楽曲データを追加
def add_data_to_list(data_list, title, version, genre, difficulty, const, score):
    new_data = {}
    new_data['title'] = title
    new_data['version'] = version
    new_data['genre'] = genre
    new_data['difficulty'] = difficulty
    new_data['const'] = const
    new_data['score'] = score

    # スコアから倍率計算
    ratio = 0
    if score == 1000000:
        ratio = 4.0
    elif score >= 940000:
        ratio = (score - 940000) // 10000 * 0.25 + 2.75
    elif score >= 900000:
        ratio = (score - 900000) // 20000 * 0.5 + 2
    elif score >= 800000:
        ratio = (score - 800000) // 50000 * 0.5 + 1
    elif ratio > 0:
        ratio = score // 100000 * 0.1 + 0.1
    else:
        ratio = 0

    new_data['rating'] = round(const * ratio, 2)
    
    data_list.append(new_data)


# 定数・スコアを読み込んでlistを作成
def make_list():
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

    for const in reversed(const_list):
        is_played = False
        for score in score_list:
            if const[0] == score[0]:
                # プレイ済なので要素を追加
                is_played = True
                add_data_to_list(data_list, const[0], const[1], const[2], 'EXP', float(const[3]), int(score[3]))
                if const[4] != 'NA':
                    # infernoがある曲なのでさらに要素を追加
                    add_data_to_list(data_list, const[0], const[1], const[2], 'INF', float(const[4]), int(score[4]))
                score_list.remove(score)
                break
        if not is_played:
            add_data_to_list(data_list, const[0], const[1], const[2], 'EXP', float(const[3]), 0)

    # 定数データのないスコアデータに対応 (定数を-1として処理)
    for score in score_list:
        add_data_to_list(data_list, score[0], 'NA', 'NA', 'EXP', -1, int(score[3]))
        if score[4] != '0':
            # infernoがある曲なのでさらに要素を追加
            add_data_to_list(data_list, score[0], 'NA', 'NA', 'INF', -1, int(score[4]))

    return data_list


# listの中身を整形して出力
def print_list(list):
    for row in list:
        if row['difficulty'] == 'INF':
            print(row['title'] + ' (INF)')
        else:
            print(row['title'])
        print("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row['version'], row['genre'], row['difficulty'], row['const'], row['score'], row['rating']))


# レート対象曲・候補曲を表示
def show_ratings(data_list):
    # プレイ済みの楽曲データを単曲レート降順でソート
    rate_list = [data for data in data_list if data['score'] > 0 and data['const'] > 0]
    rate_list = sorted(rate_list, key=lambda x: x['rating'], reverse=True)

    new_value = 0
    old_value = 0
    new_list = []
    old_list = []

    for data in rate_list:
        if data['version'] == 'R':
            if len(new_list) < 15:
                new_value += data['rating']
                new_list.append(data)
                data_list.remove(data)
            else:
                break
    
    for data in rate_list:
        if data['version'] != 'R':
            if len(old_list) < 35:
                old_value += data['rating']
                old_list.append(data)
                data_list.remove(data)
            else:
                break

    print("Rating: {:.3f}\n".format(new_value + old_value))
    print("--- 新枠 対象曲 (average: {:.3f})\n".format(new_value / 15))
    print_list(new_list)
    print("--- 旧枠 対象曲 (average: {:.3f})\n".format(old_value / 35))
    print_list(old_list)



def main():
    data_list = make_list()
    show_ratings(data_list)


if __name__ == "__main__":
    main()