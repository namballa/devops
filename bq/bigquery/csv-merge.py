import csv
with open('us-states-by-date.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            new_row = [' '.join([row[0], row[1]])] + row[2:]
            writer.writerow(new_row)