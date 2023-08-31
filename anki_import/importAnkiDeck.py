from ankisync2 import Apkg
import shutil
import re
import os

def makeApkgInstance(apkgname):
    apkgPath = f"anki_import/apkg_exports/{apkgname}.apkg"
    if not os.path.exists(apkgPath):
        return
    
    if not apkgPath.endswith(".apkg"):
        return
    
    apkg = Apkg(apkgPath) # Apkg instance
    shutil.rmtree(apkgPath.replace(".apkg", "")) # Remove unrequired directory
    
    convertAndWrite(apkg)

def convertAndWrite(apkg):
    cards = []

    for card in apkg:
        cards.append(dict(card.items()))
    
    with open(f"flash_sets/anki-{cards[0]['deck']['name']}.txt", "w") as f:
        for card in cards:
            f.write(f"{removeMarkdown(card['note']['flds'][0])}\n")
            f.write(f"{removeMarkdown(card['note']['flds'][1])}\n\n")

def removeMarkdown(text):
    # Remove markdown and html
    pattern = re.compile(r'<(\/)?(\w+)(\s+(\w+)(\s*=\s*"[^"]*")?)*(\s*\/)?>|<sup>(.*?)<\/sup>|\s*&nbsp;')
    result = re.sub(pattern, '', text)
    return result
        
makeApkgInstance("TestDeck")