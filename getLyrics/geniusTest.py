import syncedlyrics
lrc = syncedlyrics.search("[get lucky] [daft punk]")
lrc_line = lrc.split("\n")
#print(lrc)
print(lrc[0])
with open('lyrics/funk/Get_lucky.txt', 'w') as f:
    f.write(lrc)

words_list = []
for i in range(len(lrc_line)):
    line = lrc_line[i]
    line = line[11:]
    for word in line.split():
        words_list.append(word)

# with open('lyrics_train/pop/Al', 'w') as f:
#     for word in words_list:
#         f.write(word + "\n")
