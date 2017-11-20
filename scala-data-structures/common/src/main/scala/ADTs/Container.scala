package ADTs

trait Container[T] {

  def add(elem: T): Unit

  def remove(elem: T): Unit

  def head(): T

  def size(): Long
}
