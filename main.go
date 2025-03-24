package main

import (
	"log"
	"runtime"

	"github.com/go-gl/glfw/v3.3/glfw"
)

func init() {
	runtime.LockOSThread()
}

func main() {
	if err := glfw.Init(); err != nil {
		log.Fatalf("Failed to initialize GLFW: %v", err)
	}
	defer glfw.Terminate()

	displays := glfw.GetMonitors()
	if len(displays) == 0 {
		log.Fatalf("Could not find any displays")
	}

	for i, display := range displays {
		mode := display.GetVideoMode()
		width, height := 300, 100

		window, err := glfw.CreateWindow(width, height, "Alert", nil, nil)
		if err != nil {
			log.Fatalf("Failed to create window: %v", err)
		}

		// Position the window based on monitor
		xPos := i * (mode.Width)
		yPos := mode.Height - height // Show at the bottom of the screen
		window.SetPos(xPos, yPos)

		window.MakeContextCurrent()

		go func(w *glfw.Window) {
			// This is where you update and render
			for !w.ShouldClose() {
				// Clear screen
				glfw.PollEvents()
				w.SwapBuffers()
			}
		}(window)
	}

	// Keep running
	select {}
}
