# app.py
# ------------------------------------------------------------------
# IPL Match Insights & Player Performance Analytics Dashboard
# Run with:  streamlit run app.py
# ------------------------------------------------------------------

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ── Import helper modules ──────────────────────────────────────────
from utils.data_loader    import load_matches, load_deliveries, merge_datasets
from utils.analysis       import (
    matches_won_by_team, toss_impact, toss_decision_impact,
    top_run_scorers, top_wicket_takers, team_win_percentage,
    highest_scoring_venues, season_wise_trends, season_avg_score,
    player_strike_rate, orange_cap, purple_cap,
    player_batting_summary, head_to_head,
)
from utils.visualizations import (
    plot_matches_won, plot_toss_impact, plot_top_run_scorers,
    plot_top_wicket_takers, plot_team_win_pct, plot_venues,
    plot_season_avg_score, plot_strike_rate,
    plot_orange_cap, plot_purple_cap, plot_dismissal_heatmap,
)

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for dark IPL theme ─────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0D1117; color: #C9D1D9; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #161B22; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 12px;
    }

    /* Headers */
    h1, h2, h3 { color: #E8871E !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] { color: #8B949E; }
    .stTabs [aria-selected="true"] { color: #E8871E !important; border-bottom-color: #E8871E !important; }

    /* Divider */
    hr { border-color: #30363D; }
</style>
""", unsafe_allow_html=True)


# ── Data Loading (cached so it runs only once) ────────────────────
@st.cache_data
def load_data():
    """Load and cache both IPL datasets."""
    matches_path    = "datasets/matches.csv"
    deliveries_path = "datasets/deliveries.csv"

    # Friendly error if CSV files are missing
    if not os.path.exists(matches_path) or not os.path.exists(deliveries_path):
        st.error(
            "⚠️  Dataset files not found!\n\n"
            "Please place `matches.csv` and `deliveries.csv` inside the `datasets/` folder.\n\n"
            "You can download them from Kaggle: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020"
        )
        st.stop()

    matches    = load_matches(matches_path)
    deliveries = load_deliveries(deliveries_path)
    return matches, deliveries


matches, deliveries = load_data()


# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg",
    width=160,
)
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("---")

# Season filter
all_seasons = sorted(matches["season"].dropna().unique().astype(int))
selected_seasons = st.sidebar.multiselect(
    "📅 Select Season(s)",
    options=all_seasons,
    default=all_seasons,
    help="Filter all charts by IPL season"
)

# Team filter
all_teams = sorted(
    set(matches["team1"].unique()) | set(matches["team2"].unique())
)
selected_teams = st.sidebar.multiselect(
    "🏟️ Select Team(s)",
    options=all_teams,
    default=all_teams,
)

# Player search
all_batsmen = sorted(deliveries["batsman"].unique())
selected_player = st.sidebar.selectbox(
    "🧑 Player Spotlight",
    options=["-- Select Player --"] + all_batsmen,
)

st.sidebar.markdown("---")
st.sidebar.caption("Data: Kaggle IPL Dataset (2008-2020)")

# ── Apply Filters ─────────────────────────────────────────────────
def filter_matches(df):
    return df[
        df["season"].isin(selected_seasons) &
        (df["team1"].isin(selected_teams) | df["team2"].isin(selected_teams))
    ]

def filter_deliveries(df, match_ids):
    return df[df["match_id"].isin(match_ids)]

filtered_matches    = filter_matches(matches)
filtered_match_ids  = filtered_matches["id"].unique()
filtered_deliveries = filter_deliveries(deliveries, filtered_match_ids)


# ── Header ───────────────────────────────────────────────────────
st.title("🏏 IPL Match Insights & Player Performance Dashboard")
st.caption(
    f"Showing data for **{len(selected_seasons)} season(s)** "
    f"• **{len(selected_teams)} team(s)** "
    f"• **{len(filtered_matches)} matches**"
)
st.markdown("---")


# ── KPI Metrics Row ───────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🏟️ Total Matches",    len(filtered_matches))
with col2:
    st.metric("🏏 Total Runs",        f"{int(filtered_deliveries['total_runs'].sum()):,}")
with col3:
    st.metric("🎳 Total Wickets",     int(filtered_deliveries["is_wicket"].sum()))
with col4:
    top_team = matches_won_by_team(filtered_matches).idxmax() if not filtered_matches.empty else "N/A"
    st.metric("🥇 Most Wins",         top_team)
with col5:
    top_scorer = top_run_scorers(filtered_deliveries, 1)
    ts_name    = top_scorer.iloc[0]["Player"] if not top_scorer.empty else "N/A"
    ts_runs    = int(top_scorer.iloc[0]["Total Runs"]) if not top_scorer.empty else 0
    st.metric("🔥 Top Scorer",        ts_name, f"{ts_runs} runs")

st.markdown("---")


# ── Tab Navigation ────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏆 Teams",
    "🏏 Batting",
    "🎳 Bowling",
    "🏟️ Venues",
    "📈 Trends",
    "👤 Player Spotlight",
])


# ═══════════════════════════════════════════════════════
#  TAB 1 — Teams
# ═══════════════════════════════════════════════════════
with tab1:
    st.subheader("Team Performance Overview")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Matches Won")
        wins = matches_won_by_team(filtered_matches)
        st.pyplot(plot_matches_won(wins))

    with col_b:
        st.markdown("#### Win Percentage")
        win_pct = team_win_percentage(filtered_matches)
        if not win_pct.empty:
            st.pyplot(plot_team_win_pct(win_pct))
        else:
            st.info("Not enough data for selected filters.")

    st.markdown("---")

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### Toss Impact on Match Result")
        toss_df = toss_impact(filtered_matches)
        st.pyplot(plot_toss_impact(toss_df))

    with col_d:
        st.markdown("#### Toss Decision Impact")
        td_df = toss_decision_impact(filtered_matches)
        st.dataframe(td_df, use_container_width=True, hide_index=True)

        # Head-to-head section
        st.markdown("#### Head-to-Head")
        teams_for_h2h = sorted(
            set(filtered_matches["team1"].unique()) |
            set(filtered_matches["team2"].unique())
        )
        if len(teams_for_h2h) >= 2:
            h2h_col1, h2h_col2 = st.columns(2)
            with h2h_col1:
                t1 = st.selectbox("Team A", teams_for_h2h, key="t1")
            with h2h_col2:
                remaining = [t for t in teams_for_h2h if t != t1]
                t2 = st.selectbox("Team B", remaining, key="t2")

            h2h_df = head_to_head(filtered_matches, t1, t2)
            if h2h_df.empty:
                st.info("No matches found between selected teams.")
            else:
                st.write(f"**{t1}** vs **{t2}** — {len(h2h_df)} match(es)")
                wins_t1 = (h2h_df["winner"] == t1).sum()
                wins_t2 = (h2h_df["winner"] == t2).sum()
                st.write(f"🏆 {t1}: **{wins_t1}** | {t2}: **{wins_t2}**")
                st.dataframe(h2h_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
#  TAB 2 — Batting
# ═══════════════════════════════════════════════════════
with tab2:
    st.subheader("Batting Insights")

    col_a, col_b = st.columns([3, 2])

    with col_a:
        top_n = st.slider("Top N run scorers", 5, 20, 10, key="run_slider")
        runs_df = top_run_scorers(filtered_deliveries, top_n)
        st.pyplot(plot_top_run_scorers(runs_df))

    with col_b:
        st.markdown("#### Leaderboard")
        st.dataframe(runs_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Strike Rate Analysis (min 500 runs)")
    sr_df = player_strike_rate(filtered_deliveries, min_runs=500)
    if not sr_df.empty:
        st.pyplot(plot_strike_rate(sr_df))
        st.dataframe(sr_df.head(20), use_container_width=True, hide_index=True)
    else:
        st.info("Not enough data for selected filters.")

    st.markdown("---")
    st.subheader("🟠 Orange Cap Winners")
    oc_df = orange_cap(filtered_deliveries, filtered_matches)
    if not oc_df.empty:
        col_e, col_f = st.columns([2, 1])
        with col_e:
            st.pyplot(plot_orange_cap(oc_df))
        with col_f:
            st.dataframe(oc_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
#  TAB 3 — Bowling
# ═══════════════════════════════════════════════════════
with tab3:
    st.subheader("Bowling Insights")

    col_a, col_b = st.columns([3, 2])
    with col_a:
        top_n_w = st.slider("Top N wicket takers", 5, 20, 10, key="wkt_slider")
        wkt_df = top_wicket_takers(filtered_deliveries, top_n_w)
        st.pyplot(plot_top_wicket_takers(wkt_df))
    with col_b:
        st.markdown("#### Leaderboard")
        st.dataframe(wkt_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🟣 Purple Cap Winners")
    pc_df = purple_cap(filtered_deliveries, filtered_matches)
    if not pc_df.empty:
        col_e, col_f = st.columns([2, 1])
        with col_e:
            st.pyplot(plot_purple_cap(pc_df))
        with col_f:
            st.dataframe(pc_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔥 Dismissal Type Heatmap")
    if not filtered_deliveries.empty:
        st.pyplot(plot_dismissal_heatmap(filtered_deliveries))


# ═══════════════════════════════════════════════════════
#  TAB 4 — Venues
# ═══════════════════════════════════════════════════════
with tab4:
    st.subheader("Venue Analysis")
    top_n_v = st.slider("Top N venues", 5, 15, 10, key="venue_slider")
    venue_df = highest_scoring_venues(filtered_deliveries, filtered_matches, top_n_v)
    st.pyplot(plot_venues(venue_df))
    st.dataframe(venue_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
#  TAB 5 — Season Trends
# ═══════════════════════════════════════════════════════
with tab5:
    st.subheader("Season-wise Trends")

    avg_score_df = season_avg_score(filtered_deliveries, filtered_matches)
    if not avg_score_df.empty:
        st.pyplot(plot_season_avg_score(avg_score_df))

    st.markdown("---")
    st.markdown("#### Season Summary Table")
    trends_df = season_wise_trends(filtered_matches)
    st.dataframe(trends_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
#  TAB 6 — Player Spotlight
# ═══════════════════════════════════════════════════════
with tab6:
    st.subheader("👤 Player Spotlight")

    if selected_player == "-- Select Player --":
        st.info("👈 Select a player from the sidebar to see their stats.")
    else:
        stats = player_batting_summary(filtered_deliveries, selected_player)
        if not stats:
            st.warning(f"No batting data found for **{selected_player}** in the selected filters.")
        else:
            st.markdown(f"### {selected_player}")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total Runs",   stats["Runs"])
            m2.metric("Balls Faced",  stats["Balls"])
            m3.metric("Strike Rate",  stats["Strike Rate"])
            m4.metric("Fours (4s)",   stats["4s"])
            m5.metric("Sixes (6s)",   stats["6s"])

            # Runs per season for this player
            meta = filtered_matches[["id", "season"]].rename(columns={"id": "match_id"})
            pdf  = filtered_deliveries[filtered_deliveries["batsman"] == selected_player]
            if not pdf.empty:
                season_runs = (
                    pdf.merge(meta, on="match_id")
                    .groupby("season")["batsman_runs"]
                    .sum()
                    .reset_index()
                )
                fig, ax = plt.subplots(figsize=(10, 4),
                                       facecolor="#0D1117")
                ax.set_facecolor("#161B22")
                ax.plot(season_runs["season"], season_runs["batsman_runs"],
                        marker="o", color="#E8871E", linewidth=2.5, markersize=8)
                ax.fill_between(season_runs["season"], season_runs["batsman_runs"],
                                alpha=0.15, color="#E8871E")
                ax.set_title(f"{selected_player} – Runs per Season",
                             color="#F0F6FC", fontweight="bold")
                ax.set_xlabel("Season", color="#C9D1D9")
                ax.set_ylabel("Runs", color="#C9D1D9")
                ax.tick_params(colors="#C9D1D9")
                ax.grid(color="#21262D")
                st.pyplot(fig)

# ── Footer ───────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "🏏 IPL Analytics Dashboard  •  Built with Python, Pandas, Seaborn & Streamlit  •  "
    "Data Source: Kaggle IPL Dataset"
)
