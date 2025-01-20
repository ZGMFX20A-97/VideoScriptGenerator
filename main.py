import streamlit as st
from utils import generate_script
import openai


st.title("🎬视频文案生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI密钥](https://platform.openai.com/account/api-keys)")

subject = st.text_input("💡请输入视频主题")

video_length = st.number_input(
    "⏰请输入视频的大致时长（单位：分钟）", min_value=0.1, step=1.0
)

creativity = st.slider(
    "✨请输入视频文案的创造力（数字越小越严谨，数字越大越天马行空）",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1,
)

submit = st.button("生成脚本")

if submit and not openai_api_key:
    st.info("请输入你的OpenAI AI密钥")
    st.stop()
if submit and not subject:
    st.info("请输入视频主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需大于等于0.1分钟")
    st.stop()
if submit:
    with st.spinner(("AI正在思考，请稍等。。。")):
        try:
            _, title, script = generate_script(
                subject, video_length, creativity, openai_api_key
            )
            st.success("视频脚本已生成！")
            st.subheader("🔥标题")
            st.write(title)
            st.subheader("📝脚本")
            st.write(script)
        except openai.AuthenticationError as e:
            st.error("错误：提供的 API 密钥无效")

        except openai.RateLimitError as e:
            st.error(
                """错误：达到了 API 的请求速率限制
                        或免费账户或订阅账户的使用配额已用完"""
            )
        except openai.APIConnectionError as e:
            st.error("错误：无法连接到OPENAI服务器，请稍后再试")
        except openai.InternalServerError as e:
            st.error("错误：OPENAI服务器出现错误，请稍后再试")
