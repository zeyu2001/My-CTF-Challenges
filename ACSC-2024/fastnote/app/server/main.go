package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {

	r := gin.Default()

	r.Static("/static", "./static")
	r.LoadHTMLGlob("templates/*.html")

	r.Use(func() gin.HandlerFunc {
		return func(c *gin.Context) {
			c.Writer.Header().Set("Content-Security-Policy", "script-src 'self' 'unsafe-eval'")
		}
	}())

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	r.GET("/flag", func(c *gin.Context) {
		secret, _ := c.Cookie("SECRET")
		if secret != (os.Getenv("SECRET")) {
			c.String(http.StatusForbidden, "You are not allowed to see the flag")
			return
		}
		c.String(http.StatusOK, os.Getenv("FLAG"))
	})

	r.NoRoute(func(c *gin.Context) {
		c.String(http.StatusOK, fmt.Sprintf("%s not found", c.Request.URL))
	})

	r.Run(":80")
}
