import tweepy
import time
import random
import datetime
import locale
from pykakasi import kakasi

# 自分のスクリーンネーム(認証キーを変えたら合わせて変える)　#
my_screen_name = ""

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

# consumer　第一引数に(consumer　key)　第二引数に(consumer　secret) #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# ACCESS_TOKEN_KEY 第一引数に(Access token)　第二引数に(Access token secret) #
auth.set_access_token(access_token_key, access_token_secret)

# wait_on_rate_limit = レート制限が補充されるのを自動的に待つかどうか #
# wait_on_rate_limit_notify = Tweepyがレート制限の補充を待っているときに通知を出力するかどうか #
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def parameter():#各種パラメーター
    # 取得したいキーワード #
    search_list = [ohasen]

    # いいねの上限設定 #
    favorite_max = 30
    # リプライの上限設定 #
    reply_max = 25

    #処理のfor文、自体を回すか？
    favorite_loop_run = False #True
    reply_loop_run = False #True
    favorite_mention_to_me_loop_run = True
    favorite_to_friend_loop_run = False #True

    #いいね・リプライ・ツイート処理の実行有無
    favorite_run = True
    reply_run =  False #True
    post_run = True

    # フォローの間隔を決めるための乱数の範囲（2つの数字の範囲からランダムに数字を返す）（＊アカバンされない為に超重要） #
    interval = [300,360]
    # 指定ユーザーへのいいねの数を乱数で決定 #
    friend_favorite_num = [1,3]

    # ターゲットワード指定 #
    target_word =[
    "無料"
    ,"就活支援"
    ]

    # NGワード指定 #
    NG_word =[
    "momomomomoo"
    ]

    # 検索するツイート数（＊いいねする数ではない） #
    search_num = 200
    return search_list ,favorite_max ,reply_max ,interval ,NG_word ,search_num ,favorite_run ,reply_run ,favorite_loop_run ,reply_loop_run ,favorite_mention_to_me_loop_run ,favorite_to_friend_loop_run ,friend_favorite_num ,target_word ,post_run

def reply_text():#リプライの内容(n:改行、l1：１行目)
    l1 =[
    "こんにちは😆"
    ,"こんにちは❗️"
    ]
    l2 =[
    "とうも"
    ,"はーい"
    ]
    l3 =[
    "gaga"
    ,"gaaaa"
    ]
    n = "\n"
    return n ,l1 ,l2 ,l3

def favorite_to_friend():# いいねする友達のスクリーネームを指定
    friends = [
    "******"
    ,"*****"
    ,"****"
    ]
    return friends

def stop_time(interval):#処理の間隔を開ける関数
    # フォローの間隔を決めるための乱数の範囲（2つの数字の範囲からランダムに数字を返す）（＊アカバンされない為に超重要） #
    #interval =[1,1]#[120,360]
    time.sleep(random.randint(interval[0], interval[1]))

def keyword_exclusion(NG_word):#judgment_result = keyword_exclusion() みたいに結果を入れる（1→NG 0→対象者！）
    # 除外処理 #
    judgment_result = False
    for NG in NG_word:
        if NG in tweet.text:
            judgment_result = True
            #print("【ツイート】NG処理！！！！！！！！！！！！","\n"*5)
            break
        if "RT @" in tweet._json['text']:
            if NG in tweet._json['retweeted_status']['user']['description']:
                judgment_result = True
                #print("自分メンション【プロフ①】NG処理！！！！！！！！！！！！","\n"*5)
                break
        else:
        #if len(tweet._json['entities']['user_mentions']) == 0:
            if NG in tweet._json['user']['description']:
                judgment_result = True
                #print("メンションなし【プロフ②】NG処理！！！！！！！！！！！！","\n"*5)
                break
    return judgment_result

def keyword_inclusion(target_word):#ターゲットワードが1つでも含む
    judgment_result = False
    for word in target_word:
        if word in tweet.text:
            judgment_result = True
            #print("【ツイート】含む処理！！！！！！！！！！！！","\n"*5)
            break
        if "RT @" in tweet._json['text']:
            if word in tweet._json['retweeted_status']['user']['description']:
                judgment_result = True
                #print("自分メンション【プロフ①】含む処理！！！！！！！！！！！！","\n"*5)
                break
        else:
        #if len(tweet._json['entities']['user_mentions']) == 0:
            if word in tweet._json['user']['description']:
                judgment_result = True
                #print("メンションなし【プロフ②】含む処理！！！！！！！！！！！！","\n"*5)
                break
    return judgment_result

def keyword_all_inclusion(target_word):#ターゲットワードが全部含む
    judgment_result = False
    for word in target_word:
        if word in tweet.text:
            judgment_result = True
            #print("【ツイート】含む処理！！！！！！！！！！！！","\n"*5)
            continue
        if "RT @" in tweet._json['text']:
            if word in tweet._json['retweeted_status']['user']['description']:
                judgment_result = True
                #print("自分メンション【プロフ①】含む処理！！！！！！！！！！！！","\n"*5)
                continue
            else:
                judgment_result = False
                print("指定ワードを含まない")
                break
        else:
        #if len(tweet._json['entities']['user_mentions']) == 0:
            if word in tweet._json['user']['description']:
                judgment_result = True
                #print("メンションなし【プロフ②】含む処理！！！！！！！！！！！！","\n"*5)
                continue
            else:
                judgment_result = False
                print("指定ワードを含まない")
                break
    return judgment_result

def reply_processing():#リプライ処理を実行する関数
    #ツイートからスクリーンネームを取得して格納し、リプライの文章を組み立てる
    target_screen_name = get_screen_name_from_tweet()
    reply_to = "@" + target_screen_name + " "
    reply_text = reply_to + n*2 + random.choice(l1) + n*2 + random.choice(l2)+ n + random.choice(l3)
    try:
        #リプライ処理
        if reply_run == True:
            stop_time(interval)
            api.update_status(reply_text, in_reply_to_status_id = tweet.id)        
        print(">"*35,'No.',reply_count+1)
        print("\n","【リプライ本文】\n", reply_text,"\n")
        print("-"*10,"リプライ完了","-"*10,"\n"*3)
        #stop_time(interval)
        processing_result = 0
    except tweepy.TweepError as e:
        print(e.reason)
        #print("-"*15,"すでに同様の内容でリプライ済みでした","\n"*3)
        processing_result = 1
    except StopIteration:
        processing_result = 2
    return processing_result

def favorite_processing():#いいね処理を実行する関数
    try:
        # いいねの処理 #
        if favorite_run == True:
            print("いいね処理ループがちゃんと回ってる！！！！！！！！！")##########デバック
            api.create_favorite(id=tweet.id)
        print(">"*35,'No.',favorite_count+1)
        print("\n","【ツイート本文】\n", tweet.text,"\n")
        print("-"*10,"いいね完了","-"*10,"\n"*3)
        stop_time(interval)
        processing_result = 0
    except tweepy.TweepError as e:
        #print('すでにいいね済みです！\n')
        #print("【ツイート本文】\n", tweet.text,"\n"*3)
        print(e.reason)
        processing_result = 1
    except StopIteration:
        processing_result = 2
    return processing_result

def get_screen_name_from_tweet():#ツイートからスクリーンネームを取得する関数
        #自分メンションのツイートの場合
    if "RT @" in tweet._json['text']:
        target_screen_name = tweet._json['retweeted_status']['user']['screen_name']
            #print("自分メンションツイートのスクリーネーム取得","\n"*5)
    #メンションなしツイートの場合
    else:
        target_screen_name = tweet._json['user']['screen_name']
            #print("メンションなし【プロフ②】NG処理！！！！！！！！！！！！","\n"*5)
    return target_screen_name

def reply_history():#作る関数は、リプライ履歴があるかを確認する関数
    #上限は200
    timeline_search_count = 200
    my_timelines = api.user_timeline(screen_name = my_screen_name ,count = timeline_search_count)
    target_screen_name = get_screen_name_from_tweet()
    for my_timeline in my_timelines:
        if target_screen_name in my_timeline._json['text']:
            #target_screen_nameを含む投稿がある場合は、リプライ処理を行わない。
            judgment_result = True
            print("⚠️リプライ履歴あり","\n")
            break
        else:
            #含まない場合にのみ処理を行う。
            judgment_result = False
    if target_screen_name == my_screen_name:
        judgment_result = True#自分が投稿したツイートの場合も処理除外
        print("自分が投稿したツイートのため除外処理")
    return judgment_result

def post_processing():#リプライ処理を実行する関数
    post_text = "定期ツイートの内容をここに記載" + ohasen
    try:
        #リプライ処理
        if post_run == True:
            api.update_status(post_text)        
        print(">"*35,'No.')
        print("\n","【ツイート本文】\n", post_text,"\n")
        print("-"*10,"ツイート完了","-"*10,"\n"*3)
        stop_time(interval)
        processing_result = 0
    except tweepy.TweepError as e:
        print(e.reason)
        #print("-"*15,"すでに同様の内容でツイート済みでした","\n"*3)
        processing_result = 1
    except StopIteration:
        processing_result = 2
    return processing_result

def now_time():
    now = datetime.datetime.now()
    print("\n","【",now.strftime('%Y年%m月%d日 %H:%M:%S'),"】")


################おは戦用#######################
kakasi = kakasi()

kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')

conv = kakasi.getConverter()

dt_now = datetime.datetime.now()

month = dt_now.strftime('%m')
day = dt_now.strftime('%d')
#月の頭文字を取得
month_en = str.lower(dt_now.strftime('%B'))
#曜日の頭文字を日本語ローマ字で取得
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
week = str.lower(dt_now.strftime('%A'))
week_jp = conv.do(week)

ohasen = "#おは戦3" + month + day + month_en[0] + week_jp[0]
################おは戦用#######################
   

# パラメーター関数から変数を格納 #
search_list = parameter()[0]
favorite_max = parameter()[1]
reply_max = parameter()[2]
interval = parameter()[3]
NG_word =parameter()[4]
search_num = parameter()[5]
favorite_run = parameter()[6]
reply_run = parameter()[7]
favorite_loop_run = parameter()[8]
reply_loop_run = parameter()[9]
favorite_mention_to_me_loop_run = parameter()[10]
favorite_to_friend_loop_run = parameter()[11]
friend_favorite_num = parameter()[12]
target_word = parameter()[13]
post_run = parameter()[14]

#　リプライの本文　#
l1 = reply_text()[1]
l2 = reply_text()[2]
l3 = reply_text()[3]
n = reply_text()[0]

# いいねする友達のスクリーネーム #
friends = favorite_to_friend()

#　カウンター #
favorite_count = 0
reply_count = 0
i = 0


now_time()
post_processing()
stop_time(interval)


if favorite_loop_run == True:#いいね処理の有無
    print("\n","いいね処理をします","\n")
    for search in search_list:# 検索ワードの数だけループを回す #
        print("\n",'検索ワード【{}】' .format(search),"\n")
        i = 0
        while search_num > i:
            if favorite_max > favorite_count:#いいね上限に達するまでいいね処理を行う     
                # キーワードを含むツイートを検索する #
                search_result = api.search(q=search, count=1)
                i += 1
                for tweet in search_result:#いいね処理を行うfor文                 
                        #これは指定ワードがあるか判定する処理                    
                    #judgment_result = keyword_inclusion(target_word)
                    ##ターゲットワードを含まない場合は、スキップする
                    #if judgment_result == False:
                    #    print("⚠️ターゲットワード含まない","\n")
                    #    continue
                    ##ターゲットワードを含んだ場合は処理をする
                       #これはNGワードを除外する処理
                    judgment_result = keyword_exclusion(NG_word)
                    #NGワードを含んだ場合は、スキップする
                    if judgment_result == True:
                        print("⚠️NG処理","\n")
                        continue
                    ##NGを含まなかった場合は処理をする

                    else:
                        if tweet._json['in_reply_to_screen_name'] == None:

                            ####いいね処理####
                            processing_result = favorite_processing()
                                #処理成功
                            if processing_result == 0:
                                favorite_count += 1
                                #エラー
                            elif processing_result == 1:
                                continue
                                #検索した分処理し切った
                            elif processing_result == 2:
                                break
                        else:
                            #print("誰かへのリプライでした","\n"*5)
                            continue
            else:
                print("\n"*5,"🙅‍♂️"*15,"いいね上限です","‍🙅‍♂️"*15,"\n"*2)
                break

if reply_loop_run == True:#リプライ処理の有無
    print("\n","リプライ処理をします","\n")
    for search in search_list:# 検索ワードの数だけループを回す #
        print("\n",'検索ワード【{}】' .format(search),"\n")
        i = 0
        while search_num > i:
            if reply_max > reply_count:#リプライ上限に達するまでリプライ処理を行う
                # キーワードを含むツイートを検索する #
                search_result = api.search(q=search, count=1)
                i += 1
                for tweet in search_result:#いいね処理を行うfor文
                    #NGワードを含んだ場合は、スキップする
                    judgment_result = keyword_exclusion(NG_word)
                    if judgment_result == True:
                        print("⚠️NG処理","\n")
                        continue

                    #リプライ履歴がある・自分のツイートだった場合は、スキップする
                    judgment_result = reply_history()
                    if judgment_result == True:
                        continue

                    #NGを含まず、リプライ履歴がなかった場合は処理をする
                    else:
                        if tweet._json['in_reply_to_screen_name'] == None:
                            ####リプライ処理####
                            processing_result = reply_processing()
                            if processing_result == 0:
                                reply_count += 1
                                #エラー
                            elif processing_result == 1:
                                continue
                                #検索した分処理し切った
                            elif processing_result == 2:
                                break
                        else:
                            #print("誰かへのリプライでした","\n"*5)
                            continue
            else:
                print("\n"*5,"🙅‍♂️"*15,"リプライ上限です","‍🙅‍♂️"*15,"\n"*2)
                break

if favorite_mention_to_me_loop_run == True:#自分へのリプライにいいね処理の有無
    print("\n","自分へのリプライにいいね処理をします","\n")
    # キーワードを含むツイートを検索する #
    search_result = api.search(q= "@" + my_screen_name ,count = search_num)
    for tweet in search_result:#いいね処理を行うfor文
        if favorite_max > favorite_count:#いいね上限に達するまでいいね処理を行う
            """
            judgment_result = keyword_exclusion(NG_word)
            #NGワードを含んだ場合は、スキップする
            if judgment_result == True:
                print("⚠️NG処理","\n")
                continue
            #NGを含まなかった場合は処理をする
            else:
            """
            ####いいね処理####
            processing_result = favorite_processing()
                #処理成功
            if processing_result == 0:
                favorite_count += 1
                #エラー
            elif processing_result == 1:
                continue
                #検索した分処理し切った
            elif processing_result == 2:
                break
        else:
            print("\n"*5,"🙅‍♂️"*15,"いいね上限です","‍🙅‍♂️"*15,"\n"*2)
            break

if favorite_to_friend_loop_run == True:#指定ユーザーのツイートにいいね処理の有無
    print("\n","合計【",len(friends),"】人の指定ユーザーへのいいね処理をします","\n")
    #各ユーザーごとのいいねの上限を乱数で決定
    favorite_this_user_max = random.randint(friend_favorite_num[0] ,friend_favorite_num[1])
    print("⚠️","今回の各ユーザーのいいね上限は【",favorite_this_user_max,"】回です！！","\n"*3)

    for friend in friends:
        if favorite_max > favorite_count:
            favorite_count_this_user = 0
            print("-"*10,"【",friend,"】さんへのいいねを開始します","-"*10)
            friend_timelines = api.user_timeline(screen_name = friend ,count = 100)
            for tweet in friend_timelines:
                if favorite_max > favorite_count:#いいね上限に達するまでいいね処理を行う
                   if favorite_this_user_max > favorite_count_this_user:
                    """
                    judgment_result = keyword_exclusion(NG_word)
                    #NGワードを含んだ場合は、スキップする
                    if judgment_result == True:
                        print("⚠️NG処理","\n")
                        continue
                    #NGを含まなかった場合は処理をする
                    else:
                    """
                    if tweet._json['in_reply_to_screen_name'] == None:

                        ####いいね処理####
                        processing_result = favorite_processing()
                            #処理成功
                        if processing_result == 0:
                            favorite_count += 1
                            favorite_count_this_user += 1
                            #エラー
                        elif processing_result == 1:
                            continue
                            #検索した分処理し切った
                        elif processing_result == 2:
                            break
                    else:
                        #print("誰かへのリプライでした","\n"*5)
                        continue
                else:
                    print("\n"*5,"🙅‍♂️"*15,"いいね上限です","‍🙅‍♂️"*15,"\n"*2)
                    break
        else:
            break


print('>'*15,"処理が終了しました",'<'*15,"\n")
print('>'*15,"処理の結果【",favorite_count,"】回のいいねをしました",'<'*15,"\n")
print('>'*15,"処理の結果【",reply_count,"】回のリプライをしました",'<'*15,"\n")

now_time()
print("\n"*10)
