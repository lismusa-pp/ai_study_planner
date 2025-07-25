def display_schedule(schedule):
    print("\n📅 Your Study Schedule:")
    for block in schedule:
        print(f"🔸 {block['subject']} from {block['start']} to {block['end']}")
