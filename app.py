#トロッコ問題
#トロッコが暴走して5人いる線路に突っ込みそう！線路を切り替えれば1人いる線路に突っ込む。
#線路を切り替えるレバーを引く？

from flask import Flask, render_template, request, session
import random as rd
import time
import os
import openai

app = Flask(__name__)
app.secret_key = 'shoya_secret_key'  # ← 任意の文字列（絶対に必要）【sessionを使う場合には必ず必要】


class Person:
    def __init__(self, age, gender):
        self.age = age
        self.gender = gender

gender_list = ["男性", "女性"]
num_on_main_track = 5
num_on_sub_track = 1

@app.route("/", methods=["GET", "POST"])    #URLにアクセスされたとき（GET）か、HTMLからデータが送信（POST）されたときに下記の関数を実行
def trocco_game():                  #sessionは今何問目か記憶しておく（Flaskのsessionは関数の中で使っていても、リクエストをまたいで値を保持できる）
    if "round" not in session:      #sessionにroundが存在していなければ0にして、answer(引くor引かないをいれる)も空にしておく
        session["round"] = 0
        session["answers"] = []

    if request.method == "POST":    #ボタンを押されたときにHTMLから値を受け取る
        user_choice = request.form.get("thinking")
        session["answers"].append(user_choice)
        session["round"] += 1

    if session["round"] >= 10:
        return render_template("finished.html", answers=session["answers"])

    # 問題生成
    main_track_person = [
        Person(rd.randint(0, 80), rd.choice(gender_list)) for _ in range(num_on_main_track)
    ]
    sub_track_person = [
        Person(rd.randint(0, 80), rd.choice(gender_list)) for _ in range(num_on_sub_track)
    ]

    main_people = [f"{p.age}歳の{p.gender}" for p in main_track_person]
    sub_people = [f"{p.age}歳の{p.gender}" for p in sub_track_person]

    return render_template("index.html", main_people=main_people, sub_people=sub_people)
        
        
    # #AIによる考察を生成
    # openai.api_key = os.environ.get("openai_api")

    # response = openai.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #     {
    #         "role": "system",
    #         "content": (
    #             "あなたは一流の哲学者です。箇条書きでの出力はせずに話し言葉でお願いします。また、必ず日本語で出力してください"
    #             "それぞれの人の年齢や性別を考慮した発言も踏まえた考察をするように心掛けてください"
    #             "1人1人の人生についての話をするのではなく、あくまで解答者の考え方の考察を出力してください。"
    #             "トロッコ問題の解答を受け取り、その思考から分析・考察を出力してください。"
    #             "口調は親しみやすく、カジュアルで、柔らかい好感の持てる口調でお願いします。"
    #         )
    #     },
    #     {
    #         "role": "user",
    #         "content": (
    #             "次に渡すリストにはトロッコ問題での10回分の問題とユーザーの解答が[ [ [ メイン線路にいる人物の属性のリスト（レバーを引けば助かる人たち） ], [ サブ線路にいる人物の属性のリスト（レバーを引かなければ助かる人） ], [ ユーザーの解答 ] ], [・・・]]のようにリストで入っています。" 
    #             "前提条件としてメイン線路には5人、サブ線路には1人いて、それぞれの年齢や性別はランダムで設定されるようになっています。"       
    #             "問題の内容とユーザーの解答から、ユーザーの思考の癖や、問題を経るにつれて思考の変化がある場合にはそれらを考察して結果を出力してください"
    #             f"こちらがリストです：{total_question_answer}。"
    #             "超一流の哲学者としてあいまいな避けて高校生にも分かるような説明をしてください"
    #         )
    #     }
    # ],
    #     temperature=0.8,
    #     presence_penalty=0.7,
    #     frequency_penalty=0.5,
    #     max_tokens=2000
        
    #     )

    # ai_res = response.choices[0].message.content


#解答までの時間を設定する
#それぞれの線路にいる人間をGUIアプリに表示する（おそらくfor文で表示しておいて、レバーを引いて結果が出たら次のループに行くから変更される）
#レバー引くかどうかはボタンで引くボタン、引かないボタンを創ってそれぞれにuser_inputの値が"引く"or"引かない"が設定される関数をつくる。

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
