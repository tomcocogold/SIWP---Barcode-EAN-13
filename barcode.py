from PIL import Image, ImageDraw, ImageFont

GROUP_2_dict = {"0": "LLLLLL",
           "1": "LLGLGG",
           "2": "LLGGLG",
           "3": "LLGGGL",
           "4": "LGLLGG",
           "5": "LGGLLG",
           "6": "LGGGLL",
           "7": "LGLGLG",
           "8": "LGLGGL",
           "9": "LGGLGL"}

L_CODE = {"0": "0001101",
               "1": "0011001",
               "2": "0010011",
               "3": "0111101",
               "4": "0100011",
               "5": "0110001",
               "6": "0101111",
               "7": "0111011",
               "8": "0110111",
               "9": "0001011"}

G_CODE = {"0": "0100111",
               "1": "0110011",
               "2": "0011011",
               "3": "0100001",
               "4": "0011101",
               "5": "0111001",
               "6": "0000101",
               "7": "0010001",
               "8": "0001001",
               "9": "0010111"}

R_CODE = {"0": "1110010",
               "1": "1100110",
               "2": "1101100",
               "3": "1000010",
               "4": "1011100",
               "5": "1001110",
               "6": "1010000",
               "7": "1000100",
               "8": "1001000",
               "9": "1110100"}

#Zapisanie kodu jako ciąg binarny
input_code = 0
input_code_len = 12

while True:
    try:
        input_code = int(input("Enter barcode: "))
        if len(str(input_code)) == input_code_len:
            break
        print("Try again..")
    except ValueError:
        print("Try again...")

input_code = str(input_code)
odd_sum = 0
even_sum = 0

for count, digit in enumerate(input_code):
    if (count+1) % 2 == 0:
        even_sum += int(input_code[count])
    else:
        odd_sum += int(input_code[count])

check_digit = (10 - (odd_sum + 3 * even_sum) % 10) % 10
full_code_decimal = str(input_code) + str(check_digit)

first_digit = str(full_code_decimal[0])
second_group = str(full_code_decimal[1:7])
third_group = str(full_code_decimal[7:])

start_sign = '101'
stop_sign = '101'
separator_sign = '01010'
full_code_binary = ''

full_code_binary += start_sign

for count, digit in enumerate(second_group):
    if GROUP_2_dict[first_digit][count] == 'L':
        full_code_binary += L_CODE[digit]
    else:
        full_code_binary += G_CODE[digit]

full_code_binary += separator_sign

for count, digit in enumerate(third_group):
    full_code_binary += R_CODE[digit]

full_code_binary += stop_sign

print('Kod kreskowy binarnie: ', full_code_binary)
print('Kod kreskowy decymalnie: ', full_code_decimal)
print('Cyfra kontrolna: ', check_digit)

full_code_binary = list(full_code_binary)

# Stworzenie obrazu kodu kreskowego na podstawie kodu binarnego

barcode_color = 0  # czarny
background_color = 255  # biały

module_height = 90 # wysokość jednej kreski
module_width = 1 # szerokość jednej kreski

left_margin_width = 15 * module_width  # minimum 7 modułów
right_margin_width = 15 * module_width  # minimum 11 modułów

special_sign_height = 100  # znak startu, stopu i połowy kodu

start_w = len(start_sign) * module_width  # START lines width
stop_w = len(stop_sign) * module_width  # STOP lines width
break_w = len(separator_sign) * module_width  # BREAK lines width

background_height = 120                          # image background height
background_width = left_margin_width + start_w + break_w + stop_w + right_margin_width + 12 * 7 * module_width

image = Image.new("L", (background_width, background_height), background_color)
ttf = ImageFont.truetype(font="c:/Windows/Fonts/cour.ttf", size=20)
draw = ImageDraw.Draw(image)
x_pos = left_margin_width
y_top = 10
y_bottom = y_top + module_height

mid = int(len(full_code_binary)/2)

end = len(full_code_binary)

for count, digit in enumerate(full_code_binary):
    y_bottom = y_top + module_height
    if count in [0, 1, 2, mid-2, mid-1, mid, mid+1, mid+2, end-3, end-2, end-1]:  #znaki specjalne
        y_bottom = y_top + special_sign_height

    if digit == '1':
        draw.line((x_pos, y_top, x_pos, y_bottom), barcode_color, module_width)
    x_pos += module_width

image.show()