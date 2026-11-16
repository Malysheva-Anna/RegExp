import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


for contact in contacts_list[1:]:
    fio = " ".join(contact[:3]).split()
    contact[:3] = (fio + ["", "", ""])[:3]


for contact in contacts_list[1:]:
    phone = contact[5]

    if phone:
        extension = re.search(r'доб\.\s*\(?(\d+)\)?', phone, re.IGNORECASE)

        additional = ""
        if extension:
            additional = " доб." + extension.group(1)
            phone = phone[:extension.start()]

        digits = re.sub(r'\D', '', phone)

        if len(digits) == 11 and digits[0] in "78":
            digits = digits[1:]

        if len(digits) == 10:
            contact[5] = (
                f"+7({digits[:3]}){digits[3:6]}-"
                f"{digits[6:8]}-{digits[8:10]}{additional}"
            )


contacts_dict = {}

for contact in contacts_list[1:]:
    key = (contact[0], contact[1])

    if key not in contacts_dict:
        contacts_dict[key] = contact.copy()
    else:
        for i in range(len(contact)):
            if not contacts_dict[key][i] and contact[i]:
                contacts_dict[key][i] = contact[i]

contacts_list = [contacts_list[0]] + list(contacts_dict.values())


with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list)