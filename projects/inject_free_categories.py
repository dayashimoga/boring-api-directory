import json
import os
import shutil

TOOLS_DB = r"H:\boring\projects\tools-directory\data\database.json"
OS_DB = r"H:\boring\projects\opensource-directory\data\database.json"

# 50+ High-Quality Free Resources expanding across multiple categories
news_education_media = [
    # Free News (10)
    {"slug": "reuters", "title": "Reuters", "url": "https://www.reuters.com/", "description": "Free, unbiased breaking world news and investigative journalism.", "category": "World News", "tags": ["news", "journalism", "world", "finance"], "is_free": True},
    {"slug": "ap-news", "title": "AP News", "url": "https://apnews.com/", "description": "Trusted global news network providing free, fact-based reporting.", "category": "World News", "tags": ["news", "independent", "world", "journalism"], "is_free": True},
    {"slug": "npr", "title": "NPR", "url": "https://www.npr.org/", "description": "National Public Radio offers free news, podcasts, and deep coverage.", "category": "World News", "tags": ["news", "radio", "podcasts", "usa"], "is_free": True},
    {"slug": "bbc-news", "title": "BBC News", "url": "https://www.bbc.com/news", "description": "Global breaking news, analysis, and comprehensive coverage.", "category": "World News", "tags": ["news", "uk", "world", "journalism"], "is_free": True},
    {"slug": "al-jazeera", "title": "Al Jazeera", "url": "https://www.aljazeera.com/", "description": "Independent news bringing a global perspective on world events.", "category": "World News", "tags": ["news", "global", "middle-east"], "is_free": True},
    {"slug": "the-guardian", "title": "The Guardian", "url": "https://www.theguardian.com/", "description": "High-quality, independent journalism covering world news and opinion.", "category": "World News", "tags": ["news", "journalism", "uk", "independent"], "is_free": True},
    {"slug": "propublica", "title": "ProPublica", "url": "https://www.propublica.org/", "description": "Independent, non-profit newsroom that produces investigative journalism.", "category": "World News", "tags": ["investigative", "news", "journalism"], "is_free": True},
    {"slug": "pbs-newshour", "title": "PBS NewsHour", "url": "https://www.pbs.org/newshour/", "description": "Trusted daily news program offering deep analysis.", "category": "World News", "tags": ["news", "television", "analysis"], "is_free": True},
    {"slug": "financial-times-free", "title": "FT Free to Read", "url": "https://www.ft.com/free-to-read", "description": "Select free business and financial news from the Financial Times.", "category": "World News", "tags": ["finance", "business", "news"], "is_free": True},
    {"slug": "euronews", "title": "Euronews", "url": "https://www.euronews.com/", "description": "European perspective on breaking global news and affairs.", "category": "World News", "tags": ["news", "europe", "world"], "is_free": True},

    # Free Education / University (15)
    {"slug": "khan-academy", "title": "Khan Academy", "url": "https://www.khanacademy.org/", "description": "Expert-created free study material covering math, science, and computing.", "category": "Education", "tags": ["learning", "math", "science", "free"], "is_free": True},
    {"slug": "mit-ocw", "title": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/", "description": "A web-based publication of virtually all MIT course content.", "category": "Education", "tags": ["university", "college", "engineering"], "is_free": True},
    {"slug": "libretexts", "title": "LibreTexts", "url": "https://libretexts.org/", "description": "Free, open-access college textbooks across all academic fields.", "category": "Education", "tags": ["textbooks", "university", "science"], "is_free": True},
    {"slug": "coursera-free", "title": "Coursera (Free Courses)", "url": "https://www.coursera.org/courses?query=free", "description": "Access hundreds of free courses from top universities worldwide.", "category": "Education", "tags": ["courses", "university", "learning"], "is_free": True},
    {"slug": "edx-free", "title": "edX (Free Audit)", "url": "https://www.edx.org/", "description": "Free courses from Harvard, MIT, and more (audit track).", "category": "Education", "tags": ["university", "courses", "learning"], "is_free": True},
    {"slug": "stanford-online", "title": "Stanford Online", "url": "https://online.stanford.edu/free-courses", "description": "Free online courses directly from Stanford University.", "category": "Education", "tags": ["university", "stanford", "courses"], "is_free": True},
    {"slug": "harvard-online", "title": "Harvard Free Courses", "url": "https://pll.harvard.edu/catalog/free", "description": "Explore free online courses from Harvard University.", "category": "Education", "tags": ["university", "harvard", "courses"], "is_free": True},
    {"slug": "openstax", "title": "OpenStax", "url": "https://openstax.org/", "description": "Free, peer-reviewed, openly licensed college textbooks.", "category": "Education", "tags": ["textbooks", "college", "free"], "is_free": True},
    {"slug": "codecademy-basic", "title": "Codecademy Basic", "url": "https://www.codecademy.com/", "description": "Free interactive coding lessons covering Python, web dev, and more.", "category": "Education", "tags": ["coding", "programming", "interactive"], "is_free": True},
    {"slug": "freecodecamp", "title": "freeCodeCamp", "url": "https://www.freecodecamp.org/", "description": "Learn to code for free with massive certification curriculums.", "category": "Education", "tags": ["coding", "programming", "tech"], "is_free": True},
    {"slug": "w3schools", "title": "W3Schools", "url": "https://www.w3schools.com/", "description": "The world's largest web developer learning and reference site.", "category": "Education", "tags": ["web", "development", "reference"], "is_free": True},
    {"slug": "mdn-web-docs", "title": "MDN Web Docs", "url": "https://developer.mozilla.org/", "description": "Comprehensive documentation and learning resources for web developers.", "category": "Education", "tags": ["web", "documentation", "mozilla"], "is_free": True},
    {"slug": "brilliant-preview", "title": "Brilliant", "url": "https://brilliant.org/", "description": "Interactive learning for math, science, and computer science fundamentals.", "category": "Education", "tags": ["math", "science", "interactive"], "is_free": True},
    {"slug": "crash-course", "title": "Crash Course", "url": "https://thecrashcourse.com/", "description": "High-quality educational videos covering history, science, and humanities.", "category": "Education", "tags": ["video", "history", "science"], "is_free": True},
    {"slug": "ted-ed", "title": "TED-Ed", "url": "https://ed.ted.com/", "description": "Carefully curated educational videos and animations exploring profound ideas.", "category": "Education", "tags": ["video", "ideas", "animation"], "is_free": True},

    # Free Books / Media (10)
    {"slug": "project-gutenberg", "title": "Project Gutenberg", "url": "https://www.gutenberg.org/", "description": "A library of over 70,000 free eBooks. Focuses on older works.", "category": "Free Books", "tags": ["ebooks", "literature", "download"], "is_free": True},
    {"slug": "internet-archive", "title": "Internet Archive", "url": "https://archive.org/", "description": "A non-profit library of millions of free books, movies, software.", "category": "Free Books", "tags": ["archive", "history", "media"], "is_free": True},
    {"slug": "open-library", "title": "Open Library", "url": "https://openlibrary.org/", "description": "An open, editable library catalog building a web page for every book.", "category": "Free Books", "tags": ["books", "catalog", "library"], "is_free": True},
    {"slug": "manybooks", "title": "ManyBooks", "url": "https://manybooks.net/", "description": "Massive library of free, discounted, and classic digital books.", "category": "Free Books", "tags": ["ebooks", "fiction", "download"], "is_free": True},
    {"slug": "pdf-drive", "title": "PDF Drive", "url": "https://www.pdfdrive.com/", "description": "Search engine to find, download, and read PDF files for free.", "category": "Free Books", "tags": ["pdf", "books", "download"], "is_free": True},
    {"slug": "unsplash", "title": "Unsplash", "url": "https://unsplash.com/", "description": "Beautiful, free images and photos that you can download.", "category": "Free Stock Media", "tags": ["photos", "stock-photos", "design"], "is_free": True},
    {"slug": "pexels", "title": "Pexels", "url": "https://www.pexels.com/", "description": "The best free stock photos, royalty free images & videos.", "category": "Free Stock Media", "tags": ["photos", "videos", "stock-media"], "is_free": True},
    {"slug": "pixabay", "title": "Pixabay", "url": "https://pixabay.com/", "description": "Over 4.3 million+ high quality stock images, videos, and music.", "category": "Free Stock Media", "tags": ["photos", "vectors", "images"], "is_free": True},
    {"slug": "freepik", "title": "Freepik", "url": "https://www.freepik.com/", "description": "Millions of free graphic resources. Vectors, stock photos, PSD.", "category": "Free Stock Media", "tags": ["graphics", "vectors", "design"], "is_free": True},
    {"slug": "mixkit", "title": "Mixkit", "url": "https://mixkit.co/", "description": "Free assets for your next video project: video clips, music, templates.", "category": "Free Stock Media", "tags": ["video", "music", "templates"], "is_free": True}
]

# Free Software / Open Source (15)
free_software = [
    {"slug": "vlc-media-player", "title": "VLC Media Player", "url": "https://www.videolan.org/vlc/", "description": "Free and open source cross-platform multimedia player.", "category": "Free Software", "github_repo": "https://github.com/videolan/vlc", "tags": ["video", "player", "open-source"]},
    {"slug": "obs-studio", "title": "OBS Studio", "url": "https://obsproject.com/", "description": "Free open source software for video recording and live streaming.", "category": "Free Software", "github_repo": "https://github.com/obsproject/obs-studio", "tags": ["streaming", "recording", "video"]},
    {"slug": "gimp", "title": "GIMP", "url": "https://www.gimp.org/", "description": "Cross-platform advanced image editor available for GNU/Linux, macOS, Windows.", "category": "Free Software", "github_repo": "https://github.com/GNOME/gimp", "tags": ["graphics", "editor", "design"]},
    {"slug": "blender", "title": "Blender", "url": "https://www.blender.org/", "description": "The free and open source 3D creation suite.", "category": "Free Software", "github_repo": "https://github.com/blender/blender", "tags": ["3d", "animation", "modeling"]},
    {"slug": "rufus", "title": "Rufus", "url": "https://rufus.ie/", "description": "Utility that helps format and create bootable USB flash drives.", "category": "Free Software", "github_repo": "https://github.com/pbatard/rufus", "tags": ["usb", "bootable", "utility"]},
    {"slug": "7-zip", "title": "7-Zip", "url": "https://www.7-zip.org/", "description": "A file archiver with a high compression ratio.", "category": "Free Software", "github_repo": "https://github.com/mcmilk/7-Zip", "tags": ["archiver", "compression", "utility"]},
    {"slug": "audacity", "title": "Audacity", "url": "https://www.audacityteam.org/", "description": "Free, open source, cross-platform audio software for multi-track recording and editing.", "category": "Free Software", "github_repo": "https://github.com/audacity/audacity", "tags": ["audio", "editing", "music"]},
    {"slug": "kdenlive", "title": "Kdenlive", "url": "https://kdenlive.org/", "description": "An open source video editor based on MLT Framework.", "category": "Free Software", "github_repo": "https://github.com/KDE/kdenlive", "tags": ["video", "editor", "linux"]},
    {"slug": "krita", "title": "Krita", "url": "https://krita.org/", "description": "Professional free and open source painting program.", "category": "Free Software", "github_repo": "https://github.com/KDE/krita", "tags": ["painting", "art", "drawing"]},
    {"slug": "inkscape", "title": "Inkscape", "url": "https://inkscape.org/", "description": "Professional quality vector graphics software.", "category": "Free Software", "github_repo": "https://gitlab.com/inkscape/inkscape", "tags": ["vector", "graphics", "design"]},
    {"slug": "handbrake", "title": "HandBrake", "url": "https://handbrake.fr/", "description": "An open source video transcoder available for Linux, Mac, and Windows.", "category": "Free Software", "github_repo": "https://github.com/HandBrake/HandBrake", "tags": ["video", "transcoder", "converter"]},
    {"slug": "filezilla", "title": "FileZilla", "url": "https://filezilla-project.org/", "description": "The free FTP solution for both client and server.", "category": "Free Software", "github_repo": "https://github.com/FileZilla/FileZilla", "tags": ["ftp", "transfer", "network"]},
    {"slug": "qbittorrent", "title": "qBittorrent", "url": "https://www.qbittorrent.org/", "description": "A free software alternative to µTorrent.", "category": "Free Software", "github_repo": "https://github.com/qbittorrent/qBittorrent", "tags": ["torrent", "p2p", "download"]},
    {"slug": "keepassxc", "title": "KeePassXC", "url": "https://keepassxc.org/", "description": "Cross-Platform Password Manager securely storing passwords.", "category": "Free Software", "github_repo": "https://github.com/keepassxreboot/keepassxc", "tags": ["password", "manager", "security"]},
    {"slug": "brave-browser", "title": "Brave Browser", "url": "https://brave.com/", "description": "Secure, fast, and private web browser with ad blocker.", "category": "Free Software", "github_repo": "https://github.com/brave/brave-browser", "tags": ["browser", "web", "privacy"]}
]

def append_to_db(filepath, new_records):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        existing_slugs = {item['slug'] for item in data}
        added = 0
        for record in new_records:
            if record['slug'] not in existing_slugs:
                data.append(record)
                added += 1
                
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"Added {added} records to {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Inject the 35 Tools/News/Edu/Media into Tools Directory
append_to_db(TOOLS_DB, news_education_media)
# Inject the 15 Free Software applications into Open Source Directory
append_to_db(OS_DB, free_software)
print(f"Total specific Free Resources processed: {len(news_education_media) + len(free_software)} (50 records total over DBs)")
