import scala.io.Source

// get source data file
val sourceFile = "/opt/futbol/champions_data.csv"
val srcItr = Source.fromFile(filename).getLines

// remove header lines
srcItr.next; srcItr.next

//read source iterator into array structure
val srcArr = srcItr.toArray

//get a list of tuples representing name and 

