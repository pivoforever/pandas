def colored_diff(file1, file2):
    """Сравнение с цветным выводом различий"""
    from difflib import ndiff, SequenceMatcher
    
    with open(file1, 'r', encoding='utf-8') as f1, \
        open(file2, 'r', encoding='utf-8') as f2:
        similarity = SequenceMatcher(None, f1.read(), f2.read()).ratio()
    # ratio() возвращает число от 0.0 (совсем разные) до 1.0 (идентичные)
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        diff = list(ndiff(lines1, lines2))
        
        print("Сравнение файлов:")
        print(f"{file1} vs {file2}")
        print("=" * 60)
        if similarity == 1.0:
            print('Изменений в расписании нет')
        else:
            for i, line in enumerate(diff, 1):
                if line.startswith('- '):
                    # Строка есть только в первом файле
                    print(f"\033[91m- строка {i}: {line[2:].rstrip()}\033[0m")
                elif line.startswith('+ '):
                    # Строка есть только во втором файле
                    print(f"\033[92m+ строка {i}: {line[2:].rstrip()}\033[0m")
                elif line.startswith('? '):
                    # Изменения внутри строки
                    print(f"\033[93m? {line[2:].rstrip()}\033[0m")
                elif line.startswith('  '):
                    # Общие строки
                    print(f"  строка {i}: {line[2:].rstrip()}")