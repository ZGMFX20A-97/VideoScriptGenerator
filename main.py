import streamlit as st
from utils import generate_script
import openai

#アプリのタイトルを定義
st.title("🎬動画台本ジェネレーター")

#api keyを入力するためのサイドバーを定義
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Keyを入力してください：", type="password"
    )
    st.markdown(
        "[OpenAI API Keyを取得する](https://platform.openai.com/account/api-keys)"
    )

#動画テーマを受け取る変数を定義
subject = st.text_input("💡動画のテーマを入力してください")

#動画の長さを受け取る変数を定義
video_length = st.number_input(
    "⏰動画の長さを入力してください（単位：分）", min_value=0.1, step=1.0
)

#モデルのtemperatureを受け取る変数を定義
creativity = st.slider(
    "✨AIのクリエーティビティ（数字が小さいほど控えめ，大きいほど自由奔放）",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1,
)

#生成ボタンの定義
submit = st.button("台本を生成する")

if submit and not openai_api_key:
    st.info("OpenAI API Keyを入力してください")
    st.stop()
if submit and not subject:
    st.info("動画のテーマを入力してください")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("動画の長さは最低でも0.1分です")
    st.stop()
if submit:
    with st.spinner(("AIが考えています。少々お待ちを。。。")):
        try:
            _, title, script = generate_script(
                subject, video_length, creativity, openai_api_key
            )
            st.success("台本が出来上がりました！")
            st.subheader("🔥タイトル")
            st.write(title)
            st.subheader("📝内容")
            st.write(script)
        except openai.AuthenticationError as e:
            st.error("エラー：正しいAPI Keyを入力してください")
