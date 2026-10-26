import json, sys

files = ["temp_probe1.json", "temp_probe2.json", "temp_probe3.json"]
labels = ["DJI_0057", "DJI_0062", "DJI_0064"]

for f, label in zip(files, labels):
    with open(f, encoding="utf-8-sig") as fp:
        d = json.load(fp)
    fmt = d["format"]
    duration = float(fmt["duration"])
    size_mb = int(fmt["size"]) / 1024 / 1024
    vs = next(s for s in d["streams"] if s["codec_type"] == "video")
    a_streams = [s for s in d["streams"] if s["codec_type"] == "audio"]
    fps_raw = vs.get("r_frame_rate", "?")
    print(f"FILE: {label}")
    print(f"  Duration:   {duration:.1f}s  ({duration/60:.1f} min)")
    print(f"  Size:       {size_mb:.0f} MB")
    print(f"  Resolution: {vs['width']}x{vs['height']}")
    print(f"  FPS:        {fps_raw}")
    print(f"  Codec:      {vs['codec_name']} / Profile: {vs.get('profile','?')}")
    print(f"  Audio:      {len(a_streams)} stream(s)")
    if a_streams:
        a = a_streams[0]
        print(f"    Codec: {a['codec_name']}, Channels: {a.get('channels','?')}, Sample rate: {a.get('sample_rate','?')}")
    print()
