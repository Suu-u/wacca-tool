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
    elif score > 0:
        ratio = score // 100000 * 0.1 + 0.1

    new_data['rating'] = round(const * ratio, 2)

    data_list.append(new_data)


# 定数・スコアを読み込んでlistを作成
def make_list():
    # wacca_const.csvの読み込み
    # [title, version, genre, h_const, e_const, i_const]
    const_file = open('wacca_const.csv', 'r', encoding='utf-8')
    fc = csv.reader(const_file)
    header = next(fc)
    const_list = []
    for row in fc:
        const_list.append(row)

    # wacca_score.csvの読み込み
    # [title, n_score, h_score, e_score, i_score]
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
                if const[3] != 'NA': # hard
                    add_data_to_list(data_list, const[0], const[1], const[2], 'HRD', float(const[3]), int(score[2]))
                if const[4] != 'NA': # expert
                    add_data_to_list(data_list, const[0], const[1], const[2], 'EXP', float(const[4]), int(score[3]))
                if const[5] != 'NA': # inferno
                    add_data_to_list(data_list, const[0], const[1], const[2], 'INF', float(const[5]), int(score[4]))
                score_list.remove(score)
                break
        if not is_played:
            # 未プレイなのでスコアを0にして要素を追加
            if const[3] != 'NA': # hard
                add_data_to_list(data_list, const[0], const[1], const[2], 'HRD', float(const[3]), 0)
            if const[4] != 'NA': # expert
                add_data_to_list(data_list, const[0], const[1], const[2], 'EXP', float(const[4]), 0)
            if const[5] != 'NA': # inferno
                add_data_to_list(data_list, const[0], const[1], const[2], 'INF', float(const[5]), 0)

    # 定数データのないスコアデータを定数を-1にして追加
    for score in score_list:
        if score[2] != '0': # hard
            add_data_to_list(data_list, score[0], 'NA', 'NA', 'HRD', -1, int(score[2]))
        if score[3] != '0': # expert
            add_data_to_list(data_list, score[0], 'NA', 'NA', 'EXP', -1, int(score[3]))
        if score[4] != '0': # inferno
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
    tmp_list = [data for data in data_list if data['rating'] > 0]
    tmp_list = sorted(tmp_list, key=lambda x: x['rating'], reverse=True)

    new_value = 0
    old_value = 0
    new_list = []
    old_list = []
    new_candidate_list = []
    old_candidate_list = []

    # 新枠対象曲を追加
    is_full_new = False
    for data in tmp_list[:]:
        if data['version'] == 'R':
            if len(new_list) < 15:
                new_value += data['rating']
                new_list.append(data)
                tmp_list.remove(data)
            else:
                is_full_new = True
                break
    
    # 旧枠対象曲を追加
    is_full_old = False
    for data in tmp_list[:]:
        if data['version'] != 'R':
            if len(old_list) < 35:
                old_value += data['rating']
                old_list.append(data)
                tmp_list.remove(data)
            else:
                is_full_old = True
                break

    # 新枠候補曲を追加
    if (is_full_new):
        for data in tmp_list:
            if data['version'] == 'R' and data['score'] < 990000:
                if len(new_candidate_list) < 10:
                    new_candidate_list.append(data)
                else:
                    break
    else:
        # 新枠が埋まりきっていないので空データを追加
        for i in range(len(new_list), 15):
            add_data_to_list(new_list, "Not played", 'NA', 'NA', 'NA', 0, 0)

    # 旧枠候補曲を追加
    if (is_full_old):
        for data in tmp_list:
            if data['version'] != 'R' and data['score'] < 990000:
                if len(old_candidate_list) < 10:
                    old_candidate_list.append(data)
                else:
                    break
    else:
        # 旧枠が埋まりきっていないので空データを追加
        for i in range(len(old_list), 35):
            add_data_to_list(old_list, "Not played", 'NA', 'NA', 'NA', 0, 0)

    print("Rating: {:.3f}\n".format(new_value + old_value))
    print("--- 新枠 対象曲 (average: {:.3f})\n".format(new_value / len(new_list)))
    print_list(new_list)
    print("--- 旧枠 対象曲 (average: {:.3f})\n".format(old_value / len(old_list)))
    print_list(old_list)
    print("--- 新枠 候補曲\n")
    if (is_full_new):
        print_list(new_candidate_list)
    print("--- 旧枠 候補曲\n")
    if (is_full_old):
        print_list(old_candidate_list)



def main():
    data_list = make_list()
    show_ratings(data_list)


if __name__ == "__main__":
    main()