def group_id_creator(faculty, year, group):
        faculty_list = ['Лечебный', 'Медико-профилактический', 'Педиатрический', 'Стоматологический', 'Фармацевтический', 'Medical']
        for i in range(len(faculty_list)):
            if faculty == faculty_list[i]:
                faculty_number = i + 1
        group_id = str(faculty_number) + year + group
        group_id = int(group_id)
        return group_id


