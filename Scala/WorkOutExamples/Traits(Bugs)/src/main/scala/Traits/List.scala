package Traits

trait List[T] {
  def isEmpty: Boolean
  def head: T
  def tail: List[T]
}
abstract class Cons[T](val head: T, tail: List[T]) extends List[T] {
  def isEmpty = false
}
class Nil[T] extends List[T] {
  def isEmpty = true
  def head = throw new NoSuchElementException("Nil.head")
  def tail = throw new NoSuchElementException("Nil.tail")

}
