import re

filepath = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove line `let currentSelectedDay = 13;`
content = content.replace("let currentSelectedDay = 13;\n", "")
content = content.replace("let currentSelectedDay = 13;", "")

# Also, let's update Card 1 initial HTML so that by default on load it displays Day 18:
# Photo: cat_bathrobe_coffee_day18.jpg
# Focus: Устанавливайте границы с людьми, которые забирают больше энергии, чем дают
content = content.replace(
    'src="09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/02_The_13th_Moon_Day.jpg"',
    'src="09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/cat_bathrobe_coffee_day18.jpg"'
)

content = content.replace(
    'Энергия между вами и человеком из ваших мыслей трансформируется. Обратите внимание на тонкие внутренние отклики.',
    'Устанавливайте границы с людьми, которые забирают больше энергии, чем дают'
)

# And Card 2: 8-й лунный день • Растущая Луна
content = content.replace(
    '<div class="calendar-event-day-title" id="calendar-lunar-phase-title">13-й лунный день • Растущая Луна</div>',
    '<div class="calendar-event-day-title" id="calendar-lunar-phase-title">8-й лунный день • Растущая Луна</div>'
)

content = content.replace(
    '<img class="calendar-event-3d-moon-corner" id="calendar-moon-corner" src="moonly_3d_icons/moon_13.png" alt="3D Moon Sphere">',
    '<img class="calendar-event-3d-moon-corner" id="calendar-moon-corner" src="moonly_3d_icons/moon_8.png" alt="3D Moon Sphere">'
)

content = content.replace(
    'Энергия направлена вовне — замыслы обретают форму, а намерения набирают устойчивую силу.',
    'Сегодняшний день приносит долгосрочные стабильные результаты'
)

content = content.replace(
    '<span id="calendar-lunar-zodiac">Телец ♉</span>',
    '<span id="calendar-lunar-zodiac">Козерог ♑</span>'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Duplicates removed and initial Card 1 & 2 values set to Day 18!")
