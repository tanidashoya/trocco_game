#トロッコ問題
#トロッコが暴走して5人いる線路に突っ込みそう！線路を切り替えれば1人いる線路に突っ込む。
#線路を切り替えるレバーを引く？

import tkinter as tk
from tkinter import ttk

#GUIアプリのウィンドウ・ラベルを作成
# window = tk.Tk()
# window.title("トロッコ問題～あなたの倫理観は？～")
# window.geometry("700x800")
# label1 = tk.Label(window,text=("暴走するトロッコがこのまま進むと、メイン線路上の5人をひいてしまう。\n"
#                     "しかし、あなたの目の前にはレバーがあり、それを引くとトロッコはサブ線路に切り替わり、そちらには1人がいる。\n"
#                     "あなたはレバーを引いて1人を犠牲にし、5人を救うべきか？"),justify="left")
# label1.place(x=50,y=50)

# label2 = tk.Label(window,text="メイン線路にいる人")
# label2.place(x=50,y=200)

# label3 = tk.Label(window,text="サブ線路にいる人")
# label3.place(x=50,y=300)

# label4 = tk.Label(window,text="レバーをどうする？")
# label4.place(x=50,y=300)

# window.mainloop()

#トロッコ問題基本コード
def trocco_run(num_on_main_track,num_on_sub_track,thinking):        
    
    if thinking == "引く":           #功利主義の場合
        if num_on_main_track > num_on_sub_track:
            return f"サブ線路にいた{num_on_sub_track}人が犠牲になりました"
        elif num_on_main_track < num_on_sub_track:
            return f"メイン線路にいた{num_on_main_track}人が犠牲になりました"
    elif thinking == "引かない":      #義務論的な場合
        return f"メイン線路にいた{num_on_main_track}人が犠牲になりました"
    else:
        return "どうするのかを教えてください"


num_on_main_track = 5
num_on_sub_track = 1

print(f"---倫理的問題---\n\
メイン線路に{num_on_main_track}人いて、トロッコが突っ込みそうです！！\n\
線路を切り替えれば{num_on_sub_track}人いるサブ線路にトロッコが突っ込みます!\n\
線路を切り替えるレバーを引きますか？")



#人のクラスを定義（トロッコ問題に書く人の属性を定義して問題の厚みを持たせる）
import random as rd
import openai
import os
import time

class Person:       
    
    def __init__(self,age,gender):
        self.age = age
        self.gender = gender


total_question_answer = []          #最終的に[ [ [ メイン線路にいる人物の属性のリスト ], [ サブ線路にいる人物の属性のリスト ], [ ユーザーの解答 ] ], [・・・]]のようにする

for _ in range(10):      #問題の繰り返し
    print("-----------メイン線路-------------")
    gender_list = ["男性","女性"]
    main_track_person = []      #メイン線路にいる人のインスタンスを決める
    for i in range(num_on_main_track):
        age = rd.randint(0,80)
        gender = rd.choice(gender_list)
        person = Person(age,gender)       #ランダムに年齢、性別を持つPersonインスタンスを生成してリストに格納する
        main_track_person.append(person)

    for j in main_track_person:
        print(f"{j.age}歳の{j.gender}")
        
    main_person_detail_list = [f"{person.age}歳の{person.gender}" for person in main_track_person]

    print("-----------サブ線路-------------")

    sub_track_person = []      #サブ線路にいる人を決める
    for i in range(num_on_sub_track):
        age = rd.randint(0,80)
        gender = rd.choice(gender_list)
        person = Person(age,gender)       #ランダムに年齢、性別を持つPersonインスタンスを生成してリストに格納する
        sub_track_person.append(person)

    for j in sub_track_person:
        print(f"{j.age}歳の{j.gender}")
        
    sub_person_detail_list = [f"{person.age}歳の{person.gender}" for person in sub_track_person]

    print("-----------あなたの考えは？-------------")
    user_thinking = input("レバー（引く or 引かない）？：")
    print("-----------------結果------------------")
    print(trocco_run(num_on_main_track,num_on_sub_track,user_thinking))

    result = [main_person_detail_list,sub_person_detail_list,user_thinking]
    total_question_answer.append(result)
    time.sleep(2)
    
print("☆ AIによる考察")
openai.api_key = os.environ.get("openai_api")

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
    {
        "role": "system",
        "content": (
            "あなたは一流の哲学者です。箇条書きでの出力はせずに話し言葉でお願いします。また、必ず日本語で出力してください"
            "それぞれの人の年齢や性別を考慮した発言も踏まえた考察をするように心掛けてください"
            "1人1人の人生についての話をするのではなく、あくまで解答者の考え方の考察を出力してください。"
            "トロッコ問題の解答を受け取り、その思考から分析・考察を出力してください。"
            "口調は親しみやすく、カジュアルで、柔らかい好感の持てる口調でお願いします。"
        )
    },
    {
        "role": "user",
        "content": (
            "次に渡すリストにはトロッコ問題での10回分の問題とユーザーの解答が[ [ [ メイン線路にいる人物の属性のリスト（レバーを引けば助かる人たち） ], [ サブ線路にいる人物の属性のリスト（レバーを引かなければ助かる人） ], [ ユーザーの解答 ] ], [・・・]]のようにリストで入っています。" 
            "前提条件としてメイン線路には5人、サブ線路には1人いて、それぞれの年齢や性別はランダムで設定されるようになっています。"       
            "問題の内容とユーザーの解答から、ユーザーの思考の癖や、問題を経るにつれて思考の変化がある場合にはそれらを考察して結果を出力してください"
            f"こちらがリストです：{total_question_answer}。"
            "超一流の哲学者としてあいまいな避けて高校生にも分かるような説明をしてください"
        )
    }
],
    temperature=0.8,
    presence_penalty=0.7,
    frequency_penalty=0.5,
    max_tokens=2000
    
    )

print(response.choices[0].message.content)


#解答までの時間を設定する
#それぞれの線路にいる人間をGUIアプリに表示する（おそらくfor文で表示しておいて、レバーを引いて結果が出たら次のループに行くから変更される）
#レバー引くかどうかはボタンで引くボタン、引かないボタンを創ってそれぞれにuser_inputの値が"引く"or"引かない"が設定される関数をつくる。