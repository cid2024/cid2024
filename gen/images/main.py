import os
from PIL import Image, ImageFont, ImageDraw

dirname = os.path.dirname(__file__)

def conversation_image(people, statements, genders):
  assert("Length of arrays 'people', 'statements', and 'genders' must be same" and len(people) == len(statements) and len(people) == len(genders))

  personas = []
  mcnt, fcnt = 1, 1
  for gender in genders:
    if gender == 'M':
      personas.append(Image.open(os.path.join(dirname, "./m" + str(mcnt) + ".png")))
      mcnt += 1
    else:
      personas.append(Image.open(os.path.join(dirname, "./w" + str(fcnt) + ".png")))
      fcnt += 1
    if mcnt > 3 or fcnt > 3:
      raise Exception("Too many people!")
  for persona in personas:
    persona.thumbnail((120, 180))
  
  image = Image.new('RGB', (720, 240 * len(people)), (255, 255, 255))

  for i in range(len(people)):
    image.paste(personas[i], (30, 240*i + 15), mask=personas[i])
    draw = ImageDraw.Draw(image)
    pfont = ImageFont.truetype(os.path.join(dirname, "./SDMiSaeng.ttf"), 20)
    tfont = ImageFont.truetype(os.path.join(dirname, "./SDMiSaeng.ttf"), 30)
    _, _, pw, ph = draw.textbbox((0, 0), people[i], font=pfont)
    draw.text((75 - pw/2, 240*i + 205 - ph/2), people[i], (0, 0, 0), font=pfont)
    _, _, _, th = draw.textbbox((0, 0), statements[i], font=tfont)
    draw.text((180, 240*i + 120 - th/2), statements[i], (0, 0, 0), font=tfont)

  image.save("./conversation_image.png")

conversation_image(['윤교준', '김세빈'], ['오늘 노량진 갈 사람!', '난 가기 싫어!'], ['M', 'F'])