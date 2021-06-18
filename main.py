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

    # レーティング値を追加
    if const != 'NA':
        new_data['rating'] = format(const * ratio, '.2f')
    else:
        new_data['rating'] = 'NA'
    
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

    for const in const_list:
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

    # 定数データのないスコアデータに対応
    for score in score_list:
        add_data_to_list(data_list, score[0], 'NA', 'NA', 'EXP', 'NA', int(score[3]))
        if score[4] != '0':
            # infernoがある曲なのでさらに要素を追加
            add_data_to_list(data_list, score[0], 'NA', 'NA', 'INF', 'NA', int(score[4]))

    return data_list


# listの中身を整形して出力
def print_list(list):
    for row in list:
        if row['difficulty'] == 'INF':
            print(row['title'] + ' (INF)')
        else:
            print(row['title'])
        print("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row['version'], row['genre'], row['difficulty'], row['const'], row['score'], row['rating']))


def main():
    data_list = make_list()
    print_list(data_list)


if __name__ == "__main__":
    main()