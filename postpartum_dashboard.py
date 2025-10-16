import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# --- Konfiguration ---
FIBER_GOAL = 25     # g
WATER_GOAL = 2.5    # Liter
FEED_GOAL = 8       # Still-/Flaschenmahlzeiten
FILENAME = "tracker.csv"

# --- Daten laden oder initialisieren ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv(FILENAME, parse_dates=["Date"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Fiber_g", "Water_L", "Baby_Feeds", "Notes"])

tracker = load_data()

# --- Logging-Funktion mit Zielprüfung ---
def log_day(fiber, water, feeds, notes):
    today = pd.to_datetime(date.today())
    new_entry = pd.DataFrame([[today, fiber, water, feeds, notes]],
                             columns=["Date", "Fiber_g", "Water_L", "Baby_Feeds", "Notes"])
    global tracker
    tracker = pd.concat([tracker, new_entry], ignore_index=True)
    tracker.to_csv(FILENAME, index=False)

    # Feedback
    st.success(f"✅ Eingetragen: {fiber}g Ballaststoffe, {water}L Wasser, {feeds} Stillmahlzeiten")
    if fiber < FIBER_GOAL:
        st.warning(f"⚠️ Ballaststoffe unter Ziel ({fiber}g). Tipp: Haferflocken, Linsen, Pflaumen.")
    else:
        st.info("🎉 Ballaststoff-Ziel erreicht!")

    if water < WATER_GOAL:
        st.warning(f"⚠️ Trinkmenge unter Ziel ({water}L). Tipp: Kräutertee, Zitronenwasser.")
    else:
        st.info("💧 Hydrationsziel erreicht!")

    if feeds < FEED_GOAL:
        st.warning(f"🍼 Weniger als {FEED_GOAL} Mahlzeiten. Bei Bedarf Still-/Pumpzeiten notieren.")
    else:
        st.info("👶 Stillziel erreicht!")

# --- Sidebar: Eingabe ---
st.sidebar.title("🍼 Tagesprotokoll")
fiber = st.sidebar.number_input("Ballaststoffe (g)", min_value=0, max_value=100, value=25)
water = st.sidebar.number_input("Wasser (L)", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
feeds = st.sidebar.number_input("Still-/Flaschenmahlzeiten", min_value=0, max_value=20, value=8)
notes = st.sidebar.text_area("Notizen", placeholder="Stimmung, Symptome, Beobachtungen…")
submit = st.sidebar.button("Heute eintragen")

if submit:
    log_day(fiber, water, feeds, notes)

# --- Hauptbereich: Dashboard ---
st.title("🌿 Postpartum Tracker")
st.markdown("Verfolge Ballaststoffe, Hydration & Stillen – für dich und dein Baby.")

if not tracker.empty:
    tracker["Date"] = pd.to_datetime(tracker["Date"])
    tracker.sort_values("Date", inplace=True)

    # --- Diagramm ---
    st.subheader("📈 Verlauf")
    fig, ax = plt.subplots(figsize=(10, 4))
    tracker.set_index("Date")[["Fiber_g", "Water_L", "Baby_Feeds"]].plot(ax=ax, marker='o')
    plt.ylabel("Tageswerte")
    plt.grid(True)
    st.pyplot(fig)

    # --- Tabelle ---
    st.subheader("📋 Letzte Einträge")
    st.dataframe(tracker.tail(7).sort_values("Date", ascending=False), use_container_width=True)

    # --- Export ---
    st.download_button("📤 Als CSV exportieren", data=tracker.to_csv(index=False),
                       file_name="postpartum_tracker.csv", mime="text/csv")
else:
    st.info("Noch keine Einträge. Nutze die Sidebar, um zu starten.")
