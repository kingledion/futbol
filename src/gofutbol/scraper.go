package main

import (
    "fmt"
    "strings"
//    "os"
    
//    "golang.org/x/net/html"
    "github.com/antchfx/htmlquery"
)

type FutbolEvent struct {
    Round      string
    HomeTeam   string 
    AwayTeam   string 
    HomeGoals  int    
    AwayGoals  int  
    WinTeam    string
}

func main() {
    doc, err := htmlquery.LoadURL("https://kassiesa.home.xs4all.nl/bert/uefa/data/method5/match2019.html")
    if err != nil {panic(err)}
    
    competitions := htmlquery.Find(doc, "//table[@class='t1']")
    for _, comp := range competitions {
        
        comp_title := strings.TrimSpace(htmlquery.InnerText(htmlquery.Find(comp, "//tr[@class='blue']//div")[0]))
        
        //html.Render(os.Stdout, comp_title)
        fmt.Println(comp_title)
        
        roundName := ""
        datarows := htmlquery.Find(comp, "//tr")
        for _, row := range datarows {
            rowClass := htmlquery.SelectAttr(row, "class")
            if rowClass == "yellow" {
                roundName = strings.TrimSpace(htmlquery.InnerText(row))
                fmt.Println(roundName)
            }
        }
    }
        
        
}
