import os
from PIL import Image, ImageFont, ImageDraw

dirname = os.path.dirname(__file__)

WIDTH, HEIGHT = 720, 240
TH_WIDTH, TH_HEIGHT = 114, 210

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
    persona.thumbnail((TH_WIDTH, TH_HEIGHT))
  
  image = Image.new('RGB', (WIDTH, HEIGHT * len(people)), (255, 255, 255))

  for i in range(len(people)):
    draw = ImageDraw.Draw(image)
    pfont = ImageFont.truetype(os.path.join(dirname, "./SDMiSaeng.ttf"), 20)
    tfont = ImageFont.truetype(os.path.join(dirname, "./SDMiSaeng.ttf"), 30)
    _, _, pw, ph = draw.textbbox((0, 0), people[i], font=pfont)
    _, _, _, th = draw.textbbox((0, 0), statements[i], font=tfont)
    image.paste(personas[i], (int((WIDTH/4 - TH_WIDTH)/2), 240*i + int((HEIGHT - TH_HEIGHT - ph)/2)), mask=personas[i])
    draw.text((int(WIDTH/8 - pw/2), 240*i + int((HEIGHT + TH_HEIGHT - ph)/2)), people[i], (0, 0, 0), font=pfont)
    draw.text((int(3*WIDTH/8 - TH_WIDTH/2), 240*i + int(HEIGHT/2 - th/2)), statements[i], (0, 0, 0), font=tfont)

  image.save("./conversation_image.png")

conversation_image(['윤교준', '김세빈'], ['오늘 노량진 갈 사람!', '난 가기 싫어!'], ['M', 'F'])