import argparse, requests, os
from mangadex import Manga, Chapter
from prompt.prompt import Prompt, Colors

parser = argparse.ArgumentParser(
    prog = 'MangaDownloader',
    description = 'Simple Manga Downloader'
)

parser.add_argument('-q', '--query', help = 'Manga Query')
parser.add_argument('-t', '--translation', help = 'Manga Translation', default = 'en')
parser.add_argument('-o', '--output', help = 'Output Directory')

args = parser.parse_args()

query = args.query
transLang = args.translation
outputDir = args.output

manga = Manga()
chapter = Chapter()

mangas = manga.get_manga_list(title = query)
mangaIndex = 0

if len(mangas) > 1:
    
    for index, manga in enumerate(mangas):
        print(f'{Colors.gray}[{Colors.end}{Colors.blue}{index}{Colors.end}{Colors.gray}]{Colors.end} {manga.title['en']}')
    
    mangaIndex = int(Prompt.ask('Choose Manga To Download'))

os.mkdir(outputDir)

volsData = manga.get_manga_volumes_and_chapters(manga_id = mangas[mangaIndex].manga_id)

for volIndex in volsData:
    vol = volsData[volIndex]

    chapters = vol['chapters']
    chapterCount = len(chapters)

    Prompt.success(f'Found {chapterCount} Chapters In Vol {Colors.blue}{volIndex}{Colors.end}')

    for chapterIndex in chapters:

        chapterData = chapters[chapterIndex]
        chapterId = chapterData['id']
        otherChapterIds = chapterData['others']
        
        for id in [chapterId, *otherChapterIds]:
            foundChapter = chapter.get_chapter_by_id(id)

            if (foundChapter.translatedLanguage != transLang):
                continue

            Prompt.info(f'Downloading Chapter {Colors.blue}{chapterIndex}{Colors.end}')

            imgLinks = foundChapter.fetch_chapter_images()
            linkCount = len(imgLinks)

            Prompt.success(f'Found {linkCount} Images In Chapter {Colors.blue}{chapterIndex}{Colors.end}')

            dirPath = f'{outputDir}/Chapter {chapterIndex}'
            os.mkdir(dirPath)

            for imgIndex, imgLink in enumerate(imgLinks):
                
                r = requests.get(imgLink)

                with open(f'{dirPath}/{imgIndex}.jpg', 'wb') as chapterImg:
                    chapterImg.write(r.content)
                    chapterImg.close()
