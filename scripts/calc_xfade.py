import sys, os, json

# Danh sách 12 clips với timeline dự kiến và transitions:
# Target timeline:
# Scene 1: 0.0 -> 3.5s (dur 3.5s)
# Scene 2: 3.5 -> 6.5s (dur 3.0s)
# Scene 3: 6.5 -> 14.5s (dur 8.0s)
# Scene 4: 14.5 -> 21.5s (dur 7.0s)
# Scene 5: 21.5 -> 27.9s (dur 6.4s)
# Scene 6: 27.9 -> 34.0s (dur 6.1s)
# Scene 7: 34.0 -> 40.5s (dur 6.5s)
# Scene 8: 40.5 -> 45.0s (dur 4.5s)
# Scene 9: 45.0 -> 52.0s (dur 7.0s)
# Scene 10: 52.0 -> 61.6s (dur 9.6s)
# Scene 11: 61.6 -> 71.8s (dur 10.2s)
# Scene 12: 71.8 -> 82.0s (dur 10.2s)

CLIPS_SPEC = [
    # seg_id, source, ss, net_dur, is_night, trans_to_next, trans_dur
    (1, "DJI_0057", 1.0, 3.5, False, "smoothleft", 0.35),
    (2, "DJI_0062", 1.0, 3.0, True, "fadeblack", 0.40),
    (3, "DJI_0057", 5.0, 8.0, False, "dissolve", 0.40),
    (4, "DJI_0057", 13.0, 7.0, False, "smoothleft", 0.35),
    (5, "DJI_0057", 20.0, 6.4, False, "fadeblack", 0.50),
    (6, "DJI_0062", 6.0, 6.1, True, "dissolve", 0.40),
    (7, "DJI_0062", 14.0, 6.5, True, "smoothleft", 0.35),
    (8, "DJI_0062", 38.0, 4.5, True, "fadeblack", 0.50),
    (9, "DJI_0064", 25.0, 7.0, True, "dissolve", 0.40),
    (10, "DJI_0064", 75.0, 9.6, True, "dissolve", 0.40),
    (11, "DJI_0064", 135.0, 10.2, True, "dissolve", 0.40),
    (12, "DJI_0064", 150.0, 10.2, True, None, 0.0),
]

# Với mỗi clip i:
# Nguồn vào cần có độ dài raw_dur = net_dur + trans_dur (để bù lại phần bị overlap bởi xfade)
# Như vậy, timeline của video sau khi qua tất cả các xfade sẽ có độ dài = sum(net_dur) = 82.0s!
total_net = sum(c[3] for c in CLIPS_SPEC)
print(f"Total net duration: {total_net:.2f}s")

# Tính toán offset cho từng xfade:
# Clip 0 có raw_dur_0 = net_dur_0 + trans_dur_0.
# xfade 0 xảy ra tại offset_0 = net_dur_0.
# Sau xfade 0, độ dài luồng kết quả v1 là: offset_0 + raw_dur_1 = net_dur_0 + net_dur_1 + trans_dur_1.
# xfade 1 xảy ra tại offset_1 = net_dur_0 + net_dur_1.
# Và tổng quát: offset_k = sum(net_dur_0 .. net_dur_k)!
print("\nXfade offsets:")
cur_offset = 0.0
for i in range(len(CLIPS_SPEC) - 1):
    c = CLIPS_SPEC[i]
    cur_offset += c[3] # net_dur
    print(f"Xfade {i:02d} -> {i+1:02d}: transition={c[5]:10s} duration={c[6]:4.2f}s at offset={cur_offset:5.2f}s")
