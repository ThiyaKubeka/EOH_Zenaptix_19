package Elements_of_Programming

object Tailrecursion {
  def factorial(n: Int): Int = {
    @scala.annotation.tailrec
    def loop(acc: Int, n: Int): Int =
      if (n == 0) acc
      else loop(acc * n, n-1)
    loop(1,n)
  }
}
