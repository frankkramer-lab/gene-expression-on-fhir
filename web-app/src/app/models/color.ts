export class Color {
  // 0=>100, 10=>55
  static minL = 55;
  static maxL = 100;

  public static getColor(value: number): string {
    const restL = Color.maxL - Color.minL;
    const l = restL - Math.round((restL / 10) * value) + Color.minL;
    return 'hsl(216, 100%, ' + l + '%)';
  }
}
