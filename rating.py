import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import random
import string

# 配置文件路径
DATA_FILE = "arknights_scores.json"

# 职业派系列表
FACTIONS = [
    '绵绵细雨', '狂风暴雨', '王后恩赐', '国王圣谕', '炮击强化', '火力强化',
    '归元', '勇气激发', '狂战士秘技', '疯狂', '修罗之路', '拳王破天舞',
    '强化武器', '手枪手', '弥留之息', '爆裂', '重力修练', '愤怒之锤',
    '节制', '巅峰', '战斗姿态', '孤独的骑士', '和平之光', '狩猎时刻',
    '阿尔泰因科技', '超同步核心', '裁决许可', '饥渴', '月声', '冲击修炼',
    '极义：体术', '无尽冲动', '完美抑制', '终结袭击', '第二个伙伴', '捕食者',
    '处决者', '点火', '环流', '满月鬼门开', '晦朔边界', '经脉打通',
    '逆天之体', '一击必杀', '奥义乱舞', '心有灵犀', '高阶召唤', '奥义精通',
    '赤子之心', '野性', '幻兽觉醒'
]


# 初始化数据结构
def init_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"scores": {}, "history": {}}


# 保存数据
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 生成匿名用户ID
def generate_anonymous_id():
    if 'anonymous_id' not in st.session_state:
        # 生成随机匿名ID
        st.session_state.anonymous_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return st.session_state.anonymous_id


# 主应用
def main():
    st.set_page_config(page_title="命运方舟职业派系打分", layout="wide")
    st.title("命运方舟职业派系打分系统")
    st.markdown("---")

    # 生成匿名用户ID
    anonymous_id = generate_anonymous_id()
    st.info(f"当前匿名用户ID: {anonymous_id}（你的所有评分都会关联到这个ID）")

    # 初始化数据
    data = init_data()

    # 创建标签页
    tab1, tab2 = st.tabs(["打分", "查看历史"])

    with tab1:
        st.header("为职业派系打分")
        st.info("请为你知道的职业派系打分（1-5分），不了解的可以不打分")

        # 获取当前用户的评分数据
        scores = {}
        if anonymous_id in data["scores"]:
            scores = data["scores"][anonymous_id]

        # 按行显示派系，每行3个
        for i in range(0, len(FACTIONS), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(FACTIONS):
                    faction = FACTIONS[i + j]
                    with cols[j]:
                        current_score = scores.get(faction, 0)
                        score = st.selectbox(
                            faction,
                            options=[0, 1, 2, 3, 4, 5],
                            format_func=lambda x: "不打分" if x == 0 else f"{x}分",
                            key=f"score_{faction}",
                            index=[0, 1, 2, 3, 4, 5].index(current_score) if current_score in [0, 1, 2, 3, 4, 5] else 0
                        )
                        scores[faction] = score

        # 保存按钮
        if st.button("保存打分", type="primary", use_container_width=True):
            # 更新数据
            if anonymous_id not in data["scores"]:
                data["scores"][anonymous_id] = {}

            # 记录历史
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if anonymous_id not in data["history"]:
                data["history"][anonymous_id] = []

            data["history"][anonymous_id].append({
                "timestamp": timestamp,
                "scores": scores.copy()
            })

            # 只保留最近10条历史记录
            if len(data["history"][anonymous_id]) > 10:
                data["history"][anonymous_id] = data["history"][anonymous_id][-10:]

            data["scores"][anonymous_id] = scores
            save_data(data)
            st.success("打分已保存！")

            # 显示保存的评分摘要
            rated_count = len([s for s in scores.values() if s > 0])
            st.info(f"你本次共评分 {rated_count} 个派系")

    with tab2:
        st.header("历史打分记录")

        # 选择要查看的派系
        selected_faction = st.selectbox("选择要查看的派系:", ["全部"] + FACTIONS)

        if selected_faction == "全部":
            # 显示所有派系的统计信息
            st.subheader("所有派系打分统计")

            # 计算每个派系的统计数据
            faction_stats = {}
            all_users = list(data["scores"].keys())

            for faction in FACTIONS:
                scores_list = []
                user_count = 0
                for user in all_users:
                    if faction in data["scores"][user] and data["scores"][user][faction] > 0:
                        scores_list.append(data["scores"][user][faction])
                        user_count += 1

                if scores_list:
                    faction_stats[faction] = {
                        "平均分": round(sum(scores_list) / len(scores_list), 2),
                        "最高分": max(scores_list),
                        "最低分": min(scores_list),
                        "评分人数": user_count,
                        "总评分": scores_list
                    }
                else:
                    faction_stats[faction] = {
                        "平均分": 0,
                        "最高分": 0,
                        "最低分": 0,
                        "评分人数": 0,
                        "总评分": []
                    }

            # 显示统计表格
            stats_df = pd.DataFrame(faction_stats).T
            stats_df = stats_df[['平均分', '最高分', '最低分', '评分人数']]

            # 按平均分排序
            stats_df = stats_df.sort_values('平均分', ascending=False)

            st.dataframe(stats_df.style.format({
                '平均分': '{:.2f}',
                '最高分': '{:.0f}',
                '最低分': '{:.0f}'
            }).background_gradient(cmap='Blues', subset=['平均分']))

            # 显示评分分布图表
            st.subheader("评分分布")
            import matplotlib.pyplot as plt

            plt.rcParams['font.family'] = 'Heiti TC'

            # 过滤出有评分的派系
            rated_factions = [f for f in FACTIONS if faction_stats[f]["评分人数"] > 0]
            if rated_factions:
                fig, ax = plt.subplots(figsize=(12, 8))
                factions_for_chart = rated_factions[:20]  # 只显示前20个有评分的
                avg_scores = [faction_stats[f]["平均分"] for f in factions_for_chart]

                bars = ax.bar(range(len(factions_for_chart)), avg_scores, color='skyblue')
                ax.set_xlabel('职业派系')
                ax.set_ylabel('平均分')
                ax.set_title('职业派系平均分排名（有评分的前20）')
                ax.set_xticks(range(len(factions_for_chart)))
                ax.set_xticklabels(factions_for_chart, rotation=45, ha='right')

                # 在柱子上显示数值
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{height:.1f}', ha='center', va='bottom')

                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("暂无评分数据")

            # 显示参与用户统计
            st.subheader("参与统计")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("参与用户数", len(all_users))
            with col2:
                total_ratings = sum([len([s for s in user_scores.values() if s > 0])
                                     for user_scores in data["scores"].values()])
                st.metric("总评分次数", total_ratings)

        else:
            # 显示特定派系的历史记录
            st.subheader(f"「{selected_faction}」派系详细评分记录")

            # 收集该派系的所有评分
            faction_scores = []
            for user, user_scores in data["scores"].items():
                if selected_faction in user_scores and user_scores[selected_faction] > 0:
                    faction_scores.append({
                        "用户ID": user[:6] + "..." if len(user) > 6 else user,  # 简化显示
                        "评分": user_scores[selected_faction]
                    })

            if faction_scores:
                df = pd.DataFrame(faction_scores)
                df = df.sort_values("评分", ascending=False)
                st.dataframe(df, use_container_width=True)

                # 显示统计信息
                scores_only = [item["评分"] for item in faction_scores]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("平均分", f"{sum(scores_only) / len(scores_only):.2f}")
                with col2:
                    st.metric("最高分", max(scores_only))
                with col3:
                    st.metric("最低分", min(scores_only))
                with col4:
                    st.metric("评分人数", len(scores_only))

                # 显示评分分布
                st.subheader("评分分布图表")
                import matplotlib.pyplot as plt
                import numpy as np

                fig, ax = plt.subplots(figsize=(8, 4))
                scores_count = {i: scores_only.count(i) for i in range(1, 6)}
                bars = ax.bar(scores_count.keys(), scores_count.values(),
                              color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
                ax.set_xlabel('评分')
                ax.set_ylabel('人数')
                ax.set_title(f'「{selected_faction}」评分分布')
                ax.set_xticks(range(1, 6))

                # 在柱子上显示数值
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width() / 2., height,
                                f'{int(height)}', ha='center', va='bottom')

                st.pyplot(fig)
            else:
                st.info("暂无用户对该派系进行评分")

        # 显示当前用户的打分历史
        st.markdown("---")
        st.subheader(f"你的打分历史（ID: {anonymous_id[:6]}...）")

        if anonymous_id in data["history"] and data["history"][anonymous_id]:
            history_list = []
            for record in data["history"][anonymous_id]:
                history_item = {"时间": record["timestamp"]}
                rated_count = len([s for s in record["scores"].values() if s > 0])
                history_item["评分数量"] = rated_count
                # 显示前5个评分作为示例
                rated_items = {k: v for k, v in record["scores"].items() if v > 0}
                if rated_items:
                    sample_items = dict(list(rated_items.items())[:5])
                    history_item["示例评分"] = ", ".join([f"{k}:{v}分" for k, v in sample_items.items()])
                    if len(rated_items) > 5:
                        history_item["示例评分"] += f" (等{len(rated_items)}个)"
                else:
                    history_item["示例评分"] = "无评分"
                history_list.append(history_item)

            history_df = pd.DataFrame(history_list)
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("暂无打分历史记录")

        # 显示你的当前评分
        if anonymous_id in data["scores"]:
            current_scores = data["scores"][anonymous_id]
            rated_factions = {k: v for k, v in current_scores.items() if v > 0}
            if rated_factions:
                st.subheader("你当前的评分")
                rated_df = pd.DataFrame(list(rated_factions.items()), columns=['派系', '评分'])
                rated_df = rated_df.sort_values('评分', ascending=False)
                st.dataframe(rated_df, use_container_width=True)


if __name__ == "__main__":
    main()
