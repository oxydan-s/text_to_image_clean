from PIL import Image, ImageDraw
import math
import os

def text_to_image_visualizer(input_text: str, encoding: str, output_filename: str, cell_size: int = 20, line_width: int = 2):
    """
    Перетворює текстовий рядок у зображення на основі його бітового представлення
    у вказаному кодуванні.

    Args:
        input_text (str): Вхідний текст.
        encoding (str): Кодування для тексту (наприклад, 'utf-8', 'koi8-u', 'windows-1251').
        output_filename (str): Ім'я файлу для збереження зображення (наприклад, 'output.png').
        cell_size (int): Розмір кожної клітинки для одного 4-бітного символу.
        line_width (int): Товщина ліній.
    """
    try:
        # 1. Кодуємо текст у байти
        encoded_bytes = input_text.encode(encoding)
    except UnicodeEncodeError as e:
        print(f"Помилка: Неможливо закодувати текст '{input_text}' у кодуванні '{encoding}'.")
        print(e)
        return
    except LookupError:
        print(f"Помилка: Невідоме кодування '{encoding}'.")
        return

    # 2. Перетворюємо байти в 16-річний рядок
    hex_string = encoded_bytes.hex()

    if not hex_string:
        print("Попередження: Вхідний текст порожній або складається лише з символів, що не кодуються.")
        # Створюємо маленьке пусте зображення
        img = Image.new('RGB', (cell_size, cell_size), 'black')
        img.save(output_filename)
        return

    # 3. Розраховуємо розміри зображення
    num_hex_digits = len(hex_string)
    # Кількість клітинок має відповідати кількості 4-бітних блоків
    width_in_cells = num_hex_digits
    height_in_cells = 1

    img_width = width_in_cells * cell_size
    img_height = height_in_cells * cell_size

    # 4. Створюємо зображення та об'єкт для малювання
    img = Image.new('RGB', (img_width, img_height), 'black') # Змінено фон на чорний
    draw = ImageDraw.Draw(img)

    # 5. Ітеруємо по 16-річним цифрам і малюємо відрізки
    for i, hex_digit in enumerate(hex_string):
        # Конвертуємо 16-річну цифру в 4 біти
        # f'{...:04b}' гарантує, що у нас завжди буде 4 біти (з нулями на початку)
        bits = f'{int(hex_digit, 16):04b}'

        # Визначаємо координати поточної клітинки
        cell_x = (i % width_in_cells) * cell_size
        cell_y = (i // width_in_cells) * cell_size

        # Спочатку малюємо відрізки
        # bits[0] - найстарший біт, bits[3] - наймолодший

        # 1-й біт: зворотний слеш (\) - від лівого верхнього до правого нижнього
        if bits[0] == '1':
            draw.line([(cell_x, cell_y), (cell_x + cell_size, cell_y + cell_size)], fill='white', width=2)

        # 2-й біт: слеш (/) - від правого верхнього до лівого нижнього
        if bits[1] == '1':
            draw.line([(cell_x + cell_size, cell_y), (cell_x, cell_y + cell_size)], fill='white', width=2)

        # 3-й біт: вертикальна лінія (|) - від лівого верхнього до лівого нижнього
        if bits[2] == '1':
            draw.line([(cell_x, cell_y), (cell_x, cell_y + cell_size)], fill='white', width=2)

        # 4-й біт: горизонтальна лінія (-) - від лівого верхнього до правого верхнього
        if bits[3] == '1':
            draw.line([(cell_x, cell_y), (cell_x + cell_size, cell_y)], fill='white', width=2)

    # 6. Зберігаємо зображення у теці text_to_image
    output_path = os.path.join('text_to_image', output_filename)
    img.save(output_path)
    print(f"Зображення успішно створено та збережено у файлі '{output_path}'")

def image_to_text_reader(input_filename: str, encoding: str, cell_size: int = 20) -> str:
    """
    Читає зображення, аналізуючи тонкі лінії, і декодує його назад у текст.
    """
    try:
        # Формуємо шлях до зображення у теці text_to_image
        input_path = os.path.join('text_to_image', input_filename)
        img = Image.open(input_path).convert('RGB')
    except FileNotFoundError:
        print(f"Помилка: Файл '{input_filename}' не знайдено у теці 'text_to_image'.")
        return ""

    # Встановлюємо розмір клітинки, щоб відповідати візуалізатору
    cell_size = 20

    hex_string = analyze_grid_lines(img, cell_size)

    if not hex_string:
        print("Помилка: Не вдалося знайти дані на зображенні.")
        return ""

    try:
        if len(hex_string) % 2 != 0:
            # Це може статися, якщо останній байт був неповним
            # Ми не можемо його декодувати, тому ігноруємо
            hex_string = hex_string[:-1]

        byte_data = bytes.fromhex(hex_string)
    except ValueError:
        print(f"Помилка: Не вдалося перетворити 16-річний рядок '{hex_string}' у байти.")
        return ""

    decoded_text = byte_data.decode(encoding, errors='ignore')

    return decoded_text

def analyze_grid_lines(img: Image.Image, cell_size: int = 20) -> str:
    """
    Аналізує тонкі лінії на зображенні та декодує їх у текст.
    """
    width, height = img.size
    pixels = img.load()

    hex_string = ""
    WHITE_THRESHOLD = 200

    def is_white(x, y):
        if 0 <= x < width and 0 <= y < height:
            r, _, _ = pixels[x, y]
            return r > WHITE_THRESHOLD
        return False

    for cell_y in range(0, height, cell_size):
        for cell_x in range(0, width, cell_size):
            # Аналізуємо кожну клітинку
            bits = ""

            # 1-й біт: зворотний слеш (\)
            has_backslash = is_white(cell_x + 1, cell_y + 1) and is_white(cell_x + cell_size - 1, cell_y + cell_size - 1)
            bits += '1' if has_backslash else '0'

            # 2-й біт: слеш (/)
            has_slash = is_white(cell_x + cell_size - 1, cell_y + 1) and is_white(cell_x + 1, cell_y + cell_size - 1)
            bits += '1' if has_slash else '0'

            # 3-й біт: вертикальна лінія (|)
            has_vertical = is_white(cell_x + 1, cell_y + cell_size // 2)
            bits += '1' if has_vertical else '0'

            # 4-й біт: горизонтальна лінія (-)
            has_horizontal = is_white(cell_x + cell_size // 2, cell_y + 1)
            bits += '1' if has_horizontal else '0'

            # Конвертуємо біти у 16-річну цифру
            hex_digit = hex(int(bits, 2))[2:]
            hex_string += hex_digit

    return hex_string

if __name__ == '__main__':
    # --- Перевірка роботи процедур ---

    original_texts = {
        'utf-8': "Привіт, світе! Це тест візуалізації.",
        'koi8-u': "Привіт, світе! Це тест візуалізації.",
        'windows-1251': "Привіт, світе! Це тест візуалізації.",
        'ascii': "Hello, world! This is a test."
    }

    for encoding, original_text in original_texts.items():
        try:
            # Перевіряємо, чи текст можна закодувати у вибраному кодуванні
            original_text.encode(encoding)
        except UnicodeEncodeError:
            print(f"\nКодування '{encoding}' не підтримує текст: '{original_text}'. Пропускаємо.")
            continue

        filename_to_read = f'output_{encoding}.png'

        print(f"\nСтворюємо зображення для кодування '{encoding}'...")
        text_to_image_visualizer(original_text, encoding, filename_to_read)

        print(f"Читаємо файл '{filename_to_read}' з кодуванням '{encoding}'...")
        restored_text = image_to_text_reader(filename_to_read, encoding)

        # Порівняння текстів
        if restored_text:
            print("\n--- Відновлений текст ---")
            print(restored_text)
            print("------------------------")

            if original_text == restored_text:
                print("\nТексти співпадають! ✅")
            else:
                print("\nТексти не співпадають! ❌")
                print("Оригінал:", original_text)
                print("Відновлений:", restored_text)

        # Перевірка кількості клітинок
        expected_cells = len(original_text.encode(encoding)) * 2  # 2 клітинки на байт
        print(f"Очікувана кількість клітинок: {expected_cells}")

        from PIL import Image
        img = Image.open(f'text_to_image/{filename_to_read}')
        width, height = img.size
        actual_cells = (width // 20) * (height // 20)  # 20 - розмір клітинки
        print(f"Фактична кількість клітинок: {actual_cells}")

        if expected_cells == actual_cells:
            print("Кількість клітинок відповідає тексту! ✅")
        else:
            print("Кількість клітинок не відповідає тексту! ❌")