float x;
float y;
void setup() {
  size(8, 8);
  frameRate(7);
  //colorMode(HSB, 255);
}

void draw() {
  background(0);
  x = random(255);
  y = random(255);
  stroke(x,0,0);
  fill(y);
  /*for (int x = 0; x < 8; x++) {
    for (int y = 0; y < 8; y++) {
      stroke(random(120,255));
      if (random(1)>0.5) point(x,y);
    }
  }*/
  rect(0,0,4,4);
  save("frame.png");
}

