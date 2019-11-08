package FuncData.FuncData.FuncData

object Func extends App {
  val x = new Func(1, 2)
  val y = new Func(5,7)
  val z = new Func(3,2)

  x.numer
  x.denom
  x.sub(y).sub(z)
}
 class Func(x: Int, y: Int) {
   def numer:Int = x
   def denom: Int = y

   def add(that: Func) =
     new Func(
       numer * that.denom + that.numer * denom,
       denom*that.denom)
   def neg: Func = new Func(-numer, denom)

   def sub(that: Func) = add(that.neg)

   override def toString: String = numer + "/" + denom
 }
