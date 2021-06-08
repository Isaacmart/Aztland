import csv


def write_to_csv(a_string):
    to_write = open('webhook_log.csv', 'a')
    writer = csv.writer(to_write)
    writer.writerow(a_string)
    to_write.close()


