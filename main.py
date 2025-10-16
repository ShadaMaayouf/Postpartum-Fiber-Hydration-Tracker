import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Initialize tracker
tracker = pd.DataFrame(columns=["Date", "Fiber_g", "Water_L", "Baby_Feeds", "Notes"])

# Recommended daily intake
FIBER_GOAL = 25  # grams
WATER_GOAL = 2.5  # liters
FEED_GOAL = 8     # feeds/day

def log_day(fiber, water, feeds, notes=""):
    today = datetime.date.today().isoformat()
    global tracker
    tracker.loc[len(tracker)] = [today, fiber, water, feeds, notes]
    print(f"\n✅ Logged for {today}: {fiber}g fiber, {water}L water, {feeds} feeds.")
    check_goals(fiber, water, feeds)

def check_goals(fiber, water, feeds):
    if fiber < FIBER_GOAL:
        print(f"⚠️ Fiber below goal ({fiber}g). Add oats, lentils, or prunes.")
    else:
        print("🎉 Fiber goal met!")

    if water < WATER_GOAL:
        print(f"⚠️ Hydration below goal ({water}L). Sip warm lemon water or herbal tea.")
    else:
        print("💧 Hydration goal met!")

    if feeds < FEED_GOAL:
        print(f"🍼 Baby feeds below goal ({feeds}). Consider tracking nursing/pumping intervals.")
    else:
        print("👶 Baby feeding goal met!")

def show_tracker():
    print("\n📊 Last 7 Days Summary:")
    print(tracker.tail(7))

def plot_trends():
    tracker["Date"] = pd.to_datetime(tracker["Date"])
    tracker.set_index("Date", inplace=True)
    tracker[["Fiber_g", "Water_L", "Baby_Feeds"]].plot(marker='o', figsize=(10, 5))
    plt.title("Postpartum Wellness Trends")
    plt.ylabel("Daily Totals")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    tracker.reset_index(inplace=True)

def export_to_excel(filename="postpartum_tracker.xlsx"):
    tracker.to_excel(filename, index=False)
    print(f"📤 Tracker exported to {filename}")

# Example usage
log_day(fiber=22, water=2.0, feeds=6, notes="Low energy, skipped afternoon snack.")
log_day(fiber=28, water=2.7, feeds=9, notes="Added flax to porridge, felt great.")
show_tracker()
plot_trends()
export_to_excel()
