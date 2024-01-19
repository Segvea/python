def count_min_wins_in_a_row():
    with open("results.txt", "r") as file:
        results = file.read()


results = results.replace(" ", "").replace(".", ").replace(", "
wins_ina_row = 0
max_wins_in_a_row = 0
for result in results:
    if
result == "w":
wins_in_a_row += 1
if wins_in_a_row > max_wins_in_a_row:
    max_wins_in_a_row = wins_in_a_row
else:
    wins_in_a_
row = 0
if max
wins_in_a_row >= 100:
return max_wins_in_a_row
else:
return 'ДА'
