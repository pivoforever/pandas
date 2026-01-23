def colored_diff(file1, file2):
    """Сравнение с цветным выводом различий"""
    from difflib import ndiff, SequenceMatcher
    
    with open(file1, 'r', encoding='utf-8') as f1, \
        open(file2, 'r', encoding='utf-8') as f2:
        
        # Сначала читаем ВСЁ содержимое для SequenceMatcher
        content1 = f1.read()
        content2 = f2.read()
        
        similarity = SequenceMatcher(None, content1, content2).ratio()
        
        # Сбрасываем позицию чтения в начало файлов
        f1.seek(0)  # 🔧 КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ
        f2.seek(0)
        
        # Теперь читаем построчно
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        diff = list(ndiff(lines1, lines2))
        
        print("Сравнение файлов:")
        print(f"{file1} vs {file2}")
        print(f"Сходство: {similarity:.1%}")
        print("=" * 60)
        
        if similarity == 1.0:
            print('✅ Изменений в расписании нет')
        else:
            # Показываем только реальные различия, не все строки
            has_diff = False
            for i, line in enumerate(diff, 1):
                if line.startswith('- ') or line.startswith('+ ') or line.startswith('? '):
                    if not has_diff:
                        print("Обнаружены изменения:")
                        has_diff = True
                    
                    if line.startswith('- '):
                        print(f"\033[91m- {line[2:].rstrip()}\033[0m")
                    elif line.startswith('+ '):
                        print(f"\033[92m+ {line[2:].rstrip()}\033[0m")
                    elif line.startswith('? '):
                        print(f"\033[93m  {line[2:].rstrip()}\033[0m")
            
            if not has_diff:
                print("✅ Файлы идентичны (различия только в пробелах/переносах)")