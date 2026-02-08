#!/usr/bin/env python3
"""
GitHub Actions için YouTube M3U Oluşturucu
"""

import json
import os
from yt_dlp import YoutubeDL

def load_streams():
    """streams.json dosyasından yayın listesini yükler"""
    try:
        with open('streams.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('streams', [])
    except FileNotFoundError:
        print("HATA: streams.json dosyası bulunamadı!")
        return []
    except json.JSONDecodeError:
        print("HATA: streams.json geçersiz JSON formatında!")
        return []

def get_stream_url(youtube_url):
    """YouTube URL'si için akış URL'sini alır"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'live_from_start': True,
        # Bot engelini aşmak için en etkili ayar
        'extractor_args': {'youtube': {'player_client': ['tv', 'android', 'web']}},
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get('url') if info else None
    except Exception as e:
        print(f"  ✗ Hata: {e}")
        return None

def create_m3u():
    """M3U dosyasını oluşturur"""
    streams = load_streams()
    if not streams:
        print("HATA: Yayın listesi boş veya yüklenemedi!")
        return False
    
    print(f"📡 Toplam {len(streams)} yayın işleniyor...")
    
    m3u_entries = []
    successful = 0
    
    for idx, stream in enumerate(streams, 1):
        print(f"\n[{idx}/{len(streams)}] {stream['name']}")
        print(f"   🔗 {stream['url']}")
        
        stream_url = get_stream_url(stream['url'])
        if stream_url:
            m3u_entries.append({
                'name': stream['name'],
                'url': stream_url
            })
            successful += 1
            print(f"   ✅ Başarılı")
        else:
            print(f"   ❌ Başarısız")
    
    # M3U dosyasını yaz
    if m3u_entries:
        with open('yt.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write('# YouTube Canlı Yayın Playlist\n')
            f.write(f'# Otomatik oluşturuldu - {successful} yayın\n\n')
            
            for entry in m3u_entries:
                f.write(f'#EXTINF:-1, {entry["name"]}\n')
                f.write(f'{entry["url"]}\n\n')
        
        print(f"\n{'='*50}")
        print(f"✅ BAŞARILI: {successful}/{len(streams)} yayın eklendi")
        print(f"💾 Dosya: yt.m3u")
        print(f"{'='*50}")
        return True
    
    print("\n❌ HİÇBİR yayın alınamadı!")
    return False

if __name__ == '__main__':
    success = create_m3u()
    exit(0 if success else 1)
