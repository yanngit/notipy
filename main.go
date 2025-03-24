package main

import (
	"log"
	"os/exec"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	a := app.New()

	displays, err := getDisplays()
	if err != nil || len(displays) == 0 {
		log.Fatalf("Could not find displays: %v", err)
	}

	for _, display := range displays {
		win := a.NewWindow("Alert")
		win.SetContent(container.NewVBox(
			widget.NewLabel("This is a notification on screen " + display + "!"),
		))

		win.SetFixedSize(true)
		win.Resize(fyne.NewSize(300, 100))

		win.Show()
	}

	a.Run()
}

func getDisplays() ([]string, error) {
	cmd := exec.Command("xrandr", "--listmonitors")
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(output), "\n")
	var displays []string

	for _, line := range lines {
		if strings.Contains(line, "+") {
			fields := strings.Fields(line)
			if len(fields) > 3 {
				displays = append(displays, fields[3])
			}
		}
	}
	return displays, nil
}
