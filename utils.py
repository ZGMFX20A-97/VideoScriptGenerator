from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

#AI処理を定義する
def generate_script(subject, video_length, creativity, api_key):

    #タイトルを生成するためのプロンプトをAIに渡し、レスポンスを受け取る
    title_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                "'{subject}'をテーマとした動画のためにリスナーを惹きつけるタイトルを考えてください",
            )
        ]
    )

    #台本を生成するためのプロンプトを渡し、レスポンスを受け取る
    script_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                """あなたにショート動画の製作者になりすましてほしいです。以下で提示した動画のタイトルと情報に基づいて動画の台本を生成してください。
             動画のタイトル：{title}，動画の長さ：{duration}分。
             生成した台本のボリュームはできる限り動画の長さに収めること。
             台本内容の具体的な要求としては、
             1.動画のイントロからリスナーを惹きつけるような内容にしておくこと。
             2.中身の部分は論理的な内容で、出鱈目だと感じさせないようににしておくこと。
             3.締めの部分は動画内容についての思考を発展させるような内容にしておくこと。
             4.台本の出力フォーマットはマークダウン記法で【イントロ、中身、締め】の形にしておくこと。
             全体としてはリスナーに面白みを感じさせることを第一にし、若者を惹きつける内容にすること。
             台本の生成には以下のウィキペディアから取得した情報を参考にしても良い。テーマと無関係な情報は無視してください。
             ```{wikipedia_search}```""",
            )
        ]
    )
    #モデルを定義する
    model = ChatOpenAI(model="gpt-3.5-turbo",api_key=api_key, temperature=creativity)

    #タイトルを生成する処理チェーン
    title_chain = title_template | model
    #台本を生成する処理チェーン
    script_chain = script_template | model

    #タイトル生成チェーンのinvoke関数にユーザーが入力したテーマを渡す
    title = title_chain.invoke({"subject": subject}).content

    """モデルの訓練時期によって最新の情報を持っていない可能性があるため、
    WikipediaのAPIを使用してテーマに関する最新情報を検索しそれを含めてAIに渡す"""
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    #台本生成チェーンのinvoke関数にAIが生成したタイトル、ユーザーが入力した動画の長さ、Wikipediaの検索結果を渡す
    script = script_chain.invoke(
        {"title": title, "duration": video_length, "wikipedia_search": search_result}
    ).content

    return search_result, title, script
