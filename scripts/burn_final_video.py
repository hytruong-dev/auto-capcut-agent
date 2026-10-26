import subprocess, os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ass_path = r'c:\QuangHy\editvideo\processed\xanhsm_story_master.ass'
fonts_dir = r'c:\QuangHy\editvideo\portable_trained_brain\portable_assets\fonts'

ass_filter = ass_path.replace('\\', '/').replace(':', r'\:')
fonts_filter = fonts_dir.replace('\\', '/').replace(':', r'\:')

mix_cmd = [
    'ffmpeg', '-y',
    '-i', r'c:\QuangHy\editvideo\processed\xanhsm_story_raw.mp4',
    '-i', r'c:\QuangHy\editvideo\processed\voiceover\xanhsm_story_vo.mp3',
    '-i', r'c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3',
    '-filter_complex',
    f"[0:v]ass='{ass_filter}':fontsdir='{fonts_filter}'[v];[0:a]volume=0.12[amb];[1:a]volume=1.0[vo];[2:a]volume=0.14[bgm];[amb][vo][bgm]amix=inputs=3:duration=first:dropout_transition=2[a]",
    '-map', '[v]',
    '-map', '[a]',
    '-c:v', 'libx264',
    '-crf', '19',
    '-preset', 'fast',
    '-c:a', 'aac',
    '-b:a', '256k',
    r'c:\QuangHy\editvideo\processed\Vlog_XanhSM_Story_FINAL.mp4'
]

print('[*] Re-burning final video with emotional VoiceStudio voice and dynamic subtitles...')
subprocess.run(mix_cmd, check=True)

print('[*] Capturing QA snapshots with emotional voice...')
snap_dir = r'c:\QuangHy\editvideo\processed\snapshots'
os.makedirs(snap_dir, exist_ok=True)

# 0.35s: "THÁCH" đang nói -> THÁCH màu xanh Cyan
subprocess.run(['ffmpeg', '-y', '-ss', '0.35', '-i', r'c:\QuangHy\editvideo\processed\Vlog_XanhSM_Story_FINAL.mp4', '-vframes', '1', '-q:v', '2', os.path.join(snap_dir, 'qa_emo_w1_thach.jpg')], check=True)
# 1.20s: "MÁY" đang nói -> MÁY màu xanh Cyan
subprocess.run(['ffmpeg', '-y', '-ss', '1.20', '-i', r'c:\QuangHy\editvideo\processed\Vlog_XanhSM_Story_FINAL.mp4', '-vframes', '1', '-q:v', '2', os.path.join(snap_dir, 'qa_emo_w2_may.jpg')], check=True)
# 6.55s: "TEST" đang nói -> TEST màu xanh Cyan
subprocess.run(['ffmpeg', '-y', '-ss', '6.55', '-i', r'c:\QuangHy\editvideo\processed\Vlog_XanhSM_Story_FINAL.mp4', '-vframes', '1', '-q:v', '2', os.path.join(snap_dir, 'qa_emo_w3_test.jpg')], check=True)
# 6.85s: "THỰC" đang nói -> THỰC màu xanh Cyan
subprocess.run(['ffmpeg', '-y', '-ss', '6.85', '-i', r'c:\QuangHy\editvideo\processed\Vlog_XanhSM_Story_FINAL.mp4', '-vframes', '1', '-q:v', '2', os.path.join(snap_dir, 'qa_emo_w4_thuc.jpg')], check=True)

print('[SUCCESS] Video re-burn & QA snapshots completed!')
