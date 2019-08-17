import scala.io.Source
import scala.util.Try

// get source data file
val sourceFile = "/opt/futbol/champions_data.csv"
val srcItr = Source.fromFile(filename).getLines

// remove header lines
srcItr.next; srcItr.next

//read source iterator into array structure
val srcSeq = srcItr.toSeq.map(_.split(",").padTo(58, ""))

println( srcSeq.map(ls => ls.length).max)

//get a list of tuples representing name and 
val nameSeq = srcSeq.map{ ls => 
    (ls(0), ls(1))
}
    
// get last year's results
val lastYear = srcSeq.map{ ls =>
    (ls(2), ls(3), ls(4), ls(5))
}
    
// get interpretation of rounds
val roundNames = Map(1 -> "Champion",
    2 -> "Runner-up",
    3 -> "Semi Final",
    4 -> "Quarter Final",
    5 -> "Round of 16",
    6 -> "Group 3rd",
    7 -> "Group 4th",
    0 -> None
)

// display team names with output
val teamResults = (nameSeq, lastYear.map(_._2)).zipped.map { 
    case ((team: String, cntry: String), rslt: String) => 
        (team, cntry, Try(rslt.toInt).getOrElse(0))
    }.sortBy(_._3).foreach{ case (team, cntry, rsltInt) => 
        if (rsltInt != 0)
            println(s"$team, $cntry: ${roundNames(rsltInt)}")
    }

