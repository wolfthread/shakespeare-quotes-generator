#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import uuid

def removing_braquets(l):
    no_braquets = ''
    if "[" in l and "]" in l:
        start = l.index('[')
        stop = l.index(']') + 1
        no_braquets = l[0:start] + l[stop:]
    elif "[" in l:
        start = l.index('[')
        no_braquets = l[0:start]
    elif "]" in l:
        position = l.index("]") + 1
        no_braquets = l[position:]
    if l is not None:
        return no_braquets.strip()
    else:
        return ''

def clean_up_line(l):
    cleaned = ''
    # checking for "=" char
    if not "=" in l:
        l = l.split()
        for word in l:
            if not word.isupper():
                cleaned += word + ' '
        # Cleaning braquets
        if ("]" in cleaned or "[" in cleaned):
            cleaned = removing_braquets(cleaned)
        cleaned = cleaned.strip()
    if len(cleaned) > 0:
        cleaned = cleaned[0].lower()+cleaned[1:]
    return cleaned

def clean_up_scenes(scene, min):
    cleaned_up_scene = []
    complete_sentence = ''
    for line in scene:
        line = clean_up_line(line)
        for letter in line:
            complete_sentence += letter
            if letter == '.' or letter == '?' or letter == '!':
                if len(complete_sentence) >= min:
                    if complete_sentence[0].isdigit():
                        complete_sentence = complete_sentence[1:]
                    cleaned_up_scene.append((complete_sentence).strip())
                    complete_sentence = ''
        complete_sentence += ' '
    return cleaned_up_scene

def get_play_data(play, min):
    """
    Desired format:

    List of lists with indexes corresponding to acts and scenes respectively
    Each scene will be an list of lines.
    When pulling off the quote later on, the indexes will be easy to pull out.
    Need to add 1 for quote layout.

    """
    # Counting acts and scenes
    total_acts = 0
    total_scenes = 0
    for line in play:
        if line.startswith("ACT"):
            total_acts += 1
        if line.startswith("Scene"):
            total_scenes += 1
    play_data = [[[] for x in range(total_scenes)] for y in range(total_acts)]

    # Adding lines in scenes
    current_act = 0
    current_scene = 0
    for line in play:
        if line.startswith("ACT"):
            # substracting 1 because using this for indexing
            current_act = int(line[4:]) - 1
        if line.startswith("Scene"):
            current_scene = int(line[6:]) - 1
        if not (line.startswith("Scene") or line.isdigit()):
            play_data[current_act][current_scene].append(line)
    cleaned_up_play_data = []
    for i in range(1, len(play_data)):
        for j in range(len(play_data[i])):
            cleaned_up_play_data.append(clean_up_scenes(play_data[i][j], min))

    return cleaned_up_play_data


def get_content(filename, enc, content, min):
    with open(filename, encoding=enc) as content_f:
        raw_content = [line.strip() for line in content_f]

    play_title = raw_content[0]

    # Add play title in content storage
    content[play_title] = []

    # Get play data
    play_data = get_play_data(raw_content, min)

    # Add play data to content
    content[play_title] = play_data

    return content

def checkPunctuation(line):
    punc = [".", "!", "?"]
    line = line.split()
    for i in range(len(line)-1):
        if line[i][-1] in punc:
            if len(line[i+1]) > 2:
                line[i+1] = "{}{}".format(line[i+1][0].upper(), line[i+1][1:])
            else:
                line[i+1] = line[i+1][0].upper()
    return(" ".join(line))


def search_by_theme(content, theme):
    """
    Quote format desired is a list of tuples with the (quote, cite) modeL:
    [(
        'Could such inordinate and low desires, such poor, such bare, such lewd,
        such mean attempts, such barren pleasures, rude society as thou art matched withal,
        and grafted to, accompany the greatness of thy blood,
        and hold their level with thy princely heart?',
        '(Henry IV, Part I, Act 3, Scene 2)'
    )]
    """
    quotes = []
    for play in content:
        for i in range(len(play)):
            scenes = content[play][i]
            for j in range(len(scenes)):
                if theme in scenes[j].lower():
                    quote_id = str(uuid.uuid1())
                    # last punctuation work on line
                    scenes[j] = checkPunctuation(scenes[j])
                    thisQuote = {"id": quote_id, "rating": 0, "theme": theme, "quote": "{}{}".format(scenes[j][0].upper(), scenes[j][1:]), "play": "({}, Act {}, Scene {})".format(play, i, j)}
                    if len(theme) > 0:
                        quotes.append(thisQuote)
    return quotes

if __name__ == '__main__':
    # Config
    config_file = "src/config/themes.txt"
    encoding = "utf8"

    # Paths
    source_dir = "src/complete-works/folger-shakespeare/"
    data_store_dir_json = "data/json/"
    data_store_dir_raw = "data/raw/"
    stored_quotes_raw_fname = "stored_quotes.txt"
    stored_quotes_json_fname = "stored_quotes.json"
    stored_quotes_json_fname = "stored_quotes.json"

    # Minimum length of quote
    min_len_quote = 50

    # Content storage, which will be a dictionary with play titles as keys and plays as values
    content = {}

    # Pull themes from config
    with open(config_file) as config_f:
        themes = [line.strip() for line in config_f]

    # Get content from all play files
    for filename in os.listdir(source_dir):
        if filename.endswith(".txt"):
            get_content("{}{}".format(source_dir, filename), encoding, content, min_len_quote)

    # TODO: Get content from Poems and Sonnets

    stored_by_theme = {theme: [] for theme in themes}

    # Theme search algorithm and Storage
    for theme in themes:
        this_theme_quotes = search_by_theme(content, theme)
        # Store search results
        if len(this_theme_quotes):
            stored_by_theme[theme] = this_theme_quotes
            # Storing quotes by themes in json file
            if len(theme):
                with open("{}{}_{}".format(data_store_dir_json, theme, stored_quotes_json_fname), "w") as stored_by_theme_f:
                    json.dump(stored_by_theme[theme], stored_by_theme_f, indent=2)
            # Uncomment this block in dev mode to store quotes in raw txt file
            # -----------------------------
            # for quote in this_theme_quotes:
            #     with open("{}{}".format(data_store_dir_raw, stored_quotes_raw_fname), "a") as stored_f:
            #         stored_f.write(quote[0].strip())
            #         stored_f.write(quote[1].strip())
            #         stored_f.write("\n")
            # -----------------------------
    # Storing all quotes by themes in single json file
    with open("{}all_themes_{}".format(data_store_dir_json, stored_quotes_json_fname), "w") as stored_by_theme_f:
        json.dump(stored_by_theme, stored_by_theme_f, indent=2)
