TOL = 1e-5
HUE_DELTA = 1
POINT_SIZE = 3
IT_DEPTH = 20
BG_COL = color(50)
MAX_ITERS = 10

def draw_mandel():
    loadPixels()
    for ind, pixel in enumerate(pixels):
        x = ind % width
        y = ind // width
        if mandel_in(map_coord_complex(x, y), IT_DEPTH):
            pixels[ind] = BG_COL
    updatePixels()

def setup():
    global m_iters, f
    f = createFont("courier", 20)
    size(800, 800)
    m_iters = []
    background(0)
    noStroke()
    colorMode(HSB, 255, 255, 255)
    ellipseMode(CENTER)
    textFont(f, 20)
    print("...")
    draw_mandel()
    print("ready")

def map_coord_complex(x, y):
    return complex(1. * x / width * 4 - 2,
                   1. * y / height * 4 - 2)

def map_complex_coord(z):
    return ((z.real + 2) * width / 4.0,
            (z.imag + 2) * height / 4.0)

def mandel_in(c, depth, tol=TOL):
    z = 0
    i = 0
    zprev = 1
    while abs(z) <= 2:
        i += 1
        if i > depth:
            return True
        if abs(z - zprev) < TOL:
            return True
        zprev = z
        z = z ** 2 + c
    return False

def mandel(c, tol=TOL):
    print(c)
    z = 0
    zprev = 1
    while abs(z) <= 2 and abs(z - zprev) > tol:
        zprev = z
        z = z ** 2 + c
        yield z

def draw():
    txt = "{:.0f}".format(frameRate)
    fill(10)
    rect(10, 30 - textAscent() - textDescent(), 10 + textWidth(txt), 30)
    fill(BG_COL)
    text(txt, 10, 30)
    for ind, m_iter in reversed(list(enumerate(m_iters))):
        try:
            nxt = next(m_iter[0])
        except StopIteration:
            m_iters.pop(ind)
            print(len(m_iters))
        else:
            m_iter[1] += 1
            fill(m_iter[1] % 255, 255, 255)
            x, y = map_complex_coord(nxt)
            ellipse(x, y, POINT_SIZE, POINT_SIZE)

def keyPressed():
    if keyCode == ord("R"):
        setup()
    if keyCode == ord(" "):
        mousePressed()
    if keyCode == ord("X"):
        m_iters[:] = []
    if keyCode == ord("Z"):
        m_iters.pop(0)

def mousePressed():
    m_iters.append([mandel(map_coord_complex(mouseX, mouseY)), random(255)])
    if len(m_iters) > MAX_ITERS:
        m_iters.pop(0)
    print(len(m_iters))
