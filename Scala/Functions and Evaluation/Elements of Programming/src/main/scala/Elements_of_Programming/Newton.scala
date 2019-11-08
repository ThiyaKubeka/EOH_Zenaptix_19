package Elements_of_Programming

object Newton {
  1+3
  def abs(x: Double) = if (x < 0) -x else x

  def sqrt(x: Double) = {


    def sqrtIter(guess: Double, x: Double): Double =
      if (isGoodEnough(guess, x)) guess
      else sqrtIter(improve(guess, x), x)


  def isGoodEnough(guess: Double, x: Double) =
    abs(guess * guess - x) < 0.001

  def improve(guess: Double, x: Double): Double = (guess + x / guess) / 2

  sqrtIter( 1.0, x)
}
  sqrt(2)
  sqrt(4)

}
