import csv

VERSION = '1.2.1'
UPDATE_DATE = '2021/09/09'


# listに楽曲データを追加
def add_data_to_list(data_list, title, genre, difficulty, version, const, score):
    new_data = {}
    new_data['title'] = title
    new_data['genre'] = genre
    new_data['difficulty'] = difficulty
    new_data['version'] = version
    new_data['const'] = const
    new_data['score'] = score

    # スコアから倍率計算
    if score == 1000000:
        ratio = 4.0
    elif score >= 940000:
        ratio = (score - 940000) // 10000 * 0.25 + 2.75
    elif score >= 900000:
        ratio = (score - 900000) // 20000 * 0.5 + 2
    elif score >= 800000:
        ratio = (score - 800000) // 50000 * 0.5 + 1
    elif score > 0:
        ratio = score // 100000 * 0.1 + 0.1
    else:
        ratio = 0

    if const != 'NA':
        new_data['rating'] = round(const * ratio, 2)
    else:
        new_data['rating'] = 0

    data_list.append(new_data)


# 定数・スコアを読み込んでlistを作成
def make_list():
    # wacca_const.csvの読み込み
    # CSV: title, version, genre, h_const, e_const, i_const, i_version
    # これを、以下の構造のリストに整形して格納
    # [title, genre, [version, h_const], [version, e_const], [version, i_const]]
    const_file = open('wacca_const.csv', 'r', encoding='utf-8')
    fc = csv.reader(const_file)
    header = next(fc)
    const_list = []
    for row in fc:
        new_data = [row[0], row[2]]
        new_data.append([row[1], row[3]])
        new_data.append([row[1], row[4]])
        if row[5] != 'NA':
            if row[6] != 'NA':
                new_data.append([row[6], row[5]])
            else:
                new_data.append([row[1], row[5]])
        else:
            new_data.append('NA')
        const_list.append(new_data)

    # wacca_score.csvの読み込み
    # CSV: title, n_score, h_score, e_score, i_score
    # この順のままリストにして格納
    score_file = open('wacca_score.csv', 'r', encoding='utf-8')
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
                if const[2] != 'NA': # hard
                    add_data_to_list(data_list, const[0], const[1], 'HRD', const[2][0], float(const[2][1]), int(score[2]))
                if const[3] != 'NA': # expert
                    add_data_to_list(data_list, const[0], const[1], 'EXP', const[3][0], float(const[3][1]), int(score[3]))
                if const[4] != 'NA': # inferno
                    add_data_to_list(data_list, const[0], const[1], 'INF', const[4][0], float(const[4][1]), int(score[4]))
                score_list.remove(score)
                break
        if not is_played:
            # 未プレイなのでスコアを0にして要素を追加
            if const[2] != 'NA': # hard
                add_data_to_list(data_list, const[0], const[1], 'HRD', const[2][0], float(const[2][1]), 0)
            if const[3] != 'NA': # expert
                add_data_to_list(data_list, const[0], const[1], 'EXP', const[3][0], float(const[3][1]), 0)
            if const[4] != 'NA': # inferno
                add_data_to_list(data_list, const[0], const[1], 'INF', const[4][0], float(const[4][1]), 0)

    # 定数データのないスコアデータを定数を'NA'にして追加
    no_const_num = 0
    for score in score_list:
        if score[2] != '0': # hard
            no_const_num += 1
            add_data_to_list(data_list, score[0], 'NA', 'HRD', 'NA', 'NA', int(score[2]))
        if score[3] != '0': # expert
            no_const_num += 1
            add_data_to_list(data_list, score[0], 'NA', 'EXP', 'NA', 'NA', int(score[3]))
        if score[4] != '0': # inferno
            no_const_num += 1
            add_data_to_list(data_list, score[0], 'NA', 'INF', 'NA', 'NA', int(score[4]))
    if no_const_num > 0:
        print("[NOTICE] {} song have no const data. Rating may be incorrect value. Please check if your 'wacca_const.csv' is the newest version.\n".format(no_const_num))

    return data_list


# listの中身を整形して出力
def print_list(list):
    for row in list:
        if row['difficulty'] == 'HRD':
            print(row['title'] + ' (HRD)')
        elif row['difficulty'] == 'INF':
            print(row['title'] + ' (INF)')
        else:
            print(row['title'])
        print("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row['version'], row['genre'], row['difficulty'], row['const'], row['score'], row['rating']))


# レート対象曲・候補曲を表示
def show_ratings(data_list):
    # プレイ済みの楽曲データを単曲レート降順でソート
    tmp_list = [data for data in data_list if data['rating'] > 0]
    tmp_list = sorted(tmp_list, key=lambda x: (int)(x['rating']/0.1)*0.1, reverse=True)

    new_value = 0
    old_value = 0
    new_list = []
    old_list = []
    new_list_len = 0
    old_list_len = 0
    new_candidate_list = []
    old_candidate_list = []

    # 新枠対象曲を追加
    for data in tmp_list[:]:
        if data['version'] == 'Re':
            if new_list_len < 15:
                new_value += data['rating']
                new_list.append(data)
                tmp_list.remove(data)
                new_list_len += 1
            else:
                break
    
    # 旧枠対象曲を追加
    for data in tmp_list[:]:
        if data['version'] != 'Re':
            if old_list_len < 35:
                old_value += data['rating']
                old_list.append(data)
                tmp_list.remove(data)
                old_list_len += 1
            else:
                break

    if (new_list_len == 15):
        # 新枠候補曲を追加
        for data in tmp_list:
            if data['version'] == 'Re' and data['score'] < 990000:
                if len(new_candidate_list) < 10 and data['const'] * 4.0 >= new_list[14]['rating']:
                    new_candidate_list.append(data)
                else:
                    break
    else:
        # 新枠が埋まりきっていないので空データを追加
        for i in range(len(new_list), 15):
            add_data_to_list(new_list, "Not played", 'NA', 'NA', 'NA', 0, 0)

    if (old_list_len == 35):
        # 旧枠候補曲を追加
        for data in tmp_list:
            if data['version'] != 'Re' and data['score'] < 990000:
                if len(old_candidate_list) < 10 and data['const'] * 4.0 >= old_list[34]['rating']:
                    old_candidate_list.append(data)
                else:
                    break
    else:
        # 旧枠が埋まりきっていないので空データを追加
        for i in range(len(old_list), 35):
            add_data_to_list(old_list, "Not played", 'NA', 'NA', 'NA', 0, 0)

    print("Rating: {:.3f}\n".format(new_value + old_value))
    if new_list_len != 0:
        print("--- 新枠 対象曲 (average: {:.3f})\n".format(new_value / new_list_len))
        print_list(new_list)
    else:
        print("--- 新枠 対象曲 (average: --)\n")
    if old_list_len != 0:
        print("--- 旧枠 対象曲 (average: {:.3f})\n".format(old_value / old_list_len))
        print_list(old_list)
    else:
        print("--- 旧枠 対象曲 (average: --)\n")
    print("--- 新枠 候補曲\n")
    if (new_list_len == 15):
        print_list(new_candidate_list)
    print("--- 旧枠 候補曲\n")
    if (old_list_len == 35):
        print_list(old_candidate_list)



def main():
    print("WACCA Tool ver.{} (released on {})\n".format(VERSION, UPDATE_DATE))
    data_list = make_list()
    show_ratings(data_list)


if __name__ == "__main__":
    main()