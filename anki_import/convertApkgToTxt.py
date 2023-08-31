from ankisync2 import Apkg
import shutil
import re
import os

errors = ["doesntExistError", "incorrectExtensionError", "alreadyConvertedError"]

def makeApkgInstance(apkgname, isall = False):
    apkgPath = f"anki_import/imports/{apkgname}.apkg"
    
    if (errName := handleErrors(apkgPath, apkgname, isall)) in errors:
        return errName
    
    apkg = Apkg(apkgPath) # Apkg instance
    shutil.rmtree(apkgPath.replace(".apkg", "")) # Remove unrequired directory
    
    convertAndWrite(apkg, apkgname)

def handleErrors(apkgpath, apkgname, isall):
    if not os.path.exists(apkgpath):
        return "doesntExistError"
    
    if not apkgpath.endswith(".apkg"):
        return "incorrectExtensionError"

    if f"anki-{apkgname}.txt" in os.listdir("flash_sets"):
        if isall:
            return
        else:
            return "alreadyConvertedError"

def convertAndWrite(apkg, apkgname):
    cards = []

    for card in apkg:
        cards.append(dict(card.items()))
    
    with open(f"flash_sets/anki-{apkgname}.txt", "w") as f:
        for card in cards:
            f.write(f"{removeMarkdown(card['note']['flds'][0])}\n")
            f.write(f"{removeMarkdown(card['note']['flds'][1])}\n\n")

def bulkConversion():
    for apkgFileName in (cd := os.listdir("anki_import/imports")):
        if all(item in [file.replace(".txt", ".apkg").replace("anki-", "") for file in os.listdir("flash_sets")] 
               for item in [file for file in cd if file != ".DS_Store"]):
            return "identicalFoldersError"        
        
        makeApkgInstance(apkgFileName.replace(".apkg", ""), isall = True)

def removeMarkdown(text):
    # Remove markdown and html
    pattern = re.compile(r'<(\/)?(\w+)(\s+(\w+)(\s*=\s*"[^"]*")?)*(\s*\/)?>|<sup>(.*?)<\/sup>|\s*&nbsp;')
    result = re.sub(pattern, '', text)
    return result