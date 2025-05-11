#トロッコ問題
#トロッコが暴走して5人いる線路に突っ込みそう！線路を切り替えれば1人いる線路に突っ込む。
#線路を切り替えるレバーを引く？

from flask import Flask, render_template, request, session
import random as rd
import os
import openai

app = Flask(__name__)
app.secret_key = 'shoya_secret_key'  # ← 任意の文字列（絶対に必要）【sessionを使う場合には必ず必要】
openai.api_key = os.environ.get("OPENAI_API_KEY")

class Person:
    def __init__(self, age, gender):
        self.age = age
        self.gender = gender

gender_list = ["男性", "女性"]
num_on_main_track = 5
num_on_sub_track = 1
result = []

#クッキーが残っていたら1回目は正常にできても2回目からはすぐにfinished.htmlにいってしまうためクッキーの初期化が必要
@app.before_request     #すべてのリクエストの前に毎回呼び出される特別な関数
def cleanup_session_and_result():
    #「ラウンドが終わっている」か「そもそも round が無い」なら新しいゲームにする
    if request.method == "GET" and session.get("round", 0) >= 10:   #sessionをクリアーするのはリクエストがGETのときのみ
        session.clear()          # ← round・answers など全部消す(クッキーを初期化している)
    if "round" not in session:   # sessionの各値を初期化している
        session["round"] = 0
        session["answers"] = []
        global result            #global変数のresultに
        result = []
    #AIに渡す結果のリスト[ [ [ メイン線路にいる人物の属性のリスト（レバーを引けば助かる人たち） ], [ サブ線路にいる人物の属性のリスト（レバーを引かなければ助かる人） ], [ ユーザーの解答 ] ], [・・・]]

@app.route("/", methods=["GET", "POST"])    #URLにアクセスされたとき（GET）か、HTMLからデータが送信（POST）されたときに下記の関数を実行
def trocco_game():                  #sessionは今何問目か記憶しておく（Flaskのsessionは関数の中で使っていても、リクエストをまたいで値を保持できる）
    
    if "round" not in session:      #sessionにroundが存在していなければ0にして、answer(引くor引かないをいれる)も空にしておく
        session["round"] = 0
        session["answers"] = []

    if request.method == "POST":    #ボタンを押されたときにHTMLから値を受け取る
        user_choice = request.form.get("thinking")
        # session["answers"].append(user_choice)
        session["round"] += 1
        result.append([session.get("main_people"), session.get("sub_people"), user_choice]) #resultリストへの追加はれクエストがPOSTの時のみに実行されるべき

    if session["round"] >= 10 and len(result) >= 10:
         #AI機能とresultを渡す
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
            {
                "role": "system",
                "content": (
                    "あなたは一流の哲学者です。箇条書き（1. 全体的な傾向  2. 命の数に対する重視  3. 年齢や性別による影響  4. 思考の変化について  5. 倫理観と価値観  6. 人間関係への考察 ）での出力で分かりやすく整理してください。また、必ず日本語で出力してください"
                    "それぞれの人の年齢や性別を考慮した発言も踏まえた考察をするように心掛けてください"
                    "1人1人の人生についての話をするのではなく、あくまで解答者の考え方の考察を出力してください。"
                    "トロッコ問題の解答を受け取り、その思考から分析・考察を出力してください。"
                    "口調は親しみやすく、カジュアルで、柔らかい好感の持てる口調でお願いします。"
                    "前置きはいりません。加えて、さらなる質問はしないようにしてください"
                    "ユーザーのことはあなたと呼ぶようにしてください。"
                    "その選択から人間関係の考察を最後にしてください"
                )
            },
            {
                "role": "user",
                "content": (
                    "次に渡すリストにはトロッコ問題での10回分の問題とユーザーの解答が[ [ [ メイン線路にいる人物の属性のリスト（レバーを引けば助かる人たち） ], [ サブ線路にいる人物の属性のリスト（レバーを引かなければ助かる人） ], [ ユーザーの解答 ] ], [・・・]]のようにリストで入っています。" 
                    "前提条件としてメイン線路には5人、サブ線路には1人いて、それぞれの年齢や性別はランダムで設定されるようになっています。"       
                    "問題の内容とユーザーの解答から、ユーザーの思考の癖や、問題を経るにつれて思考の変化がある場合にはそれらを考察して結果を出力してください"
                    f"こちらがリストです：{result}。"
                    "超一流の哲学者としてあいまいな答えを避けて詳細に分かりやすく説明をしてください"
                )
            }
        ],
            temperature=0.5,
            presence_penalty=0.7,
            frequency_penalty=0.5,
            max_tokens=2500
            
            )

        ai_res = response.choices[0].message.content
        return render_template("finished.html", result=result, ai_res=ai_res)

    # 問題生成（リクエストがGETでもPOSTでも問題の生成は行われる）※最初はGETなのでこの部分だけ行われる
    main_track_person = [
        Person(rd.randint(0, 80), rd.choice(gender_list)) for _ in range(num_on_main_track)
    ]
    sub_track_person = [
        Person(rd.randint(0, 80), rd.choice(gender_list)) for _ in range(num_on_sub_track)
    ]

    main_people = [f"{p.age}歳 の {p.gender}" for p in main_track_person]
    sub_people = [f"{p.age}歳 の {p.gender}" for p in sub_track_person]

    session["main_people"] = main_people #sessionで一時的に値を保持
    session["sub_people"] = sub_people  
    round_count = session["round"] + 1 #何問目かを表示するために

    return render_template("index.html", main_people=main_people, sub_people=sub_people,round_count=round_count)
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



#finished.htmlに行くところがAI処理が入るのでページ遷移が遅くなる。
#そのためいったん別の画面をfinished.htmlに表示するか、別のhtmlファイルに移動してそこで処理を進めるか？



"""
Flaskの session とは？
ユーザーごとの情報を一時的に保存しておくしくみです。

🔍 もう少し丁寧に説明すると…
Flaskアプリは基本的に「毎回ゼロから処理する」もの
Flaskは、ページを開くたび（GET）、ボタンを押すたび（POST）に、
関数（@app.route()）が毎回最初から実行されます。

つまり、ふつうなら「前回どんな回答をしたか」とか「今何問目か」という情報は忘れてしまうんです。

そこで登場するのが session
session["round"] = 3
このように書くと、

🔒 Flaskが「このユーザーは3問目だな」と情報を記録して、次のリクエストでも使えるようにしてくれます。

保存場所はどこかというと：

🧠 ユーザーのブラウザ（クッキー）に、暗号化された状態で保存されます。

Flaskが secret_key を使って、安全にデータを守ります。

Flaskの session は、Pythonの辞書（dict）みたいなものなので、

また、sessionは

session = {
    "round": 3,
    "answers": ["引く", "引かない"],
    "main_people": ["20歳の男性", "80歳の女性"],
}

のように、「キー（名前）」と「値」をセットで保存できます。
"""
