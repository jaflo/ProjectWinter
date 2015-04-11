void setup() {
  size(8, 8);
  frameRate(7);
  colorMode(HSB, 255);
}

void draw() {
  background(0);
  for (int x = 0; x < 8; x++) {
    for (int y = 0; y < 8; y++) {
      stroke(random(120,255));
      if (random(1)>0.5) point(x,y);
    }
  }
  save("frame.png");
}

