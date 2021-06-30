# wacca-tool

最終楽曲追加対応日：2021/07/01

## 使い方

1. [こちら](https://github.com/saezurucrow/wacca-score-csv)のツールを用いてマイページサイトからCSVファイルを取得
2. 取得した```wacca_score.csv```と```main.py```、```wacca_const.csv```を同じディレクトリに置く
3. ```main.py```を実行

## 機能

WACCAのレーティング対象曲・候補曲を表示します

- 各譜面のバージョン、ジャンル、難易度、譜面定数、スコア、単曲レーティング値が表示されます
  - バージョン
    - R: WACCA Lily R
    - L: WACCA Lily
    - S: WACCA, WACCA S
  - ジャンル
    - ap: アニメ/POP
    - vo: ボカロ
    - th: 東方アレンジ
    - 25: 2.5次元
    - va: バラエティ
    - or: オリジナル
    - ta: TANO*C
    - to: TANO*Cオリジナル
  - 難易度
    - HRD: hard
    - EXP: expert
    - INF: inferno
- 譜面定数データがhard, expert, infernoのみの対応のため、対象曲にnormal譜面が含まれているとレーティングが正しく表示されません
- 候補曲では、対象曲でない譜面のうち、スコアが990000未満の楽曲が単曲レーティング値の高い順に10譜面表示されます
  - スコアが990000以上の場合、単曲レーティング値がこれ以上高くなることはないためです
  - よって、公式マイページにて表示されるレーティング候補曲と一致しない場合があります

```
> python3 main.py 
Rating: 2559.520

--- 新枠 対象曲 (average: 51.467)

Stasis
        R       va      EXP     13.6    991374  54.4

                            .
                            .
                            .

--- 旧枠 対象曲 (average: 51.072)

Knight Rider
        S       to      EXP     13.3    993387  53.2

                            .
                            .
                            .

--- 新枠 候補曲

You are the Miserable
        R       va      EXP     13.9    971571  48.65

                            .
                            .
                            .

--- 旧枠 候補曲

ぺこみこ大戦争！！ (INF)
        L       ap      INF     13.2    985819  49.5

                            .
                            .
                            .
```

## 最後に

何かありましたら sal_pipr ([twitter](https://twitter.com/sal_pipr)) までご連絡ください