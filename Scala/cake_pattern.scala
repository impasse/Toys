trait Logger {
  def logger(s:String) = println(s)
}

class Job {
  this: Logger =>
    def run = {
      logger("start")
      println("doing")
      logger("done")
    }
}

object Main {
  def main(args: Array[String]){
    val j = new Job with Logger
    j.run
  }
}
