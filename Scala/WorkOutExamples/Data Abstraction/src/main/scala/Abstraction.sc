object Func extends App {
  val x = new Func(1, 2)
  val y = new Func(5,7)
  val z = new Func(3,2)

  x.numer
  x.denom
  x.sub(y).sub(z)
  y.add(y)
  x.max((y))
  val strange = new Func(1, 0)
  strange.add(strange)
}
class Func(x: Int, y: Int) {

  @scala.annotation.tailrec
  private def gcd(a: Int, b: Int): Int = if(b == 0) a else gcd(b, a % b)
  private val  g = gcd(x,y)
  def numer:Int = x / g
  def denom: Int = y / g

  def less(that: Func) = numer * that.denom < that.numer * denom

  def add(that: Func) =
    new Func(
      numer * that.denom + that.numer * denom,
      denom * that.denom)

  def max(that: Func) = if (this.less(that)) that else this
  def neg: Func = new Func(-numer, denom)

  def sub(that: Func) = add(that.neg)

  override def toString: String = numer + "/" + denom
}