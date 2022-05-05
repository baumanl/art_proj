from PIL import Image
import sys

def get_brightness(pix):
  R = pix[0]
  G = pix[1]
  B = pix[2]
  return sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)

def get_avgs(img, n):
  counts = [0] * 256
  for x in range(img.width):
    for y in range(img.height):
      b = get_brightness(img.getpixel((x,y)))
      counts[int(b)] += 1
  total_pix = img.size[0] * img.size[1]
  print("total pix: ", total_pix)
  bucket = int(total_pix / n)
  print("bucket size: ", bucket)
  boundaries = [0]
  curr = 0
  i = 0
  for j in range(256):
    if curr >= (bucket):
      print("curr: ", curr)
      boundaries.append(j)
      curr = 0
      i += 1
    curr += counts[j]
  boundaries.append(255)
  boundaries.append(257)
  print("sum counts: ", sum(counts))
  return boundaries


def standard(n):
  boundaries = []
  bucket = 255 / n
  for i in range(n):
    boundaries.append(int(bucket * i))
  return boundaries

def mod_img(img, boundaries):
  colors = []
  imgs = []
  pixels  = [[]] * len(boundaries)
  positions = [[]] * len(boundaries)
  for b in boundaries:
    colors.append((b, b, b))
    im = Image.new("RGBA", img.size, (255, 255, 255))
    imgs.append(im)
  total = Image.new("RGBA", img.size, (255, 255, 255))
  for x in range(img.width):
    for y in range(img.height):
      pix = img.getpixel((x,y))
      b = get_brightness(pix)
      for i in range(len(boundaries)):
        if b >= boundaries[i]:
          if i + 1 < len(boundaries) and not  b < boundaries[i + 1]:
            continue
          color_sum = sum(colors[i])
          pix_sum = sum(pix)
          if pix_sum == 0:
            props = (0.33, 0.33, 0.33)
          else:
            props = (pix[0] / pix_sum, pix[1] / pix_sum, pix[2] / pix_sum)
          # new_pix = (int(color_sum * props[0]), int(color_sum * props[1]), int(color_sum * props[2]))
          new_pix = pix
          imgs[i].putpixel((x,y),new_pix)
          pixels[i].append(new_pix)
          positions[i].append((x,y))
          total.putpixel((x,y), new_pix)
  # avgs = []
  # print("l[0]: ", pixels[0][0:10])
  # print([x[0] for x in
  # for l in pixels:
  #   rvals = [x[0] for x in l]
  #   bvals = [x[1] for x in l]
  #   gvals = [x[2] for x in l]
  #   avg = (int((sum(rvals)/len(l))), int(sum(bvals)/len(l)), int(sum(gvals)/len(l)))
  #   avgs.append(avg)
  # print("avgs: ", avgs)
  # for i in range(len(boundaries)):
  #   pix_val = avgs[i]
  #   imgs[i].putpixel((x,y),pix_val)
  #   total.putpixel((x,y), new_pix)

  for im in imgs:
    im.show()
  total.show()


def main():
  filename = sys.argv[1]
  n = int(sys.argv[2])
  with Image.open(filename) as img:
    img.load()
    # b = get_avgs(img, 2)
    b = standard(n)
    print(b)
    mod_img(img, b)
    # img.show()

if __name__ == "__main__":
    main()
