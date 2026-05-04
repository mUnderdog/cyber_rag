scores = [67, 78, 56, 83, 94, 90, 59, 94, 78, 81, 69, 72, 67]



score_2 = []
for i in scores:
    if i!=max(scores):
        score_2.append(i)

print(score_2)
print(max(score_2))